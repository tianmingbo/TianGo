"""A WSGI and HTTP server for use **during development only**. This
server is convenient to use, but is not designed to be particularly
stable, secure, or efficient. Use a dedicate WSGI server and HTTP
server when deploying to production.

It provides features like interactive debugging and code reloading. Use
``run_simple`` to start the server. Put this in a ``run.py`` script:

.. code-block:: python

    from myapp import create_app
    from werkzeug import run_simple
"""
import errno
import io
import os
import socket
import socketserver
import sys
import typing as t
from datetime import datetime as dt
from datetime import timedelta
from datetime import timezone
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from ._internal import _log
from ._internal import _wsgi_encoding_dance
from .exceptions import InternalServerError
from .urls import uri_to_iri
from .urls import url_parse
from .urls import url_unquote

try:
    import ssl
except ImportError:

    class _SslDummy:
        def __getattr__(self, name: str) -> t.Any:
            raise RuntimeError(  # noqa: B904
                "SSL is unavailable because this Python runtime was not"
                " compiled with SSL/TLS support."
            )


    ssl = _SslDummy()  # type: ignore

_log_add_style = True

if os.name == "nt":
    try:
        __import__("colorama")
    except ImportError:
        _log_add_style = False

can_fork = hasattr(os, "fork")

if can_fork:
    ForkingMixIn = socketserver.ForkingMixIn
else:

    class ForkingMixIn:  # type: ignore
        pass

try:
    af_unix = socket.AF_UNIX
except AttributeError:
    af_unix = None  # type: ignore

LISTEN_QUEUE = 128

_TSSLContextArg = t.Optional[
    t.Union["ssl.SSLContext", t.Tuple[str, t.Optional[str]], "te.Literal['adhoc']"]
]

if t.TYPE_CHECKING:
    import typing_extensions as te  # noqa: F401
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment
    from cryptography.hazmat.primitives.asymmetric.rsa import (
        RSAPrivateKeyWithSerialization,
    )
    from cryptography.x509 import Certificate


class DechunkedInput(io.RawIOBase):
    """An input stream that handles Transfer-Encoding 'chunked'"""

    def __init__(self, rfile: t.IO[bytes]) -> None:
        self._rfile = rfile
        self._done = False
        self._len = 0

    def readable(self) -> bool:
        return True

    def read_chunk_len(self) -> int:
        try:
            line = self._rfile.readline().decode("latin1")
            _len = int(line.strip(), 16)
        except ValueError as e:
            raise OSError("Invalid chunk header") from e
        if _len < 0:
            raise OSError("Negative chunk length not allowed")
        return _len

    def readinto(self, buf: bytearray) -> int:  # type: ignore
        read = 0
        while not self._done and read < len(buf):
            if self._len == 0:
                # This is the first chunk or we fully consumed the previous
                # one. Read the next length of the next chunk
                self._len = self.read_chunk_len()

            if self._len == 0:
                # Found the final chunk of size 0. The stream is now exhausted,
                # but there is still a final newline that should be consumed
                self._done = True

            if self._len > 0:
                # There is data (left) in this chunk, so append it to the
                # buffer. If this operation fully consumes the chunk, this will
                # reset self._len to 0.
                n = min(len(buf), self._len)

                # If (read + chunk size) becomes more than len(buf), buf will
                # grow beyond the original size and read more data than
                # required. So only read as much data as can fit in buf.
                if read + n > len(buf):
                    buf[read:] = self._rfile.read(len(buf) - read)
                    self._len -= len(buf) - read
                    read = len(buf)
                else:
                    buf[read: read + n] = self._rfile.read(n)
                    self._len -= n
                    read += n

            if self._len == 0:
                # Skip the terminating newline of a chunk that has been fully
                # consumed. This also applies to the 0-sized final chunk
                terminator = self._rfile.readline()
                if terminator not in (b"\n", b"\r\n", b"\r"):
                    raise OSError("Missing chunk terminating newline")

        return read


