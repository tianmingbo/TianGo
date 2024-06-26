import typing as t

from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import Request as RequestBase
from werkzeug.wrappers import Response as ResponseBase

from . import json
from .globals import current_app
from .helpers import _split_blueprint_path

if t.TYPE_CHECKING:
    import typing_extensions as te
    from werkzeug.routing import Rule


class Request(RequestBase):
    """
    继承自werkzeug.wrappers.Request
    """
    json_module = json
    url_rule: t.Optional["Rule"] = None
    view_args: t.Optional[t.Dict[str, t.Any]] = None
    # 路由匹配异常时抛出的错误,通常是NotFound
    routing_exception: t.Optional[Exception] = None

    @property
    def max_content_length(self) -> t.Optional[int]:  # type: ignore
        """Read-only view of the ``MAX_CONTENT_LENGTH`` config key."""
        if current_app:
            return current_app.config["MAX_CONTENT_LENGTH"]
        else:
            return None

    @property
    def endpoint(self) -> t.Optional[str]:
        """The endpoint that matched the request URL.

        This will be ``None`` if matching failed or has not been
        performed yet.

        This in combination with :attr:`view_args` can be used to
        reconstruct the same URL or a modified URL.
        """
        if self.url_rule is not None:
            return self.url_rule.endpoint

        return None

    @property
    def blueprint(self) -> t.Optional[str]:
        """The registered name of the current blueprint.

        This will be ``None`` if the endpoint is not part of a
        blueprint, or if URL matching failed or has not been performed
        yet.

        This does not necessarily match the name the blueprint was
        created with. It may have been nested, or registered with a
        different name.
        """
        endpoint = self.endpoint

        if endpoint is not None and "." in endpoint:
            return endpoint.rpartition(".")[0]

        return None

    @property
    def blueprints(self) -> t.List[str]:
        """The registered names of the current blueprint upwards through
        parent blueprints.

        This will be an empty list if there is no current blueprint, or
        if URL matching failed.

        .. versionadded:: 2.0.1
        """
        name = self.blueprint

        if name is None:
            return []

        return _split_blueprint_path(name)

    def _load_form_data(self) -> None:
        RequestBase._load_form_data(self)

        # In debug mode we're replacing the files multidict with an ad-hoc
        # subclass that raises a different error for key errors.
        if (
                current_app
                and current_app.debug
                and self.mimetype != "multipart/form-data"
                and not self.files
        ):
            from .debughelpers import attach_enctype_error_multidict

            attach_enctype_error_multidict(self)

    def on_json_loading_failed(self, e: Exception) -> "te.NoReturn":
        if current_app and current_app.debug:
            raise BadRequest(f"Failed to decode JSON object: {e}")

        raise BadRequest()


class Response(ResponseBase):
    """
    Flask 默认使用的响应对象。默认mimetype为text/html
    """

    default_mimetype = "text/html"

    @property
    def max_cookie_size(self) -> int:  # type: ignore
        """Read-only view of the :data:`MAX_COOKIE_SIZE` config key.

        See :attr:`~werkzeug.wrappers.Response.max_cookie_size` in
        Werkzeug's docs.
        """
        if current_app:
            return current_app.config["MAX_COOKIE_SIZE"]

        # return Werkzeug's default when not in an app context
        return super().max_cookie_size
