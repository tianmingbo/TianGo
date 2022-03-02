var begintime = Math.round((new Date).getTime() / 1000);
"object" !== typeof JSON && (JSON = {});
(function () {
    function a(b) {
        return 10 > b ? "0" + b : b
    }

    function k(b) {
        q.lastIndex = 0;
        return q.test(b) ? '"' + b.replace(q,
            function (b) {
                var a = f[b];
                return "string" === typeof a ? a : "\\u" + ("0000" + b.charCodeAt(0).toString(16)).slice(-4)
            }) + '"' : '"' + b + '"'
    }

    function b(a, g) {
        var r, f, c = l,
            p, d = g[a];
        d && "object" === typeof d && "function" === typeof d.toJSON && (d = d.toJSON(a));
        "function" === typeof n && (d = n.call(g, a, d));
        switch (typeof d) {
            case "string":
                return k(d);
            case "number":
                return isFinite(d) ? String(d) : "null";
            case "boolean":
            case "null":
                return String(d);
            case "object":
                if (!d) return "null";
                l += m;
                p = [];
                if ("[object Array]" === Object.prototype.toString.apply(d)) {
                    g = d.length;
                    for (a = 0; a < g; a += 1) p[a] = b(a, d) || "null";
                    f = 0 === p.length ? "[]" : l ? "[\n" + l + p.join(",\n" + l) + "\n" + c + "]" : "[" + p.join(",") + "]";
                    l = c;
                    return f
                }
                if (n && "object" === typeof n) for (g = n.length, a = 0; a < g; a += 1) "string" === typeof n[a] && (r = n[a], (f = b(r, d)) && p.push(k(r) + (l ? ": " : ":") + f));
                else for (r in d) Object.prototype.hasOwnProperty.call(d, r) && (f = b(r, d)) && p.push(k(r) + (l ? ": " : ":") + f);
                f = 0 === p.length ? "{}" : l ? "{\n" + l + p.join(",\n" + l) + "\n" + c + "}" : "{" + p.join(",") + "}";
                l = c;
                return f
        }
    }

    "function" !== typeof Date.prototype.toJSON && (Date.prototype.toJSON = function () {
        return isFinite(this.valueOf()) ? this.getUTCFullYear() + "-" + a(this.getUTCMonth() + 1) + "-" + a(this.getUTCDate()) + "T" + a(this.getUTCHours()) + ":" + a(this.getUTCMinutes()) + ":" + a(this.getUTCSeconds()) + "Z" : null
    },
        String.prototype.toJSON = Number.prototype.toJSON = Boolean.prototype.toJSON = function () {
            return this.valueOf()
        });
    var g, q, l, m, f, n;
    "function" !== typeof JSON.stringify && (q = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, f = {
        "\b": "\\b",
        "\t": "\\t",
        "\n": "\\n",
        "\f": "\\f",
        "\r": "\\r",
        '"': '\\"',
        "\\": "\\\\"
    },
        JSON.stringify = function (a, g, f) {
            var k;
            m = l = "";
            if ("number" === typeof f) for (k = 0; k < f; k += 1) m += " ";
            else "string" === typeof f && (m = f);
            if ((n = g) && "function" !== typeof g && ("object" !== typeof g || "number" !== typeof g.length)) throw Error("JSON.stringify");
            return b("", {
                "": a
            })
        });
    "function" !== typeof JSON.parse && (g = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, JSON.parse = function (a, b) {
        function f(c, a) {
            var d, e, h = c[a];
            if (h && "object" === typeof h) for (d in h) Object.prototype.hasOwnProperty.call(h, d) && (e = f(h, d), void 0 !== e ? h[d] = e : delete h[d]);
            return b.call(c, a, h)
        }

        var k;
        a = String(a);
        g.lastIndex = 0;
        g.test(a) && (a = a.replace(g,
            function (c) {
                return "\\u" + ("0000" + c.charCodeAt(0).toString(16)).slice(-4)
            }));
        if (/^[\],:{}\s]*$/.test(a.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) return k = eval("(" + a + ")"),
            "function" === typeof b ? f({
                    "": k
                },
                "") : k;
        throw new SyntaxError("JSON.parse");
    })
})();

function Rnd(a, k) {
    return a + Math.round(Math.random() * (k - a))
}

function RndKey(b, a) {
    for (var k = [], g = 0; g < (a ? a : Rnd(4, 6)); g++) b = Rnd(b, b + 1),
        k.push(b);
    return k
}