class WSGIRequestHandler(BaseHTTPRequestHandler):
    """A request handler that implements WSGI dispatching."""

    server: "BaseWSGIServer"

    @property
    def server_version(self) -> str:  # type: ignore
        from . import __version__

        return f"Werkzeug/{__version__}"

    def make_environ(self) -> "WSGIEnvironment":
        request_url = url_parse(self.path)
        url_scheme = "http" if self.server.ssl_context is None else "https"

        if not self.client_address:
            self.client_address = ("<local>", 0)
        elif isinstance(self.client_address, str):
            self.client_address = (self.client_address, 0)

        # If there was no scheme but the path started with two slashes,
        # the first segment may have been incorrectly parsed as the
        # netloc, prepend it to the path again.
        if not request_url.scheme and request_url.netloc:
            path_info = f"/{request_url.netloc}{request_url.path}"
        else:
            path_info = request_url.path

        path_info = url_unquote(path_info)
        # 构造environ
        environ: "WSGIEnvironment" = {
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": url_scheme,
            "wsgi.input": self.rfile,
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": self.server.multithread,
            "wsgi.multiprocess": self.server.multiprocess,
            "wsgi.run_once": False,
            "werkzeug.socket": self.connection,
            "SERVER_SOFTWARE": self.server_version,
            "REQUEST_METHOD": self.command,
            "SCRIPT_NAME": "",
            "PATH_INFO": _wsgi_encoding_dance(path_info),
            "QUERY_STRING": _wsgi_encoding_dance(request_url.query),
            # Non-standard, added by mod_wsgi, uWSGI
            "REQUEST_URI": _wsgi_encoding_dance(self.path),
            # Non-standard, added by gunicorn
            "RAW_URI": _wsgi_encoding_dance(self.path),
            "REMOTE_ADDR": self.address_string(),
            "REMOTE_PORT": self.port_integer(),
            "SERVER_NAME": self.server.server_address[0],
            "SERVER_PORT": str(self.server.server_address[1]),
            "SERVER_PROTOCOL": self.request_version,
        }

        for key, value in self.headers.items():
            key = key.upper().replace("-", "_")
            value = value.replace("\r\n", "")
            if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                key = f"HTTP_{key}"
                if key in environ:
                    value = f"{environ[key]},{value}"
            environ[key] = value

        if environ.get("HTTP_TRANSFER_ENCODING", "").strip().lower() == "chunked":
            environ["wsgi.input_terminated"] = True
            environ["wsgi.input"] = DechunkedInput(environ["wsgi.input"])

        # Per RFC 2616, if the URL is absolute, use that as the host.
        # We're using "has a scheme" to indicate an absolute URL.
        if request_url.scheme and request_url.netloc:
            environ["HTTP_HOST"] = request_url.netloc

        try:
            # binary_form=False gives nicer information, but wouldn't be compatible with
            # what Nginx or Apache could return.
            peer_cert = self.connection.getpeercert(binary_form=True)
            if peer_cert is not None:
                # Nginx and Apache use PEM format.
                environ["SSL_CLIENT_CERT"] = ssl.DER_cert_to_PEM_cert(peer_cert)
        except ValueError:
            # SSL handshake hasn't finished.
            self.server.log("error", "Cannot fetch SSL peer certificate info")
        except AttributeError:
            # Not using TLS, the socket will not have getpeercert().
            pass

        return environ

    def run_wsgi(self) -> None:
        if self.headers.get("Expect", "").lower().strip() == "100-continue":
            self.wfile.write(b"HTTP/1.1 100 Continue\r\n\r\n")

        self.environ = environ = self.make_environ()
        status_set: t.Optional[str] = None
        headers_set: t.Optional[t.List[t.Tuple[str, str]]] = None
        status_sent: t.Optional[str] = None
        headers_sent: t.Optional[t.List[t.Tuple[str, str]]] = None
        chunk_response: bool = False

        def write(data: bytes) -> None:
            nonlocal status_sent, headers_sent, chunk_response
            assert status_set is not None, "write() before start_response"
            assert headers_set is not None, "write() before start_response"
            if status_sent is None:
                status_sent = status_set
                headers_sent = headers_set
                try:
                    code_str, msg = status_sent.split(None, 1)
                except ValueError:
                    code_str, msg = status_sent, ""
                code = int(code_str)
                self.send_response(code, msg)
                header_keys = set()
                for key, value in headers_sent:
                    self.send_header(key, value)
                    header_keys.add(key.lower())

                # Use chunked transfer encoding if there is no content
                # length. Do not use for 1xx and 204 responses. 304
                # responses and HEAD requests are also excluded, which
                # is the more conservative behavior and matches other
                # parts of the code.
                # https://httpwg.org/specs/rfc7230.html#rfc.section.3.3.1
                if (
                        not (
                                "content-length" in header_keys
                                or environ["REQUEST_METHOD"] == "HEAD"
                                or (100 <= code < 200)
                                or code in {204, 304}
                        )
                        and self.protocol_version >= "HTTP/1.1"
                ):
                    chunk_response = True
                    self.send_header("Transfer-Encoding", "chunked")

                # Always close the connection. This disables HTTP/1.1
                # keep-alive connections. They aren't handled well by
                # Python's http.server because it doesn't know how to
                # drain the stream before the next request line.
                self.send_header("Connection", "close")
                self.end_headers()

            assert isinstance(data, bytes), "applications must write bytes"

            if data:
                if chunk_response:
                    self.wfile.write(hex(len(data))[2:].encode())
                    self.wfile.write(b"\r\n")

                self.wfile.write(data)

                if chunk_response:
                    self.wfile.write(b"\r\n")

            self.wfile.flush()

        def start_response(status, headers, exc_info=None):  # type: ignore
            nonlocal status_set, headers_set
            if exc_info:
                try:
                    if headers_sent:
                        raise exc_info[1].with_traceback(exc_info[2])
                finally:
                    exc_info = None
            elif headers_set:
                raise AssertionError("Headers already set")
            status_set = status
            headers_set = headers
            return write

        def execute(app: "WSGIApplication") -> None:
            application_iter = app(environ, start_response)
            try:
                for data in application_iter:
                    write(data)
                if not headers_sent:
                    write(b"")
                if chunk_response:
                    self.wfile.write(b"0\r\n\r\n")
            finally:
                if hasattr(application_iter, "close"):
                    application_iter.close()

        try:
            execute(self.server.app)
        except (ConnectionError, socket.timeout) as e:
            self.connection_dropped(e, environ)
        except Exception as e:
            if self.server.passthrough_errors:
                raise

            if status_sent is not None and chunk_response:
                self.close_connection = True

            try:
                # if we haven't yet sent the headers but they are set
                # we roll back to be able to set them again.
                if status_sent is None:
                    status_set = None
                    headers_set = None
                execute(InternalServerError())
            except Exception:
                pass

            from .debug.tbtools import DebugTraceback

            msg = DebugTraceback(e).render_traceback_text()
            self.server.log("error", f"Error on request:\n{msg}")

    def handle(self) -> None:
        """处理请求时忽略断开的连接."""
        try:
            super().handle()
        except (ConnectionError, socket.timeout) as e:
            self.connection_dropped(e)
        except Exception as e:
            if self.server.ssl_context is not None and is_ssl_error(e):
                self.log_error("SSL error occurred: %s", e)
            else:
                raise

    def connection_dropped(
            self, error: BaseException, environ: t.Optional["WSGIEnvironment"] = None
    ) -> None:
        """Called if the connection was closed by the client.  By default
        nothing happens.
        """

    def __getattr__(self, name: str) -> t.Any:
        # All HTTP methods are handled by run_wsgi.
        if name.startswith("do_"):
            return self.run_wsgi

        # All other attributes are forwarded to the base class.
        return getattr(super(), name)

    def address_string(self) -> str:
        if getattr(self, "environ", None):
            return self.environ["REMOTE_ADDR"]  # type: ignore

        if not self.client_address:
            return "<local>"

        return self.client_address[0]

    def port_integer(self) -> int:
        return self.client_address[1]

    def log_request(
            self, code: t.Union[int, str] = "-", size: t.Union[int, str] = "-"
    ) -> None:
        try:
            path = uri_to_iri(self.path)
            msg = f"{self.command} {path} {self.request_version}"
        except AttributeError:
            # path isn't set if the requestline was bad
            msg = self.requestline

        code = str(code)

        if code[0] == "1":  # 1xx - Informational
            msg = _ansi_style(msg, "bold")
        elif code == "200":  # 2xx - Success
            pass
        elif code == "304":  # 304 - Resource Not Modified
            msg = _ansi_style(msg, "cyan")
        elif code[0] == "3":  # 3xx - Redirection
            msg = _ansi_style(msg, "green")
        elif code == "404":  # 404 - Resource Not Found
            msg = _ansi_style(msg, "yellow")
        elif code[0] == "4":  # 4xx - Client Error
            msg = _ansi_style(msg, "bold", "red")
        else:  # 5xx, or any other response
            msg = _ansi_style(msg, "bold", "magenta")

        self.log("info", '"%s" %s %s', msg, code, size)

    def log_error(self, format: str, *args: t.Any) -> None:
        self.log("error", format, *args)

    def log_message(self, format: str, *args: t.Any) -> None:
        self.log("info", format, *args)

    def log(self, type: str, message: str, *args: t.Any) -> None:
        _log(
            type,
            f"{self.address_string()} - - [{self.log_date_time_string()}] {message}\n",
            *args,
        )