var enc = function (a) {
        var k = CryptoJS.enc.Utf8.parse("0123456789abcdef");
        return CryptoJS.AES.encrypt(a, k, {
            iv: k,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        }).toString()
    },
    GetMonseMove = function (a) {
        var k = [];
        a += 1;
        for (var b = 0; b < a; b++) 0 !== b && a - 1 !== b && b !== Rnd(b, a - 1) || k.push({
            t: 1 == a ? Rnd(1, 10) : b,
            x: Rnd(123, 345),
            y: Rnd(135, 246)
        });
        return k
    },
    CryptoJS = CryptoJS ||
        function (a, k) {
            var b = {},
                g = b.lib = {},
                q = function () {
                },
                l = g.Base = {
                    extend: function (c) {
                        q.prototype = this;
                        var a = new q;
                        c && a.mixIn(c);
                        a.hasOwnProperty("init") || (a.init = function () {
                            a.$super.init.apply(this, arguments)
                        });
                        a.init.prototype = a;
                        a.$super = this;
                        return a
                    },
                    create: function () {
                        var c = this.extend();
                        c.init.apply(c, arguments);
                        return c
                    },
                    init: function () {
                    },
                    mixIn: function (c) {
                        for (var a in c) c.hasOwnProperty(a) && (this[a] = c[a]);
                        c.hasOwnProperty("toString") && (this.toString = c.toString)
                    },
                    clone: function () {
                        return this.init.prototype.extend(this)
                    }
                },
                m = g.WordArray = l.extend({
                    init: function (c, a) {
                        c = this.words = c || [];
                        this.sigBytes = a != k ? a : 4 * c.length
                    },
                    toString: function (c) {
                        return (c || n).stringify(this)
                    },
                    concat: function (c) {
                        var a = this.words,
                            d = c.words,
                            e = this.sigBytes;
                        c = c.sigBytes;
                        this.clamp();
                        if (e % 4) for (var h = 0; h < c; h++) a[e + h >>> 2] |= (d[h >>> 2] >>> 24 - h % 4 * 8 & 255) << 24 - (e + h) % 4 * 8;
                        else if (65535 < d.length) for (h = 0; h < c; h += 4) a[e + h >>> 2] = d[h >>> 2];
                        else a.push.apply(a, d);
                        this.sigBytes += c;
                        return this
                    },
                    clamp: function () {
                        var c = this.words,
                            b = this.sigBytes;
                        c[b >>> 2] &= 4294967295 << 32 - b % 4 * 8;
                        c.length = a.ceil(b / 4)
                    },
                    clone: function () {
                        var c = l.clone.call(this);
                        c.words = this.words.slice(0);
                        return c
                    },
                    random: function (c) {
                        for (var b = [], d = 0; d < c; d += 4) b.push(4294967296 * a.random() | 0);
                        return new m.init(b, c)
                    }
                }),
                f = b.enc = {},
                n = f.Hex = {
                    stringify: function (c) {
                        var a = c.words;
                        c = c.sigBytes;
                        for (var d = [], e = 0; e < c; e++) {
                            var h = a[e >>> 2] >>> 24 - e % 4 * 8 & 255;
                            d.push((h >>> 4).toString(16));
                            d.push((h & 15).toString(16))
                        }
                        return d.join("")
                    },
                    parse: function (c) {
                        for (var a = c.length,
                                 d = [], e = 0; e < a; e += 2) d[e >>> 3] |= parseInt(c.substr(e, 2), 16) << 24 - e % 8 * 4;
                        return new m.init(d, a / 2)
                    }
                },
                u = f.Latin1 = {
                    stringify: function (c) {
                        var a = c.words;
                        c = c.sigBytes;
                        for (var d = [], e = 0; e < c; e++) d.push(String.fromCharCode(a[e >>> 2] >>> 24 - e % 4 * 8 & 255));
                        return d.join("")
                    },
                    parse: function (a) {
                        for (var c = a.length,
                                 d = [], e = 0; e < c; e++) d[e >>> 2] |= (a.charCodeAt(e) & 255) << 24 - e % 4 * 8;
                        return new m.init(d, c)
                    }
                },
                w = f.Utf8 = {
                    stringify: function (a) {
                        try {
                            return decodeURIComponent(escape(u.stringify(a)))
                        } catch (p) {
                            throw Error("Malformed UTF-8 data");
                        }
                    },
                    parse: function (a) {
                        return u.parse(unescape(encodeURIComponent(a)))
                    }
                },
                r = g.BufferedBlockAlgorithm = l.extend({
                    reset: function () {
                        this._data = new m.init;
                        this._nDataBytes = 0
                    },
                    _append: function (a) {
                        "string" == typeof a && (a = w.parse(a));
                        this._data.concat(a);
                        this._nDataBytes += a.sigBytes
                    },
                    _process: function (c) {
                        var b = this._data,
                            d = b.words,
                            e = b.sigBytes,
                            h = this.blockSize,
                            g = e / (4 * h),
                            g = c ? a.ceil(g) : a.max((g | 0) - this._minBufferSize, 0);
                        c = g * h;
                        e = a.min(4 * c, e);
                        if (c) {
                            for (var f = 0; f < c; f += h) this._doProcessBlock(d, f);
                            f = d.splice(0, c);
                            b.sigBytes -= e
                        }
                        return new m.init(f, e)
                    },
                    clone: function () {
                        var a = l.clone.call(this);
                        a._data = this._data.clone();
                        return a
                    },
                    _minBufferSize: 0
                });
            g.Hasher = r.extend({
                cfg: l.extend(),
                init: function (a) {
                    this.cfg = this.cfg.extend(a);
                    this.reset()
                },
                reset: function () {
                    r.reset.call(this);
                    this._doReset()
                },
                update: function (a) {
                    this._append(a);
                    this._process();
                    return this
                },
                finalize: function (a) {
                    a && this._append(a);
                    return this._doFinalize()
                },
                blockSize: 16,
                _createHelper: function (a) {
                    return function (c, d) {
                        return (new a.init(d)).finalize(c)
                    }
                },
                _createHmacHelper: function (a) {
                    return function (c, d) {
                        return (new v.HMAC.init(a, d)).finalize(c)
                    }
                }
            });
            var v = b.algo = {};
            return b
        }(Math);