def _ansi_style(value: str, *styles: str) -> str:
    if not _log_add_style:
        return value

    codes = {
        "bold": 1,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "magenta": 35,
        "cyan": 36,
    }

    for style in styles:
        value = f"\x1b[{codes[style]}m{value}"

    return f"{value}\x1b[0m"


def generate_adhoc_ssl_pair(
        cn: t.Optional[str] = None,
) -> t.Tuple["Certificate", "RSAPrivateKeyWithSerialization"]:
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
    except ImportError:
        raise TypeError(
            "Using ad-hoc certificates requires the cryptography library."
        ) from None

    backend = default_backend()
    pkey = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=backend
    )

    # pretty damn sure that this is not actually accepted by anyone
    if cn is None:
        cn = "*"

    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Dummy Certificate"),
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
        ]
    )

    backend = default_backend()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(pkey.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(dt.now(timezone.utc))
        .not_valid_after(dt.now(timezone.utc) + timedelta(days=365))
        .add_extension(x509.ExtendedKeyUsage([x509.OID_SERVER_AUTH]), critical=False)
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(cn)]), critical=False)
        .sign(pkey, hashes.SHA256(), backend)
    )
    return cert, pkey


def make_ssl_devcert(
        base_path: str, host: t.Optional[str] = None, cn: t.Optional[str] = None
) -> t.Tuple[str, str]:
    """Creates an SSL key for development.  This should be used instead of
    the ``'adhoc'`` key which generates a new cert on each server start.
    It accepts a path for where it should store the key and cert and
    either a host or CN.  If a host is given it will use the CN
    ``*.host/CN=host``.

    For more information see :func:`run_simple`.

    .. versionadded:: 0.9

    :param base_path: the path to the certificate and key.  The extension
                      ``.crt`` is added for the certificate, ``.key`` is
                      added for the key.
    :param host: the name of the host.  This can be used as an alternative
                 for the `cn`.
    :param cn: the `CN` to use.
    """

    if host is not None:
        cn = f"*.{host}/CN={host}"
    cert, pkey = generate_adhoc_ssl_pair(cn=cn)

    from cryptography.hazmat.primitives import serialization

    cert_file = f"{base_path}.crt"
    pkey_file = f"{base_path}.key"

    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(pkey_file, "wb") as f:
        f.write(
            pkey.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    return cert_file, pkey_file


def generate_adhoc_ssl_context() -> "ssl.SSLContext":
    """Generates an adhoc SSL context for the development server."""
    import tempfile
    import atexit

    cert, pkey = generate_adhoc_ssl_pair()

    from cryptography.hazmat.primitives import serialization

    cert_handle, cert_file = tempfile.mkstemp()
    pkey_handle, pkey_file = tempfile.mkstemp()
    atexit.register(os.remove, pkey_file)
    atexit.register(os.remove, cert_file)

    os.write(cert_handle, cert.public_bytes(serialization.Encoding.PEM))
    os.write(
        pkey_handle,
        pkey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
    )

    os.close(cert_handle)
    os.close(pkey_handle)
    ctx = load_ssl_context(cert_file, pkey_file)
    return ctx


def load_ssl_context(
        cert_file: str, pkey_file: t.Optional[str] = None, protocol: t.Optional[int] = None
) -> "ssl.SSLContext":
    """Loads SSL context from cert/private key files and optional protocol.
    Many parameters are directly taken from the API of
    :py:class:`ssl.SSLContext`.

    :param cert_file: Path of the certificate to use.
    :param pkey_file: Path of the private key to use. If not given, the key
                      will be obtained from the certificate file.
    :param protocol: A ``PROTOCOL`` constant from the :mod:`ssl` module.
        Defaults to :data:`ssl.PROTOCOL_TLS_SERVER`.
    """
    if protocol is None:
        protocol = ssl.PROTOCOL_TLS_SERVER

    ctx = ssl.SSLContext(protocol)
    ctx.load_cert_chain(cert_file, pkey_file)
    return ctx


def is_ssl_error(error: t.Optional[Exception] = None) -> bool:
    """Checks if the given error (or the current one) is an SSL error."""
    if error is None:
        error = t.cast(Exception, sys.exc_info()[1])
    return isinstance(error, ssl.SSLError)


def select_address_family(host: str) -> socket.AddressFamily:
    """
    根据主机名和端口号选择合适的地址族
    Return： AF_INET4|AF_INET6|oAF_UNIX
    """
    if host.startswith("unix://"):
        return socket.AF_UNIX
    elif ":" in host and hasattr(socket, "AF_INET6"):
        return socket.AF_INET6
    return socket.AF_INET


def get_sockaddr(
        host: str, port: int, family: socket.AddressFamily
) -> t.Union[t.Tuple[str, int], str]:
    """Return a fully qualified socket address that can be passed to
    :func:`socket.bind`."""
    if family == af_unix:
        return host.split("://", 1)[1]
    try:
        res = socket.getaddrinfo(
            host, port, family, socket.SOCK_STREAM, socket.IPPROTO_TCP
        )
    except socket.gaierror:
        return host, port
    return res[0][4]  # type: ignore


def get_interface_ip(family: socket.AddressFamily) -> str:
    """Get the IP address of an external interface. Used when binding to
    0.0.0.0 or ::1 to show a more useful URL.

    :meta private:
    """
    # arbitrary private address
    host = "fd31:f903:5ab5:1::1" if family == socket.AF_INET6 else "10.253.155.219"

    with socket.socket(family, socket.SOCK_DGRAM) as s:
        try:
            s.connect((host, 58162))
        except OSError:
            return "::1" if family == socket.AF_INET6 else "127.0.0.1"

        return s.getsockname()[0]  # type: ignore


class BaseWSGIServer(HTTPServer):
    """一次处理一个请求的 WSGI 服务器。
     使用 make_server 创建服务器实例。
    """

    multithread = False
    multiprocess = False
    request_queue_size = LISTEN_QUEUE
    allow_reuse_address = True

    def __init__(
            self,
            host: str,
            port: int,
            app: "WSGIApplication",
            handler: t.Optional[t.Type[WSGIRequestHandler]] = None,
            passthrough_errors: bool = False,
            ssl_context: t.Optional[_TSSLContextArg] = None,
            fd: t.Optional[int] = None,
    ) -> None:
        if handler is None:
            handler = WSGIRequestHandler

        # 如果没有指定http version，则默认为1.1
        if "protocol_version" not in vars(handler) and (
                self.multithread or self.multiprocess
        ):
            handler.protocol_version = "HTTP/1.1"

        self.host = host
        self.port = port
        self.app = app
        self.passthrough_errors = passthrough_errors

        self.address_family = address_family = select_address_family(host)
        server_address = get_sockaddr(host, int(port), address_family)

        # 删除上次运行中剩余的 Unix 套接字文件。 不要删除由 run_simple 设置的文件。
        if address_family == af_unix and fd is None:
            server_address = t.cast(str, server_address)

            if os.path.exists(server_address):
                os.unlink(server_address)

        # Bind and activate will be handled manually, it should only
        # happen if we're not using a socket that was already set up.
        super().__init__(
            server_address,  # type: ignore[arg-type]
            handler,
            bind_and_activate=False,
        )

        if fd is None:
            # 没有socket，则创建socket
            try:
                self.server_bind()
                self.server_activate()
            except OSError as e:
                # Catch connection issues and show them without the traceback. Show
                # extra instructions for address not found, and for macOS.
                self.server_close()
                print(e.strerror, file=sys.stderr)

                if e.errno == errno.EADDRINUSE:
                    print(
                        f"Port {port} is in use by another program. Either identify and"
                        " stop that program, or start the server with a different"
                        " port.",
                        file=sys.stderr,
                    )

                    if sys.platform == "darwin" and port == 5000:
                        print(
                            "On macOS, try disabling the 'AirPlay Receiver' service"
                            " from System Preferences -> Sharing.",
                            file=sys.stderr,
                        )

                sys.exit(1)
            except BaseException:
                self.server_close()
                raise
        else:
            # TCPServer automatically opens a socket even if bind_and_activate is False.
            # Close it to silence a ResourceWarning.
            self.server_close()

            # Use the passed in socket directly.
            self.socket = socket.fromfd(fd, address_family, socket.SOCK_STREAM)
            self.server_address = self.socket.getsockname()

        if address_family != af_unix:
            # If port was 0, this will record the bound port.
            self.port = self.server_address[1]

        if ssl_context is not None:
            if isinstance(ssl_context, tuple):
                ssl_context = load_ssl_context(*ssl_context)
            elif ssl_context == "adhoc":
                ssl_context = generate_adhoc_ssl_context()

            self.socket = ssl_context.wrap_socket(self.socket, server_side=True)
            self.ssl_context: t.Optional["ssl.SSLContext"] = ssl_context
        else:
            self.ssl_context = None

    def log(self, type: str, message: str, *args: t.Any) -> None:
        _log(type, message, *args)

    def serve_forever(self, poll_interval: float = 0.5) -> None:
        try:
            super().serve_forever(poll_interval=poll_interval)
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()

    def handle_error(
            self, request: t.Any, client_address: t.Union[t.Tuple[str, int], str]
    ) -> None:
        if self.passthrough_errors:
            raise

        return super().handle_error(request, client_address)

    def log_startup(self) -> None:
        """Show information about the address when starting the server."""
        dev_warning = (
            "WARNING: This is a development server. Do not use it in a production"
            " deployment. Use a production WSGI server instead."
        )
        dev_warning = _ansi_style(dev_warning, "bold", "red")
        messages = [dev_warning]

        if self.address_family == af_unix:
            messages.append(f" * Running on {self.host}")
        else:
            scheme = "http" if self.ssl_context is None else "https"
            display_hostname = self.host

            if self.host in {"0.0.0.0", "::"}:
                messages.append(f" * Running on all addresses ({self.host})")

                if self.host == "0.0.0.0":
                    localhost = "127.0.0.1"
                    display_hostname = get_interface_ip(socket.AF_INET)
                else:
                    localhost = "[::1]"
                    display_hostname = get_interface_ip(socket.AF_INET6)

                messages.append(f" * Running on {scheme}://{localhost}:{self.port}")

            if ":" in display_hostname:
                display_hostname = f"[{display_hostname}]"

            messages.append(f" * Running on {scheme}://{display_hostname}:{self.port}")

        _log("info", "\n".join(messages))


class ThreadedWSGIServer(socketserver.ThreadingMixIn, BaseWSGIServer):
    """WSGI 服务器在单独的线程中处理并发请求。
     使用 make_server 创建服务器实例。
    """

    multithread = True
    daemon_threads = True


class ForkingWSGIServer(ForkingMixIn, BaseWSGIServer):
    """A WSGI server that handles concurrent requests in separate forked
    processes.

    Use :func:`make_server` to create a server instance.
    """

    multiprocess = True

    def __init__(
            self,
            host: str,
            port: int,
            app: "WSGIApplication",
            processes: int = 40,
            handler: t.Optional[t.Type[WSGIRequestHandler]] = None,
            passthrough_errors: bool = False,
            ssl_context: t.Optional[_TSSLContextArg] = None,
            fd: t.Optional[int] = None,
    ) -> None:
        if not can_fork:
            raise ValueError("Your platform does not support forking.")

        super().__init__(host, port, app, handler, passthrough_errors, ssl_context, fd)
        self.max_children = processes


def make_server(
        host: str,
        port: int,
        app: "WSGIApplication",
        threaded: bool = False,
        processes: int = 1,
        request_handler: t.Optional[t.Type[WSGIRequestHandler]] = None,
        passthrough_errors: bool = False,
        ssl_context: t.Optional[_TSSLContextArg] = None,
        fd: t.Optional[int] = None,
) -> BaseWSGIServer:
    if threaded and processes > 1:
        raise ValueError("不能有多线程和多进程服务器")

    if threaded:
        return ThreadedWSGIServer(
            host, port, app, request_handler, passthrough_errors, ssl_context, fd=fd
        )

    if processes > 1:
        return ForkingWSGIServer(
            host, port, app, processes, request_handler, passthrough_errors,
            ssl_context, fd=fd,
        )

    return BaseWSGIServer(
        host, port, app, request_handler, passthrough_errors, ssl_context, fd=fd
    )


def is_running_from_reloader() -> bool:
    """Check if the server is running as a subprocess within the
    Werkzeug reloader.

    .. versionadded:: 0.10
    """
    return os.environ.get("WERKZEUG_RUN_MAIN") == "true"


def run_simple(
        hostname: str,
        port: int,
        application: "WSGIApplication",
        use_reloader: bool = False,
        use_debugger: bool = False,
        use_evalex: bool = True,
        extra_files: t.Optional[t.Iterable[str]] = None,
        exclude_patterns: t.Optional[t.Iterable[str]] = None,
        reloader_interval: int = 1,
        reloader_type: str = "auto",
        threaded: bool = False,
        processes: int = 1,
        request_handler: t.Optional[t.Type[WSGIRequestHandler]] = None,
        static_files: t.Optional[t.Dict[str, t.Union[str, t.Tuple[str, str]]]] = None,
        passthrough_errors: bool = False,
        ssl_context: t.Optional[_TSSLContextArg] = None,
) -> None:
    """开发服务器不建议用于生产环境部署，仅适用于本地开发。它的设计目标不是高效、稳定或安全。


    hostname：要绑定到的主机名，可以是域名、IPv4 或 IPv6 地址，也可以是以 unix:// 开头的文件路径，用于指定 Unix socket。
    port：要绑定到的端口号，例如 8080。如果使用 0，操作系统将选择一个随机可用的端口。
    application：要运行的 WSGI 应用程序。
    use_reloader：使用重载进程在文件更改时重新启动服务器进程。
    use_debugger：使用 Werkzeug 的调试器，在未处理的异常发生时显示格式化的回溯信息。
    use_evalex：使调试器交互式。可以为回溯中的任何帧打开一个 Python 终端。通过要求输入 PIN 提供了一些保护，但绝不应在公开可见的服务器上启用此功能。
    extra_files：除 Python 模块外，重载器还会监视这些文件的更改。例如，可以监视配置文件的更改。
    exclude_patterns：重载器将忽略与这些 fnmatch 模式匹配的文件的更改。例如，可以忽略缓存文件。
    reloader_interval：重载器尝试检查更改的频率。
    reloader_type：要使用的重载器。'stat' 重载器是内置的，但可能需要占用大量 CPU 来监视文件。'watchdog' 重载器效率更高，但需要先安装 watchdog 包。
    threaded：使用线程处理并发请求。不能与 processes 一起使用。
    processes：使用最多这个数量的进程来处理并发请求。不能与 threaded 一起使用。
    request_handler：使用不同的 BaseHTTPRequestHandler 子类来处理请求。
    static_files：将 URL 前缀映射到要使用 werkzeug.middleware.SharedDataMiddleware 从中提供静态文件的目录的字典。
    passthrough_errors：不在服务器级别捕获未处理的异常，而是让服务器崩溃。如果启用了 use_debugger，调试器仍会捕获此类错误。
    ssl_context：配置 TLS 以通过 HTTPS 进行服务。可以是 ssl.SSLContext 对象、(cert_file, key_file) 元组以创建典型的上下文，或者字符串 'adhoc' 以生成临时的自签名证书。
    """
    if not isinstance(port, int):
        raise TypeError("port must be an integer")

    if static_files:
        from .middleware.shared_data import SharedDataMiddleware

        application = SharedDataMiddleware(application, static_files)

    if use_debugger:
        from .debug import DebuggedApplication

        application = DebuggedApplication(application, evalex=use_evalex)

    if not is_running_from_reloader():
        fd = None
    else:
        fd = int(os.environ["WERKZEUG_SERVER_FD"])

    srv = make_server(
        hostname,
        port,
        application,
        threaded,
        processes,
        request_handler,
        passthrough_errors,
        ssl_context,
        fd=fd,
    )
    srv.socket.set_inheritable(True)  # 设置套接字可继承，派生的子进程可以继承套接字
    os.environ["WERKZEUG_SERVER_FD"] = str(srv.fileno())

    if not is_running_from_reloader():
        srv.log_startup()
        _log("info", _ansi_style("Press CTRL+C to quit", "yellow"))  # 格式化输出

    if use_reloader:
        from ._reloader import run_with_reloader

        try:
            run_with_reloader(
                srv.serve_forever,
                extra_files=extra_files,
                exclude_patterns=exclude_patterns,
                interval=reloader_interval,
                reloader_type=reloader_type,
            )
        finally:
            srv.server_close()
    else:
        srv.serve_forever()