(function () {
    var a = CryptoJS,
        k = a.lib.WordArray;
    a.enc.Base64 = {
        stringify: function (a) {
            var b = a.words,
                k = a.sigBytes,
                l = this._map;
            a.clamp();
            a = [];
            for (var m = 0; m < k; m += 3) for (var f = (b[m >>> 2] >>> 24 - m % 4 * 8 & 255) << 16 | (b[m + 1 >>> 2] >>> 24 - (m + 1) % 4 * 8 & 255) << 8 | b[m + 2 >>> 2] >>> 24 - (m + 2) % 4 * 8 & 255, n = 0; 4 > n && m + .75 * n < k; n++) a.push(l.charAt(f >>> 6 * (3 - n) & 63));
            if (b = l.charAt(64)) for (; a.length % 4;) a.push(b);
            return a.join("")
        },
        parse: function (a) {
            var b = a.length,
                q = this._map,
                l = q.charAt(64);
            l && (l = a.indexOf(l), -1 != l && (b = l));
            for (var l = [], m = 0, f = 0; f < b; f++) if (f % 4) {
                var n = q.indexOf(a.charAt(f - 1)) << f % 4 * 2,
                    u = q.indexOf(a.charAt(f)) >>> 6 - f % 4 * 2;
                l[m >>> 2] |= (n | u) << 24 - m % 4 * 8;
                m++
            }
            return k.create(l, m)
        },
        _map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    }
})();
CryptoJS.lib.Cipher ||
function (a) {
    var k = CryptoJS,
        b = k.lib,
        g = b.Base,
        q = b.WordArray,
        l = b.BufferedBlockAlgorithm,
        m = k.enc.Base64,
        f = k.algo.EvpKDF,
        n = b.Cipher = l.extend({
            cfg: g.extend(),
            createEncryptor: function (d, a) {
                return this.create(this._ENC_XFORM_MODE, d, a)
            },
            createDecryptor: function (d, a) {
                return this.create(this._DEC_XFORM_MODE, d, a)
            },
            init: function (d, a, c) {
                this.cfg = this.cfg.extend(c);
                this._xformMode = d;
                this._key = a;
                this.reset()
            },
            reset: function () {
                l.reset.call(this);
                this._doReset()
            },
            process: function (d) {
                this._append(d);
                return this._process()
            },
            finalize: function (d) {
                d && this._append(d);
                return this._doFinalize()
            },
            keySize: 4,
            ivSize: 4,
            _ENC_XFORM_MODE: 1,
            _DEC_XFORM_MODE: 2,
            _createHelper: function (d) {
                return {
                    encrypt: function (a, h, b) {
                        return ("string" == typeof h ? p : c).encrypt(d, a, h, b)
                    },
                    decrypt: function (a, b, g) {
                        return ("string" == typeof b ? p : c).decrypt(d, a, b, g)
                    }
                }
            }
        });
    b.StreamCipher = n.extend({
        _doFinalize: function () {
            return this._process(!0)
        },
        blockSize: 1
    });
    var u = k.mode = {},
        w = function (d, e, c) {
            var b = this._iv;
            b ? this._iv = a : b = this._prevBlock;
            for (var h = 0; h < c; h++) d[e + h] ^= b[h]
        },
        r = (b.BlockCipherMode = g.extend({
            createEncryptor: function (d, a) {
                return this.Encryptor.create(d, a)
            },
            createDecryptor: function (a, e) {
                return this.Decryptor.create(a, e)
            },
            init: function (a, e) {
                this._cipher = a;
                this._iv = e
            }
        })).extend();
    r.Encryptor = r.extend({
        processBlock: function (a, e) {
            var d = this._cipher,
                c = d.blockSize;
            w.call(this, a, e, c);
            d.encryptBlock(a, e);
            this._prevBlock = a.slice(e, e + c)
        }
    });
    r.Decryptor = r.extend({
        processBlock: function (a, e) {
            var d = this._cipher,
                c = d.blockSize,
                b = a.slice(e, e + c);
            d.decryptBlock(a, e);
            w.call(this, a, e, c);
            this._prevBlock = b
        }
    });
    u = u.CBC = r;
    r = (k.pad = {}).Pkcs7 = {
        pad: function (a, e) {
            e *= 4;
            e -= a.sigBytes % e;
            for (var d = e << 24 | e << 16 | e << 8 | e,
                     c = [], b = 0; b < e; b += 4) c.push(d);
            e = q.create(c, e);
            a.concat(e)
        },
        unpad: function (a) {
            a.sigBytes -= a.words[a.sigBytes - 1 >>> 2] & 255
        }
    };
    b.BlockCipher = n.extend({
        cfg: n.cfg.extend({
            mode: u,
            padding: r
        }),
        reset: function () {
            n.reset.call(this);
            var a = this.cfg,
                e = a.iv,
                a = a.mode;
            if (this._xformMode == this._ENC_XFORM_MODE) var c = a.createEncryptor;
            else c = a.createDecryptor,
                this._minBufferSize = 1;
            this._mode = c.call(a, this, e && e.words)
        },
        _doProcessBlock: function (a, e) {
            this._mode.processBlock(a, e)
        },
        _doFinalize: function () {
            var a = this.cfg.padding;
            if (this._xformMode == this._ENC_XFORM_MODE) {
                a.pad(this._data, this.blockSize);
                var e = this._process(!0)
            } else e = this._process(!0),
                a.unpad(e);
            return e
        },
        blockSize: 4
    });
    var v = b.CipherParams = g.extend({
            init: function (a) {
                this.mixIn(a)
            },
            toString: function (a) {
                return (a || this.formatter).stringify(this)
            }
        }),
        u = (k.format = {}).OpenSSL = {
            stringify: function (a) {
                var d = a.ciphertext;
                a = a.salt;
                return (a ? q.create([1398893684, 1701076831]).concat(a).concat(d) : d).toString(m)
            },
            parse: function (a) {
                a = m.parse(a);
                var d = a.words;
                if (1398893684 == d[0] && 1701076831 == d[1]) {
                    var c = q.create(d.slice(2, 4));
                    d.splice(0, 4);
                    a.sigBytes -= 16
                }
                return v.create({
                    ciphertext: a,
                    salt: c
                })
            }
        },
        c = b.SerializableCipher = g.extend({
            cfg: g.extend({
                format: u
            }),
            encrypt: function (a, c, b, g) {
                g = this.cfg.extend(g);
                var d = a.createEncryptor(b, g);
                c = d.finalize(c);
                d = d.cfg;
                return v.create({
                    ciphertext: c,
                    key: b,
                    iv: d.iv,
                    algorithm: a,
                    mode: d.mode,
                    padding: d.padding,
                    blockSize: a.blockSize,
                    formatter: g.format
                })
            },
            decrypt: function (a, c, b, g) {
                g = this.cfg.extend(g);
                c = this._parse(c, g.format);
                return a.createDecryptor(b, g).finalize(c.ciphertext)
            },
            _parse: function (a, c) {
                return "string" == typeof a ? c.parse(a, this) : a
            }
        }),
        k = (k.kdf = {}).OpenSSL = {
            execute: function (a, c, b, g) {
                g || (g = q.random(8));
                a = f.create({
                    keySize: c + b
                }).compute(a, g);
                b = q.create(a.words.slice(c), 4 * b);
                a.sigBytes = 4 * c;
                return v.create({
                    key: a,
                    iv: b,
                    salt: g
                })
            }
        },
        p = b.PasswordBasedCipher = c.extend({
            cfg: c.cfg.extend({
                kdf: k
            }),
            encrypt: function (a, b, g, f) {
                f = this.cfg.extend(f);
                g = f.kdf.execute(g, a.keySize, a.ivSize);
                f.iv = g.iv;
                a = c.encrypt.call(this, a, b, g.key, f);
                a.mixIn(g);
                return a
            },
            decrypt: function (a, b, g, f) {
                f = this.cfg.extend(f);
                b = this._parse(b, f.format);
                g = f.kdf.execute(g, a.keySize, a.ivSize, b.salt);
                f.iv = g.iv;
                return c.decrypt.call(this, a, b, g.key, f)
            }
        })
}();
(function () {
    for (var a = CryptoJS,
             k = a.lib.BlockCipher,
             b = a.algo,
             g = [], q = [], l = [], m = [], f = [], n = [], u = [], w = [], r = [], v = [], c = [], p = 0; 256 > p; p++) c[p] = 128 > p ? p << 1 : p << 1 ^ 283;
    for (var d = 0,
             e = 0,
             p = 0; 256 > p; p++) {
        var h = e ^ e << 1 ^ e << 2 ^ e << 3 ^ e << 4,
            h = h >>> 8 ^ h & 255 ^ 99;
        g[d] = h;
        q[h] = d;
        var x = c[d],
            y = c[x],
            z = c[y],
            t = 257 * c[h] ^ 16843008 * h;
        l[d] = t << 24 | t >>> 8;
        m[d] = t << 16 | t >>> 16;
        f[d] = t << 8 | t >>> 24;
        n[d] = t;
        t = 16843009 * z ^ 65537 * y ^ 257 * x ^ 16843008 * d;
        u[h] = t << 24 | t >>> 8;
        w[h] = t << 16 | t >>> 16;
        r[h] = t << 8 | t >>> 24;
        v[h] = t;
        d ? (d = x ^ c[c[c[z ^ x]]], e ^= c[c[e]]) : d = e = 1
    }
    var A = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54],
        b = b.AES = k.extend({
            _doReset: function () {
                for (var a = this._key,
                         c = a.words,
                         b = a.sigBytes / 4,
                         a = 4 * ((this._nRounds = b + 6) + 1), d = this._keySchedule = [], e = 0; e < a; e++) if (e < b) d[e] = c[e];
                else {
                    var f = d[e - 1];
                    e % b ? 6 < b && 4 == e % b && (f = g[f >>> 24] << 24 | g[f >>> 16 & 255] << 16 | g[f >>> 8 & 255] << 8 | g[f & 255]) : (f = f << 8 | f >>> 24, f = g[f >>> 24] << 24 | g[f >>> 16 & 255] << 16 | g[f >>> 8 & 255] << 8 | g[f & 255], f ^= A[e / b | 0] << 24);
                    d[e] = d[e - b] ^ f
                }
                c = this._invKeySchedule = [];
                for (b = 0; b < a; b++) e = a - b,
                    f = b % 4 ? d[e] : d[e - 4],
                    c[b] = 4 > b || 4 >= e ? f : u[g[f >>> 24]] ^ w[g[f >>> 16 & 255]] ^ r[g[f >>> 8 & 255]] ^ v[g[f & 255]]
            },
            encryptBlock: function (a, b) {
                this._doCryptBlock(a, b, this._keySchedule, l, m, f, n, g)
            },
            decryptBlock: function (a, b) {
                var c = a[b + 1];
                a[b + 1] = a[b + 3];
                a[b + 3] = c;
                this._doCryptBlock(a, b, this._invKeySchedule, u, w, r, v, q);
                c = a[b + 1];
                a[b + 1] = a[b + 3];
                a[b + 3] = c
            },
            _doCryptBlock: function (a, b, c, d, e, f, g, h) {
                for (var k = this._nRounds,
                         l = a[b] ^ c[0], m = a[b + 1] ^ c[1], n = a[b + 2] ^ c[2], p = a[b + 3] ^ c[3], q = 4, r = 1; r < k; r++) var t = d[l >>> 24] ^ e[m >>> 16 & 255] ^ f[n >>> 8 & 255] ^ g[p & 255] ^ c[q++],
                         u = d[m >>> 24] ^ e[n >>> 16 & 255] ^ f[p >>> 8 & 255] ^ g[l & 255] ^ c[q++],
                         v = d[n >>> 24] ^ e[p >>> 16 & 255] ^ f[l >>> 8 & 255] ^ g[m & 255] ^ c[q++],
                         p = d[p >>> 24] ^ e[l >>> 16 & 255] ^ f[m >>> 8 & 255] ^ g[n & 255] ^ c[q++],
                         l = t,
                         m = u,
                         n = v;
                t = (h[l >>> 24] << 24 | h[m >>> 16 & 255] << 16 | h[n >>> 8 & 255] << 8 | h[p & 255]) ^ c[q++];
                u = (h[m >>> 24] << 24 | h[n >>> 16 & 255] << 16 | h[p >>> 8 & 255] << 8 | h[l & 255]) ^ c[q++];
                v = (h[n >>> 24] << 24 | h[p >>> 16 & 255] << 16 | h[l >>> 8 & 255] << 8 | h[m & 255]) ^ c[q++];
                p = (h[p >>> 24] << 24 | h[l >>> 16 & 255] << 16 | h[m >>> 8 & 255] << 8 | h[n & 255]) ^ c[q++];
                a[b] = t;
                a[b + 1] = u;
                a[b + 2] = v;
                a[b + 3] = p
            },
            keySize: 8
        });
    a.AES = k._createHelper(b)
})();
var Hs = function (xxx, a, k, b, g) {
    var q = Math.round((new Date).getTime()),
        l = Rnd(5, 10),
        m = Rnd(4, 6),
        f = [[800, 600], [1024, 768], [1280, 720], [1280, 768], [1280, 800], [1280, 960], [1280, 1024], [1360, 768], [1360, 1024], [1440, 900], [1600, 1024], [1600, 1200], [1800, 1440], [1920, 1080], [1920, 1200], [1920, 1440]],
        f = [1440, 900],
        n = function () {
            var d = Rnd(1, 9).toString();
            for (var x = 0; x < 9; x++) d += Rnd(0, 9).toString();
            return parseInt(d)
        },
        k = Rnd(4, 10),
        tkid = n();
    a = {
        mousemove: GetMonseMove(l),
        mouseclick: GetMonseMove(0),
        keyvalue: RndKey(m),
        user_Agent: b ? b : "chrome/53.0.2785.104;",
        resolutionx: f[0],
        resolutiony: f[1],
        winSize: [300, 152],
        url: a ? a : "https://captcha.guard.qcloud.com/cap_union_new_show",
        refer: k ? k : "https://m.10010.com/queen/tencent/fill.html",
        begintime: begintime,
        endtime: Math.round(q / 1000) + Rnd(5, 10),
        platform: 1,
        os: g ? g : "Win7",
        keyboards: m,
        flash: 1,
        pluginNum: Rnd(1, 50),
        index: 10,
        ptcz: "",
        tokenid: tkid,
        i: tkid,
        btokenid: null,
        tokents: (begintime) - Rnd(631084, 666666),
        ips: {},
        colorDepth: 24,
        cookieEnabled: !0,
        timezone: 8,
        wDelta: 0,
        keyUpCnt: 0,
        keyUpValue: [],
        mouseUpValue: [],
        mouseUpCnt: 9,
        mouseDownValue: [],
        mouseDownCnt: 2,
        orientation: {x: 0, y: 0, z: 0},
        bSimutor: 0,
        focusBlur: {
            "in": [],
            out: [],
            t: []
        },
        fVersion: 23.9,
        charSet: "utf-8",
        resizeCnt: 0,
        errors: [],
        screenInfo: f[0] + "-" + f[1] + "-818-24-*-*-*",
        elapsed: 0,
        ft: "6f_7P_n_H",
        clientType: "1",
        coordinate: [0, 0, 0.6821],
        trycnt: 10,
        refreshcnt: 1,
        slideValue: [[118, 288, 17], [xxx, 0, 12]]
    };

    a = JSON.stringify(a);
    var salt = 15 - a["length"] % 16;
    for (i = 0; i < salt; i++) {
        a += " "
    }
    ;
    return encodeURIComponent(enc(a))
};

function getbadbdd(a) {
    var salt = 15 - a["length"] % 16;
    for (i = 0; i < salt; i++) {
        a += " "
    }
    ;
    return enc(a);
}