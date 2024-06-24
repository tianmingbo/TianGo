window.captchaConfig = {
  htdocsPath: "https://captcha.gtimg.com/1",
  lang: "1",
  color: "007aff",
  tdcHtdocsPath: "",
  dcFileName: "tdc.js?app_data=6928701972885299200&t=730734640?t=1651931279",
  vmFileName: "",
  noheader: "1",
  showtype: "embed",
  theme: "",
  uid: "",
  subcapclass: "",
  aid: "",
  uip: "240e:388:8212:d600:e005:7d41:7c78:30f3",
  clientype: "",
  websig: "",
  collectdata: "collect",
  asig: "",
  buid: "",
  vmData: "",
  vsig: "",
  dst: "",
  nonce: "eda1152f11f1daf0",
  capSrc: "capFrame",
  spt: "58",
  curenv: "inner",
  fwidth: "",
  slink: "",
  sess: "s0Gy-HhW02Hg8alHgEGBiIdtBysOXUgd-8WvcIumegD9oZia7LANn41JT4n06ernd7TSFM8FEjzKGElXK0DDshRSKmZwgGvCeFztkc2B2vmTYDCQY7NkUZsr5V5nZ-5bae4CL2DJSWOXS2KoRwxPMtFGqX37nzcbd41B7_9VToh0EZ322-ih5v1n3aPmjwc775GJx-Izhb6eJsbn8zJYYDeyFae5TPdTKMb7drxCRk7BiXDVnFjgMMdHCKXoR7IShdnon0QRpyiXxs9ySSBxeKGg66GNH0fUbeJTeXQ6Dg25gOHulK03WNkQT6mWFM_CypugYkCkeLVP8x2aBARTlgB5uhAhqCrczmwhZhRnn4O6-9vMMQzsEnp9OazPatsNCb_7Ga_1b1TX4*",
  cdnPic1: "/hycdn?index=1&image=937121325369518592",
  cdnPic2: "/hycdn?index=2&image=937121325369518592",
  iscdn: "1",
  vmByteCode: "",
  vmAvailable: "",
  TuCao: "https://support.qq.com/products/2136",
  ticket: "",
  randstr: "",
  powCfg: {md5: "c623296e7e613ea4bb50ee4132736c81", prefix: "942e435e81de4c2#"}
}

!function (e) {
  var t = {};

  function n(r) {
    if (t[r])
      return t[r].exports;
    var i = t[r] = {
      i: r,
      l: !1,
      exports: {
        __esModule: undefined
      }
    };
    return e[r].call(i.exports, i, i.exports, n),
      i.l = !0,
      i.exports
  }

  n.m = e,
    n.c = t,
    n.d = function (e, t, r) {
      n.o(e, t) || Object.defineProperty(e, t, {
        enumerable: !0,
        get: r
      })
    }
    ,
    n.r = function (e) {
      "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
        value: "Module"
      }),
        Object.defineProperty(e, "__esModule", {
          value: !0
        })
    }
    ,
    n.t = function (e, t) {
      if (1 & t && (e = n(e)),
      8 & t)
        return e;
      if (4 & t && "object" == typeof e && e && e.__esModule)
        return e;
      var r = Object.create(null);
      if (n.r(r),
        Object.defineProperty(r, "default", {
          enumerable: !0,
          value: e
        }),
      2 & t && "string" != typeof e)
        for (var i in e)
          n.d(r, i, function (t) {
            return e[t]
          }
            .bind(null, i));
      return r
    }
    ,
    n.n = function (e) {
      var t = e && e.__esModule ? function () {
          return e["default"]
        }
        : function () {
          return e
        }
      ;
      return n.d(t, "a", t),
        t
    }
    ,
    n.o = function (e, t) {
      return Object.prototype.hasOwnProperty.call(e, t)
    }
    ,
    n.p = "",
    n(n.s = 62)
  console.log(n(68).tdc, 'dddddddddddddddd')
}([function (e, t, n) {
  "use strict";
  var r = this && this.__createBinding || (Object.create ? function (e, t, n, r) {
        r === undefined && (r = n),
          Object.defineProperty(e, r, {
            enumerable: !0,
            get: function () {
              return t[n]
            }
          })
      }
      : function (e, t, n, r) {
        r === undefined && (r = n),
          e[r] = t[n]
      }
    )
    , i = this && this.__exportStar || function (e, t) {
      for (var n in e)
        "default" === n || Object.prototype.hasOwnProperty.call(t, n) || r(t, e, n)
    }
  ;
  t.__esModule = !0,
    i(n(3), t),
    i(n(8), t),
    i(n(1), t),
    i(n(9), t),
    i(n(10), t)
}
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0,
      t.addUrlParam = t.getQueryParam = t.getQueryMap = t.getQuery = t.getHref = void 0;
    t.getHref = function () {
      try {
        return location.href
      } catch (e) {
        try {
          return document.URL
        } catch (e) {
        }
      }
      return ""
    }
    ;
    t.getQuery = function (e) {
      var t = e ? 1 : 0;
      try {
        return location.search.substr(t)
      } catch (i) {
        try {
          var n = document.URL
            , r = n.indexOf("?");
          if (r >= 0)
            return n.substr(r + t)
        } catch (i) {
        }
      }
      return ""
    }
    ;
    t.getQueryMap = function () {
      for (var e = {}, n = t.getQuery(!0).split("&"), r = 0; r < n.length; r++) {
        var i = /(.*?)=(.*)/.exec(n[r]);
        i && (e[i[1]] = i[2])
      }
      return e
    }
    ;
    t.getQueryParam = function (e) {
      return t.getQueryMap()[e]
    }
    ;
    var r = function (e, t, n) {
      if (-1 != e.indexOf("?")) {
        var r = new RegExp("(\\?|&" + t + ")=[^&]*");
        e = r.test(e) ? e.replace(r, "$1=" + n) : e + "&" + t + "=" + n
      } else
        e = e + "?" + t + "=" + n;
      return e
    };
    t.addUrlParam = function (e, t) {
      var n;
      for (n in t)
        "undefined" != typeof t[n] && (e = r(e, encodeURIComponent(n), encodeURIComponent("" + t[n])));
      return e
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = Object.prototype.hasOwnProperty
      , i = Object.prototype.toString
      , a = Object.defineProperty
      , o = Object.getOwnPropertyDescriptor
      , s = function (e) {
      return "function" == typeof Array.isArray ? Array.isArray(e) : "[object Array]" === i.call(e)
    }
      , c = function (e) {
      if (!e || "[object Object]" !== i.call(e))
        return !1;
      var t, n = r.call(e, "constructor"),
        a = e.constructor && e.constructor.prototype && r.call(e.constructor.prototype, "isPrototypeOf");
      if (e.constructor && !n && !a)
        return !1;
      for (t in e)
        ;
      return void 0 === t || r.call(e, t)
    }
      , u = function (e, t) {
      a && "__proto__" === t.name ? a(e, t.name, {
        enumerable: !0,
        configurable: !0,
        value: t.newValue,
        writable: !0
      }) : e[t.name] = t.newValue
    }
      , l = function (e, t) {
      if ("__proto__" === t) {
        if (!r.call(e, t))
          return;
        if (o)
          return o(e, t).value
      }
      return e[t]
    };
    e.exports = function d() {
      var e, t, n, r, i, a, o = arguments[0], f = 1, p = arguments.length, h = !1;
      for ("boolean" == typeof o && (h = o,
        o = arguments[1] || {},
        f = 2),
           (null == o || "object" != typeof o && "function" != typeof o) && (o = {}); f < p; ++f)
        if (null != (e = arguments[f]))
          for (t in e)
            n = l(o, t),
            o !== (r = l(e, t)) && (h && r && (c(r) || (i = s(r))) ? (i ? (i = !1,
              a = n && s(n) ? n : []) : a = n && c(n) ? n : {},
              u(o, {
                name: t,
                newValue: d(h, a, r)
              })) : void 0 !== r && u(o, {
              name: t,
              newValue: r
            }));
      return o
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = this && this.__importDefault || function (e) {
        return e && e.__esModule ? e : {
          "default": e
        }
      }
    ;
    t.__esModule = !0,
      t.addAriaModel = t.isTouchEventSupported = t.get$EventPosition = t.test$TouchEvent = t.supportsPassive = t.isWindow = t.getWindow = t.getOffset = t.isDarkMode = t.shakeEl = t.addOnceAnimationClass = t.animationEndName = t.removeClass = t.addClass = t.setCss = t.getCSS = t.supportsCSS = t.createGeneralIframe = void 0;
    var i = n(0)
      , a = r(n(4));
    t.createGeneralIframe = function (e) {
      var t = document.createElement("iframe");
      return (null === e || void 0 === e ? void 0 : e.id) && (t.id = e.id),
      (null === e || void 0 === e ? void 0 : e.className) && (t.className = e.className),
        t.setAttribute("frameborder", "0"),
        t.setAttribute("border", "0"),
        t.setAttribute("marginheight", "0"),
        t.setAttribute("marginwidth", "0"),
        t.setAttribute("scrolling", "no"),
        t
    }
    ;
    t.supportsCSS = function (e, t) {
      var n = document.createElement("div");
      return e in n.style && "length" !== e && "parentRule" !== e && (n.style[e] = t,
      n.style[e] === t)
    }
    ;
    t.getCSS = function (e, t) {
      return e.currentStyle ? e.currentStyle[t] : window.getComputedStyle(e, null)[t]
    }
    ;
    t.setCss = function (e, t) {
      if (e && t && i.isObject(t)) {
        for (var n in t)
          try {
            e.style[n] = t[n]
          } catch (r) {
          }
        return t
      }
    }
    ;
    t.addClass = function (e, t) {
      if (e.classList)
        e.classList.add(t);
      else {
        var n = e.className
          , r = n + ("" !== n ? " " : "") + t;
        e.className = r
      }
    }
    ;
    t.removeClass = function (e, t) {
      if (e.classList)
        return e.classList.remove(t);
      var n = " " + e.className + " "
        , r = (n = n.replace(/(\s+)/gi, " ")).replace(" " + t + " ", " ");
      r = r.replace(/(^\s+)|(\s+$)/g, ""),
        e.className = r
    }
      ,
      t.animationEndName = function () {
        var e, t = document.createElement("fake"), n = {
          animation: "animationend",
          mozAnimation: "mozAnimationEnd",
          webkitAnimation: "webkitAnimationEnd"
        };
        for (e in n)
          if (t.style[e] !== undefined)
            return n[e];
        return !1
      }();
    t.addOnceAnimationClass = function (e) {
      var n = e.el
        , r = e.className
        , o = e.callback
        , s = e.duration;
      s || (s = 400),
      i.isArray(n) || (n = [n]);
      for (var c = 0; c < n.length; c++) {
        var u = n[c];
        t.addClass(u, r)
      }
      var l = function () {
        i.isArray(n) || (n = [n]);
        for (var e = 0; e < n.length; e++) {
          var s = n[e];
          t.removeClass(s, r)
        }
        o(),
        t.animationEndName && a["default"].remove(n[0], t.animationEndName, l)
      };
      t.animationEndName ? a["default"].add(n[0], t.animationEndName, l) : setTimeout(l, s)
    }
    ;
    t.shakeEl = function (e, n) {
      t.addOnceAnimationClass({
        el: e,
        className: "shake",
        callback: n
      })
    }
    ;

    function o(e) {
      return s(e) ? e : 9 === e.nodeType && (e.defaultView || e.parentWindow)
    }

    function s(e) {
      return null != e && e == e.window
    }

    function c(e) {
      return /^touch/.test(e.type)
    }

    t.isDarkMode = function () {
      var e;
      return null === (e = window.matchMedia) || void 0 === e ? void 0 : e.call(window, "(prefers-color-scheme: dark)").matches
    }
      ,
      t.getOffset = function (e) {
        var t, n, r = {
          top: 0,
          left: 0
        }, i = null === e || void 0 === e ? void 0 : e.ownerDocument;
        if (i) {
          t = i.documentElement,
          "undefined" != typeof e.getBoundingClientRect && (r = e.getBoundingClientRect());
          var a = 0
            , s = 0;
          return (n = o(i)) && (a = (n.pageYOffset || t.scrollTop) - (t.clientTop || 0),
            s = (n.pageXOffset || t.scrollLeft) - (t.clientLeft || 0)),
            {
              top: r.top + a,
              left: r.left + s
            }
        }
      }
      ,
      t.getWindow = o,
      t.isWindow = s,
      t.supportsPassive = function () {
        var e = !1;
        try {
          var t = Object.defineProperty({}, "passive", {
            get: function () {
              e = !0
            }
          });
          window.addEventListener("testPassive", null, t),
            window.removeEventListener("testPassive", null, t)
        } catch (n) {
        }
        return e
      }(),
      t.test$TouchEvent = c,
      t.get$EventPosition = function (e) {
        if (c(e)) {
          var t;
          e.originalEvent && (t = e.originalEvent);
          var n = ((null === t || void 0 === t ? void 0 : t.touches) || [])[0];
          return n ? {
            x: n.clientX,
            y: n.clientY
          } : null
        }
        return {
          x: e.pageX,
          y: e.pageY
        }
      }
      ,
      t.isTouchEventSupported = function () {
        return "ontouchstart" in document.createElement("div")
      }
      ,
      t.addAriaModel = function (e) {
        try {
          e.setAttribute("role", "dialog"),
            e.setAttribute("aria-modal", "true"),
            e.setAttribute("aria-labelledby", "\u9a8c\u8bc1\u7801")
        } catch (t) {
        }
      }
  }
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0;
    t["default"] = {
      add: function (e, t, n) {
        e && (e.addEventListener ? e.addEventListener(t, n, !1) : e.attachEvent ? e.attachEvent("on" + t, n) : e["on" + t] = n)
      },
      remove: function (e, t, n) {
        e && (e.removeEventListener ? e.removeEventListener(t, n, !1) : e.detachEvent ? e.detachEvent("on" + t, n) : e["on" + t] = null)
      }
    }
  }
  , function (e, t, n) {
    "use strict";

    function r(e, n, r) {
      return "terror_" + t.ErrorCode[e] + "_" + n + "_" + Math.floor((new Date).getTime() / 1e3) + (r ? "_" + r : "")
    }

    function i() {
      return "@" + Math.random().toString(36).substr(2)
    }

    t.__esModule = !0,
      t.getRandStr = t.getErrorRes = t.getErrorTicket = t.ErrorCode = void 0,
      t.ErrorCode = {
        ENTRYJS_LOAD_ERROR: 1001,
        CAPTCHA_SHOW_TIMEOUT: 1002,
        FRAMEJS_LOAD_TIMEOUT: 1003,
        FRAMEJS_LOAD_ERROR: 1004,
        FRAMEJS_RUN_ERROR: 1005,
        GET_CAPTCHA_CONFIG_REQUEST_ERROR: 1006,
        PRE_TEMPLATE_LOAD_TIMEOUT: 1007,
        IFRAME_LOAD_TIMEOUT: 1008,
        LIB_JQ_LOAD_ERROR: 1009,
        CAPTCHA_JS_LOAD_ERROR: 1010,
        CAPTCHA_JS_RUN_ERROR: 1011,
        REFRESH_ERROR: 1012,
        VERIFY_ERROR: 1013
      },
      t.getErrorTicket = r,
      t.getErrorRes = function (e, n, a) {
        return {
          ret: 0,
          randstr: i(),
          ticket: r(e, n || "", a),
          errorCode: t.ErrorCode[e],
          errorMessage: e.toLowerCase()
        }
      }
      ,
      t.getRandStr = i
  }
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0,
      t.getScriptUrl = t.getScript = void 0,
      t.getScript = function r(e, t) {
        var n = 3
          , i = e.src
          , a = e.successCheck
          , o = e.success
          , s = e.error
          , c = e.crossOrigin
          ,
          u = Boolean(e.inHead) ? document.getElementsByTagName("head").item(0) : document.getElementsByTagName("body").item(0)
          , l = !1
          , d = document.createElement("script");

        function f(e) {
          if (!l) {
            var t = !1;
            e && "type" in e && (t = "load" === e.type),
            "readyState" in this && /^(loaded|complete)$/.test(this.readyState) && (t = !0),
            t && (!a || a() ? (h(),
              l = !0,
            null === o || void 0 === o || o()) : p())
          }
        }

        function p() {
          l || (h(),
            l = !0,
            (t = t || 1) >= n ? null === s || void 0 === s || s() : r({
              src: i,
              successCheck: a,
              success: o,
              error: s
            }, t + 1))
        }

        function h() {
          try {
            u && d && u.removeChild(d)
          } catch (s) {
          }
        }

        d.type = "text/javascript",
          d.async = !0,
          d.src = i,
        c && d.setAttribute("crossorigin", c),
          "onload" in d ? d.onload = f : d.onreadystatechange = f,
          d.onerror = p,
        null === u || void 0 === u || u.appendChild(d)
      }
      ,
      t.getScriptUrl = function () {
        try {
          throw new Error("domain")
        } catch (n) {
          var e = null === n || void 0 === n ? void 0 : n.stack;
          if (!e)
            return;
          var t = ("" + e).match(/(https?:\/\/.*\.js)/);
          return {
            url: null === t || void 0 === t ? void 0 : t[1],
            stack: e
          }
        }
      }
  }
  , function (e, t, n) {
    "use strict";
    var r = function () {
      var e = 1
        , t = /subsid=(\d+)/.exec(location.href);
      t && (e = parseInt(t[1], 10) + 1);
      var n = function (t, n) {
        var r = n || e;
        return t = /subsid=\d+/.test(t) ? t.replace(/subsid=\d+/g, "subsid=" + r) : t + "&subsid=" + r,
        n || e++,
          t
      };
      return n.get = function () {
        return e
      }
        ,
        n.bind = function () {
          var t = e++;
          return function (e) {
            return n(e, t)
          }
        }
        ,
        n
    }();
    e.exports = r
  }
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0,
      t.isArray = t.isObject = void 0;
    var r = function (e) {
      return function (t) {
        return Object.prototype.toString.call(t) === "[object " + e + "]"
      }
    };
    t.isObject = r("Object"),
      t.isArray = r("Array")
  }
  , function (e, t, n) {
    "use strict";
    var r = this && this.__importDefault || function (e) {
        return e && e.__esModule ? e : {
          "default": e
        }
      }
    ;
    t.__esModule = !0,
      t.shrinkArraySizeFromRuisun = t.shrinkArraySize = t.extend = void 0;
    var i = r(n(2));
    t.extend = Object.assign || i["default"],
      t.shrinkArraySize = function (e, t, n) {
        var r = e.length;
        if (r <= t)
          return e;
        var i = [];
        (n = n || {}).keepStart && (t -= 1,
          r -= 1,
          i.push(e[0])),
        n.keepLast && (r -= 1,
          t -= 1);
        for (var a = t / r, o = 0, s = 0; s < r; s++)
          (o += a) >= 1 && (i.push(e[s]),
            o -= 1);
        return n.keepLast && i.push(e[e.length - 1]),
          i
      }
      ,
      t.shrinkArraySizeFromRuisun = function (e, t, n) {
        var r = e.length;
        if (r <= t)
          return e;
        (n = n || {}).keepStart && (r -= 1),
        n.keepLast && (r -= 1,
          t -= 1);
        for (var i = Math.floor(r / (t - 1)), a = 0, o = []; o.length < t;)
          o.push(e[a]),
            a += i;
        return n.keepLast && o.push(e[e.length - 1]),
          o
      }
  }
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0,
      t.isWebWorkerSupport = void 0,
      t.isWebWorkerSupport = function () {
        var e = self || window;
        try {
          try {
            var t = void 0;
            try {
              t = new e.Blob([""])
            } catch (a) {
              (t = new (e.BlobBuilder || e.WebKitBlobBuilder || e.MozBlobBuilder || e.MSBlobBuilder)).append(""),
                t = t.getBlob()
            }
            var n = e.URL || e.webkitURL
              , r = n.createObjectURL(t)
              , i = new e.Worker(r);
            return n.revokeObjectURL(r),
              i
          } catch (a) {
            return new e.Worker("data:application/javascript,".concat(encodeURIComponent("")))
          }
        } catch (a) {
          return null
        }
      }
  }
  , , , , , , , , , , , , function (e, t, n) {
    "use strict";

    function r() {
      return Math.floor(1e8 * Math.random())
    }

    var i = function (e) {
      e = e ? 1 : 0;
      try {
        return c(location.search.substr(e))
      } catch (r) {
        try {
          var t = document.URL
            , n = t.indexOf("?");
          if (n >= 0)
            return c(t.substr(n + e))
        } catch (r) {
        }
      }
      return ""
    }
      , a = {};
    !function () {
      for (var e = i(!0).split("&"), t = 0; t < e.length; t++) {
        var n = /(.*?)=(.*)/.exec(e[t]);
        n && (a[n[1]] = n[2])
      }
    }();
    var o = a.sess;

    function s(e) {
      a.sess = e
    }

    function c(e) {
      try {
        return a ? e.replace(o, a.sess) : e
      } catch (t) {
        return e
      }
    }

    window.captchaConfig && window.captchaConfig.sess && s(window.captchaConfig.sess);
    e.exports = {
      href: function () {
        try {
          return location.href
        } catch (e) {
          try {
            return document.URL
          } catch (e) {
          }
        }
        return ""
      },
      getQuery: function (e) {
        var t = i();
        return t = t ? t.replace(/&rand=[^&]+/, "") + "&rand=" + r() : "?rand=" + r(),
          e = e ? 1 : 0,
          t.substr(e)
      },
      queryParam: function (e) {
        return a[e]
      },
      queryMap: function () {
        return $.extend({}, a)
      },
      parse2rgb: function (e) {
        if (!e || "string" != typeof e)
          return null;
        e = e.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i, function (e, t, n, r) {
          return t + t + n + n + r + r
        });
        var t = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(e);
        return t ? {
          r: parseInt(t[1], 16),
          g: parseInt(t[2], 16),
          b: parseInt(t[3], 16),
          s: "#" + t[1] + t[2] + t[3]
        } : null
      },
      arrIndexOf: function (e, t) {
        if ("function" == typeof e.indexOf)
          return e.indexOf(t);
        for (var n = 0; n < e.length; n++)
          if (e[n] === t)
            return n;
        return -1
      },
      updateSession: s,
      isLowIE: function () {
        var e = navigator.userAgent.toLowerCase()
          , t = e.indexOf("msie") > -1
          , n = void 0
          , r = void 0;
        if (t) {
          if (n = e.match(/msie ([\d.]+)/)[1],
            r = t && document.documentMode,
          n && n <= 8)
            return !0;
          if (r && r < 9)
            return !0
        }
        return !1
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0,
      t["default"] = {
        loadState: {
          ready: 0,
          fail: 1,
          mixing: 2
        },
        messageType: {
          hybridVerify: 8,
          loadReady: 10,
          preloadReady: 30,
          checkPreLoadReady: 31,
          sendPreloadData: 32,
          goAged: 36,
          goNormalVerify: 37,
          windowChanged: 38,
          readyConfirm: 39
        },
        preloadMsgType: {
          capClose: 33,
          verifySuccess: 34,
          sessionTimeout: 35
        },
        templateKeys: ["drag", "dy"],
        retCode: {
          success: 0,
          errorWithTicket: 0,
          close: 2
        }
      }
  }
  , , function (e, t, n) {
    "use strict";
    t.__esModule = !0;
    var r = "[CODE_VERIFY]"
      , i = "postMessage" in window
      , a = function () {
      function e(e, t, n) {
        var r = "";
        if (arguments.length < 2 ? r = "[Msger] error 1" : "object" != typeof e ? r = "[Msger] error 2" : "string" != typeof t && (r = "[Msger] error 3"),
          r)
          throw new Error(r);
        this.target = e,
          this.name = t,
          this.domain = n || "*"
      }

      return e.prototype.send = function (e) {
        if (i)
          this.target.postMessage(e, this.domain);
        else {
          var t = window.navigator[r + this.name];
          if ("function" != typeof t)
            throw new Error("target callback function is not defined");
          t(e, window)
        }
      }
        ,
        e
    }()
      , o = function () {
      function e(e, t, n) {
        this.targets = {},
          this.name = e,
          this.listenFunc = [],
          this.domain = n || "",
          r = t || r,
          this.listenCb = this.initListen()
      }

      return e.prototype.addTarget = function (e, t, n) {
        var r = new a(e, t, n);
        this.targets[t] = r
      }
        ,
        e.prototype.initListen = function () {
          var e = this
            , t = function (t) {
            if (!e.domain || !t.origin || -1 !== t.origin.indexOf(e.domain)) {
              "object" == typeof t && t.data && (t = t.data);
              for (var n = 0; n < e.listenFunc.length; n++)
                e.listenFunc[n](t)
            }
          };
          return i ? "addEventListener" in document ? window.addEventListener("message", t, !1) : "attachEvent" in document && window.attachEvent("onmessage", t) : window.navigator[r + this.name] = t,
            t
        }
        ,
        e.prototype.unlisten = function () {
          this.listenCb && (i ? "addEventListener" in document ? window.removeEventListener("message", this.listenCb) : "attachEvent" in document && window.detachEvent("onmessage", this.listenCb) : window.navigator[r + this.name] = null)
        }
        ,
        e.prototype.listen = function (e) {
          this.listenFunc.push(e)
        }
        ,
        e.prototype.clear = function () {
          this.listenFunc = []
        }
        ,
        e.prototype.send = function (e) {
          var t, n = this.targets;
          for (t in n)
            n.hasOwnProperty(t) && n[t].send(e)
        }
        ,
        e
    }();
    window.TCapMsg = o,
      t["default"] = o
  }
  , , , , , , , function (e, t, n) {
    "use strict";

    function r(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++)
          n[t] = e[t];
        return n
      }
      return Array.from(e)
    }

    var i, a, o = n(33), s = n(22), c = n(7), u = window.captchaConfig, l = (i = document.referrer,
        a = s.href(),
        i = i.length > 512 ? i.substr(0, 512) : i,
        a = a.length > 1024 ? a.substr(0, 1024) : a,
        ["appid=" + u.aid, "uid=" + u.uid, "sid=" + s.queryParam("sid"), "referer=" + encodeURIComponent(i), "href=" + encodeURIComponent(a)].join("&")),
      d = void 0, f = [];

    function p(e, t, n, r) {
      try {
        if (void 0 === d)
          return void f.push([e, t, n, r]);
        if (d)
          return;
        t = (t = t && t.length > 1024 ? t.substr(0, 1024) : t) || "";
        var i = ["type=" + e, "errType=" + (n = n || u.subcapclass), "tokenid=" + o.getToken(), "timing=" + (r || ""), "reason=" + encodeURIComponent(t)]
          , a = "https://sv.aq.qq.com/cn2/manage/mbtoken/cap_monitor?" + l + "&" + i.join("&");
        (new Image).src = c(a)
      } catch (s) {
      }
    }

    e.exports = {
      type: {
        ERROR_TYPE_TDC_DOWNLOAD_FAIL: 20,
        ERROR_TYPE_TDC_RUN_FAIL: 21,
        ERROR_TYPE_TDC_DOWNLOAD_RETRY_SUCCESS: 22,
        ERROR_TYPE_TDC_RUN_RETRY_SUCCESS: 23,
        ERROR_TYPE_TOUCH_CANCEL: 14,
        ERROR_TYPE_TWICE_IMAGE_ONERROR: 13,
        ERROR_TYPE_CGI_IMAGE_ONERROR: 12,
        ERROR_TYPE_IMAGE_ONERROR: 11,
        ERROR_TYPE_AJAX_GETSIG: 9,
        ERROR_TYPE_AJAX_VERIFY: 8,
        ERROR_TYPE_IMAGE_BEYONDSIZE: 7,
        ERROR_TYPE_MB_FP_REGISTER_TIMEOUT: 6,
        ERROR_TYPE_MB_FPJS_DOWNLOAD_FAIL: 5,
        ERROR_TYPE_PC_FP_REGISTER_TIMEOUT: 4,
        ERROR_TYPE_PC_FPJS_DOWNLOAD_FAIL: 3,
        ERROR_TYPE_BADJS_DOWNLOAD_FAIL: 2,
        ERROR_TYPE_BADJS_REPORT: 1
      },
      send: p,
      setGlobalStatus: function (e) {
        if (!(d = e))
          for (var t = 0; t < f.length; t++) {
            var n = f[t];
            p.apply(undefined, r(n))
          }
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(51)
      , i = n(22).arrIndexOf
      , a = n(64)
      , o = {}
      , s = !1;

    function c(e) {
      (o = window.TDC || {}).initReport || (setTimeout(function () {
        !function (e) {
          if (!e)
            return;
          var t = window.scriptSuccess.tdc
            , n = "number" == typeof t && t > 1;
          1 !== t || d() || (g(e),
            window.scriptRunFailure = {
              tdc: 1
            });
          n && (d() || g(e),
            h(e),
            p(e, t));
          f() && h(e)
        }(e)
      }, 1200),
        o.initReport = !0)
    }

    function u(e) {
      o.setData && o.setData(e)
    }

    function l() {
      return "function" == typeof o.getInfo && o.getInfo() || {}
    }

    function d() {
      return "undefined" != typeof window.TDC && "function" == typeof o.getData
    }

    function f() {
      return i(window.scriptErrors, "tdc") > -1
    }

    function p(e, t) {
      e && e.send(e.type.ERROR_TYPE_TDC_DOWNLOAD_RETRY_SUCCESS, t)
    }

    function h(e) {
      e && e.send(e.type.ERROR_TYPE_TDC_DOWNLOAD_FAIL)
    }

    function g(e) {
      e && e.send(e.type.ERROR_TYPE_TDC_RUN_FAIL)
    }

    e.exports = {
      link: c,
      setData: u,
      getData: function () {
        u({
          ft: r()
        });
        var e = window.scriptErrors || []
          , t = i(e, "tdc") > -1;
        return "function" == typeof o.getData ? o.getData(!0) || "---" : t ? "------" : "---"
      },
      clearData: function () {
        o.clearTc && o.clearTc()
      },
      getInfo: l,
      getToken: function () {
        return (l() || {}).tokenid || ""
      },
      getEks: function () {
        return (l() || {}).info || ""
      },
      getTlg: function () {
        return "undefined" == typeof window.TDC ? 0 : 1
      },
      checkTdcSuccess: d,
      retryLoad: function (e) {
        try {
          if (window.TDC || s || !e)
            return;
          var t = window.captchaConfig.tdcHtdocsPath + "/" + window.captchaConfig.dcFileName;
          s = !0,
            a(t, function (t) {
              s = !1,
              t || setTimeout(function () {
                c(),
                f() && (function () {
                  for (var e = void 0, t = 0; t < window.scriptErrors.length; t++)
                    if ("tdc" === window.scriptErrors[t]) {
                      e = t;
                      break
                    }
                  "number" == typeof e && window.scriptErrors.splice(e, 1)
                }(),
                  p(e, 4)),
                  d() ? window.scriptRunFailure && 1 === window.scriptRunFailure.tdc && function (e) {
                    e && e.send(e.type.ERROR_TYPE_TDC_RUN_RETRY_SUCCESS)
                  }(e) : window.scriptRunFailure = {
                    tdc: 1
                  }
              }, 500)
            })
        } catch (n) {
        }
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(0).isMobileUa
      , i = n(35)
      , a = navigator.userAgent
      , o = /nettype\/(4g|wifi)/i.test(a)
      , s = /iphone|ipad|ipod/gi.test(a) ? "ios" : "android"
      , c = "https:" === location.protocol ? "https" : "http"
      , u = window.captchaConfig;
    r || (s = "pc"),
      e.exports = {
        ua: a,
        loadState: {
          ready: 0,
          fail: 1,
          mixing: 2
        },
        cgiImg: "/cap_union_new_getcapbysig",
        isFastNet: o,
        loadImgTimeout: o ? 8e3 : 15e3,
        platform: s,
        protocol: c,
        config: u,
        popup: "popup" === u.showtype,
        corsAttr: {
          attrs: {
            crossorigin: "anonymous"
          }
        },
        companyInfo: "1" === u.slink && ("zh-cn" === i.currentLanguage || "zh" === i.currentLanguage) && "pc" === s,
        needFp: "tokenidiframe_d.js" !== u.fpFileName,
        needVm: "dc_vx.js" !== u.vmFileName
      }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(0).getQueryParam
      ,
      i = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20", "puzzle1", "puzzle2", "puzzle3", "puzzle4", "puzzle5", "puzzle6", "puzzle7", "puzzle8", "puzzle9", "puzzle10", "c21", "c22", "c23", "aged"]
      , a = {
        "zh-cn": ["\u70b9\u51fb\u5f00\u59cb\u9a8c\u8bc1", "\u5b89\u5168\u9a8c\u8bc1", "\u9a8c\u8bc1\u6210\u529f\uff0c\u7cbe\u51c6\u65e0\u654c\u4e86\uff01", "\u95ee\u9898\u53cd\u9988", "\u6362\u4e00\u5f20\u56fe\u7247", "\u9a8c\u8bc1", "\u8bf7\u70b9\u51fb\u91cd\u65b0\u52a0\u8f7d", "\u7f51\u7edc\u8d85\u65f6\uff0c\u8bf7\u91cd\u8bd5", "\u9a8c\u8bc1\u9519\u8bef\uff0c\u8bf7\u91cd\u65b0\u9a8c\u8bc1", "\u9a8c\u8bc1\u7801", "\u8fd4\u56de", "\u6b63\u5728\u9a8c\u8bc1...", "\u5f53\u524d\u7f51\u7edc\u8f83\u5dee\uff0c\u8bf7\u70b9\u51fb\u5237\u65b0\u6309\u94ae\u91cd\u8bd5", "\u56fe\u7247\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u70b9\u51fb\u5237\u65b0", "\u6b63\u5728\u9a8c\u8bc1", ["\u53ea\u7528\u4e86+s\uff0c\u7b80\u76f4\u6bd4\u95ea\u7535\u8fd8\u5feb", "\u53ea\u7528\u4e86+s\uff0c\u8fd9\u901f\u5ea6\u7b80\u76f4\u5b8c\u7f8e", "\u9a8c\u8bc1\u6210\u529f\uff0c\u7cbe\u51c6\u65e0\u654c\u4e86\uff01"], "\u5237\u65b0", "\u5173\u95ed", "\u53cd\u9988", "\u5237\u65b0\u8fc7\u591a\uff0c\u8bf7\u70b9\u51fb\u91cd\u8bd5", "\u8bf7\u5411\u53f3\u62d6\u52a8\u6ed1\u5757\u5b8c\u6210\u62fc\u56fe", "\u9a8c\u8bc1\u9519\u8bef\uff0c\u8bf7\u91cd\u8bd5", "\u62d6\u52a8\u6ed1\u5757\u5230\u6700\u53f3\u8fb9", "\u8bf7\u518d\u6b21\u62d6\u52a8\u6ed1\u5757\u5230\u6700\u53f3\u8fb9", "\u8bf7\u62d6\u52a8\u6ed1\u5757\u5230\u6700\u53f3\u8fb9", "\u62d6\u52a8\u4e0b\u65b9\u6ed1\u5757\u5b8c\u6210\u62fc\u56fe", "\u8bf7\u63a7\u5236\u62fc\u56fe\u5757\u5bf9\u9f50\u7f3a\u53e3", "\u8fd9\u9898\u6709\u70b9\u96be\u5462\uff0c\u5df2\u4e3a\u60a8\u66f4\u6362\u9898\u76ee", ["\u5f53\u524d\u4e0a\u7f51\u73af\u5883\u5f02\u5e38\uff0c\u8bf7\u66f4\u6362\u7f51\u7edc\u73af\u5883\u6216\u7a0d\u540e\u518d\u8bd5"], "\u56fe\u7247\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u70b9\u51fb\u5237\u65b0", "\u9a8c\u8bc1\u6210\u529f", "\u5237\u65b0\u8fc7\u591a", "\u7f51\u7edc\u604d\u60da\u4e86\u4e00\u4e0b(+)\uff0c\u518d\u8bd5\u4e00\u6b21\u5427", "\u6211\u4e0d\u4f1a\uff0c\u6362\u4e00\u79cd"],
        "zh-hk": ["\u9ede\u64ca\u958b\u59cb\u9a57\u8b49", "\u5b89\u5168\u9a57\u8b49", "\u9a57\u8b49\u6210\u529f\uff0c\u767e\u5206\u767e\u7cbe\u6e96\uff01", "\u554f\u984c\u610f\u898b\u53cd\u6620", "\u63db\u4e00\u5f35\u5716\u7247", "\u9a57\u8b49", "\u8acb\u9ede\u64ca\u91cd\u65b0\u52a0\u8f09", "\u7db2\u7d61\u903e\u6642\uff0c\u8acb\u91cd\u8a66", "\u9a57\u8b49\u932f\u8aa4\uff0c\u8acb\u91cd\u65b0\u9a57\u8b49", "\u9a57\u8b49\u78bc", "\u8fd4\u56de", "\u6b63\u5728\u9a57\u8b49\u22ef", "\u76ee\u524d\u7db2\u7d61\u8f03\u5dee\uff0c\u8acb\u9ede\u64ca\u5237\u65b0\u6309\u9215\u91cd\u8a66", "\u7121\u6cd5\u52a0\u8f09\u5716\u7247\uff0c\u8acb\u9ede\u64ca\u5237\u65b0", "\u6b63\u5728\u9a57\u8b49", ["\u53ea\u7528\u4e86+s\uff0c\u7c21\u76f4\u5feb\u5982\u9583\u96fb", "\u53ea\u7528\u4e86+s\uff0c\u901f\u5ea6\u7c21\u76f4\u5b8c\u7f8e", "\u9a57\u8b49\u6210\u529f\uff0c\u767e\u5206\u767e\u7cbe\u6e96\uff01"], "\u5237\u65b0", "\u95dc\u9589", "\u610f\u898b\u53cd\u6620", "\u5237\u65b0\u6b21\u6578\u904e\u591a\uff0c\u8acb\u9ede\u64ca\u91cd\u8a66", "\u8acb\u5411\u53f3\u62d6\u52d5\u6ed1\u584a\u5b8c\u6210\u62fc\u5716", "\u9a57\u8b49\u932f\u8aa4\uff0c\u8acb\u91cd\u8a66", "\u62d6\u52d5\u6ed1\u584a\u5230\u6700\u53f3\u908a", "\u8acb\u518d\u6b21\u62d6\u52d5\u6ed1\u584a\u5230\u6700\u53f3\u908a", "\u8acb\u62d6\u52d5\u6ed1\u584a\u5230\u6700\u53f3\u908a", "\u62d6\u52d5\u4e0b\u65b9\u6ed1\u584a\u5b8c\u6210\u62fc\u5716", "\u8acb\u63a7\u5236\u62fc\u5716\u584a\u5c0d\u9f4a\u7f3a\u53e3", "\u9019\u984c\u6709\u9ede\u96e3\uff0c\u5df2\u70ba\u4f60\u66f4\u63db\u984c\u76ee", ["\u62fc\u5716\u584a\u534a\u8def\u6389\u4e0b\u4e86\uff0c\u518d\u8a66\u4e00\u6b21\u5427", "\u518d\u8a66\u4e00\u6b21\uff0c\u8981\u62fc\u5f97\u6bd4\u4e0a\u6b21\u66f4\u6e96", "\u7db2\u7d61\u505c\u9813\u4e86\u4e00\u4e0b\uff0c\u518d\u8a66\u4e00\u6b21\u5427"], "\u7121\u6cd5\u52a0\u8f09\u5716\u7247\uff0c\u8acb\u9ede\u64ca\u5237\u65b0", "\u9a57\u8b49\u6210\u529f", "\u5237\u65b0\u6b21\u6578\u904e\u591a", "\u7db2\u7d61\u505c\u9813\u4e86\u4e00\u4e0b(+)\uff0c\u518d\u8a66\u4e00\u6b21\u5427", "\u7121\u969c\u7919\u65b9\u5f0f"],
        "zh-tw": ["\u9ede\u64ca\u958b\u59cb\u9a57\u8b49", "\u5b89\u5168\u9a57\u8b49", "\u9a57\u8b49\u6210\u529f\uff0c\u7cbe\u6e96\u7121\u6575\u4e86\uff01", "\u554f\u984c\u53cd\u6620\u610f\u898b", "\u63db\u4e00\u5f35\u5716\u7247", "\u9a57\u8b49", "\u8acb\u9ede\u64ca\u91cd\u65b0\u8f09\u5165", "\u7db2\u8def\u903e\u6642\uff0c\u8acb\u91cd\u8a66", "\u9a57\u8b49\u932f\u8aa4\uff0c\u8acb\u91cd\u65b0\u9a57\u8b49", "\u9a57\u8b49\u78bc", "\u8fd4\u56de", "\u6b63\u5728\u9a57\u8b49...", "\u76ee\u524d\u7db2\u8def\u4e0d\u7a69\uff0c\u8acb\u9ede\u64ca\u91cd\u65b0\u6574\u7406\u6309\u9215\u91cd\u8a66", "\u5716\u7247\u8f09\u5165\u5931\u6557\uff0c\u8acb\u9ede\u64ca\u91cd\u65b0\u6574\u7406", "\u6b63\u5728\u9a57\u8b49", ["\u53ea\u7528\u4e86+s\uff0c\u7c21\u76f4\u6bd4\u9583\u96fb\u9084\u5feb", "\u53ea\u7528\u4e86+s\uff0c\u9019\u901f\u5ea6\u7c21\u76f4\u5b8c\u7f8e", "\u9a57\u8b49\u6210\u529f\uff0c\u7cbe\u6e96\u7121\u6575\u4e86\uff01"], "\u91cd\u65b0\u6574\u7406", "\u95dc\u9589", "\u53cd\u6620\u610f\u898b", "\u91cd\u65b0\u6574\u7406\u6b21\u6578\u904e\u591a\uff0c\u8acb\u9ede\u64ca\u91cd\u8a66", "\u8acb\u5411\u53f3\u62d6\u66f3\u6ed1\u584a\u5b8c\u6210\u62fc\u5716", "\u9a57\u8b49\u932f\u8aa4\uff0c\u8acb\u91cd\u8a66", "\u5c07\u6ed1\u584a\u62d6\u66f3\u5230\u6700\u53f3\u908a", "\u8acb\u518d\u6b21\u5c07\u6ed1\u584a\u62d6\u66f3\u5230\u6700\u53f3\u908a", "\u8acb\u5c07\u6ed1\u584a\u62d6\u66f3\u5230\u6700\u53f3\u908a", "\u62d6\u66f3\u4e0b\u65b9\u6ed1\u584a\u5b8c\u6210\u62fc\u5716", "\u8acb\u63a7\u5236\u62fc\u5716\u7247\u5c0d\u9f4a\u7f3a\u53e3", "\u9019\u984c\u6709\u9ede\u96e3\uff0c\u5df2\u70ba\u4f60\u66f4\u63db\u984c\u76ee", ["\u62fc\u5716\u7247\u907a\u5931\u4e86\uff0c\u8acb\u518d\u8a66\u4e00\u6b21", "\u518d\u8a66\u4e00\u6b21\uff0c\u62fc\u5f97\u6bd4\u4e0a\u6b21\u66f4\u6e96\u4e9b", "\u7db2\u8def\u4e2d\u65b7\u4e86\u4e00\u4e0b\uff0c\u518d\u8a66\u4e00\u6b21\u5427"], "\u5716\u7247\u8f09\u5165\u5931\u6557\uff0c\u8acb\u9ede\u64ca\u91cd\u65b0\u6574\u7406", "\u9a57\u8b49\u6210\u529f", "\u5617\u8a66\u6b21\u6578\u904e\u591a", "\u7db2\u8def\u4e2d\u65b7\u4e86\u4e00\u4e0b(+)\uff0c\u518d\u8a66\u4e00\u6b21\u5427", "\u7121\u969c\u7919\u65b9\u5f0f"],
        en: ["Tap to verify", "Security Verification", "Verification is successful", "Feedback", "Refresh", "Verify", "Tap to reload", "Timeout. Try again.", "Verification error. Try again.", "Verification Code", "Back", "Verifying...", "Unstable network. Tap Refresh to retry.", "Loading failed. Tap the image to refresh.", "Verifying", ["+s spent. You beat the Flash!", "+s spent. Perfect!", "Verification is successful"], "Refresh", "Close", "Feedback", "Refreshing too often. Tap to retry.", "Drag the slider to the right to fix the puzzle.", "Verification error. Try again.", "Drag the slider to the rightmost slot", "Drag it once more", "Drag the slider to the rightmost slot", "Drag the slider below to fit the puzzle piece", "Put the piece right into the slot", "That one seems a bit tough. Try this one.", ["The piece got lost. Try again.", "Try again and make it fit in more precisely", "Unstable network. Try again."], "Loading failed. Tap the image to refresh.", "Verification is successful", "Refreshing too often", "Unstable network(+). Try again.", "Accessibility"],
        "en-o": ["Click here to verify", "Security Verification", "Verification success", "Feedback", "Refresh", "Verify", "Click to refresh", "Network timed out. Please try again", "Verification failed. Please try again", "Captcha", "Back", "Verify...", "Network is poor. Please try again later", "Fail to load image, click to refresh", "Verifying", ["Wow, only +s, blazing speed!", "Wow, only +s, near perfection!", "Success! Great precision."], "Refresh", "Close", "Help", "Click to reopen captcha", "Slide to complete the jigsaw", "Verification failed. Please try again", "Drag this arrow to the far right", "Drag this arrow to the far right again", "Please drag this arrow to the far right", "Drag to complete the jigsaw", "Please piece together the jigsaw", "Try agian with refreshed image", ["Something went wrong, please try again", "Bad network connection, please try again", "Our mistake, sorry to ask you try again"], "Fail to load image, click to refresh", "Verification is successful", "Refreshing too often", "Our mistake(+), sorry to ask you try again", "Accessibility"],
        ar: ["\u0627\u0646\u0642\u0631 \u0644\u0644\u062a\u062d\u0642\u0642", "\u0627\u0644\u062a\u062d\u0642\u0642 \u0645\u0646 \u0627\u0644\u062d\u0645\u0627\u064a\u0629", "\u0646\u062c\u0627\u062d \u0627\u0644\u062a\u062d\u0642\u0642", "\u062a\u0639\u0642\u064a\u0628", "\u062a\u062d\u062f\u064a\u062b", "\u062a\u062d\u0642\u0642", "\u0627\u0646\u0642\u0631 \u0644\u0625\u0639\u0627\u062f\u0629 \u0627\u062a\u062d\u0645\u064a\u0644", "\u0627\u0646\u062a\u0647\u062a \u0627\u0644\u0645\u0647\u0644\u0629. \u062d\u0627\u0648\u0644 \u0645\u062c\u062f\u062f\u0627", "\u062e\u0644\u0644 \u0641\u064a \u0627\u0644\u062a\u062d\u0642\u0642. \u0623\u0639\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629", "\u0643\u0648\u062f \u0627\u0644\u062a\u062d\u0642\u0642", "\u0639\u0648\u062f\u0629", "\u062c\u0627\u0631\u064a \u0627\u0644\u062a\u062d\u0642\u0642...", "\u0634\u0628\u0643\u0629 \u0645\u0636\u0637\u0631\u0628\u0629. \u0627\u0646\u0642\u0631 \u0639\u0644\u0649 \u062a\u062d\u062f\u064a\u062b \u0644\u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629", "\u0641\u0634\u0644 \u0627\u0644\u062a\u062d\u0645\u064a\u0644. \u0627\u0646\u0642\u0631 \u0639\u0644\u0649 \u0627\u0644\u0635\u0648\u0631\u0629 \u0644\u0644\u062a\u062d\u062f\u064a\u062b", "\u062c\u0627\u0631\u064a \u0627\u0644\u062a\u062d\u0642\u0642", ["+\u062b\u0627 \u0645\u0636\u062a. \u0647\u0632\u0645\u062a \u0627\u0644\u0641\u0644\u0627\u0634!", "+\u062b\u0627 \u0645\u0636\u062a. \u0631\u0627\u0626\u0639!", "\u0646\u062c\u0627\u062d \u0627\u0644\u062a\u062d\u0642\u0642"], "\u062a\u062d\u062f\u064a\u062b", "\u0625\u063a\u0644\u0627\u0642", "\u062a\u0639\u0642\u064a\u0628", "\u0643\u062b\u0631\u0629 \u0627\u0644\u062a\u062d\u062f\u064a\u062b. \u0627\u0646\u0642\u0631 \u0644\u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629", "\u0627\u0633\u062d\u0628 \u0627\u0644\u0645\u0646\u0632\u0644\u0642\u0629 \u0644\u0644\u064a\u0645\u064a\u0646 \u0644\u0625\u062a\u0645\u0627\u0645 \u0627\u0644\u0644\u063a\u0632", "\u062e\u0644\u0644 \u0641\u064a \u0627\u0644\u062a\u062d\u0642\u0642. \u0623\u0639\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629", "\u0627\u0633\u062d\u0628 \u0627\u0644\u0645\u0646\u0632\u0644\u0642\u0629 \u0625\u0644\u0649 \u0627\u0644\u0641\u062a\u062d\u0629 \u0641\u064a \u0623\u0642\u0635\u0649 \u0627\u0644\u064a\u0645\u064a\u0646", "\u0627\u0633\u062d\u0628\u0647\u0627 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649", "\u0627\u0633\u062d\u0628 \u0627\u0644\u0645\u0646\u0632\u0644\u0642\u0629 \u0625\u0644\u0649 \u0627\u0644\u0641\u062a\u062d\u0629 \u0641\u064a \u0623\u0642\u0635\u0649 \u0627\u0644\u064a\u0645\u064a\u0646", "\u0627\u0633\u062d\u0628 \u0627\u0644\u0645\u0646\u0632\u0644\u0642\u0629 \u0623\u0633\u0641\u0644\u0647 \u0644\u0625\u062a\u0645\u0627\u0645 \u0627\u0644\u0644\u063a\u0632", "\u0636\u0639 \u0627\u0644\u0642\u0637\u0639\u0629 \u0645\u0628\u0627\u0634\u0631\u0629 \u0641\u064a \u0627\u0644\u0641\u062a\u062d\u0629", "\u0647\u0630\u0647 \u062a\u0628\u062f\u0648 \u0635\u0639\u0628\u0629 \u0642\u0644\u064a\u0644\u0627 \u062c\u0631\u0651\u0628 \u0647\u0630\u0647", ["\u0644\u0642\u062f \u0636\u0627\u0639\u062a \u0647\u0630\u0647 \u0627\u0644\u0642\u0637\u0639\u0629. \u062d\u0627\u0648\u0644 \u0645\u062c\u062f\u062f\u0627", "\u0623\u0639\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0648 \u0627\u062c\u0639\u0644\u0647\u0627 \u062a\u062a\u0646\u0627\u0633\u0628 \u0628\u0634\u0643\u0644 \u0623\u062f\u0642", "\u0634\u0628\u0643\u0629 \u0645\u0636\u0637\u0631\u0628\u0629. \u0623\u0639\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629"], "\u0641\u0634\u0644 \u0627\u0644\u062a\u062d\u0645\u064a\u0644. \u0627\u0646\u0642\u0631 \u0639\u0644\u0649 \u0627\u0644\u0635\u0648\u0631\u0629 \u0644\u0644\u062a\u062d\u062f\u064a\u062b", "\u0646\u062c\u0627\u062d \u0627\u0644\u062a\u062d\u0642\u0642", "\u0643\u062b\u0631\u0629 \u0627\u0644\u062a\u062d\u062f\u064a\u062b", "\u0634\u0628\u0643\u0629 \u0645\u0636\u0637\u0631\u0628\u0629.(+) \u0623\u0639\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629"],
        my: ["\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u101b\u1014\u1039\u108f\u103d\u102d\u1015\u1039\u1015\u102b", "\u101c\u1036\u102f\u107f\u1001\u1036\u1033\u1031\u101b\u1038\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u103b\u1001\u1004\u1039\u1038", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u1019\u1088 \u1031\u1021\u102c\u1004\u1039\u103b\u1019\u1004\u1039\u1015\u102b\u101e\u100a\u1039", "\u1010\u102f\u1036\u1094\u103b\u1015\u1014\u1039\u1001\u103a\u1000\u1039", "\u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u101b\u1014\u1039", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u101b\u1014\u1039", "\u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u101b\u1014\u1039\u108f\u103d\u102d\u1015\u1039\u1015\u102b", "\u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b", "\u1021\u1019\u103d\u102c\u1038\u1021\u101a\u103c\u1004\u1039\u1038\u101b\u103d\u102d\u101e\u103b\u1016\u1004\u1039\u1037 \u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u101b\u1014\u1039 Code", "\u1031\u1014\u102c\u1000\u1039\u101e\u102d\u102f\u1094", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u1031\u1014\u101e\u100a\u1039...", "\u1000\u103c\u1014\u1039\u101b\u1000\u1039\u1019\u1010\u100a\u1039\u107f\u1004\u102d\u1019\u1039\u1015\u102b\u104a \u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u101b\u1014\u1039\u1000\u102d\u102f \u108f\u103d\u102d\u1015\u1039\u1015\u102b", "\u1031\u1012\u1010\u102c\u101b\u101a\u1030\u1019\u1088 \u1019\u1031\u1021\u102c\u1004\u1039\u103b\u1019\u1004\u1039\u1015\u102b\u104b \u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u101b\u1014\u1039\u1015\u1036\u102f\u1000\u102d\u102f\u108f\u103d\u102d\u1015\u1039\u1015\u102b", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u1031\u1014\u101e\u100a\u1039", ["+s \u101e\u1036\u102f\u1038\u1005\u103c\u1032\u107f\u1015\u102e\u1038\u104b \u101e\u1004\u1039 Flash \u1000\u102d\u102f \u1021\u108f\u102d\u102f\u1004\u1039\u101a\u1030\u101c\u102d\u102f\u1000\u1039\u1015\u102b\u107f\u1015\u102e!", "+s \u101e\u1036\u102f\u1038\u1005\u103c\u1032\u107f\u1015\u102e\u1038\u104b \u107f\u1015\u102e\u1038\u103b\u1015\u100a\u1039\u1037\u1005\u1036\u102f\u1015\u102b\u1010\u101a\u1039!", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u1019\u1088 \u1031\u1021\u102c\u1004\u1039\u103b\u1019\u1004\u1039\u1015\u102b\u101e\u100a\u1039"], "\u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u101b\u1014\u1039", "\u1015\u102d\u1010\u1039\u101b\u1014\u1039", "\u1010\u102f\u1036\u1094\u103b\u1015\u1014\u1039\u1001\u103a\u1000\u1039", "\u1019\u107e\u1000\u102c\u1001\u1014\u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u1031\u1014\u101b\u101e\u100a\u1039\u104b \u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u101b\u1014\u1039\u108f\u103d\u102d\u1015\u1039\u1015\u102b", "\u1015\u1031\u101f\u1020\u102d\u103b\u1015\u100a\u1039\u1037\u1005\u1036\u102f\u1031\u1005\u101b\u1014\u1039 \u1005\u101c\u102d\u102f\u1000\u1039\u1012\u102b\u1000\u102d\u102f \u100a\u102c\u1018\u1000\u1039\u101e\u102d\u102f\u1094\u1006\u103c\u1032\u1015\u102b", "\u1021\u1019\u103d\u102c\u1038\u1021\u101a\u103c\u1004\u1039\u1038\u101b\u103d\u102d\u101e\u103b\u1016\u1004\u1039\u1037 \u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b", "\u1005\u101c\u102d\u102f\u1000\u1039\u1012\u102b\u1000\u102d\u102f \u100a\u102c\u1018\u1000\u1039\u1021\u1005\u103c\u1014\u1039\u1006\u1036\u102f\u1038\u1000\u103c\u1000\u1039\u101e\u102d\u102f\u1094 \u1006\u103c\u1032\u1015\u102b", "\u1031\u1014\u102c\u1000\u1039\u1010\u1005\u1039\u1080\u1000\u102d\u1019\u1039\u1011\u1015\u1039\u1006\u103c\u1032\u1015\u102b", "\u1005\u101c\u102d\u102f\u1000\u1039\u1012\u102b\u1000\u102d\u102f \u100a\u102c\u1018\u1000\u1039\u1021\u1005\u103c\u1014\u1039\u1006\u1036\u102f\u1038\u1000\u103c\u1000\u1039\u101e\u102d\u102f\u1094 \u1006\u103c\u1032\u1015\u102b", "\u1015\u1031\u101f\u1020\u102d\u103b\u1015\u100a\u1039\u1037\u1005\u1036\u102f\u1031\u1005\u101b\u1014\u1039 \u1005\u101c\u102d\u102f\u1000\u1039\u1012\u102b\u1000\u102d\u102f \u1031\u1021\u102c\u1000\u1039\u101e\u102f\u102d\u1094\u1006\u103c\u1032\u1015\u102b", "\u1021\u1000\u103c\u1000\u1039\u1010\u103c\u1004\u1039\u1038\u101e\u102d\u102f\u1094 \u1019\u103d\u1014\u1039\u1000\u1014\u1039\u1031\u1021\u102c\u1004\u1039 \u1011\u100a\u1039\u1037\u101e\u103c\u1004\u1039\u1038\u1015\u102b", "\u1011\u102d\u102f\u1010\u1005\u1039\u1001\u102f\u1000 \u1001\u1000\u1039\u1001\u1032\u108f\u102d\u102f\u1004\u1039\u101e\u103b\u1016\u1004\u1039\u1037 \u1024\u1010\u1005\u1039\u1001\u102f\u1000\u102d\u102f \u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u107e\u1000\u100a\u1039\u1037\u1015\u102b", ["\u1011\u100a\u1039\u1037\u101b\u1019\u100a\u1039\u1037\u1021\u1015\u102d\u102f\u1004\u1039\u1038\u1031\u1015\u103a\u102c\u1000\u1039\u101e\u103c\u102c\u1038\u101e\u100a\u1039\u104b \u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b", "\u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b\u104a \u1031\u1014\u101b\u102c\u1015\u102d\u102f\u1019\u102d\u102f\u1010\u102d\u1000\u103a\u1015\u102b\u1031\u1005", "\u1000\u103c\u1014\u1039\u101b\u1000\u1039\u1019\u1010\u100a\u1039\u107f\u1004\u102d\u1019\u1039\u1015\u102b\u104a \u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b"], "\u1031\u1012\u1010\u102c\u101b\u101a\u1030\u1019\u1088 \u1019\u1031\u1021\u102c\u1004\u1039\u103b\u1019\u1004\u1039\u1015\u102b\u104b \u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u101b\u1014\u1039\u1015\u1036\u102f\u1000\u102d\u102f\u108f\u103d\u102d\u1015\u1039\u1015\u102b", "\u1021\u1010\u100a\u1039\u103b\u1015\u1033\u1019\u1088 \u1031\u1021\u102c\u1004\u1039\u103b\u1019\u1004\u1039\u1015\u102b\u101e\u100a\u1039", "\u1019\u107e\u1000\u102c\u1001\u1014\u103b\u1015\u1014\u1039\u1016\u103c\u1004\u1039\u1037\u1031\u1014\u101b\u101e\u100a\u1039\u104b", "\u1000\u103c\u1014\u1039\u101b\u1000\u1039\u1019\u1010\u100a\u1039\u107f\u1004\u102d\u1019\u1039\u1015\u102b\u104a \u1011\u1015\u1039\u1019\u1036\u1080\u1000\u102d\u1033\u1038\u1005\u102c\u1038\u1015\u102b(+)"],
        fr: ["Touchez pour v\xe9rifier", "V\xe9rification de s\xe9curit\xe9", "La v\xe9rification est r\xe9ussie", "Commentaire", "Actualiser", "V\xe9rifier", "Touchez pour recharger", "Session expir\xe9e. R\xe9essayez.", "Erreur de v\xe9rification. R\xe9essayez.", "Code de v\xe9rification", "Retour", "V\xe9rification...", "R\xe9seau instable. Touchez Actualiser pour r\xe9essayer.", "Chargement \xe9chou\xe9. Touchez l'image pour actualiser.", "V\xe9rification", ["+s. Vous avez battu Lucky Luke\xa0!", "+s. Parfait\xa0!", "La v\xe9rification est r\xe9ussie"], "Actualiser", "Fermer", "Commentaire", "Trop actualis\xe9. Touchez pour r\xe9essayer.", "Glissez le curseur vers la droite pour terminer le puzzle.", "Erreur de v\xe9rification. R\xe9essayez.", "Glissez le curseur le plus \xe0 droite possible", "Glissez-la encore une fois", "Glissez le curseur le plus \xe0 droite possible", "Glissez le curseur ci-dessous pour terminer le puzzle", "Embo\xeetez la pi\xe8ce au bon endroit", "Celui-ci \xe9tait un peu dur. Essayez celui-l\xe0.", ["La pi\xe8ce a disparu. R\xe9essayez.", "R\xe9essayez de mieux l'embo\xeeter", "R\xe9seau instable. R\xe9essayez."], "Chargement \xe9chou\xe9. Touchez l'image pour actualiser.", "La v\xe9rification est r\xe9ussie", "Trop actualis\xe9", "R\xe9seau instable(+). R\xe9essayez.", "Accessibilit\xe9"],
        de: ["Tippen zum Best\xe4tigen", "Sicherheitsbest\xe4tigung", "Verifizierung erfolgreich", "Feedback", "Aktualisieren", "Verifizieren", "Tippen zum Neuladen", "Zeit\xfcberschreitung. Bitte nochmal versuchen.", "Fehler bei Verifizierung. Bitte nochmal versuchen.", "Verifzierung", "Zur\xfcck", "Wird verifziert\xa0\u2026", "Netzwerk instabil. Zum Wiederholen \u201eAktualisieren\u201c.", "Ladefehler. Zum Aktualisieren Bild antippen.", "Wird verifiziert", ["+s verbraucht. Schneller als der Blitz!", "+s verbraucht. Perfekt!", "Verifizierung erfolgreich"], "Aktualisieren", "Schlie\xdfen", "Feedback", "Zu oft aktualisiert. Tippen zum Wiederholen.", "Um das Puzzle abzuschlie\xdfen, Schieber nach rechts ziehen.", "Fehler bei Verifizierung. Bitte nochmal versuchen.", "Schieber in die Position ganz rechts ziehen", "Noch einmal ziehen", "Schieber in die Position ganz rechts ziehen", "Zum Abschlie\xdfen des Puzzles den Schieber unten bewegen", "Das St\xfcck rechts ins Fach stecken", "Das scheint zu schwer zu sein. Versuchen Sie es hiermit.", ["Das St\xfcck ist verlorengegangen. Bitte nochmal versuchen.", "Versuchen Sie es nochmal, so dass es genauer passt.", "Netzwerk instabil. Bitte nochmal versuchen."], "Ladefehler. Zum Aktualisieren Bild antippen.", "Verifizierung erfolgreich", "Zu oft aktualisiert", "Netzwerk instabil(+). Bitte nochmal versuchen.", "Barrierefreiheit"],
        he: ["\u05dc\u05d7\u05e6\u05d5 \u05d1\u05db\u05d3\u05d9 \u05dc\u05d0\u05de\u05ea", "\u05d0\u05d9\u05de\u05d5\u05ea \u05d0\u05d1\u05d8\u05d7\u05d4", "\u05d4\u05d0\u05d9\u05de\u05d5\u05ea \u05e2\u05d1\u05e8 \u05d1\u05d4\u05e6\u05dc\u05d7\u05d4", "\u05de\u05e9\u05d5\u05d1", "\u05e8\u05e2\u05e0\u05df", "\u05dc\u05d0\u05de\u05ea", "\u05dc\u05d7\u05e6\u05d5 \u05d1\u05db\u05d3\u05d9 \u05dc\u05d8\u05e2\u05d5\u05df \u05de\u05d7\u05d3\u05e9", "\u05e9\u05d2\u05d9\u05d0\u05ea \u05d6\u05de\u05df. \u05d0\u05e0\u05d0 \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1", "\u05d8\u05e2\u05d5\u05ea \u05d1\u05d0\u05d9\u05de\u05d5\u05ea. \u05d0\u05e0\u05d0 \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1", "\u05e7\u05d5\u05d3 \u05d0\u05d9\u05de\u05d5\u05ea", "\u05d7\u05d6\u05e8\u05d4", "\u05de\u05d0\u05de\u05ea", "\u05e8\u05e9\u05ea \u05dc\u05d0 \u05d9\u05e6\u05d9\u05d1\u05d4. \u05dc\u05d7\u05e6\u05d5 \u05e2\u05dc \u05e8\u05e2\u05e0\u05df \u05d1\u05db\u05d3\u05d9 \u05dc\u05e0\u05e1\u05d5\u05ea \u05e9\u05d5\u05d1", "\u05d4\u05d8\u05e2\u05d9\u05e0\u05d4 \u05e0\u05db\u05e9\u05dc\u05d4. \u05dc\u05d7\u05e6\u05d5 \u05e2\u05dc \u05d4\u05ea\u05de\u05d5\u05e0\u05d4 \u05d1\u05db\u05d3\u05d9 \u05dc\u05d8\u05e2\u05d5\u05df \u05de\u05d7\u05d3\u05e9", "\u05de\u05d0\u05de\u05ea", ["+s \u05d1\u05d5\u05d6\u05d1\u05d6. \u05e0\u05d9\u05e6\u05d7\u05ea \u05d0\u05ea \u05d4\u05d1\u05d6\u05e7!", "+s \u05d1\u05d5\u05d6\u05d1\u05d6. \u05de\u05d5\u05e9\u05dc\u05dd!", "\u05d4\u05d0\u05d9\u05de\u05d5\u05ea \u05e2\u05d1\u05e8 \u05d1\u05d4\u05e6\u05dc\u05d7\u05d4"], "\u05e8\u05e2\u05e0\u05df", "\u05e1\u05d2\u05d5\u05e8", "\u05de\u05e9\u05d5\u05d1", "\u05de\u05e8\u05e2\u05e0\u05df \u05dc\u05e2\u05ea\u05d9\u05dd \u05e7\u05e8\u05d5\u05d1\u05d5\u05ea \u05de\u05d9\u05d3\u05d9. \u05dc\u05d7\u05e6\u05d5 \u05d1\u05db\u05d3\u05d9 \u05dc\u05e0\u05e1\u05d5\u05ea \u05e9\u05d5\u05d1", "\u05d2\u05e8\u05e8\u05d5 \u05d0\u05ea \u05de\u05d7\u05d5\u05d5\u05df \u05dc\u05d9\u05de\u05d9\u05df \u05d1\u05db\u05d3\u05d9 \u05dc\u05d4\u05e9\u05dc\u05d9\u05dd \u05d0\u05ea \u05d4\u05e4\u05d0\u05d6\u05dc", "\u05d8\u05e2\u05d5\u05ea \u05d1\u05d0\u05d9\u05de\u05d5\u05ea. \u05d0\u05e0\u05d0 \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1", "\u05d2\u05e8\u05e8\u05d5 \u05d0\u05ea \u05d4\u05de\u05d7\u05d5\u05d5\u05df \u05dc\u05de\u05e9\u05d1\u05e6\u05ea \u05d1\u05d9\u05de\u05d9\u05df \u05d4\u05e7\u05d9\u05e6\u05d5\u05df", "\u05d2\u05e8\u05e8\u05d5 \u05d6\u05d0\u05ea \u05e2\u05d5\u05d3 \u05e4\u05e2\u05dd", "\u05d2\u05e8\u05e8\u05d5 \u05d0\u05ea \u05d4\u05de\u05d7\u05d5\u05d5\u05df \u05dc\u05de\u05e9\u05d1\u05e6\u05ea \u05d1\u05d9\u05de\u05d9\u05df \u05d4\u05e7\u05d9\u05e6\u05d5\u05df", "\u05d2\u05e8\u05e8\u05d5 \u05d0\u05ea \u05d4\u05de\u05d7\u05d5\u05d5\u05df \u05dc\u05de\u05d8\u05d4 \u05d1\u05db\u05d3\u05d9 \u05dc\u05d4\u05e9\u05dc\u05d9\u05dd \u05d0\u05ea \u05d4\u05e4\u05d0\u05d6\u05dc", "\u05d4\u05db\u05e0\u05d9\u05e1\u05d5 \u05d0\u05ea \u05d4\u05d7\u05ea\u05d9\u05db\u05d4 \u05d9\u05e9\u05e8 \u05d0\u05ea \u05d4\u05de\u05e9\u05d1\u05e6\u05ea", "\u05d6\u05d4 \u05e0\u05e8\u05d0\u05d4 \u05d8\u05d9\u05e4\u05d4 \u05e7\u05e9\u05d4. \u05e0\u05e1\u05d5 \u05d0\u05ea \u05d6\u05d4 \u05d1\u05de\u05e7\u05d5\u05dd", ["\u05d4\u05ea\u05d9\u05db\u05d4 \u05d4\u05dc\u05db\u05d4 \u05dc\u05d0\u05d9\u05d1\u05d5\u05d3. \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1", "\u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1 \u05d5\u05d5\u05d3\u05d0\u05d5 \u05e9\u05d6\u05d4 \u05de\u05ea\u05d0\u05d9\u05dd \u05d9\u05d5\u05ea\u05e8 \u05d1\u05de\u05d3\u05d5\u05d9\u05e7", "\u05e8\u05e9\u05ea \u05dc\u05d0 \u05d9\u05e6\u05d9\u05d1\u05d4. \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1"], "\u05d4\u05d8\u05e2\u05d9\u05e0\u05d4 \u05e0\u05db\u05e9\u05dc\u05d4. \u05dc\u05d7\u05e6\u05d5 \u05e2\u05dc \u05d4\u05ea\u05de\u05d5\u05e0\u05d4 \u05d1\u05db\u05d3\u05d9 \u05dc\u05e8\u05e2\u05e0\u05df", "\u05d4\u05d0\u05d9\u05de\u05d5\u05ea \u05e2\u05d1\u05e8 \u05d1\u05d4\u05e6\u05dc\u05d7\u05d4", "\u05de\u05e8\u05e2\u05e0\u05df \u05dc\u05e2\u05ea\u05d9\u05dd \u05e7\u05e8\u05d5\u05d1\u05d5\u05ea \u05de\u05d9\u05d3\u05d9", "\u05e8\u05e9\u05ea \u05dc\u05d0 \u05d9\u05e6\u05d9\u05d1\u05d4. (+)\u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1"],
        hi: ["\u0938\u0924\u094d\u092f\u093e\u092a\u093f\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u091f\u0948\u092a \u0915\u0930\u0947\u0902", "\u0938\u0941\u0930\u0915\u094d\u0937\u093e \u0938\u0924\u094d\u092f\u093e\u092a\u0928", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0938\u092b\u0932", "\u092b\u0940\u0921\u092c\u0948\u0915", "\u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u0915\u0930\u0947\u0902", "\u0938\u0924\u094d\u092f\u093e\u092a\u093f\u0924 \u0915\u0930\u0947\u0902", "\u0930\u0940\u0932\u094b\u0921 \u0915\u0930\u0947\u0902", "\u091f\u093e\u0907\u092e\u0906\u0909\u091f\u0964 \u092a\u0941\u0928\u0903 \u092a\u094d\u0930\u092f\u093e\u0938 \u0915\u0930\u0947\u0902", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0924\u094d\u0930\u0941\u091f\u093f\u0964 \u092a\u0941\u0928\u0903 \u092a\u094d\u0930\u092f\u093e\u0938 \u0915\u0930\u0947\u0902", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0915\u094b\u0921", "\u092a\u0940\u091b\u0947", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u091c\u093e\u0930\u0940...", "\u0905\u0938\u094d\u0925\u093e\u0908 \u0928\u0947\u091f\u0935\u0930\u094d\u0915\u0964 \u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u091f\u0948\u092a \u0915\u0930 \u0926\u0941\u092c\u093e\u0930\u093e \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902", "\u0932\u094b\u0921 \u0928\u0939\u0940\u0902 \u0913 \u092a\u093e\u092f\u093e\u0964 \u091a\u093f\u0924\u094d\u0930 \u092a\u0930 \u091f\u0948\u092a \u0915\u0930 \u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u0915\u0930\u0947\u0902", "\u0938\u0924\u094d\u092f\u093e\u092a\u093f\u0924 \u0939\u094b \u0930\u0939\u093e \u0939\u0948", ["+s \u0916\u0930\u094d\u091a \u0939\u0941\u0906\u0964 \u0906\u092a\u0928\u0947 \u092b\u094d\u0932\u0948\u0936 \u0915\u094b \u0939\u0930\u093e \u0926\u093f\u092f\u093e!", "+s \u0916\u0930\u094d\u091a \u0939\u0941\u0906\u0964 \u092c\u0939\u0941\u0924 \u0905\u091a\u094d\u091b\u093e!", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0938\u092b\u0932 \u0939\u0941\u0906"], "\u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u0915\u0930\u0947\u0902", "\u092c\u0902\u0926 \u0915\u0930\u0947\u0902", "\u0938\u0941\u091d\u093e\u0935", "\u0905\u0915\u094d\u0938\u0930 \u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u0939\u094b \u0930\u0939\u093e \u0939\u0948\u0964 \u091f\u0948\u092a \u0915\u0930 \u0926\u0941\u092c\u093e\u0930\u093e \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902\u0964", "\u092a\u0939\u0947\u0932\u0940 \u092a\u0942\u0930\u093e \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0938\u094d\u0932\u093e\u0907\u0921\u0930 \u0926\u093e\u090f\u0902 \u0916\u0940\u0902\u091a\u0947\u0902", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0924\u094d\u0930\u0941\u091f\u093f\u0964 \u092a\u0941\u0928\u0903 \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902", "\u0938\u092c\u0938\u0947 \u0926\u093e\u090f\u0902 \u0935\u093e\u0932\u0947 \u0916\u093e\u0928\u0947 \u092e\u0947\u0902 \u0938\u094d\u0932\u093e\u0908\u0921\u0930 \u0916\u0940\u0902\u091a\u0947\u0902", "\u0907\u0938\u0947 \u090f\u0915 \u092c\u093e\u0930 \u092b\u093f\u0930 \u0938\u0947 \u0916\u0940\u0902\u091a\u0947", "\u0938\u092c\u0938\u0947 \u0926\u093e\u090f\u0902 \u0916\u093e\u0928\u0947 \u092e\u0947\u0902 \u0938\u094d\u0932\u093e\u0907\u0921\u0930 \u0916\u0940\u0902\u091a \u0915\u0947 \u0932\u0947 \u091c\u093e\u090f\u0902", "\u092a\u0939\u0947\u0932\u0940 \u092a\u0942\u0930\u093e \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0938\u094d\u0932\u093e\u0907\u0921\u0930 \u0928\u0940\u091a\u0947 \u0916\u0940\u0902\u091a\u0947\u0902", "\u0907\u0938 \u091f\u0941\u0915\u095c\u0947 \u0915\u094b \u0926\u093e\u090f\u0902 \u0915\u0947 \u0916\u093e\u0928\u0947 \u092e\u0947\u0902 \u0930\u0916\u0947\u0902", "\u092f\u0939 \u0925\u094b\u095c\u093e \u0915\u0920\u093f\u0928 \u0939\u0948\u0964 \u0907\u0938\u0947 \u0906\u091c\u092e\u093e\u090f\u0902", ["\u092f\u0939 \u091f\u0941\u0915\u095c\u093e \u0916\u094b \u0917\u092f\u093e \u0939\u0948\u0964 \u092a\u0941\u0928\u0903 \u092a\u094d\u0930\u092f\u093e\u0938 \u0915\u0930\u0947\u0902", "\u0926\u0941\u092c\u093e\u0930\u093e \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902 \u0914\u0930 \u0907\u0938\u0947 \u092c\u0947\u0939\u0924\u0930 \u0924\u0930\u0940\u0915\u0947 \u0938\u0947 \u092e\u093f\u0932\u093e\u090f\u0902", "\u0905\u0938\u094d\u0925\u093e\u0908 \u0928\u0947\u091f\u0935\u0930\u094d\u0915\u0964 \u092a\u0941\u0928\u0903 \u092a\u094d\u0930\u092f\u093e\u0938 \u0915\u0930\u0947\u0902"], "\u0932\u094b\u0921 \u0928\u0939\u0940\u0902 \u0939\u094b \u092a\u093e\u092f\u093e\u0964 \u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u091f\u0948\u092a \u0915\u0930\u0947\u0902", "\u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0938\u092b\u0932", "\u0905\u0915\u094d\u0938\u0930 \u0930\u0940\u092b\u094d\u0930\u0947\u0936 \u0939\u094b \u0930\u0939\u093e \u0939\u0948\u0964", "\u0905\u0938\u094d\u0925\u093e\u0908 \u0928\u0947\u091f\u0935\u0930\u094d\u0915\u0964 \u092a\u0941\u0928\u0903 \u092a\u094d\u0930\u092f\u093e\u0938 \u0915\u0930\u0947\u0902(+)"],
        id: ["Ketuk untuk memverifikasi", "Verifikasi Keamanan", "Verifikasi berhasil", "Masukan", "Refresh", "Verifikasi", "Ketuk untuk memuat ulang", "Waktu habis. Coba lagi.", "Error verifikasi. Coba lagi.", "Kode Verifikasi", "Kembali", "Memverifikasi...", "Jaringan tidak stabil. Ketuk Refresh.", "Gagal memuat. Ketuk gambar untuk merefresh.", "Memverifikasi", ["+s dihabiskan. Flash pun Anda kalahkan!", "+s dihabiskan. Sempurna!", "Verifikasi berhasil"], "Refresh", "Tutup", "Masukan", "Terlalu sering merefresh. Ketuk untuk mencoba lagi.", "Geser slider ke kanan untuk menyelesaikan puzzle.", "Verifikasi gagal. Coba lagi.", "Geser slider ke slot paling kanan", "Geser sekali lagi", "Geser slider ke slot paling kanan", "Geser slider di bawah untuk menyelesaikan puzzle", "Letakkan potongan puzzle ke dalam slot", "Sepertinya agak sulit. Coba yang ini.", ["Potongannya tidak sesuai. Coba lagi.", "Coba lagi, pastikan lebih pas", "Jaringan tidak stabil. Coba lagi."], "Gagal memuat. Ketuk gambar untuk merefresh.", "Verifikasi berhasil", "Terlalu sering merefresh.", "Jaringan tidak stabil(+). Coba lagi."],
        it: ["Tocca per verificare", "Verifica di sicurezza", "Verifica completata", "Opinioni", "Aggiorna", "Verifica", "Tocca per ricaricare", "Scaduto, riprova.", "Errore di verifica, riprova", "Codice di verifica", "Indietro", "Verifica in corso", "Rete instabile. Tocca Aggiorna per riprovare.", "Caricamento fallito. Tocca immagine per aggiornare.", "Verifica in corso", ["+s spesi. Hai battuto il Flash!", "+s spesi. Perfetto!", "Verifica completata"], "Aggiorna", "Chiudi", "Opinioni", "Aggiornam. troppo frequente, tocca per riprovare.", "Trascina dispos. scorrim. a destra per completare il puzzle.", "Errore di verifica, riprova.", "Trascina dispos. di scorrimento verso lo slot pi\xf9 a destra", "Trascinalo un'altra volta", "Trascina dispos. di scorrimento verso lo slot pi\xf9 a destra", "Trascina dispos. scorrim. in basso per completare il puzzle", "Inserisci il pezzo nello slot", "Quello sembra difficile, prova con questo.", ["Il pezzo si \xe8 perso, riprova.", "Riprova e fallo entrare meglio", "Rete instabile, riprova."], "Caricamento non riuscito, tocca l'immagine per aggiornare.", "Verifica completata", "Troppo frequente", "Rete instabile(+), riprova.", "Accessibilit\xe0"],
        ja: ["\u30bf\u30c3\u30d7\u3057\u3066\u8a8d\u8a3c\u3057\u3066\u304f\u3060\u3055\u3044", "\u30bb\u30ad\u30e5\u30ea\u30c6\u30a3\u8a8d\u8a3c", "\u8a8d\u8a3c\u304c\u6b63\u5e38\u306b\u5b8c\u4e86", "\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af", "\u66f4\u65b0", "\u8a8d\u8a3c", "\u30bf\u30c3\u30d7\u3057\u3066\u518d\u5ea6\u8aad\u307f\u8fbc\u3093\u3067\u304f\u3060\u3055\u3044", "\u30bf\u30a4\u30e0\u30a2\u30a6\u30c8\u3057\u307e\u3057\u305f\uff0c\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044", "\u8a8d\u8a3c\u30a8\u30e9\u30fc\uff0c\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044", "\u8a8d\u8a3c\u30b3\u30fc\u30c9", "\u623b\u308b", "\u8a8d\u8a3c\u4e2d\u2026", "\u63a5\u7d9a\u304c\u4e0d\u5b89\u5b9a\u3067\u3059\uff0c\u66f4\u65b0\u3092\u30bf\u30c3\u30d7\u3057\u3066\u304f\u3060\u3055\u3044", "\u8aad\u307f\u8fbc\u307f\u5931\u6557\uff0c\u753b\u50cf\u3092\u30bf\u30c3\u30d7\u3057\u3066\u66f4\u65b0\u3057\u3066\u304f\u3060\u3055\u3044", "\u8a8d\u8a3c\u4e2d", ["+s\u79d2\u3067\u5b8c\u6210\u3002\u96fb\u5149\u77f3\u706b\u306e\u901f\u3055\uff01", "+s\u79d2\u3067\u5b8c\u6210\u3002\u5b8c\u74a7\uff01", "\u8a8d\u8a3c\u304c\u6b63\u5e38\u306b\u5b8c\u4e86"], "\u66f4\u65b0", "\u9589\u3058\u308b", "\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af", "\u66f4\u65b0\u983b\u5ea6\u304c\u9ad8\u3059\u304e\u307e\u3059\uff0c\u30bf\u30c3\u30d7\u3057\u3066\u518d\u8a66\u884c\u3057\u3066\u304f\u3060\u3055\u3044", "\u30b9\u30e9\u30a4\u30c0\u30fc\u3092\u53f3\u306b\u30c9\u30e9\u30c3\u30b0\u3057\u3066\u30d1\u30ba\u30eb\u3092\u5b8c\u6210\u3055\u305b\u307e\u3059", "\u8a8d\u8a3c\u30a8\u30e9\u30fc\uff0c\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044", "\u30b9\u30e9\u30a4\u30c0\u30fc\u3092\u53f3\u7aef\u306e\u30b9\u30ed\u30c3\u30c8\u306b\u30c9\u30e9\u30c3\u30b0\u3057\u3066\u304f\u3060\u3055\u3044", "\u3082\u3046\u4e00\u5ea6\u30c9\u30e9\u30c3\u30b0\u3057\u3066\u304f\u3060\u3055\u3044", "\u30b9\u30e9\u30a4\u30c0\u30fc\u3092\u53f3\u7aef\u306e\u30b9\u30ed\u30c3\u30c8\u306b\u30c9\u30e9\u30c3\u30b0\u3057\u3066\u304f\u3060\u3055\u3044", "\u30b9\u30e9\u30a4\u30c0\u30fc\u3092\u30c9\u30e9\u30c3\u30b0\u3057\u3066\u30d1\u30ba\u30eb\u3092\u5b8c\u6210\u3055\u305b\u3066\u304f\u3060\u3055\u3044", "\u30d4\u30fc\u30b9\u3092\u30b9\u30ed\u30c3\u30c8\u306b\u306f\u3081\u3066\u304f\u3060\u3055\u3044", "\u5c11\u3057\u96e3\u3057\u3044\u3088\u3046\u3067\u3059\u306d\uff0c\u3053\u3061\u3089\u3092\u304a\u8a66\u3057\u304f\u3060\u3055\u3044", ["\u30d4\u30fc\u30b9\u304c\u5931\u308f\u308c\u307e\u3057\u305f\uff0c\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044", "\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u306b\u306a\u308a\uff0c\u3082\u3063\u3068\u6b63\u78ba\u306b\u306f\u3081\u3066\u304f\u3060\u3055\u3044", "\u63a5\u7d9a\u304c\u4e0d\u5b89\u5b9a\u3067\u3059\uff0c\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044"], "\u8aad\u307f\u8fbc\u307f\u5931\u6557\uff0c\u753b\u50cf\u3092\u30bf\u30c3\u30d7\u3057\u3066\u66f4\u65b0\u3057\u3066\u304f\u3060\u3055\u3044", "\u8a8d\u8a3c\u304c\u6b63\u5e38\u306b\u5b8c\u4e86", "\u66f4\u65b0\u983b\u5ea6\u304c\u9ad8\u3059\u304e\u307e\u3059", "\u63a5\u7d9a\u304c\u4e0d\u5b89\u5b9a\u3067\u3059(+)\uff0c\u3082\u3046\u4e00\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044"],
        ko: ["\ud0ed\ud574\uc11c \uc778\uc99d", "\ubcf4\uc548 \uc778\uc99d", "\uc778\uc99d \uc131\uacf5", "\ud53c\ub4dc\ubc31", "\uc0c8\ub85c\uace0\uce68", "\uc778\uc99d", "\ud0ed\ud574\uc11c \ub9ac\ub85c\ub4dc", "\uc2dc\uac04 \ucd08\uacfc. \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694. ", "\uc778\uc99d \uc624\ub958. \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694. ", "\uc778\uc99d \ucf54\ub4dc", "\ub4a4\ub85c\uac00\uae30", "\uc778\uc99d \uc911...", "\ub124\ud2b8\uc6cc\ud06c\uac00 \ubd88\uc548\uc815\ud569\ub2c8\ub2e4. \uc0c8\ub85c\uace0\uce68\uc744 \ud0ed\ud574\uc11c \uc7ac\uc2dc\ub3c4. ", "\ub85c\ub529\uc5d0 \uc2e4\ud328\ud588\uc2b5\ub2c8\ub2e4. \uc774\ubbf8\uc9c0\ub97c \ud0ed\ud574\uc11c \uc0c8\ub85c\uace0\uce68. ", "\uc778\uc99d \uc911", ["+s\uc744/\ub97c \uc37c\uc2b5\ub2c8\ub2e4. Flash\uc5d0\uac8c \uc774\uae30\uc168\uc5b4\uc694!", "+s\uc744/\ub97c \uc37c\uc2b5\ub2c8\ub2e4. \uc644\ubcbd\ud569\ub2c8\ub2e4!", "\uc778\uc99d \uc131\uacf5"], "\uc0c8\ub85c\uace0\uce68", "\ub2eb\uae30", "\ud53c\ub4dc\ubc31", "\uc0c8\ub85c\uace0\uce68\uc774 \ub108\ubb34 \uc7a6\uc2b5\ub2c8\ub2e4. \ud0ed\ud574\uc11c \uc7ac\uc2dc\ub3c4. ", "\uc2ac\ub77c\uc774\ub354\ub97c \uc6b0\uce21\uc73c\ub85c \ub4dc\ub798\uadf8\ud574\uc11c \ud37c\uc990\uc744 \uc644\ub8cc\ud558\uc138\uc694", "\uc778\uc99d \uc624\ub958. \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694. ", "\uc2ac\ub77c\uc774\ub354\ub97c \uc6b0\uce21 \ub05d \uc2ac\ub86f\uc73c\ub85c \ub4dc\ub798\uadf8\ud558\uc138\uc694", "\ud55c \ubc88 \ub354 \ub4dc\ub798\uadf8\ud558\uc138\uc694", "\uc2ac\ub77c\uc774\ub354\ub97c \uc6b0\uce21 \ub05d \uc2ac\ub86f\uc73c\ub85c \ub4dc\ub798\uadf8\ud558\uc138\uc694", "\uc544\ub798 \uc2ac\ub77c\uc774\ub354\ub97c \ub4dc\ub798\uadf8\ud574\uc11c \ud37c\uc990\uc744 \uc644\ub8cc\ud558\uc138\uc694", "\uc870\uac01\uc744 \uc2ac\ub86f\uc5d0 \uc815\ud655\ud788 \ub123\uc73c\uc138\uc694", "\uadf8\uac74 \uc880 \uc5b4\ub824\uc6cc \ubcf4\uc774\ub124\uc694. \uc774\uac78 \ud574 \ubcf4\uc138\uc694. ", ["\uc870\uac01\uc774 \uc5c6\uc5b4\uc84c\uc2b5\ub2c8\ub2e4. \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694. ", "\ub2e4\uc2dc \uc2dc\ub3c4\ud574\uc11c \uc815\ud655\ud788 \ub9de\ucdb0 \ubcf4\uc138\uc694", "\ub124\ud2b8\uc6cc\ud06c\uac00 \ubd88\uc548\uc815\ud569\ub2c8\ub2e4. \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694. "], "\ub85c\ub529\uc5d0 \uc2e4\ud328\ud588\uc2b5\ub2c8\ub2e4. \uc774\ubbf8\uc9c0\ub97c \ud0ed\ud574\uc11c \uc0c8\ub85c\uace0\uce68. ", "\uc778\uc99d \uc131\uacf5", "\uc0c8\ub85c\uace0\uce68\uc774 \ub108\ubb34 \uc7a6\uc2b5\ub2c8\ub2e4", "\ub124\ud2b8\uc6cc\ud06c\uac00 \ubd88\uc548\uc815\ud569\ub2c8\ub2e4(+). \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694. "],
        lo: ["\u0ec1\u0e95\u0eb0\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0e84\u0ea7\u0eb2\u0ea1\u0e9b\u0ead\u0e94\u0ec4\u0e9e", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0ec4\u0e94\u0ec9\u0eaa\u0eb3\u0ec0\u0ea5\u0eb1\u0e94\u0ec1\u0ea5\u0ec9\u0ea7", "\u0e82\u0ecd\u0ec9\u0eaa\u0eb0\u0ec0\u0edc\u0eb5\u0ec1\u0e99\u0eb0", "\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99", "\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99", "\u0ec1\u0e95\u0eb0\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0ec2\u0eab\u0ebc\u0e94", "\u0edd\u0ebb\u0e94\u0ec0\u0ea7\u0ea5\u0eb2. \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0e9a\u0ecd\u0ec8\u0e96\u0eb7\u0e81\u0e95\u0ec9\u0ead\u0e87. \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0ea5\u0eb0\u0eab\u0eb1\u0e94\u0e9c\u0ec8\u0eb2\u0e99", "\u0e81\u0eb1\u0e9a\u0e84\u0eb7\u0e99", "\u0e81\u0eb3\u0ea5\u0eb1\u0e87\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99...", "\u0ec0\u0e84\u0eb7\u0ead\u0e82\u0ec8\u0eb2\u0e8d\u0e9a\u0ecd\u0ec8\u0e96\u0eb7\u0e81\u0e95\u0ec9\u0ead\u0e87. \u0ec1\u0e97\u0eb1\u0e9a\u0ec3\u0eaa\u0ec8\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87", "\u0e81\u0eb2\u0e99\u0e94\u0eb2\u0ea7\u0ec2\u0eab\u0ebc\u0e94\u0eab\u0ebc\u0ebb\u0ec9\u0ea1\u0ec0\u0eab\u0ebc\u0ea7. \u0ec1\u0e95\u0eb0\u0ec3\u0eaa\u0ec8\u0eae\u0eb9\u0e9a\u0e9e\u0eb2\u0e9a\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99\u0ec3\u0edd\u0ec8", "\u0e81\u0eb3\u0ea5\u0eb1\u0e87\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99", ["+\u0ec3\u0e8a\u0ec9\u0e88\u0ec8\u0eb2\u0e8d\u0eae\u0ebd\u0e9a\u0eae\u0ec9\u0ead\u0e8d\u0ec1\u0ea5\u0ec9\u0ea7. \u0e97\u0ec8\u0eb2\u0e99\u0e8a\u0eb0\u0e99\u0eb0\u0ec1\u0e9f\u0ea5\u0e8a!", "+\u0ec3\u0e8a\u0ec9\u0e88\u0ec8\u0eb2\u0e8d\u0eae\u0ebd\u0e9a\u0eae\u0ec9\u0ead\u0e8d\u0ec1\u0ea5\u0ec9\u0ea7. \u0eaa\u0ebb\u0ea1\u0e9a\u0eb9\u0e99\u0ec1\u0e9a\u0e9a!", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0ec4\u0e94\u0ec9\u0eaa\u0eb3\u0ec0\u0ea5\u0eb1\u0e94\u0ec1\u0ea5\u0ec9\u0ea7"], "\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99", "\u0e9b\u0eb4\u0e94", "\u0e82\u0ecd\u0ec9\u0eaa\u0eb0\u0ec0\u0edc\u0eb5\u0ec1\u0e99\u0eb0", "\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99\u0ec0\u0ea5\u0eb7\u0ec9\u0ead\u0e8d\u0ec6. \u0ec1\u0e97\u0eb1\u0e9a\u0ec3\u0eaa\u0ec8\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87", "\u0ea5\u0eb2\u0e81\u0ec1\u0e96\u0e9a\u0ec0\u0ea5\u0eb7\u0ec8\u0ead\u0e99\u0ec4\u0e9b\u0e97\u0eb2\u0e87\u0e82\u0ea7\u0eb2\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0eaa\u0eb3\u0ec0\u0ea5\u0eb1\u0e94\u0e81\u0eb2\u0e99\u0e9b\u0eb4\u0e94", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0e9a\u0ecd\u0ec8\u0e96\u0eb7\u0e81\u0e95\u0ec9\u0ead\u0e87. \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87", "\u0ea5\u0eb2\u0e81\u0ec1\u0e96\u0e9a\u0ec0\u0ea5\u0eb7\u0ec8\u0ead\u0e99\u0ec4\u0e9b\u0e8d\u0eb1\u0e87\u0e8a\u0ec8\u0ead\u0e87\u0e82\u0ea7\u0eb2\u0eaa\u0eb8\u0e94", "\u0ea5\u0eb2\u0e81\u0ec4\u0e9b\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87\u0edc\u0eb6\u0ec8\u0e87", "\u0ea5\u0eb2\u0e81\u0ec1\u0e96\u0e9a\u0ec0\u0ea5\u0eb7\u0ec8\u0ead\u0e99\u0ec4\u0e9b\u0e8d\u0eb1\u0e87\u0e8a\u0ec8\u0ead\u0e87\u0e82\u0ea7\u0eb2\u0eaa\u0eb8\u0e94", "\u0ea5\u0eb2\u0e81\u0ec1\u0e96\u0e9a\u0ec0\u0ea5\u0eb7\u0ec8\u0ead\u0e99\u0ec4\u0e9b\u0e97\u0eb2\u0e87\u0e82\u0ea7\u0eb2\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0eaa\u0eb3\u0ec0\u0ea5\u0eb1\u0e94\u0e81\u0eb2\u0e99\u0e9b\u0eb4\u0e94", "\u0ea7\u0eb2\u0e87\u0e8a\u0eb4\u0ec9\u0e99\u0eaa\u0ec8\u0ea7\u0e99\u0ec4\u0ea7\u0ec9\u0ec3\u0e99\u0e8a\u0ec8\u0ead\u0e87\u0ea7\u0ec8\u0eb2\u0e87", "\u0eaa\u0eb4\u0ec8\u0e87\u0e99\u0eb1\u0ec9\u0e99\u0ec0\u0e9a\u0eb4\u0ec8\u0e87\u0e84\u0eb7\u0ea7\u0ec8\u0eb2\u0e9a\u0eb4\u0e94\u0e8d\u0eb2\u0e81. \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ead\u0eb1\u0e99\u0ec3\u0edd\u0ec8", ["\u0e8a\u0eb4\u0ec9\u0e99\u0eaa\u0ec8\u0ea7\u0e99\u0eab\u0eb2\u0e8d\u0ec4\u0e9b. \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87", "\u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87 \u0ec1\u0ea5\u0eb0\u0ec0\u0eae\u0eb1\u0e94\u0ec3\u0eab\u0ec9\u0ea1\u0eb1\u0e99\u0e81\u0eb1\u0e9a\u0ec0\u0e82\u0ebb\u0ec9\u0eb2\u0eab\u0eb2\u0e81\u0eb1\u0e99\u0ea2\u0ec8\u0eb2\u0e87\u0e96\u0eb7\u0e81\u0e95\u0ec9\u0ead\u0e87", "\u0ec0\u0e84\u0eb7\u0ead\u0e99\u0e82\u0ec8\u0eb2\u0e8d\u0e9a\u0ecd\u0ec8\u0e96\u0eb7\u0e81\u0e95\u0ec9\u0ead\u0e87. \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87"], "\u0e81\u0eb2\u0e99\u0e94\u0eb2\u0ea7\u0ec2\u0eab\u0ebc\u0e94\u0eab\u0ebc\u0ebb\u0ec9\u0ea1\u0ec0\u0eab\u0ebc\u0ea7. \u0ec1\u0e95\u0eb0\u0ec3\u0eaa\u0ec8\u0eae\u0eb9\u0e9a\u0e9e\u0eb2\u0e9a\u0ec0\u0e9e\u0eb7\u0ec8\u0ead\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99\u0ec3\u0edd\u0ec8", "\u0e81\u0eb2\u0e99\u0ea2\u0eb7\u0e99\u0ea2\u0eb1\u0e99\u0ec4\u0e94\u0ec9\u0eaa\u0eb3\u0ec0\u0ea5\u0eb1\u0e94\u0ec1\u0ea5\u0ec9\u0ea7", "\u0e9f\u0eb7\u0ec9\u0e99\u0e9f\u0eb9\u0e84\u0eb7\u0e99\u0ec0\u0ea5\u0eb7\u0ec9\u0ead\u0e8d\u0ec6", "\u0ec0\u0e84\u0eb7\u0ead\u0e99\u0e82\u0ec8\u0eb2\u0e8d\u0e9a\u0ecd\u0ec8\u0e96\u0eb7\u0e81\u0e95\u0ec9\u0ead\u0e87(+). \u0e81\u0eb0\u0ea5\u0eb8\u0e99\u0eb2\u0ea5\u0ead\u0e87\u0ec3\u0edd\u0ec8\u0ead\u0eb5\u0e81\u0e84\u0eb1\u0ec9\u0e87"],
        ms: ["Ketik untuk sahkan", "Pengesahan Keselamatan", "Pengesahan berjaya", "Maklum balas", "Segar Semula", "Sahkan", "Ketik untuk muat semula", "Tamat masa. Cuba lagi.", "Ralat pengesahan. Cuba lagi.", "Kod Pengesahan", "Kembali", "Mengesahkan...", "Rangkaian tak stabil. Ketik Segar Semula utk cuba.", "Gagal memuatkan. Ketik imej untuk segar semula.", "Mengesahkan", ["+s dibelanjakan. Anda sangat Pantas!", "+s dibelanjakan. Sempurna!", "Pengesahan berjaya"], "Segar Semula", "Tutup", "Maklum balas", "Terlalu kerap segar semula. Ketik utk cuba semula.", "Seret peluncur ke kanan untuk selesaikan teka-teki", "Ralat pengesahan. Cuba lagi.", "Seret peluncur ke slot paling kanan", "Seret sekali lagi", "Seret peluncur ke slot paling kanan", "Seret peluncur di bawah untuk selesaikan teka-teki", "Letakkan kepingan ke dalam slot", "Nampaknya yang itu agak sukar. Cuba yang ini.", ["Kepingan telah hilang. Cuba lagi.", "Cuba lagi dan jadikannya sesuai dengan lebih tepat", "Rangkaian tak stabil. Cuba lagi."], "Gagal memuatkan. Ketik imej untuk segar semula.", "Pengesahan berjaya", "Terlalu kerap segar semula", "Rangkaian tak stabil(+). Cuba lagi."],
        pl: ["Dotknij, aby zweryfikowa\u0107", "Weryfikacja bezpiecze\u0144stwa", "Weryfikacja powiod\u0142a si\u0119", "Opinia", "Od\u015bwie\u017c", "Weryfikuj", "Dotknij, aby wczyta\u0107 ponownie", "Przekroczono limit czasu. Spr\xf3buj ponownie.", "B\u0142\u0105d weryfikacji. Spr\xf3buj ponownie.", "Kod weryfikacyjny", "Wstecz", "Weryfikowanie...", "Niestabilna sie\u0107. Dotknij \u201eOd\u015bwie\u017c\u201d, aby ponowi\u0107.", "B\u0142\u0105d wczytywania. Dotknij obrazu, aby od\u015bwie\u017cy\u0107.", "Weryfikowanie", ["+s wydano. Pokona\u0142e\u015b(-a\u015b) Flasha!", "+s wydano. Idealnie!", "Pomy\u015blnie zweryfikowano"], "Od\u015bwie\u017c", "Zamknij", "Opinia", "Za cz\u0119sto od\u015bwie\u017casz. Dotknij, aby ponowi\u0107.", "Przeci\u0105gnij suwak w prawo, aby doko\u0144czy\u0107 uk\u0142adank\u0119", "B\u0142\u0105d weryfikacji. Spr\xf3buj ponownie.", "Przeci\u0105gnij suwak do miejsca najdalej po prawej", "Przeci\u0105gnij jeszcze raz", "Przeci\u0105gnij suwak do miejsca najdalej po prawej", "Przeci\u0105gnij poni\u017cszy suwak, aby doko\u0144czy\u0107 uk\u0142adank\u0119", "W\u0142\xf3\u017c kawa\u0142ek na jego miejsce", "Ta wydaje si\u0119 troch\u0119 za trudna. Spr\xf3buj tej.", ["Kawa\u0142ek si\u0119 zgubi\u0142. Spr\xf3buj ponownie.", "Spr\xf3buj ponownie i spr\xf3buj dopasowa\u0107 dok\u0142adniej", "Niestabilna sie\u0107. Spr\xf3buj ponownie."], "Logowanie nie powiod\u0142o si\u0119. Dotknij obrazu, aby od\u015bwie\u017cy\u0107.", "Weryfikacja powiod\u0142a si\u0119", "Za cz\u0119sto od\u015bwie\u017casz", "Niestabilna sie\u0107(+). Spr\xf3buj ponownie."],
        pt: ["Toque para verificar", "Verifica\xe7\xe3o de Seguran\xe7a", "Verificado com sucesso", "Feedback", "Atualizar", "Verificar", "Toque para recarregar", "Tempo esgotado. Tente de novo.", "Erro na verifica\xe7\xe3o. Tente de novo.", "C\xf3digo de Verifica\xe7\xe3o", "Voltar", "Verificando...", "Rede inst\xe1vel. Toque em Atualizar e tente de novo.", "Falha ao carregar. Toque na imagem para atualizar.", "Verificando", ["+s gasto. Mais r\xe1pido que o Flash!", "+s gasto. Perfeito!", "Verificado com sucesso"], "Atualizar", "Fechar", "Feedback", "Atualizando muito. Toque para tentar de novo.", "Arrastre o slider para a direita para completar o puzzle.", "Erro de verifica\xe7\xe3o. Tente de novo.", "Arrastre o slider para o slot mais \xe0 direita", "Arrastre mais uma vez", "Arrastre o slider para o slot mais \xe0 direita", "Arrastre o slider abaixo para completar o puzzle", "Coloque a pe\xe7a na sua posi\xe7\xe3o", "Esse parece ser dif\xedcil. Tente este.", ["A pe\xe7a foi perdida. Tente de novo.", "Tente de novo e encaixe com mais precis\xe3o", "Rede inst\xe1vel. Tente de novo."], "Falha ao carregar. Toque na imagem para atualizar.", "Verificado com sucesso", "Atualizando muito", "Rede inst\xe1vel(+). Tente de novo."],
        ru: ["\u0414\u043b\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438 \u043d\u0430\u0436\u043c\u0438\u0442\u0435", "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0432 \u0446\u0435\u043b\u044f\u0445 \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u0438", "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u0430", "\u041e\u0442\u0437\u044b\u0432", "\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", "\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c", "\u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u0434\u043b\u044f \u043f\u043e\u0432\u0442\u043e\u0440\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", "\u0412\u0440\u0435\u043c\u044f \u0432\u044b\u0448\u043b\u043e. \u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443.", "\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435. \u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443.", "\u041f\u0440\u043e\u0432\u0435\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u0434", "\u041d\u0430\u0437\u0430\u0434", "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430...", "\u041d\u0435\u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u0430\u044f \u0441\u0435\u0442\u044c. \u0414\u043b\u044f \u043f\u043e\u0432\u0442\u043e\u0440\u0430 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c.", "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438. \u0427\u0442\u043e\u0431\u044b \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c, \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0443.", "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430", ["\u041f\u043e\u0442\u0440\u0430\u0447\u0435\u043d\u043e +s. \u0412\u044b \u0431\u044b\u0441\u0442\u0440\u0435\u0435 \u043c\u043e\u043b\u043d\u0438\u0438!", "\u041f\u043e\u0442\u0440\u0430\u0447\u0435\u043d\u043e +s. \u041e\u0442\u043b\u0438\u0447\u043d\u043e!", "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u0430"], "\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", "\u0417\u0430\u043a\u0440\u044b\u0442\u044c", "\u041e\u0442\u0437\u044b\u0432", "\u0421\u043b\u0438\u0448\u043a\u043e\u043c \u0447\u0430\u0441\u0442\u043e\u0435 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435. \u0414\u043b\u044f \u043f\u043e\u0432\u0442\u043e\u0440\u0430 \u043d\u0430\u0436\u043c\u0438\u0442\u0435.", "\u041f\u0435\u0440\u0435\u0434\u0432\u0438\u043d\u044c\u0442\u0435 \u0431\u0435\u0433\u0443\u043d\u043e\u043a \u0432\u043f\u0440\u0430\u0432\u043e, \u0447\u0442\u043e\u0431\u044b \u0441\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u0430\u0437\u0437\u043b", "\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435. \u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443.", "\u041f\u0435\u0440\u0435\u0434\u0432\u0438\u043d\u044c\u0442\u0435 \u0431\u0435\u0433\u0443\u043d\u043e\u043a \u0432 \u0441\u0430\u043c\u043e\u0435 \u043f\u0440\u0430\u0432\u043e\u0435 \u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435", "\u041f\u0435\u0440\u0435\u0434\u0432\u0438\u043d\u044c\u0442\u0435 \u0435\u0433\u043e \u0435\u0449\u0435 \u0440\u0430\u0437", "\u041f\u0435\u0440\u0435\u0434\u0432\u0438\u043d\u044c\u0442\u0435 \u0431\u0435\u0433\u0443\u043d\u043e\u043a \u0432 \u0441\u0430\u043c\u043e\u0435 \u043f\u0440\u0430\u0432\u043e\u0435 \u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435", "\u041f\u0435\u0440\u0435\u0434\u0432\u0438\u043d\u044c\u0442\u0435 \u0431\u0435\u0433\u0443\u043d\u043e\u043a \u043d\u0438\u0436\u0435, \u0447\u0442\u043e\u0431\u044b \u0441\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u0430\u0437\u0437\u043b", "\u041f\u043e\u043c\u0435\u0441\u0442\u0438\u0442\u0435 \u0434\u0435\u0442\u0430\u043b\u044c \u0442\u043e\u0447\u043d\u043e \u043d\u0430 \u0435\u0435 \u043c\u0435\u0441\u0442\u043e", "\u041f\u043e\u0445\u043e\u0436\u0435, \u0447\u0442\u043e \u044d\u0442\u0430 \u043d\u0435 \u0432\u0445\u043e\u0434\u0438\u0442. \u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0434\u0440\u0443\u0433\u0443\u044e.", ["\u042d\u0442\u0430 \u0434\u0435\u0442\u0430\u043b\u044c \u043f\u043e\u0442\u0435\u0440\u044f\u043b\u0430\u0441\u044c. \u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443.", "\u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443 \u0438 \u043f\u043e\u0434\u0431\u0435\u0440\u0438\u0442\u0435 \u0435\u0435 \u0442\u043e\u0447\u043d\u0435\u0435.", "\u041d\u0435\u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u0430\u044f \u0441\u0435\u0442\u044c. \u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443."], "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438. \u0427\u0442\u043e\u0431\u044b \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c, \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0443.", "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u0430", "\u0421\u043b\u0438\u0448\u043a\u043e\u043c \u0447\u0430\u0441\u0442\u043e\u0435 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435", "\u041d\u0435\u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u0430\u044f \u0441\u0435\u0442\u044c(+). \u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u0435 \u043f\u043e\u043f\u044b\u0442\u043a\u0443.", "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c"],
        es: ["Toca para verificar", "Verificaci\xf3n de seguridad", "Verificaci\xf3n correcta", "Comentarios", "Actualizar", "Verificar", "Toca para volver a cargar", "Tiempo agotado. Intenta de nuevo.", "Error de verificaci\xf3n. Intenta de nuevo.", "C\xf3digo de verificaci\xf3n", "Atr\xe1s", "Verificando...", "Red inestable. Toca Actualizar para reintentar.", "Error de carga. Toca la imagen para actualizar.", "Verificando", ["+s usados. \xa1Has vencido al rel\xe1mpago!", "+s usados. \xa1Perfecto!", "Verificaci\xf3n correcta"], "Actualizar", "Cerrar", "Comentarios", "Actualizaci\xf3n muy frecuente. Toca para reintentar.", "Arrastra el deslizador a la derecha para completar el puzzle", "Error de verificaci\xf3n. Intenta de nuevo.", "Arrastra el deslizador al espacio de la derecha", "Arrastra una vez m\xe1s", "Arrastra el deslizador al espacio de la derecha", "Arrastra el siguiente deslizador para completar el puzzle", "Coloca la pieza justo en el espacio", "Ese parece un poco dif\xedcil. Prueba con este.", ["La pieza se ha perdido. Intenta de nuevo.", "Intenta de nuevo y hazla encajar con m\xe1s precisi\xf3n", "Red inestable. Intenta de nuevo."], "Error de carga. Toca la imagen para actualizar.", "Verificaci\xf3n correcta", "Actualizaci\xf3n muy frecuente", "Red inestable(+). Intenta de nuevo."],
        th: ["\u0e41\u0e15\u0e30\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", "\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19\u0e04\u0e27\u0e32\u0e21\u0e1b\u0e25\u0e2d\u0e14\u0e20\u0e31\u0e22", "\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19\u0e2a\u0e33\u0e40\u0e23\u0e47\u0e08\u0e41\u0e25\u0e49\u0e27", "\u0e04\u0e33\u0e15\u0e34\u0e0a\u0e21", "\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a", "\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", "\u0e41\u0e15\u0e30\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e42\u0e2b\u0e25\u0e14\u0e0b\u0e49\u0e33", "\u0e2b\u0e21\u0e14\u0e40\u0e27\u0e25\u0e32 \u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07", "\u0e02\u0e49\u0e2d\u0e1c\u0e34\u0e14\u0e1e\u0e25\u0e32\u0e14\u0e43\u0e19\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19 \u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07", "\u0e23\u0e2b\u0e31\u0e2a\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", "\u0e01\u0e25\u0e31\u0e1a", "\u0e01\u0e33\u0e25\u0e31\u0e07\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19...", "\u0e40\u0e04\u0e23\u0e37\u0e2d\u0e02\u0e48\u0e32\u0e22\u0e44\u0e21\u0e48\u0e40\u0e2a\u0e16\u0e35\u0e22\u0e23 \u0e41\u0e15\u0e30\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07", "\u0e01\u0e32\u0e23\u0e42\u0e2b\u0e25\u0e14\u0e25\u0e49\u0e21\u0e40\u0e2b\u0e25\u0e27 \u0e41\u0e15\u0e30\u0e17\u0e35\u0e48\u0e23\u0e39\u0e1b\u0e20\u0e32\u0e1e\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a", "\u0e01\u0e33\u0e25\u0e31\u0e07\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", ["\u0e43\u0e0a\u0e49\u0e44\u0e1b\u0e41\u0e25\u0e49\u0e27 +s \u0e04\u0e38\u0e13\u0e0a\u0e19\u0e30\u0e41\u0e1f\u0e25\u0e0a!", "\u0e43\u0e0a\u0e49\u0e44\u0e1b\u0e41\u0e25\u0e49\u0e27 +s \u0e40\u0e1e\u0e2d\u0e23\u0e4c\u0e40\u0e1f\u0e04!", "\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19\u0e2a\u0e33\u0e40\u0e23\u0e47\u0e08\u0e41\u0e25\u0e49\u0e27"], "\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a", "\u0e1b\u0e34\u0e14", "\u0e04\u0e33\u0e15\u0e34\u0e0a\u0e21", "\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a\u0e1a\u0e48\u0e2d\u0e22\u0e40\u0e01\u0e34\u0e19\u0e44\u0e1b \u0e41\u0e15\u0e30\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e25\u0e2d\u0e07\u0e43\u0e2b\u0e21\u0e48", "\u0e25\u0e32\u0e01\u0e41\u0e16\u0e1a\u0e40\u0e25\u0e37\u0e48\u0e2d\u0e19\u0e44\u0e1b\u0e17\u0e32\u0e07\u0e02\u0e27\u0e32\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e15\u0e2d\u0e1a\u0e1b\u0e23\u0e34\u0e28\u0e19\u0e32\u0e43\u0e2b\u0e49\u0e40\u0e2a\u0e23\u0e47\u0e08\u0e2a\u0e34\u0e49\u0e19", "\u0e02\u0e49\u0e2d\u0e1c\u0e34\u0e14\u0e1e\u0e25\u0e32\u0e14\u0e43\u0e19\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19 \u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07", "\u0e25\u0e32\u0e01\u0e41\u0e16\u0e1a\u0e40\u0e25\u0e37\u0e48\u0e2d\u0e19\u0e44\u0e1b\u0e17\u0e35\u0e48\u0e0a\u0e48\u0e2d\u0e07\u0e14\u0e49\u0e32\u0e19\u0e02\u0e27\u0e32\u0e2a\u0e38\u0e14", "\u0e25\u0e32\u0e01\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07", "\u0e25\u0e32\u0e01\u0e41\u0e16\u0e1a\u0e40\u0e25\u0e37\u0e48\u0e2d\u0e19\u0e44\u0e1b\u0e17\u0e35\u0e48\u0e0a\u0e48\u0e2d\u0e07\u0e14\u0e49\u0e32\u0e19\u0e02\u0e27\u0e32\u0e2a\u0e38\u0e14", "\u0e25\u0e32\u0e01\u0e41\u0e16\u0e1a\u0e40\u0e25\u0e37\u0e48\u0e2d\u0e19\u0e14\u0e49\u0e32\u0e19\u0e25\u0e48\u0e32\u0e07\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e15\u0e2d\u0e1a\u0e1b\u0e23\u0e34\u0e28\u0e19\u0e32\u0e43\u0e2b\u0e49\u0e40\u0e2a\u0e23\u0e47\u0e08\u0e2a\u0e34\u0e49\u0e19", "\u0e27\u0e32\u0e07\u0e0a\u0e34\u0e49\u0e19\u0e2a\u0e48\u0e27\u0e19\u0e43\u0e19\u0e0a\u0e48\u0e2d\u0e07\u0e17\u0e35\u0e48\u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07", "\u0e2d\u0e31\u0e19\u0e19\u0e31\u0e49\u0e19\u0e14\u0e39\u0e40\u0e2b\u0e21\u0e37\u0e2d\u0e19\u0e08\u0e30\u0e22\u0e32\u0e01\u0e2b\u0e19\u0e48\u0e2d\u0e22 \u0e25\u0e2d\u0e07\u0e2d\u0e31\u0e19\u0e19\u0e35\u0e49", ["\u0e0a\u0e34\u0e49\u0e19\u0e2a\u0e48\u0e27\u0e19\u0e2b\u0e32\u0e22\u0e44\u0e1b \u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07", "\u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07\u0e41\u0e25\u0e30\u0e17\u0e33\u0e43\u0e2b\u0e49\u0e21\u0e31\u0e19\u0e1e\u0e2d\u0e14\u0e35\u0e22\u0e34\u0e48\u0e07\u0e02\u0e36\u0e49\u0e19", "\u0e40\u0e04\u0e23\u0e37\u0e2d\u0e02\u0e48\u0e32\u0e22\u0e44\u0e21\u0e48\u0e40\u0e2a\u0e16\u0e35\u0e22\u0e23 \u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07"], "\u0e01\u0e32\u0e23\u0e42\u0e2b\u0e25\u0e14\u0e25\u0e49\u0e21\u0e40\u0e2b\u0e25\u0e27 \u0e41\u0e15\u0e30\u0e17\u0e35\u0e48\u0e23\u0e39\u0e1b\u0e20\u0e32\u0e1e\u0e40\u0e1e\u0e37\u0e48\u0e2d\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a", "\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19\u0e2a\u0e33\u0e40\u0e23\u0e47\u0e08\u0e41\u0e25\u0e49\u0e27", "\u0e23\u0e35\u0e40\u0e1f\u0e23\u0e0a\u0e1a\u0e48\u0e2d\u0e22\u0e40\u0e01\u0e34\u0e19\u0e44\u0e1b", "\u0e40\u0e04\u0e23\u0e37\u0e2d\u0e02\u0e48\u0e32\u0e22\u0e44\u0e21\u0e48\u0e40\u0e2a\u0e16\u0e35\u0e22\u0e23(+) \u0e25\u0e2d\u0e07\u0e2d\u0e35\u0e01\u0e04\u0e23\u0e31\u0e49\u0e07"],
        tr: ["Do\u011frulamak i\xe7in dokun", "G\xfcvenlik Do\u011frulamas\u0131", "Do\u011frulama ba\u015far\u0131l\u0131", "Geri bildirim", "Yenile", "Do\u011frula", "Yeniden y\xfcklemek i\xe7in dokun", "Zaman a\u015f\u0131m\u0131. Tekrar dene.", "Do\u011frulama hatas\u0131. Tekrar dene.", "Do\u011frulama Kodu", "Geri", "Do\u011frulan\u0131yor", "\u0130stikrars\u0131z ba\u011flant\u0131. Denemek i\xe7in Yenile'ye dokun.", "Y\xfckleme ba\u015far\u0131s\u0131z. Yenilemek i\xe7in g\xf6rsele dokun.", "Do\u011frulan\u0131yor", ["+s harcand\u0131. Flash'i ge\xe7tin!", "+s harcand\u0131. M\xfckemmel!", "Do\u011frulama ba\u015far\u0131l\u0131"], "Yenile", "Kapat", "Geri bildirim", "Yenilemeler \xe7ok s\u0131k. Tekrar denemek i\xe7in dokun.", "Bulmacay\u0131 \xe7\xf6zmek i\xe7in kayd\u0131r\u0131c\u0131y\u0131 sa\u011fa s\xfcr\xfckle", "Do\u011frulama hatas\u0131. Tekrar dene.", "Kayd\u0131r\u0131c\u0131y\u0131 en sa\u011fdaki yuvaya kadar s\xfcr\xfckle", "Bir kez daha s\xfcr\xfckle", "Kayd\u0131r\u0131c\u0131y\u0131 en sa\u011fdaki yuvaya kadar s\xfcr\xfckle", "Bulmacay\u0131 tamamlamak i\xe7in alttaki kayd\u0131r\u0131c\u0131y\u0131 s\xfcr\xfckle", "Par\xe7ay\u0131 yuvaya tam olarak yerle\u015ftir", "Bu biraz zor g\xf6r\xfcn\xfcyor. \u015eunu dene.", ["Par\xe7a kayboldu. Tekrar dene.", "Tekrar dene ve daha iyi yerle\u015ftirmeye \xe7al\u0131\u015f", "\u0130stikrars\u0131z ba\u011flant\u0131. Tekrar dene."], "Y\xfckleme ba\u015far\u0131s\u0131z. Yenilemek i\xe7in g\xf6rsele dokun.", "Do\u011frulama ba\u015far\u0131l\u0131", "Yenilemeler \xe7ok s\u0131k", "\u0130stikrars\u0131z ba\u011flant\u0131(+). Tekrar dene."],
        vi: ["Nh\u1ea5n \u0111\u1ec3 x\xe1c minh", "X\xe1c minh b\u1ea3o m\u1eadt", "X\xe1c minh th\xe0nh c\xf4ng", "Ph\u1ea3n h\u1ed3i", "L\xe0m m\u1edbi", "X\xe1c minh", "Nh\u1ea5n \u0111\u1ec3 t\u1ea3i l\u1ea1i", "\u0110\xe3 h\u1ebft gi\u1edd. H\xe3y th\u1eed l\u1ea1i.", "C\xf3 l\u1ed7i x\xe1c minh. H\xe3y th\u1eed l\u1ea1i.", "M\xe3 x\xe1c minh", "Quay l\u1ea1i", "\u0110ang x\xe1c minh...", "M\u1ea1ng kh\xf4ng \u1ed5n \u0111\u1ecbnh. H\xe3y nh\u1ea5n L\xe0m m\u1edbi \u0111\u1ec3 th\u1eed l\u1ea1i.", "T\u1ea3i kh\xf4ng th\xe0nh c\xf4ng. H\xe3y nh\u1ea5n v\xe0o h\xecnh \u0111\u1ec3 l\xe0m m\u1edbi.", "\u0110ang x\xe1c minh", ["+s \u0111\xe3 s\u1eed d\u1ee5ng. B\u1ea1n \u0111\xe3 th\u1eafng The Flash!", "+s \u0111\xe3 s\u1eed d\u1ee5ng. Th\u1eadt ho\xe0n h\u1ea3o!", "X\xe1c minh th\xe0nh c\xf4ng"], "L\xe0m m\u1edbi", "\u0110\xf3ng", "Ph\u1ea3n h\u1ed3i", "L\xe0m m\u1edbi qu\xe1 th\u01b0\u1eddng xuy\xean. H\xe3y nh\u1ea5n \u0111\u1ec3 th\u1eed l\u1ea1i.", "K\xe9o thanh tr\u01b0\u1ee3t sang ph\u1ea3i \u0111\u1ec3 ho\xe0n t\u1ea5t c\xe2u \u0111\u1ed1", "C\xf3 l\u1ed7i x\xe1c minh. H\xe3y th\u1eed l\u1ea1i.", "K\xe9o thanh tr\u01b0\u1ee3t sang v\u1ecb tr\xed ngo\xe0i c\xf9ng b\xean ph\u1ea3i", "H\xe3y k\xe9o n\xf3 m\u1ed9t l\u1ea7n n\u1eefa", "K\xe9o thanh tr\u01b0\u1ee3t sang v\u1ecb tr\xed ngo\xe0i c\xf9ng b\xean ph\u1ea3i", "K\xe9o thanh tr\u01b0\u1ee3t b\xean d\u01b0\u1edbi \u0111\u1ec3 ho\xe0n t\u1ea5t c\xe2u \u0111\u1ed1", "\u0110\u1eb7t mi\u1ebfng gh\xe9p v\xe0o \u0111\xfang v\u1ecb tr\xed", "C\xe1i \u0111\xf3 c\xf3 v\u1ebb h\u01a1i kh\xf3. H\xe3y th\u1eed c\xe1i n\xe0y.", ["M\u1ea3nh gh\xe9p \u0111\xe3 b\u1ecb th\u1ea5t l\u1ea1c. H\xe3y th\u1eed l\u1ea1i.", "H\xe3y th\u1eed l\u1ea1i v\xe0 gh\xe9p n\xf3 v\xe0o ch\xednh x\xe1c h\u01a1n", "M\u1ea1ng kh\xf4ng \u1ed5n \u0111\u1ecbnh. H\xe3y th\u1eed l\u1ea1i."], "T\u1ea3i kh\xf4ng th\xe0nh c\xf4ng. H\xe3y nh\u1ea5n v\xe0o h\xecnh \u0111\u1ec3 l\xe0m m\u1edbi.", "X\xe1c minh th\xe0nh c\xf4ng", "L\xe0m m\u1edbi qu\xe1 th\u01b0\u1eddng xuy\xean", "M\u1ea1ng kh\xf4ng \u1ed5n \u0111\u1ecbnh(+). H\xe3y th\u1eed l\u1ea1i."]
      };
    a.zh = a["zh-cn"],
      a.iw = a.he,
      a["in"] = a.id;
    var o = {
      2052: "zh-cn",
      1028: "zh-hk",
      1033: "en"
    }
      , s = "zh";
    /MicroMessenger/.test(navigator.userAgent) && (s = "en");
    var c = navigator.languages && navigator.languages[0] ? navigator.languages[0] : navigator.language || navigator.userLanguage || ""
      , u = {
      rightToLeft: !1
    };
    u.total = a,
      u.langExist = function (e) {
        var t = e;
        return /-/.test(e) && (t = e.split("-")[0]),
          a[e] ? e : !!a[t] && t
      }
      ,
      u.init = function (e) {
        var t = (e || c || s).toLowerCase().replace(/_/, "-")
          , n = u.langExist(t);
        n || (n = "en"),
        "embed" == window.captchaConfig.showtype && ("en" === n && (n = "en-o"),
        "zh-hk" != n && "zh-tw" != n || (n = "zh-hk"));
        for (var r = a[n], o = 0; o < i.length; o++)
          u[i[o]] = r[o] || a[s][o];
        "embed" == window.captchaConfig.showtype && "zh-hk" == n && (u.c19 = "\u53cd\u994b"),
        "ar" !== n && "he" !== n && "iw" !== n || (u.rightToLeft = !0),
          u.currentLanguage = n
      }
      ,
      u.get = function (e) {
        var t = u[e];
        if (!t)
          for (var n = 0; n < i.length; n++)
            if (i[n] === e) {
              t = a.en[n];
              break
            }
        return t || ""
      }
      ,
      u.initWxLang = function (e) {
        try {
          var t = r("wxLang") || u.langExist(e)
            , n = r("lang");
          if (o[n])
            return void u.init(o[n]);
          t ? u.init(t) : (t = window.captchaConfig.lang,
            o[t] ? u.init(o[t]) : u.init())
        } catch (i) {
        }
      }
      ,
      e.exports = u
  }
  , , , , function (e, t, n) {
    "use strict";
    var r = n(25)["default"]
      , i = n(34)
      , a = n(23)["default"]
      , o = new r("securityCode")
      , s = 1;
    o.addTarget(window.parent, "parent"),
      o.listen(function (e) {
      });
    var c = function (e, t) {
      try {
        t && (e = {
          message: e
        }),
          o.targets.parent.send(JSON.stringify(e))
      } catch (n) {
      }
    }
      , u = {
      adjustStyle: function () {
        c({
          type: 7
        }, !0)
      },
      capClose: function () {
        c({
          type: 6
        }, !0)
      },
      loadMsg: function (e, t, n, r) {
        c({
          type: 10,
          loadstate: e,
          info: t || "",
          fwidth: n,
          fheight: r
        }, !0)
      },
      loadReady: function () {
        try {
          u.loadMsg(i.loadState.ready)
        } catch (e) {
        }
      },
      loadFailure: function (e) {
        u.loadMsg(i.loadState.fail, e)
      },
      loadChange: function (e, t) {
        u.loadMsg(i.loadState.mixing, null, e, t)
      },
      hybridVerify: function (e, t) {
        c({
          type: 8,
          sess: e,
          subsid: t
        }, !0)
      },
      sessionTimeout: function () {
        c({
          type: 12
        }, !0)
      },
      verifySuccess: function (e) {
        var t = e.ticket
          , n = e.randstr
          , r = e.errorCode
          , i = e.errorMessage
          , a = e.ret;
        c({
          type: 3,
          ticket: t,
          randstr: n,
          errorCode: r,
          errorMessage: i,
          ret: a
        }, !0)
      },
      frequencyLimit: function () {
        c({
          type: 11
        }, !0)
      },
      goBack: function () {
        c({
          type: 4
        }, !0)
      },
      otherBack: function () {
        c({
          type: 2,
          seq: s++
        })
      },
      goAged: function () {
        c({
          type: a.messageType.goAged
        }, !0)
      }
    };
    e.exports = u
  }
  , function (e, t, n) {
    "use strict";
    var r = (window.lib || {}).flexible || {}
      , i = /rem$/;
    e.exports = {
      dpr: r.dpr || 0,
      rem: r.rem || 0,
      px2rem: function (e) {
        return r.px2rem ? r.px2rem(e) : e
      },
      rem2px: function (e) {
        return r.rem2px ? r.rem2px(e) : e
      },
      px2remU: function (e) {
        return r.px2rem ? r.px2rem(e) + "rem" : e + "px"
      },
      rem2pxU: function (e) {
        return i.test(e) ? r.rem2px(parseFloat(e)) || 0 : parseFloat(e) || 0
      },
      refreshRem: r.refreshRem,
      listen: function (e, t) {
        r.resizeCb && r.resizeCb.splice(e, 0, t)
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    e.exports = {
      doc: $(document.body),
      captcha: $("#tcWrap"),
      body: $("#bodyWrap"),
      fullScreenHead: $("#tcWrapHeader"),
      operation: $("#tcOperation"),
      status: $("#tcStatus"),
      imgBg: $("#slideBg"),
      imgSlide: $("#slideBlock"),
      close: $("#captcha_close"),
      btnBack: $("#btnBack"),
      guideWrap: $("#guideWrap"),
      guideText: $("#guideText"),
      title: $("#pHeaderTitle,#fsHeaderTitle"),
      statusFail: $("#statusFail"),
      txtSuccess: $("#statusSuccess"),
      txtError: $("#statusError"),
      txtErrorNote: $("#tcaptcha_note"),
      txtBack: $("#txtBack"),
      feedback: $(".show-FB"),
      site007: $("#tcaptcha_site_click"),
      btnReload: $(".show-reload"),
      btnCoverReload: $("#coverReload"),
      btnSlide: $("#tcaptcha_drag_button"),
      btnThumb: $("#tcaptcha_drag_thumb"),
      btnIconfont: $("#t_iconfont"),
      iconError: $("#errorIcon"),
      iconGoback: $("#iconGoback"),
      embedStatus: $(".tcaptcha-embed"),
      embedLab: $("#e_lab"),
      aged: $(".aged-icon"),
      agedText: $("#agedText"),
      normalVerify: $(".normal-verify-icon")
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = this && this.__assign || function () {
        return (r = Object.assign || function (e) {
            for (var t, n = 1, r = arguments.length; n < r; n++)
              for (var i in t = arguments[n])
                Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i]);
            return e
          }
        ).apply(this, arguments)
      }
      , i = this && this.__values || function (e) {
        var t = "function" == typeof Symbol && Symbol.iterator
          , n = t && e[t]
          , r = 0;
        if (n)
          return n.call(e);
        if (e && "number" == typeof e.length)
          return {
            next: function () {
              return e && r >= e.length && (e = void 0),
                {
                  value: e && e[r++],
                  done: !e
                }
            }
          };
        throw new TypeError(t ? "Object is not iterable." : "Symbol.iterator is not defined.")
      }
      , a = this && this.__importDefault || function (e) {
        return e && e.__esModule ? e : {
          "default": e
        }
      }
    ;
    t.__esModule = !0;
    var o = a(n(43))
      , s = a(n(45))
      , c = n(46)
      , u = function () {
      function e() {
        this.useWebWorker = !1,
          this.workerReady = !1,
          this.taskQueue = [],
          this.taskId = 0,
          this.callbacks = [];
        try {
          this.worker = new o["default"],
            this.useWebWorker = this.worker && !window.setImmediate,
            this.bindListener()
        } catch (e) {
        }
      }

      return e.prototype.bindListener = function () {
        var e = this;
        this.useWebWorker && (this.worker.onmessage = function (t) {
            var n, r, a, o, c = t.data, u = c.type, l = c.data;
            switch (u) {
              case s["default"].WORKER_READY:
                e.workerReady = !0;
                try {
                  for (var d = i(e.taskQueue), f = d.next(); !f.done; f = d.next()) {
                    var p = f.value;
                    e.run(p.data, p.cb),
                      window.clearTimeout(p.timeout)
                  }
                } catch (v) {
                  n = {
                    error: v
                  }
                } finally {
                  try {
                    f && !f.done && (r = d["return"]) && r.call(d)
                  } finally {
                    if (n)
                      throw n.error
                  }
                }
                e.taskQueue = [];
                break;
              case s["default"].TASK_RESULT:
                try {
                  for (var h = i(e.callbacks), g = h.next(); !g.done; g = h.next()) {
                    var m = g.value;
                    m.taskId === l.taskId && m.cb(l)
                  }
                } catch (y) {
                  a = {
                    error: y
                  }
                } finally {
                  try {
                    g && !g.done && (o = h["return"]) && o.call(h)
                  } finally {
                    if (a)
                      throw a.error
                  }
                }
            }
          }
        )
      }
        ,
        e.prototype.run = function (e, t, n) {
          var i = this;
          if (this.useWebWorker) {
            if (this.taskId += 1,
              !this.workerReady) {
              var a = window.setTimeout(function () {
                for (var e = 0; e < i.taskQueue.length; e++) {
                  var t = i.taskQueue[e];
                  if (a === t.timeout) {
                    i.taskQueue.splice(e, 1),
                      t.cb(c.getWorkloadResult(t.data, n));
                    break
                  }
                }
              }, 500);
              return void this.taskQueue.push({
                data: e,
                cb: t,
                timeout: a
              })
            }
            return this.sendToWorker(s["default"].RUN_TASK, r(r({}, e), {
              taskId: this.taskId
            })),
              void this.callbacks.push({
                taskId: this.taskId,
                cb: t
              })
          }
          window.setTimeout(function () {
            t(c.getWorkloadResult(e, n))
          }, 20)
        }
        ,
        e.prototype.sendToWorker = function (e, t) {
          var n;
          this.useWebWorker && (null === (n = this.worker) || void 0 === n || n.postMessage({
            type: e,
            data: t
          }))
        }
        ,
        e.prototype.terminate = function () {
          var e;
          this.useWebWorker && (null === (e = this.worker) || void 0 === e || e.terminate())
        }
        ,
        e
    }();
    t["default"] = u
  }
  , function (e, t, n) {
    var r = n(44);
    e.exports = function () {
      return r('!function(t){var n={};function e(r){if(n[r])return n[r].exports;var o=n[r]={i:r,l:!1,exports:{}};return t[r].call(o.exports,o,o.exports,e),o.l=!0,o.exports}e.m=t,e.c=n,e.d=function(t,n,r){e.o(t,n)||Object.defineProperty(t,n,{enumerable:!0,get:r})},e.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},e.t=function(t,n){if(1&n&&(t=e(t)),8&n)return t;if(4&n&&"object"==typeof t&&t&&t.__esModule)return t;var r=Object.create(null);if(e.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:t}),2&n&&"string"!=typeof t)for(var o in t)e.d(r,o,function(n){return t[n]}.bind(null,o));return r},e.n=function(t){var n=t&&t.__esModule?function(){return t["default"]}:function(){return t};return e.d(n,"a",n),n},e.o=function(t,n){return Object.prototype.hasOwnProperty.call(t,n)},e.p="",e(e.s=0)}([function(t,n,e){"use strict";var r=this&&this.__assign||function(){return(r=Object.assign||function(t){for(var n,e=1,r=arguments.length;e<r;e++)for(var o in n=arguments[e])Object.prototype.hasOwnProperty.call(n,o)&&(t[o]=n[o]);return t}).apply(this,arguments)},o=this&&this.__rest||function(t,n){var e={};for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&n.indexOf(r)<0&&(e[r]=t[r]);if(null!=t&&"function"==typeof Object.getOwnPropertySymbols){var o=0;for(r=Object.getOwnPropertySymbols(t);o<r.length;o++)n.indexOf(r[o])<0&&Object.prototype.propertyIsEnumerable.call(t,r[o])&&(e[r[o]]=t[r[o]])}return e},u=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{"default":t}};n.__esModule=!0;var f=e(1),a=u(e(2)),i=self;function c(t,n){i.postMessage({type:t,data:n})}c(a["default"].WORKER_READY),i.onmessage=function(t){var n=t.data;if(n.type===a["default"].RUN_TASK){var e=n.data,u=e.taskId,i=o(e,["taskId"]);c(a["default"].TASK_RESULT,r(r({},f.getWorkloadResult(i)),{taskId:u}))}},n["default"]=function(){}},function(t,n,e){"use strict";function r(t,n){var e=(65535&t)+(65535&n);return(t>>16)+(n>>16)+(e>>16)<<16|65535&e}function o(t,n,e,o,u,f){return r(function(t,n){return t<<n|t>>>32-n}(r(r(n,t),r(o,f)),u),e)}function u(t,n,e,r,u,f,a){return o(n&e|~n&r,t,n,u,f,a)}function f(t,n,e,r,u,f,a){return o(n&r|e&~r,t,n,u,f,a)}function a(t,n,e,r,u,f,a){return o(n^e^r,t,n,u,f,a)}function i(t,n,e,r,u,f,a){return o(e^(n|~r),t,n,u,f,a)}function c(t,n){var e,o,c,l,s;t[n>>5]|=128<<n%32,t[14+(n+64>>>9<<4)]=n;var d=1732584193,p=-271733879,g=-1732584194,_=271733878;for(e=0;e<t.length;e+=16)o=d,c=p,l=g,s=_,p=i(p=i(p=i(p=i(p=a(p=a(p=a(p=a(p=f(p=f(p=f(p=f(p=u(p=u(p=u(p=u(p,g=u(g,_=u(_,d=u(d,p,g,_,t[e],7,-680876936),p,g,t[e+1],12,-389564586),d,p,t[e+2],17,606105819),_,d,t[e+3],22,-1044525330),g=u(g,_=u(_,d=u(d,p,g,_,t[e+4],7,-176418897),p,g,t[e+5],12,1200080426),d,p,t[e+6],17,-1473231341),_,d,t[e+7],22,-45705983),g=u(g,_=u(_,d=u(d,p,g,_,t[e+8],7,1770035416),p,g,t[e+9],12,-1958414417),d,p,t[e+10],17,-42063),_,d,t[e+11],22,-1990404162),g=u(g,_=u(_,d=u(d,p,g,_,t[e+12],7,1804603682),p,g,t[e+13],12,-40341101),d,p,t[e+14],17,-1502002290),_,d,t[e+15],22,1236535329),g=f(g,_=f(_,d=f(d,p,g,_,t[e+1],5,-165796510),p,g,t[e+6],9,-1069501632),d,p,t[e+11],14,643717713),_,d,t[e],20,-373897302),g=f(g,_=f(_,d=f(d,p,g,_,t[e+5],5,-701558691),p,g,t[e+10],9,38016083),d,p,t[e+15],14,-660478335),_,d,t[e+4],20,-405537848),g=f(g,_=f(_,d=f(d,p,g,_,t[e+9],5,568446438),p,g,t[e+14],9,-1019803690),d,p,t[e+3],14,-187363961),_,d,t[e+8],20,1163531501),g=f(g,_=f(_,d=f(d,p,g,_,t[e+13],5,-1444681467),p,g,t[e+2],9,-51403784),d,p,t[e+7],14,1735328473),_,d,t[e+12],20,-1926607734),g=a(g,_=a(_,d=a(d,p,g,_,t[e+5],4,-378558),p,g,t[e+8],11,-2022574463),d,p,t[e+11],16,1839030562),_,d,t[e+14],23,-35309556),g=a(g,_=a(_,d=a(d,p,g,_,t[e+1],4,-1530992060),p,g,t[e+4],11,1272893353),d,p,t[e+7],16,-155497632),_,d,t[e+10],23,-1094730640),g=a(g,_=a(_,d=a(d,p,g,_,t[e+13],4,681279174),p,g,t[e],11,-358537222),d,p,t[e+3],16,-722521979),_,d,t[e+6],23,76029189),g=a(g,_=a(_,d=a(d,p,g,_,t[e+9],4,-640364487),p,g,t[e+12],11,-421815835),d,p,t[e+15],16,530742520),_,d,t[e+2],23,-995338651),g=i(g,_=i(_,d=i(d,p,g,_,t[e],6,-198630844),p,g,t[e+7],10,1126891415),d,p,t[e+14],15,-1416354905),_,d,t[e+5],21,-57434055),g=i(g,_=i(_,d=i(d,p,g,_,t[e+12],6,1700485571),p,g,t[e+3],10,-1894986606),d,p,t[e+10],15,-1051523),_,d,t[e+1],21,-2054922799),g=i(g,_=i(_,d=i(d,p,g,_,t[e+8],6,1873313359),p,g,t[e+15],10,-30611744),d,p,t[e+6],15,-1560198380),_,d,t[e+13],21,1309151649),g=i(g,_=i(_,d=i(d,p,g,_,t[e+4],6,-145523070),p,g,t[e+11],10,-1120210379),d,p,t[e+2],15,718787259),_,d,t[e+9],21,-343485551),d=r(d,o),p=r(p,c),g=r(g,l),_=r(_,s);return[d,p,g,_]}function l(t){var n,e="";for(n=0;n<32*t.length;n+=8)e+=String.fromCharCode(t[n>>5]>>>n%32&255);return e}function s(t){var n,e=[];for(e[(t.length>>2)-1]=void 0,n=0;n<e.length;n+=1)e[n]=0;for(n=0;n<8*t.length;n+=8)e[n>>5]|=(255&t.charCodeAt(n/8))<<n%32;return e}function d(t){var n,e,r="0123456789abcdef",o="";for(e=0;e<t.length;e+=1)n=t.charCodeAt(e),o+=r.charAt(n>>>4&15)+r.charAt(15&n);return o}function p(t){return unescape(encodeURIComponent(t))}function g(t){return function(t){return l(c(s(t),8*t.length))}(p(t))}function _(t,n){return function(t,n){var e,r,o=s(t),u=[],f=[];for(u[15]=f[15]=void 0,o.length>16&&(o=c(o,8*t.length)),e=0;e<16;e+=1)u[e]=909522486^o[e],f[e]=1549556828^o[e];return r=c(u.concat(s(n)),512+8*n.length),l(c(f.concat(r),640))}(p(t),p(n))}function v(t,n,e){return n?e?_(n,t):function(t,n){return d(_(t,n))}(n,t):e?g(t):function(t){return d(g(t))}(t)}n.__esModule=!0,n.getWorkloadResult=n.md5=void 0,n.md5=v,n.getWorkloadResult=function(t,n){for(var e=t.nonce,r=t.target,o=+new Date,u=0,f="number"==typeof n?n:3e4;v(""+e+u)!==r&&(u+=1,!(+new Date-o>f)););return{ans:u,duration:+new Date-o}}},function(t,n,e){"use strict";n.__esModule=!0;n["default"]={WORKER_READY:"WORKER_READY",RUN_TASK:"RUN_TASK",TASK_RESULT:"TASK_RESULT"}}]);', "Worker", undefined, undefined)
    }
  }
  , function (e, t, n) {
    "use strict";
    e.exports = function (e, t, n, r) {
      var i = self || window;
      try {
        try {
          var a;
          try {
            a = new i.Blob([e])
          } catch (u) {
            (a = new (i.BlobBuilder || i.WebKitBlobBuilder || i.MozBlobBuilder || i.MSBlobBuilder)).append(e),
              a = a.getBlob()
          }
          var o = i.URL || i.webkitURL
            , s = o.createObjectURL(a)
            , c = new i[t](s, n);
          return o.revokeObjectURL(s),
            c
        } catch (u) {
          return new i[t]("data:application/javascript,".concat(encodeURIComponent(e)), n)
        }
      } catch (u) {
        if (!r)
          throw Error("Inline worker is not supported");
        return new i[t](r, n)
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    t.__esModule = !0;
    t["default"] = {
      WORKER_READY: "WORKER_READY",
      RUN_TASK: "RUN_TASK",
      TASK_RESULT: "TASK_RESULT"
    }
  }
  , function (e, t, n) {
    "use strict";

    function r(e, t) {
      var n = (65535 & e) + (65535 & t);
      return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
    }

    function i(e, t, n, i, a, o) {
      return r(function (e, t) {
        return e << t | e >>> 32 - t
      }(r(r(t, e), r(i, o)), a), n)
    }

    function a(e, t, n, r, a, o, s) {
      return i(t & n | ~t & r, e, t, a, o, s)
    }

    function o(e, t, n, r, a, o, s) {
      return i(t & r | n & ~r, e, t, a, o, s)
    }

    function s(e, t, n, r, a, o, s) {
      return i(t ^ n ^ r, e, t, a, o, s)
    }

    function c(e, t, n, r, a, o, s) {
      return i(n ^ (t | ~r), e, t, a, o, s)
    }

    function u(e, t) {
      var n, i, u, l, d;
      e[t >> 5] |= 128 << t % 32,
        e[14 + (t + 64 >>> 9 << 4)] = t;
      var f = 1732584193
        , p = -271733879
        , h = -1732584194
        , g = 271733878;
      for (n = 0; n < e.length; n += 16)
        i = f,
          u = p,
          l = h,
          d = g,
          p = c(p = c(p = c(p = c(p = s(p = s(p = s(p = s(p = o(p = o(p = o(p = o(p = a(p = a(p = a(p = a(p, h = a(h, g = a(g, f = a(f, p, h, g, e[n], 7, -680876936), p, h, e[n + 1], 12, -389564586), f, p, e[n + 2], 17, 606105819), g, f, e[n + 3], 22, -1044525330), h = a(h, g = a(g, f = a(f, p, h, g, e[n + 4], 7, -176418897), p, h, e[n + 5], 12, 1200080426), f, p, e[n + 6], 17, -1473231341), g, f, e[n + 7], 22, -45705983), h = a(h, g = a(g, f = a(f, p, h, g, e[n + 8], 7, 1770035416), p, h, e[n + 9], 12, -1958414417), f, p, e[n + 10], 17, -42063), g, f, e[n + 11], 22, -1990404162), h = a(h, g = a(g, f = a(f, p, h, g, e[n + 12], 7, 1804603682), p, h, e[n + 13], 12, -40341101), f, p, e[n + 14], 17, -1502002290), g, f, e[n + 15], 22, 1236535329), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 1], 5, -165796510), p, h, e[n + 6], 9, -1069501632), f, p, e[n + 11], 14, 643717713), g, f, e[n], 20, -373897302), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 5], 5, -701558691), p, h, e[n + 10], 9, 38016083), f, p, e[n + 15], 14, -660478335), g, f, e[n + 4], 20, -405537848), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 9], 5, 568446438), p, h, e[n + 14], 9, -1019803690), f, p, e[n + 3], 14, -187363961), g, f, e[n + 8], 20, 1163531501), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 13], 5, -1444681467), p, h, e[n + 2], 9, -51403784), f, p, e[n + 7], 14, 1735328473), g, f, e[n + 12], 20, -1926607734), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 5], 4, -378558), p, h, e[n + 8], 11, -2022574463), f, p, e[n + 11], 16, 1839030562), g, f, e[n + 14], 23, -35309556), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 1], 4, -1530992060), p, h, e[n + 4], 11, 1272893353), f, p, e[n + 7], 16, -155497632), g, f, e[n + 10], 23, -1094730640), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 13], 4, 681279174), p, h, e[n], 11, -358537222), f, p, e[n + 3], 16, -722521979), g, f, e[n + 6], 23, 76029189), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 9], 4, -640364487), p, h, e[n + 12], 11, -421815835), f, p, e[n + 15], 16, 530742520), g, f, e[n + 2], 23, -995338651), h = c(h, g = c(g, f = c(f, p, h, g, e[n], 6, -198630844), p, h, e[n + 7], 10, 1126891415), f, p, e[n + 14], 15, -1416354905), g, f, e[n + 5], 21, -57434055), h = c(h, g = c(g, f = c(f, p, h, g, e[n + 12], 6, 1700485571), p, h, e[n + 3], 10, -1894986606), f, p, e[n + 10], 15, -1051523), g, f, e[n + 1], 21, -2054922799), h = c(h, g = c(g, f = c(f, p, h, g, e[n + 8], 6, 1873313359), p, h, e[n + 15], 10, -30611744), f, p, e[n + 6], 15, -1560198380), g, f, e[n + 13], 21, 1309151649), h = c(h, g = c(g, f = c(f, p, h, g, e[n + 4], 6, -145523070), p, h, e[n + 11], 10, -1120210379), f, p, e[n + 2], 15, 718787259), g, f, e[n + 9], 21, -343485551),
          f = r(f, i),
          p = r(p, u),
          h = r(h, l),
          g = r(g, d);
      return [f, p, h, g]
    }

    function l(e) {
      var t, n = "";
      for (t = 0; t < 32 * e.length; t += 8)
        n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
      return n
    }

    function d(e) {
      var t, n = [];
      for (n[(e.length >> 2) - 1] = void 0,
             t = 0; t < n.length; t += 1)
        n[t] = 0;
      for (t = 0; t < 8 * e.length; t += 8)
        n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
      return n
    }

    function f(e) {
      var t, n, r = "0123456789abcdef", i = "";
      for (n = 0; n < e.length; n += 1)
        t = e.charCodeAt(n),
          i += r.charAt(t >>> 4 & 15) + r.charAt(15 & t);
      return i
    }

    function p(e) {
      return unescape(encodeURIComponent(e))
    }

    function h(e) {
      return function (e) {
        return l(u(d(e), 8 * e.length))
      }(p(e))
    }

    function g(e, t) {
      return function (e, t) {
        var n, r, i = d(e), a = [], o = [];
        for (a[15] = o[15] = void 0,
             i.length > 16 && (i = u(i, 8 * e.length)),
               n = 0; n < 16; n += 1)
          a[n] = 909522486 ^ i[n],
            o[n] = 1549556828 ^ i[n];
        return r = u(a.concat(d(t)), 512 + 8 * t.length),
          l(u(o.concat(r), 640))
      }(p(e), p(t))
    }

    function m(e, t, n) {
      return t ? n ? g(t, e) : function (e, t) {
        return f(g(e, t))
      }(t, e) : n ? h(e) : function (e) {
        return f(h(e))
      }(e)
    }

    t.__esModule = !0,
      t.getWorkloadResult = t.md5 = void 0,
      t.md5 = m,
      t.getWorkloadResult = function (e, t) {
        for (var n = e.nonce, r = e.target, i = +new Date, a = 0, o = "number" == typeof t ? t : 3e4; m("" + n + a) !== r && (a += 1,
          !(+new Date - i > o));)
          ;
        return {
          ans: a,
          duration: +new Date - i
        }
      }
  }
  , , , , , function (e, t, n) {
    "use strict";

    function r(e) {
      return document.createElement(e)
    }

    function i() {
      return "history" in window && "pushState" in history
    }

    !function () {
      var e = 0
    }();
    var a, o, s = (a = [],
      o = [],
      {
        add: function (e) {
          Array.prototype.push.apply(a, e)
        },
        get: function () {
          for (var e = 0; e < a.length; e++)
            o[e] = a[e]();
          return o
        }
      });
    s.add([function () {
      return "matches" in r("div")
    }
      , function () {
        return "msMatchesSelector" in r("div")
      }
      , function () {
        return "webkitMatchesSelector" in r("div")
      }
      , function () {
        return !!(window.matchMedia && window.matchMedia("(min-width: 400px)") && window.matchMedia("(min-width: 400px)").matches)
      }
      , function () {
        return !!(window.CSS && CSS.supports && CSS.supports("display", "block"))
      }
      , function () {
        return !!document.createRange
      }
      , function () {
        return !!window.CustomEvent
      }
      , function () {
        return "scrollIntoView" in r("div")
      }
      , function () {
        return "getUserMedia" in window.navigator
      }
      , function () {
        return !!window.IntersectionObserver
      }
      , function () {
        return "ontouchstart" in r("div")
      }
      , function () {
        return "performance" in window
      }
      , function () {
        return !(!window.performance || !performance.timing)
      }
      , function () {
        return "MediaSource" in window
      }
      , function () {
        return "onpageshow" in window
      }
      , function () {
        return "onhashchange" in window
      }
      , function () {
        return !(!window.requestFileSystem && !window.webkitRequestFileSystem)
      }
      , function () {
        return !!window.screen.orientation
      }
      , function () {
        return "WebSocket" in window
      }
      , function () {
        return !1
      }
      , function () {
        return "FileReader" in window
      }
      , function () {
        return !!window.atob
      }
      , function () {
        return !(!window.JSON || !JSON.parse)
      }
      , function () {
        return "postMessage" in window
      }
      , function () {
        return "EventSource" in window
      }
      , function () {
        return "vibrate" in navigator
      }
      , function () {
        return "Promise" in window
      }
      , function () {
        return "setImmediate" in window
      }
      , function () {
        return "isInfinite" in Number
      }
      , function () {
        return "indexedDB" in window
      }
      , function () {
        return "Proxy" in window
      }
      , function () {
        return "serviceWorker" in navigator
      }
      , function () {
        return "postMessage" in window
      }
      , function () {
        return "Crypto" in window
      }
      , function () {
        return "openDatabase" in window
      }
      , function () {
        return "Notification" in window
      }
      , function () {
        return "currentScript" in document
      }
      , function () {
        var e = !1;
        return "number" == typeof window.screenX && ["webkit", "moz", "ms", "o", ""].forEach(function (t) {
          0 == e && "" + document[t + (t ? "H" : "h") + "idden"] != "undefined" && (e = !0)
        }),
          e
      }
      , function () {
        var e = !1;
        try {
          e = "localStorage" in g && "setItem" in localStorage
        } catch (t) {
        }
        return e
      }
      , function () {
        var e = !1;
        try {
          e = "sessionStorage" in g && "setItem" in sessionStorage
        } catch (t) {
        }
        return e
      }
      , function () {
        return "console" in window
      }
      , function () {
        return "requestAnimationFrame" in window
      }
      , function () {
        return "geolocation" in window.navigator
      }
      , function () {
        return "webkitSpeechRecognition" in window
      }
      , i, function () {
        return "TextEncoder" in window
      }
      , i, i, function () {
        var e = !1
          , t = "https://sv.aq.qq.com/";
        try {
          new URL("/", t).href == t && (e = !0)
        } catch (n) {
        }
        return e
      }
      , function () {
        try {
          "a".localeCompare("b", "i")
        } catch (e) {
          return "RangeError" === e.name
        }
        return !1
      }
    ]);
    for (var c = new function () {
      var e = [];
      this.set = function (t) {
        e[t] = !0
      }
        ,
        this.encode = function () {
          for (var t = [], n = 0; n < e.length; n++)
            e[n] && (t[Math.floor(n / 6)] ^= 1 << n % 6);
          for (n = 0; n < t.length; n++)
            t[n] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_".charAt(t[n] || 0);
          return t.join("")
        }
    }
           , u = s.get(), l = 0; l < u.length; l++)
      u[l] && c.set(l + 1);
    var d = c.encode();
    e.exports = function () {
      return d
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = window.timing;
    console.log('**********', n(68))
    r.log("jsInit"),
      n(105);
    var i = n(35)
      , a = n(22);
    i.initWxLang(a.queryParam("userLanguage"));
    var o = n(65)
      , s = n(39)
      , c = n(66)
      , u = n(34)
      , l = n(68)
      , d = n(72)
      , f = n(0).addUrlParam
      , p = n(40)
      , h = n(7)
      , g = n(55)
      , m = n(54)
      , v = n(32)
      , y = n(41)
      , w = n(22).updateSession
      , b = n(42)["default"]
      , k = n(5).getErrorRes
      , E = n(1)
      , _ = n(3).isTouchEventSupported
      , T = window.captchaConfig
      , S = l.tdc
      , R = S.setData
      , x = S.getData
      , C = S.getEks
      , z = void 0
      , O = 0
      , A = 0
      , P = {
      target: T.powCfg && T.powCfg.md5,
      nonce: T.powCfg && T.powCfg.prefix
    }
      , j = P.target && P.nonce
      , L = void 0
      , M = {
      ans: null,
      duration: 0
    };
    var I = function () {
      var e = T.color || "";
      if (!(e.indexOf("007aff") >= 0)) {
        var t = a.parse2rgb(e);
        t && (y.txtBack.css("color", t.s),
          y.btnThumb.css({
            "background-color": t.s,
            "box-shadow": "0 0 10px  1px rgba(" + parseInt(t.r) + "," + parseInt(t.g) + "," + parseInt(t.b) + ", .52)"
          }),
          y.btnIconfont.css({
            color: t.s
          }),
          y.txtError.css("color", t.s),
          $("line", y.iconError).css("stroke", t.s),
          $("line", y.iconGoback).css("stroke", t.s))
      }
    };

    function D(e, t) {
      e.on("mouseenter", function () {
        var n = document.createElement("div");
        $(n).text(t).addClass("hover-tip").appendTo($("body")),
          e.on("mousemove", function (e) {
            $(n).css({
              left: e.clientX - 10 + "px",
              top: e.clientY + 20 + "px"
            })
          }),
          e.on("mouseleave", function () {
            $(n).remove()
          })
      })
    }

    function N() {
      y.captcha.removeClass("loading"),
        y.guideText.text("ABCopq");
      var e = y.guideWrap.height();
      "popup" !== T.showtype ? (e -= 5,
        y.txtBack.html(i.c11),
      "function" != typeof window.open && $("#e_showFB").hide()) : s.adjustStyle(),
      _() || (D($("#e_showFB"), i.c19),
        D($("#e_reload"), i.c17),
        D($(".tcaptcha-embed .aged-icon"), i.aged)),
        function () {
          try {
            y.close.attr("aria-label", i.c18).attr("role", "button"),
              y.btnReload.attr("aria-label", i.c17).attr("role", "button"),
              y.btnBack.attr("aria-label", i.c11).attr("role", "button"),
              y.feedback.attr("aria-label", i.c19).attr("role", "button"),
              y.aged.attr("role", "button").attr("aria-label", i.aged).attr("aria-atomic", "true"),
              y.btnThumb.children("img").attr("alt", i.puzzle7),
              y.imgSlide.attr("alt", i.puzzle7),
              y.imgBg.attr("aria-hidden", "true")
          } catch (e) {
          }
        }(),
      "0" === a.queryParam("fb") && (y.status.addClass("hide-feedback"),
        $("#e_showFB").hide()),
      "1" === a.queryParam("enableAged") && "0" === a.queryParam("aged") && (y.aged.addClass("show"),
        y.agedText.text(i.get("aged"))),
        y.title.html(i.c2),
        y.guideText.html(i.puzzle6),
        y.statusFail.html(i.puzzle10),
      i.rightToLeft && y.guideText.addClass("right-to-left"),
      u.companyInfo && (y.status.addClass("show-company-note"),
        y.embedStatus.addClass("show-embed-lab")),
      y.guideText.height() > e && (y.guideText.addClass("middle-fontsize"),
      y.guideText.height() > e && y.guideText.addClass("small-fontsize"),
      y.guideText.height() > e && y.guideText.addClass("multi-line")),
        y.iconError.attr({
          width: 37 * p.dpr,
          height: 25 * p.dpr
        }),
        y.iconGoback.attr({
          width: 10 * p.dpr,
          height: 20 * p.dpr
        }),
        l.tdc.setData({
          clientType: T.clientype
        }),
        z = o(y.operation, [y.imgSlide, y.btnSlide], function () {
          g.clearErrorNote()
        }, function (e, t, n) {
          z.movable(!1);
          var i = y.imgSlide.offset()
            , o = y.imgBg.offset()
            , c = [{
            left: Math.floor((i.left - y.operation.offset().left) / T.rate),
            top: Math.floor(parseInt(T.spt, 10))
          }];
          l.tdc.setData({
            coordinate: [Math.ceil(o.left), Math.ceil(o.top), Number(T.rate.toFixed(4))]
          }),
            function (e, t, n) {
              var i = ""
                , o = void 0
                , c = 0;

              function u() {
                3 === c && function (e, t, n, i, o) {
                  for (var c = "", u = 0; u < e.length; u++)
                    c += Math.floor(e[u].left) + "," + Math.floor(e[u].top) + ";";
                  var d = a.queryMap();
                  r.log("verify"),
                    function (e, t) {
                      var n = l.challenge();
                      t.push([0, 0, n]),
                        e.cdata = n
                    }(d, n),
                    f = {
                      trycnt: ++A,
                      refreshcnt: O,
                      slideValue: n,
                      dragobj: t
                    },
                    R(f),
                    d.ans = c,
                    d.vsig = T.vsig,
                    d.websig = T.websig,
                    d.subcapclass = T.subcapclass,
                    d.pow_answer = null !== M.ans && "undefined" != typeof M.ans ? P.nonce + M.ans : M.ans,
                    d.pow_calc_time = M.duration,
                    function (e) {
                      e[T.collectdata] = decodeURIComponent(x()),
                        e.tlg = e[T.collectdata].length
                    }(d),
                  "inner" !== T.curenv && (d.asig = T.asig,
                    d.buid = T.buid);
                  var f;
                  d.fpinfo = i,
                    d.eks = C(),
                  T.nonce && (d.nonce = T.nonce);
                  $.extend(d, o),
                  l.tdc.checkTdcSuccess() || l.tdc.retryLoad(v);
                  !function (e) {
                    if (a.isLowIE()) {
                      var t = Object(e)
                        , n = [];
                      for (var i in t)
                        t.hasOwnProperty(i) && n.push(i + "=" + t[i]);
                      var o = window.getVData && window.getVData(n.join("&"));
                      o && (e.vData = o)
                    }
                    var c = $.ajax({
                      type: "POST",
                      url: "/cap_union_new_verify",
                      data: e,
                      timeout: 15e3,
                      dataType: "json",
                      success: function (e) {
                        if (e) {
                          Y = 0,
                          e.sess && w(e.sess);
                          var t = parseInt(e.errorCode, 10);
                          switch (t) {
                            case 0:
                              m.push(48, r.logEnd("verifyDuration")),
                                g.showSuccess(z.dragDuration, function () {
                                  s.verifySuccess({
                                    ticket: e.ticket,
                                    randstr: e.randstr
                                  })
                                });
                              break;
                            case 9:
                              g.showErrorNote("puzzle8", 3e3, T.showtype),
                                g.shake(W);
                              break;
                            case 12:
                              g.showCoverError("puzzle9", null, W, a.queryParam("sid"));
                              break;
                            case 16:
                            case 20:
                            case 21:
                              s.sessionTimeout();
                              break;
                            case 50:
                              g.showErrorNote("puzzle7", 3e3, T.showtype),
                                g.shake(function () {
                                  z.moveBack(!0)
                                });
                              break;
                            case 30:
                            case 51:
                              s.hybridVerify(e.sess, h.get());
                              break;
                            default:
                              g.showCoverError("c23", e.errorCode, W, a.queryParam("sid"))
                          }
                          m.push(27, r.logEnd("verify")),
                            m.send()
                        } else
                          W()
                      },
                      error: function (e, t, n) {
                        F = !1;
                        var i = "";
                        i += e && e.status ? e.status + ";" : "",
                          i += t ? t + ":" : "",
                          i += n || "",
                          v.send(v.type.ERROR_TYPE_AJAX_VERIFY, i),
                          c.abort(),
                          g.showErrorNote("c8", 3e3, T.showtype),
                        "timeout" === t || "abort" === t || "error" === t && (m.push(27, r.logEnd("verify")),
                          m.send()),
                        function () {
                          if ((Y += 1) < 3)
                            return !1;
                          return s.verifySuccess(k("VERIFY_ERROR", E.getQueryParam("aid"), E.getQueryParam("sid"))),
                            !0
                        }() || W()
                      }
                    })
                  }(d)
                }(e, t, n, i, o)
              }

              if (j && null === M.ans) {
                if (L.useWebWorker && !window.setImmediate)
                  return void q(function () {
                    c |= 1,
                    M.ans || (M.ans = ""),
                      u()
                  });
                var d = !1;
                setTimeout(function () {
                  d || (d = !0,
                    c |= 1,
                    M.ans = "",
                    u())
                }, 3e3),
                  L.run(P, function (e) {
                    M.ans = e.ans,
                      M.duration = e.duration,
                    d || (d = !0,
                      c |= 1,
                      u())
                  })
              } else
                c = 1;
              l.vm.run(function (e) {
                o = e,
                  c |= 2,
                  u()
              })
            }(c, t, n)
        }),
        c(U),
        I();
      /TCSDK\//.test(u.ua) && n(73).sdk();
      var t = Math.round(y.txtBack.css("font-size"));
      t % 2 == 1 && (t += 1),
        y.txtBack.css("font-size", p.px2remU(t)),
        y.operation.addClass("show-loading")
    }

    var F = !1
      , B = 0;

    function V() {
      (B += 1) < 3 || s.verifySuccess(k("REFRESH_ERROR", E.getQueryParam("aid"), E.getQueryParam("sid")))
    }

    function W() {
      F || (F = !0,
        O += 1,
        r.log("refresh"),
        g.showLoading(),
        z.moveBack(!1),
        l.tdc.clearData(),
        l.vm.init(),
      l.tdc.checkTdcSuccess() || l.tdc.retryLoad(v),
        $.ajax({
          type: "POST",
          url: "/cap_union_new_getsig",
          data: a.getQuery(!0),
          dataType: "json",
          error: function (e, t, n) {
            V(),
              F = !1,
              g.loadImgFailed();
            var r = "";
            r += e && e.status ? e.status + ";" : "",
              r += t ? t + ":" : "",
              r += n || "",
              v.send(v.type.ERROR_TYPE_AJAX_GETSIG, r)
          },
          success: function (e) {
            if (!e)
              return V(),
                g.loadImgFailed(),
                v.send(v.type.ERROR_TYPE_AJAX_GETSIG, "response error.");
            if (m.push(26, r.logEnd("refresh")),
              e.ret = parseInt(e.ret, 10),
            52 === e.ret)
              return s.frequencyLimit();
            T.capChallenge = e.chlg || {};
            var t = e.vsig
              , n = e.sess;
            t || n ? (t && (T.vsig = t),
            n && w(n),
              e.cdnPic1 && e.cdnPic2 && e.iscdn ? (T.iscdn = e.iscdn,
                T.cdnPic1 = e.cdnPic1,
                T.cdnPic2 = e.cdnPic2) : (T.iscdn = !1,
                T.cdnPic1 = null,
                T.cdnPic2 = null),
              T.spt = e.inity,
              c(function () {
                F = !1,
                  B = 0,
                  U()
              }, function () {
                F = !1,
                  V()
              })) : (F = !1,
              V(),
              g.loadImgFailed())
          }
        }))
    }

    function U() {
      z.boundaryCalc(),
        z.movable(!0),
        setTimeout(function () {
          y.operation.removeClass("show-loading")
        }, 20),
        F = !1,
        m.push(46, r.point("now")),
        m.send()
    }

    var q = function K(e) {
      var t = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 1;
      t > 3 ? e() : M.ans ? e() : setTimeout(function () {
        K(e, t + 1)
      }, 200)
    };
    var Y = 0;
    e.exports = function () {
      l.tdc.link(v),
        l.vm.init(),
        function () {
          if (j)
            try {
              (L = new b).useWebWorker && !window.setImmediate && L.run(P, function (e) {
                M.ans = e.ans,
                  M.duration = e.duration
              })
            } catch (e) {
            }
        }(),
        y.close.on("click", function () {
          s.capClose()
        }),
        y.btnBack.on("click", function () {
          var e = T.dst;
          e ? window.location = e : "capFrame" === T.capSrc ? s.goBack() : s.otherBack()
        }),
        y.aged.on("click", function () {
          s.goAged()
        }),
        y.feedback.on("click", function () {
          try {
            var e = f(T.TuCao, d());
            window.open(e)
          } catch (t) {
          }
        }),
        y.site007.on("click", function () {
          try {
            parseInt(T.iscdn),
              window.open("https://007.qq.com/medicine/static/html/tiyan.html")
          } catch (e) {
          }
        }),
        y.site007.on("touchstart", function () {
          $(this).addClass("show-site-underline")
        }),
        y.site007.on("touchend", function () {
          $(this).removeClass("show-site-underline")
        }),
        y.embedLab.on("click", function () {
          try {
            window.open("https://007.qq.com/medicine/static/html/tiyan.html")
          } catch (e) {
          }
        }),
        y.btnReload.on("click", W),
        y.btnCoverReload.on("click", W),
        N()
    }
  }
  , , function (e, t, n) {
    "use strict";
    var r = n(33)
      , i = n(7)
      , a = n(22)
      , o = n(34)
      , s = window.captchaConfig
      , c = !0
      , u = {}
      , l = (window.performance || {}).timing || {}
      ,
      d = ["unloadEventStart", "unloadEventEnd", "redirectStart", "redirectEnd", "fetchStart", "domainLookupStart", "domainLookupEnd", "connectStart", "connectEnd", "requestStart", "responseStart", "responseEnd", "domLoading", "domInteractive", "domContentLoadedEventStart", "domContentLoadedEventEnd", "domComplete", "loadEventStart", "loadEventEnd", ["loadEventEnd", "fetchStart"], ["domComplete", "responseEnd"], ["domainLookupEnd", "domainLookupStart"], ["responseStart", "fetchStart"], ["connectEnd", "connectStart"]]
      , f = {
        1: {
          inner: {
            http: 21406,
            https: 21408
          },
          open: {
            http: 21407,
            https: 21412
          }
        },
        2: 3,
        3: {
          cdn: 14,
          cgi: 13
        }
      };

    function p() {
      if (c) {
        for (var e = new Date, t = 0; t < d.length; t++) {
          var n = d[t];
          u[t + 1] = "string" == typeof n ? l[d[t]] || 0 : (l[d[t][0]] || e) - l[d[t][1]] || 0
        }
        !function () {
          var e = l.fetchStart || window.timing.point("domLoaded")
            , t = u[46];
          if (u[42] = parseInt(a.queryParam("TCapIframeLoadTime")) || "0",
            u[43] = parseInt(a.queryParam("prehandleLoadTime")) || "0",
            u[44] = e - parseInt(a.queryParam("createIframeStart")) || "0",
            u[46] = t - e || 0,
            u[47] = window.timing.point("domLoaded") - e || 0,
            u[49] = t - parseInt(a.queryParam("createIframeStart"), 10) + parseInt(a.queryParam("prehandleLoadTime"), 10) || "0",
          window.performance && "function" == typeof window.performance.getEntries) {
            var n = window.performance.getEntries();
            if (n.length > 0) {
              for (var r = 1 << 30, i = -1, o = 0, s = n.length; o < s; o++) {
                var c = n[o]
                  , d = c.initiatorType;
                if (d && ("link" === d || "script" === d)) {
                  var f = c.fetchStart
                    , p = c.responseEnd;
                  f && p && (r = Math.min(r, f),
                    i = Math.max(i, p))
                }
              }
              u[45] = Math.ceil(i) - Math.ceil(r)
            }
          }
        }(),
          c = !1
      } else
        u[46] = 0
    }

    e.exports = {
      push: function (e, t) {
        u[e] = t || 0
      },
      send: function () {
        p(),
          u[29] = s.aid,
          u[31] = r.getToken(),
          u[33] = s.uid,
          u[34] = a.queryParam("sid"),
          u.platform = o.platform,
          u.flag1 = f[1][s.curenv][o.protocol],
          u.flag2 = f[2],
          u.flag3 = f[3]["1" === s.iscdn ? "cdn" : "cgi"],
          u[32] = u[32] - l.fetchStart || 0,
          u[37] = u[37] - l.fetchStart || 0;
        var e = [];
        for (var t in u)
          e.push(t + "=" + u[t]);
        u = {};
        var n = s.tdcHtdocsPath + "/caplog?appid=20128&" + e.join("&");
        (new Image).src = i(n)
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(41)
      , i = n(35)
      , a = function () {
      var e = document.createElement("fake")
        , t = {
        animation: "animationend",
        mozAnimation: "mozAnimationEnd",
        webkitAnimation: "webkitAnimationEnd"
      };
      for (var n in t)
        if (e.style[n] !== undefined)
          return t[n];
      return !1
    }()
      , o = void 0
      , s = function () {
      r.status.removeClass("show-error-tip")
    };
    e.exports = {
      showErrorNote: function (e, t, n) {
        clearTimeout(o),
          n && "embed" == n ? (r.guideText.html(i[e]).css({
            color: "#ec1313"
          }),
            o = setTimeout(function () {
              r.guideText.html(i.puzzle6).css({
                color: "#000000"
              })
            }, t)) : (r.txtErrorNote.html(i[e]),
            r.status.addClass("show-error-tip"),
            o = setTimeout(function () {
              s()
            }, t))
      },
      clearErrorNote: s,
      showCoverError: function (e, t, n, a) {
        e = i[e],
        "[object Array]" === Object.prototype.toString.call(e) && (e = e[Math.floor(Math.random() * e.length)]),
        t && (e = e.replace(/\+/g, t)),
        a && (e += '<div class="tc-token">' + $("<div>").text(a).html() + "</div>"),
          r.txtError.html(e),
          r.operation.addClass("show-error"),
          setTimeout(function () {
            r.operation.removeClass("show-error"),
              n()
          }, 1e3)
      },
      loadImgFailed: function () {
        r.operation.removeClass("show-loading"),
          r.operation.addClass("show-fail")
      },
      showLoading: function () {
        r.operation.addClass("show-loading"),
          r.operation.removeClass("show-fail show-success show-error")
      },
      hideLoading: function () {
        r.operation.removeClass("show-loading")
      },
      showSuccess: function (e, t) {
        r.operation.addClass("show-success"),
          i.c16 = i.c16.join("%^").replace(/\+/g, (e / 1e3).toFixed(1)).split("%^"),
          e <= 4e3 ? r.txtSuccess.html(i.c16[Math.floor(2 * Math.random())]) : r.txtSuccess.html(i.c16[2]),
          setTimeout(function () {
            t()
          }, 800)
      },
      shake: function (e) {
        r.imgSlide.addClass("shake"),
          r.btnSlide.addClass("shake"),
          a ? r.imgSlide.one(a, function () {
            r.imgSlide.removeClass("shake"),
              r.btnSlide.removeClass("shake"),
              e()
          }) : setTimeout(function () {
            r.imgSlide.removeClass("shake"),
              r.btnSlide.removeClass("shake"),
              e()
          }, 400)
      }
    }
  }
  , , , , , , , function (e, t, n) {
    // "use strict";
    // n(63);
    // var r = n(22)
    //   , i = n(39);
    // i.loadReady();
    // var a = n(32)
    //   , o = n(6).getScript
    //   , s = n(5).getErrorRes
    //   , c = n(1)
    //   , u = /(iPhone|iPad|iPod|Android|ios|SymbianOS|Mobile)/i.test(navigator.userAgent);
    // if (!window.addEventListener || !document.querySelector) {
    //   var l = document.getElementById("inlineCaptchaStyle");
    //   l.parentNode.removeChild(l)
    // }
    //
    // function d() {
    //   i.verifySuccess(s("LIB_JQ_LOAD_ERROR", c.getQueryParam("aid"), c.getQueryParam("sid")))
    // }
    //
    // a.setGlobalStatus("1" === c.getQueryParam("global"));
    // var f = null;
    //
    // function p() {
    //   window.$ ? (null !== f && (clearTimeout(f),
    //     f = null),
    //     n(52)()) : setTimeout(p, 20)
    // }
    //
    // var h, g = window.captchaConfig, m = g.ticket, v = g.randstr;
    // m && v ? i.verifySuccess({
    //   ticket: m,
    //   randstr: v
    // }) : u ? (window.$ = n(74),
    //   n(52)()) : (f = window.setTimeout(function () {
    //   d()
    // }, 15e3),
    //   o({
    //     src: window.captchaConfig.htdocsPath + "/slide-jy.js",
    //     successCheck: function () {
    //       return !!window.$
    //     },
    //     success: function () {
    //       p()
    //     },
    //     error: function () {
    //       o({
    //         src: "/slide-jy.js",
    //         successCheck: function () {
    //           return !!window.$
    //         },
    //         success: function () {
    //           p()
    //         },
    //         error: function () {
    //           d()
    //         }
    //       })
    //     }
    //   })),
    // (h = r.queryParam("logJs")) && o({
    //   src: c.addUrlParam(decodeURIComponent(h), {
    //     capid: r.queryParam("sid")
    //   }),
    //   success: function () {
    //     a.send(42, "success")
    //   },
    //   error: function () {
    //     a.send(41, "error")
    //   }
    // }),
    //   window.TCaptchaLoaded = !0
  }
  , function (e, t, n) {
    "use strict";
    var r = n(32)
      , i = {}
      , a = function (e) {
      var t = "";
      e && e.stack && (t = e.stack.replace(/\n/gi, "").split(/\bat\b/).join("\n").replace(/\?[^:]+/gi, ""));
      try {
        var n = e.toString();
        t.indexOf(n) < 0 && (t = n + "@" + t)
      } catch (r) {
      }
      return t
    }
      , o = function (e) {
      var t = a(e);
      i[t] || (i[t] = !0,
        r.send(1, t))
    };
    window.addEventListener ? addEventListener("error", function (e) {
      o(e.error)
    }) : window.onerror = function (e, t, n, o, s) {
      var c = "";
      c = s && s.stack ? a(s) : e,
      i[c] || (i[c] = !0,
        r.send(1, c, 20))
    }
      ,
      e.exports = o
  }
  , function (e, t) {
    function n(e, t) {
      e.onload = function () {
        this.onerror = this.onload = null,
          t(null, e)
      }
        ,
        e.onerror = function () {
          this.onerror = this.onload = null,
            t(new Error("Failed to load " + this.src), e)
        }
    }

    function r(e, t) {
      e.onreadystatechange = function () {
        "complete" != this.readyState && "loaded" != this.readyState || (this.onreadystatechange = null,
          t(null, e))
      }
    }

    e.exports = function (e, t, i) {
      var a = document.head || document.getElementsByTagName("head")[0]
        , o = document.createElement("script");
      "function" == typeof t && (i = t,
        t = {}),
        t = t || {},
        i = i || function () {
        }
        ,
        o.type = t.type || "text/javascript",
        o.charset = t.charset || "utf8",
        o.async = !("async" in t) || !!t.async,
        o.src = e,
      t.attrs && function (e, t) {
        for (var n in t)
          e.setAttribute(n, t[n])
      }(o, t.attrs),
      t.text && (o.text = "" + t.text),
        ("onload" in o ? n : r)(o, i),
      o.onload || n(o, i),
        a.appendChild(o)
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(40)
      , i = n(0).supportsPassive
      , a = 300
      , o = /^touch/
      , s = /^(relative|absolute)$/
      , c = !1
      , u = n(22)
      , l = {
      x: "left",
      y: "top",
      "-x": "right",
      "-y": "bottom"
    }
      , d = {
      x: "width",
      y: "height"
    }
      , f = navigator.userAgent
      , p = /TCSDK\//.test(f) && /iphone|ipad|ipod/i.test(f)
      , h = /(iPhone|iPad|iPod|Android|ios|SymbianOS|Mobile)/i.test(navigator.userAgent)
      , g = document.body
      , m = {
      width: Math.max(g.clientWidth, g.offsetWidth),
      height: Math.max(g.clientHeight, g.offsetHeight, g.scrollHeight) - 10
    };
    e.exports = function (e, t, n, f) {
      var g = void 0
        , v = void 0
        , y = void 0
        , w = void 0
        , b = !1
        , k = -1
        , E = {}
        , _ = -1
        , T = 1 << 30
        , S = []
        , R = []
        , x = "x"
        , C = l[x];

      function z(e) {
        var t = e.target.id;
        if (e.preventDefault && e.preventDefault(),
        "coverReload" !== t)
          return !1
      }

      function O() {
        S = [],
          _ = -1,
          T = 1 << 30;
        for (var e = function (e) {
          var t = R[e]
            , n = t.offset();
          n.width || (n.width = t.width() || parseInt(t.css("width"), 10));
          var r = d[x];
          t.parents().each(function (i, a) {
            var o = $(a);
            if (s.test(o.css("position"))) {
              var c = o.offset();
              return c.width || (c.width = o.width()),
                0 === e ? (S[e] = E.left,
                  E.middle = E.left + n.width / 2,
                  E.min = c[C],
                  E.max = c[r] + c[C] - n[r],
                  t.css(C, E.left + "px")) : (S[e] = E.middle - n[r] / 2,
                  t.css(C, E.middle - n[r] / 2 + "px")),
                !1
            }
          })
        }, t = 0; t < R.length; t++)
          e(t)
      }

      function A(e) {
        if (o.test(e.type)) {
          var t = e;
          e.originalEvent && o.test(e.originalEvent.type) && (t = e.originalEvent);
          var n = t.touches[0];
          return n ? {
            x: n.clientX,
            y: n.clientY,
            t: +new Date - y
          } : null
        }
        return {
          x: e.pageX,
          y: e.pageY,
          t: +new Date - y
        }
      }

      function P() {
        for (var e = 0; e < R.length; e++) {
          var t = R[e]
            , n = S[e] + v[x] - g[x];
          t.css(C, n + "px")
        }
      }

      function j(e) {
        if (h || e && e.preventDefault && e.preventDefault(),
        b && !y) {
          y = !1,
            k = -1;
          for (var t = 0; t < R.length; t++) {
            var r = R[t];
            if (r[0] === e.target || $(e.target).parents().index(r) >= 0) {
              w = [],
                y = +new Date,
                k = t,
                v = g = A(e);
              var i = g[x] - r.offset()[l[x]]
                , a = S[t] - S[0];
              _ = E.min + i + a,
                T = E.max + i + a
            }
          }
          y && c && c(D),
            setTimeout(function () {
              n && n()
            }, 0)
        }
      }

      var L = void 0;

      function M(e) {
        var t, n;
        h || e && e.preventDefault && e.preventDefault(),
        y && (clearTimeout(L),
        p && (t = e.pageX,
          n = e.pageY,
        t < 0 || n < 0 || t > m.width || n > m.height) && (L = setTimeout(function () {
          I()
        }, 350)),
          v = A(e) || g,
        w.length < a && w.push(v),
          _ > v[x] ? v[x] = _ : T < v[x] && (v[x] = T),
        c || P())
      }

      function I() {
        if (y && (0 === w.length && w.push(g),
          !(w.length <= 2))) {
          N.dragDuration = +new Date - y,
            y = !1;
          for (var e = [], t = w.length - 1; t >= 0; t--)
            t > 0 ? (w[t].x = Math.ceil(w[t].x - w[t - 1].x),
              w[t].y = Math.ceil(w[t].y - w[t - 1].y),
              w[t].t = w[t].t - w[t - 1].t) : (w[t].x = Math.ceil(w[t].x),
              w[t].y = Math.ceil(w[t].y)),
            0 == w[t].x && 0 == w[t].y || e.push([w[t].x, w[t].y, w[t].t]);
          setTimeout(function () {
            "function" == typeof f && f(v, k, e.reverse())
          }, 0)
        }
      }

      function D() {
        y && (P(),
          c(D))
      }

      !function () {
        var t = $(e);
        t.on("mousedown touchstart", j),
          t.on("mousemove touchmove", M),
          t.on("mouseup touchend touchcancel", I),
          $(document).on("mousemove", M),
          $(document).on("mouseup mouseleave", I);
        var n = !!i && {
          passive: !1
        };
        document.addEventListener && (document.addEventListener("touchmove", z, n),
        "1" !== u.queryParam("enableAged") && e[0].addEventListener("touchstart", z, !1)),
          r.listen(1, O)
      }(),
        function () {
          var e = $(t[0]);
          E.left = parseInt(e.css("left")),
            R = [];
          for (var n = 0; n < t.length; n++)
            R.push($(t[n]))
        }();
      var N = {
        moveBack: function (e) {
          for (var t = 0; t < R.length; t++)
            R[t].animate({
              left: S[t] + "px"
            }, 300, "linear", function () {
            });
          e !== undefined && (b = !!e)
        },
        boundaryCalc: O,
        movable: function (e) {
          b = e
        }
      };
      return N
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(41)
      , i = n(40)
      , a = n(22)
      , o = n(54)
      , s = n(32)
      , c = n(67)
      , u = n(55)
      , l = n(34)
      , d = n(39)
      , f = n(35)
      , p = window.captchaConfig
      , h = window.timing
      , g = 0
      , m = {}
      , v = {
      1: r.imgBg,
      2: r.imgSlide
    }
      , y = {
      cgi: {
        img: [],
        onErrorCode: 12,
        timing: [null, 25, 28]
      },
      cdn: {
        retry: 2,
        img: [],
        timeout: l.loadImgTimeout,
        timing: [null, 35, 36],
        onErrorCode: 11,
        fallback: "cgi-retry"
      },
      "cgi-retry": {
        img: [],
        extParams: "&retry=1",
        onErrorCode: 13,
        timing: [null, 25, 28]
      }
    }
      , w = !0;

    function b(e, t, n) {
      var i = (e.img[t] || l.cgiImg) + e.params + "&img_index=" + t + (e.extParams || "")
        , a = {
        timeout: 15e3,
        success: function (n) {
          o.push(e.timing[t], h.logEnd("imgLoad-" + e.loadIndex + "-" + t)),
            m[e.loadIndex][t] = n,
            function (e) {
              if (m[g] && m[g][1] && m[g][2] && g === e.loadIndex) {
                v[1].attr("src", m[g][1].src),
                  v[2].attr("src", m[g][2].src),
                  p.rate = r.operation.width() / 680;
                var t = parseInt(m[g][2].height * p.rate) + "px"
                  , n = parseInt(e.posY * p.rate) + "px";
                r.imgSlide.css({
                  height: t,
                  width: t,
                  top: n
                }),
                w && (w = !1,
                  setTimeout(function () {
                    $("#bodyWrap").addClass("body-wrap-show")
                  }, 16)),
                e.callback && e.callback(),
                  u.hideLoading(),
                  h.log("verifyDuration")
              }
            }(e)
        },
        error: function () {
          s.send(e.onErrorCode, t, null, h.logEnd("imgLoad-" + e.loadIndex + "-" + t)),
            n = n || 1,
            !e.retry || n >= e.retry ? function (e, t) {
              e.fallback ? b(e = $.extend({
                posY: e.posY,
                params: e.params,
                callback: e.callback,
                loadIndex: e.loadIndex
              }, y[e.fallback]), t) : (u.loadImgFailed(),
                d.loadFailure(f.c14),
              "function" == typeof e.onerror && (e.onerror(),
                e.onerror = null))
            }(e, t) : b(e, t, n + 1)
        }
      };
      h.log("imgLoad-" + e.loadIndex + "-" + t),
        c(v[t], i, a)
    }

    i.listen(0, function () {
      if (m[g] && m[g][2]) {
        p.rate = r.operation.width() / 680;
        var e = i.px2remU(m[g][2].height * p.rate)
          , t = i.px2remU(p.spt * p.rate);
        r.imgSlide.css({
          height: e,
          width: e,
          top: t
        })
      }
    }),
      e.exports = function (e, t) {
        m[g += 1] = [];
        var n = $.extend({
          posY: parseInt(p.spt, 10)
        }, y[p.iscdn ? "cdn" : "cgi"]);
        n.img[1] = p.cdnPic1,
          n.img[2] = p.cdnPic2,
          n.callback = e,
          n.onerror = t,
          n.params = "?aid=" + a.queryParam("aid") + "&sess=" + a.queryParam("sess") + "&sid=" + a.queryParam("sid"),
          n.loadIndex = g,
          h.logEnd("jsInit"),
          b(n, 1),
          b(n, 2)
      }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(7)
      , i = 0
      , a = function (e, t, n) {
      i += 1,
        t = r(t);
      var a = !1
        , o = void 0
        , s = function (e) {
        return function () {
          a || (clearTimeout(o),
            e())
        }
      }
        , c = new Image;
      c.onload = s(function () {
        n.success && n.success(c, t)
      }),
        c.onerror = s(function () {
          n.error && n.error(null, t)
        }),
      n.timeout && (o = setTimeout(function () {
        a = !0,
        n.error && n.error(null, t)
      }, n.timeout)),
        c.src = t
    };
    a.loading = function () {
      return i
    }
      ,
      e.exports = a
  }
  , function (e, t, n) {
    "use strict";
    n(51);
    var r = n(33)
      , i = n(69)
      , a = n(70);
    e.exports = {
      vm: i,
      tdc: r,
      challenge: a
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = window.timing
      , i = window.captchaConfig
      , a = void 0;
    e.exports = {
      init: function () {
        return a = null,
        "undefined" != typeof window.vm && window.vm.entry && (r.log("vmInit"),
          a = new window.vm.entry(i.vmByteCode),
          r.logEnd("vmInit")),
          a
      },
      run: function (e) {
        var t = {}
          , n = i.vmAvailable
          , o = i.vmByteCode;
        t.vlg = [n ? 1 : 0, o ? 1 : 0, 1].join("_"),
          n && o ? (r.log("vmRun"),
            a && a.run ? a.run(function (n) {
              t.vmData = n,
                t.vmtime = [r.logEnd("vmInit"), r.logEnd("vmRun")].join("_"),
                e(t)
            }) : e(t)) : e(t)
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
        return typeof e
      }
      : function (e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
      }
      , i = n(71)
      , a = window.captchaConfig;
    e.exports = function () {
      var e = 0
        , t = a.capChallenge;
      if ("object" === (void 0 === t ? "undefined" : r(t)) && "string" == typeof t.randstr && ("string" == typeof t.M || "number" == typeof t.M) && "string" == typeof t.ans) {
        t.ans = t.ans.toLowerCase(),
          t.M = parseInt(t.M);
        for (var n = 0; n < t.M && n < 1e3; n++) {
          var o = t.randstr + n
            , s = i(o);
          if (t.ans === s.toLowerCase()) {
            e = n;
            break
          }
        }
      }
      return e
    }
  }
  , function (e, t, n) {
    "use strict";

    function r(e, t) {
      var n = (65535 & e) + (65535 & t);
      return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
    }

    function i(e, t, n, i, a, o) {
      return r(function (e, t) {
        return e << t | e >>> 32 - t
      }(r(r(t, e), r(i, o)), a), n)
    }

    function a(e, t, n, r, a, o, s) {
      return i(t & n | ~t & r, e, t, a, o, s)
    }

    function o(e, t, n, r, a, o, s) {
      return i(t & r | n & ~r, e, t, a, o, s)
    }

    function s(e, t, n, r, a, o, s) {
      return i(t ^ n ^ r, e, t, a, o, s)
    }

    function c(e, t, n, r, a, o, s) {
      return i(n ^ (t | ~r), e, t, a, o, s)
    }

    function u(e, t) {
      e[t >> 5] |= 128 << t % 32,
        e[14 + (t + 64 >>> 9 << 4)] = t;
      var n = void 0
        , i = void 0
        , u = void 0
        , l = void 0
        , d = void 0
        , f = 1732584193
        , p = -271733879
        , h = -1732584194
        , g = 271733878;
      for (n = 0; n < e.length; n += 16)
        i = f,
          u = p,
          l = h,
          d = g,
          p = c(p = c(p = c(p = c(p = s(p = s(p = s(p = s(p = o(p = o(p = o(p = o(p = a(p = a(p = a(p = a(p, h = a(h, g = a(g, f = a(f, p, h, g, e[n], 7, -680876936), p, h, e[n + 1], 12, -389564586), f, p, e[n + 2], 17, 606105819), g, f, e[n + 3], 22, -1044525330), h = a(h, g = a(g, f = a(f, p, h, g, e[n + 4], 7, -176418897), p, h, e[n + 5], 12, 1200080426), f, p, e[n + 6], 17, -1473231341), g, f, e[n + 7], 22, -45705983), h = a(h, g = a(g, f = a(f, p, h, g, e[n + 8], 7, 1770035416), p, h, e[n + 9], 12, -1958414417), f, p, e[n + 10], 17, -42063), g, f, e[n + 11], 22, -1990404162), h = a(h, g = a(g, f = a(f, p, h, g, e[n + 12], 7, 1804603682), p, h, e[n + 13], 12, -40341101), f, p, e[n + 14], 17, -1502002290), g, f, e[n + 15], 22, 1236535329), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 1], 5, -165796510), p, h, e[n + 6], 9, -1069501632), f, p, e[n + 11], 14, 643717713), g, f, e[n], 20, -373897302), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 5], 5, -701558691), p, h, e[n + 10], 9, 38016083), f, p, e[n + 15], 14, -660478335), g, f, e[n + 4], 20, -405537848), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 9], 5, 568446438), p, h, e[n + 14], 9, -1019803690), f, p, e[n + 3], 14, -187363961), g, f, e[n + 8], 20, 1163531501), h = o(h, g = o(g, f = o(f, p, h, g, e[n + 13], 5, -1444681467), p, h, e[n + 2], 9, -51403784), f, p, e[n + 7], 14, 1735328473), g, f, e[n + 12], 20, -1926607734), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 5], 4, -378558), p, h, e[n + 8], 11, -2022574463), f, p, e[n + 11], 16, 1839030562), g, f, e[n + 14], 23, -35309556), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 1], 4, -1530992060), p, h, e[n + 4], 11, 1272893353), f, p, e[n + 7], 16, -155497632), g, f, e[n + 10], 23, -1094730640), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 13], 4, 681279174), p, h, e[n], 11, -358537222), f, p, e[n + 3], 16, -722521979), g, f, e[n + 6], 23, 76029189), h = s(h, g = s(g, f = s(f, p, h, g, e[n + 9], 4, -640364487), p, h, e[n + 12], 11, -421815835), f, p, e[n + 15], 16, 530742520), g, f, e[n + 2], 23, -995338651), h = c(h, g = c(g, f = c(f, p, h, g, e[n], 6, -198630844), p, h, e[n + 7], 10, 1126891415), f, p, e[n + 14], 15, -1416354905), g, f, e[n + 5], 21, -57434055), h = c(h, g = c(g, f = c(f, p, h, g, e[n + 12], 6, 1700485571), p, h, e[n + 3], 10, -1894986606), f, p, e[n + 10], 15, -1051523), g, f, e[n + 1], 21, -2054922799), h = c(h, g = c(g, f = c(f, p, h, g, e[n + 8], 6, 1873313359), p, h, e[n + 15], 10, -30611744), f, p, e[n + 6], 15, -1560198380), g, f, e[n + 13], 21, 1309151649), h = c(h, g = c(g, f = c(f, p, h, g, e[n + 4], 6, -145523070), p, h, e[n + 11], 10, -1120210379), f, p, e[n + 2], 15, 718787259), g, f, e[n + 9], 21, -343485551),
          f = r(f, i),
          p = r(p, u),
          h = r(h, l),
          g = r(g, d);
      return [f, p, h, g]
    }

    function l(e) {
      var t = void 0
        , n = "";
      for (t = 0; t < 32 * e.length; t += 8)
        n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
      return n
    }

    function d(e) {
      var t = void 0
        , n = [];
      for (n[(e.length >> 2) - 1] = void 0,
             t = 0; t < n.length; t += 1)
        n[t] = 0;
      for (t = 0; t < 8 * e.length; t += 8)
        n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
      return n
    }

    function f(e) {
      var t = void 0
        , n = void 0
        , r = "0123456789abcdef"
        , i = "";
      for (n = 0; n < e.length; n += 1)
        t = e.charCodeAt(n),
          i += r.charAt(t >>> 4 & 15) + r.charAt(15 & t);
      return i
    }

    function p(e) {
      return unescape(encodeURIComponent(e))
    }

    function h(e) {
      return function (e) {
        return l(u(d(e), 8 * e.length))
      }(p(e))
    }

    function g(e, t) {
      return function (e, t) {
        var n, r = void 0, i = d(e), a = [], o = [];
        for (a[15] = o[15] = void 0,
             i.length > 16 && (i = u(i, 8 * e.length)),
               r = 0; r < 16; r += 1)
          a[r] = 909522486 ^ i[r],
            o[r] = 1549556828 ^ i[r];
        return n = u(a.concat(d(t)), 512 + 8 * t.length),
          l(u(o.concat(n), 640))
      }(p(e), p(t))
    }

    e.exports = function (e, t, n) {
      return t ? n ? g(t, e) : function (e, t) {
        return f(g(e, t))
      }(t, e) : n ? h(e) : function (e) {
        return f(h(e))
      }(e)
    }
  }
  , function (e, t, n) {
    "use strict";
    var r = n(33)
      , i = n(22).queryParam
      , a = window.navigator.userAgent
      , o = window.captchaConfig
      , s = function () {
      var e = {
        info: "unknown",
        version: 0
      };
      try {
        /micromessenger/i.test(a) ? (e.info = "micromessenger",
          e.version = a.match(/micromessenger\/([\d.]+)/i)[1]) : /mqqbrowser/i.test(a) ? (e.info = "qqbroswer",
          e.version = a.match(/mqqbrowser\/([\d.]+)/i)[1]) : /ucbrowser/i.test(a) ? (e.info = "UCbrowser",
          e.version = a.match(/ucbrowser\/([\d.]+)/i)[1]) : /ucweb/i.test(a) ? (e.info = "UCWeb",
          e.version = a.match(/ucweb\/([\d.]+)/i)[1]) : /MiuiBrowser/i.test(a) ? (e.info = "MiuiBrowser",
          e.version = a.match(/miuibrowser\/([\d.]+)/i)[1]) : /hs-t929_td/i.test(a) ? (e.info = "HS-T929_TD",
          e.version = a.match(/hs-t929_td\/([\d.]+)/i)[1]) : /k-touch_tou_ch_2/i.test(a) ? (e.info = "k-touch_tou_ch_2",
          e.version = a.match(/k-touch_tou_ch_2\/([\s]+)/i)[1]) : /chrome/i.test(a) ? (e.info = "chrome",
          e.version = a.match(/chrome\/([\d.]+)/i)[1]) : /safari/i.test(a) && /iphone/i.test(a) ? (e.info = "safari",
          e.version = a.match(/safari\/([\d.]+)/i)[1]) : (e.info = "unknown",
          e.version = 0)
      } catch (t) {
      }
      return e
    }
      , c = {
      clientInfo: s().info,
      clientVersion: s().version,
      os: function () {
        var e = "";
        try {
          /android/i.test(a) ? e = "Android " + a.match(/android\s+([^\s]*)/i)[1] : /iphone/i.test(a) && (e = "IOS " + a.match(/iphone\s+os\s+([^\s]*)/i)[1].replace("_", "."))
        } catch (t) {
        }
        return e
      }(),
      osVersion: function () {
        try {
          if (/android/i.test(a))
            return a.match(/([^;]+)\s+Build/i)[1];
          if (/iphone/i.test(a))
            return a.match(/([^(]*);/)[1]
        } catch (e) {
        }
        return ""
      }(),
      netType: o.aid || i("aid"),
      customInfo: "custominfo:clientIP:" + o.uip + ",sid:" + i("sid"),
      "d-wx-push": 1
    };
    e.exports = function () {
      return c.imei = r.getToken(),
        c
    }
  }
  , function (e, t, n) {
    "use strict";
    e.exports = {
      sdk: function () {
        window.open = function (e) {
          var t = $('<a target="_blank">');
          t.attr("href", e),
            t.click()
        }
      }
    }
  }
  , function (e, t, n) {
    "use strict";
    var r, i, a = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
        return typeof e
      }
      : function (e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
      }
    ;
    i = window,
    (r = function () {
      return e = i,
        t = function () {
          var t, n, r, i, o, s, c = [], u = c.concat, l = c.filter, d = c.slice, f = e.document, p = {}, h = {}, g = {
              "column-count": 1,
              columns: 1,
              "font-weight": 1,
              "line-height": 1,
              opacity: 1,
              "z-index": 1,
              zoom: 1
            }, m = /^\s*<(\w+|!)[^>]*>/, v = /^<(\w+)\s*\/?>(?:<\/\1>|)$/,
            y = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi, w = /^(?:body|html)$/i,
            b = /([A-Z])/g, k = ["val", "css", "html", "text", "data", "width", "height", "offset"],
            E = f.createElement("table"), _ = f.createElement("tr"), T = {
              tr: f.createElement("tbody"),
              tbody: E,
              thead: E,
              tfoot: E,
              td: _,
              th: _,
              "*": f.createElement("div")
            }, S = /^[\w-]*$/, R = {}, x = R.toString, C = {}, z = f.createElement("div"), O = {
              tabindex: "tabIndex",
              readonly: "readOnly",
              "for": "htmlFor",
              "class": "className",
              maxlength: "maxLength",
              cellspacing: "cellSpacing",
              cellpadding: "cellPadding",
              rowspan: "rowSpan",
              colspan: "colSpan",
              usemap: "useMap",
              frameborder: "frameBorder",
              contenteditable: "contentEditable"
            }, A = Array.isArray || function (e) {
              return e instanceof Array
            }
          ;

          function P(e) {
            return null == e ? String(e) : R[x.call(e)] || "object"
          }

          function j(e) {
            return "function" == P(e)
          }

          function L(e) {
            return null != e && e == e.window
          }

          function M(e) {
            return null != e && e.nodeType == e.DOCUMENT_NODE
          }

          function I(e) {
            return "object" == P(e)
          }

          function D(e) {
            return I(e) && !L(e) && Object.getPrototypeOf(e) == Object.prototype
          }

          function N(e) {
            var t = !!e && "length" in e && e.length
              , n = r.type(e);
            return "function" != n && !L(e) && ("array" == n || 0 === t || "number" == typeof t && t > 0 && t - 1 in e)
          }

          function F(e) {
            return e.replace(/::/g, "/").replace(/([A-Z]+)([A-Z][a-z])/g, "$1_$2").replace(/([a-z\d])([A-Z])/g, "$1_$2").replace(/_/g, "-").toLowerCase()
          }

          function B(e) {
            return e in h ? h[e] : h[e] = new RegExp("(^|\\s)" + e + "(\\s|$)")
          }

          function $(e, t) {
            return "number" != typeof t || g[F(e)] ? t : t + "px"
          }

          function V(e) {
            return "children" in e ? d.call(e.children) : r.map(e.childNodes, function (e) {
              if (1 == e.nodeType)
                return e
            })
          }

          function W(e, t) {
            var n, r = e ? e.length : 0;
            for (n = 0; n < r; n++)
              this[n] = e[n];
            this.length = r,
              this.selector = t || ""
          }

          function U(e, t) {
            return null == t ? r(e) : r(e).filter(t)
          }

          function q(e, t, n, r) {
            return j(t) ? t.call(e, n, r) : t
          }

          function Y(e, t, n) {
            null == n ? e.removeAttribute(t) : e.setAttribute(t, n)
          }

          function K(e, n) {
            var r = e.className || ""
              , i = r && r.baseVal !== t;
            if (n === t)
              return i ? r.baseVal : r;
            i ? r.baseVal = n : e.className = n
          }

          function H(e) {
            try {
              return e ? "true" == e || "false" != e && ("null" == e ? null : +e + "" == e ? +e : /^[\[\{]/.test(e) ? r.parseJSON(e) : e) : e
            } catch (t) {
              return e
            }
          }

          return C.matches = function (e, t) {
            if (!t || !e || 1 !== e.nodeType)
              return !1;
            var n = e.matches || e.webkitMatchesSelector || e.mozMatchesSelector || e.oMatchesSelector || e.matchesSelector;
            if (n)
              return n.call(e, t);
            var r, i = e.parentNode, a = !i;
            return a && (i = z).appendChild(e),
              r = ~C.qsa(i, t).indexOf(e),
            a && z.removeChild(e),
              r
          }
            ,
            o = function (e) {
              return e.replace(/-+(.)?/g, function (e, t) {
                return t ? t.toUpperCase() : ""
              })
            }
            ,
            s = function (e) {
              return l.call(e, function (t, n) {
                return e.indexOf(t) == n
              })
            }
            ,
            C.fragment = function (e, n, i) {
              var a, o, s;
              return v.test(e) && (a = r(f.createElement(RegExp.$1))),
              a || (e.replace && (e = e.replace(y, "<$1></$2>")),
              n === t && (n = m.test(e) && RegExp.$1),
              n in T || (n = "*"),
                (s = T[n]).innerHTML = "" + e,
                a = r.each(d.call(s.childNodes), function () {
                  s.removeChild(this)
                })),
              D(i) && (o = r(a),
                r.each(i, function (e, t) {
                  k.indexOf(e) > -1 ? o[e](t) : o.attr(e, t)
                })),
                a
            }
            ,
            C.Z = function (e, t) {
              return new W(e, t)
            }
            ,
            C.isZ = function (e) {
              return e instanceof C.Z
            }
            ,
            C.init = function (e, n) {
              var i, a;
              if (!e)
                return C.Z();
              if ("string" == typeof e)
                if ("<" == (e = e.trim())[0] && m.test(e))
                  i = C.fragment(e, RegExp.$1, n),
                    e = null;
                else {
                  if (n !== t)
                    return r(n).find(e);
                  i = C.qsa(f, e)
                }
              else {
                if (j(e))
                  return r(f).ready(e);
                if (C.isZ(e))
                  return e;
                if (A(e))
                  a = e,
                    i = l.call(a, function (e) {
                      return null != e
                    });
                else if (I(e))
                  i = [e],
                    e = null;
                else if (m.test(e))
                  i = C.fragment(e.trim(), RegExp.$1, n),
                    e = null;
                else {
                  if (n !== t)
                    return r(n).find(e);
                  i = C.qsa(f, e)
                }
              }
              return C.Z(i, e)
            }
            ,
            (r = function (e, t) {
                return C.init(e, t)
              }
            ).extend = function (e) {
              var r, i = d.call(arguments, 1);
              return "boolean" == typeof e && (r = e,
                e = i.shift()),
                i.forEach(function (i) {
                  !function a(e, r, i) {
                    for (n in r)
                      i && (D(r[n]) || A(r[n])) ? (D(r[n]) && !D(e[n]) && (e[n] = {}),
                      A(r[n]) && !A(e[n]) && (e[n] = []),
                        a(e[n], r[n], i)) : r[n] !== t && (e[n] = r[n])
                  }(e, i, r)
                }),
                e
            }
            ,
            C.qsa = function (e, t) {
              var n, r = "#" == t[0], i = !r && "." == t[0], a = r || i ? t.slice(1) : t, o = S.test(a);
              return e.getElementById && o && r ? (n = e.getElementById(a)) ? [n] : [] : 1 !== e.nodeType && 9 !== e.nodeType && 11 !== e.nodeType ? [] : d.call(o && !r && e.getElementsByClassName ? i ? e.getElementsByClassName(a) : e.getElementsByTagName(t) : e.querySelectorAll(t))
            }
            ,
            r.contains = f.documentElement.contains ? function (e, t) {
                return e !== t && e.contains(t)
              }
              : function (e, t) {
                for (; t && (t = t.parentNode);)
                  if (t === e)
                    return !0;
                return !1
              }
            ,
            r.type = P,
            r.isFunction = j,
            r.isWindow = L,
            r.isArray = A,
            r.isPlainObject = D,
            r.isEmptyObject = function (e) {
              var t;
              for (t in e)
                return !1;
              return !0
            }
            ,
            r.isNumeric = function (e) {
              var t = Number(e)
                , n = void 0 === e ? "undefined" : a(e);
              return null != e && "boolean" != n && ("string" != n || e.length) && !isNaN(t) && isFinite(t) || !1
            }
            ,
            r.inArray = function (e, t, n) {
              return c.indexOf.call(t, e, n)
            }
            ,
            r.camelCase = o,
            r.trim = function (e) {
              return null == e ? "" : String.prototype.trim.call(e)
            }
            ,
            r.uuid = 0,
            r.support = {},
            r.expr = {},
            r.noop = function () {
            }
            ,
            r.map = function (e, t) {
              var n, i, a, o, s = [];
              if (N(e))
                for (i = 0; i < e.length; i++)
                  null != (n = t(e[i], i)) && s.push(n);
              else
                for (a in e)
                  null != (n = t(e[a], a)) && s.push(n);
              return (o = s).length > 0 ? r.fn.concat.apply([], o) : o
            }
            ,
            r.each = function (e, t) {
              var n, r;
              if (N(e)) {
                for (n = 0; n < e.length; n++)
                  if (!1 === t.call(e[n], n, e[n]))
                    return e
              } else
                for (r in e)
                  if (!1 === t.call(e[r], r, e[r]))
                    return e;
              return e
            }
            ,
            r.grep = function (e, t) {
              return l.call(e, t)
            }
            ,
          e.JSON && (r.parseJSON = JSON.parse),
            r.each("Boolean Number String Function Array Date RegExp Object Error".split(" "), function (e, t) {
              R["[object " + t + "]"] = t.toLowerCase()
            }),
            r.fn = {
              constructor: C.Z,
              length: 0,
              forEach: c.forEach,
              reduce: c.reduce,
              push: c.push,
              sort: c.sort,
              splice: c.splice,
              indexOf: c.indexOf,
              concat: function () {
                var e, t, n = [];
                for (e = 0; e < arguments.length; e++)
                  t = arguments[e],
                    n[e] = C.isZ(t) ? t.toArray() : t;
                return u.apply(C.isZ(this) ? this.toArray() : this, n)
              },
              map: function (e) {
                return r(r.map(this, function (t, n) {
                  return e.call(t, n, t)
                }))
              },
              slice: function () {
                return r(d.apply(this, arguments))
              },
              ready: function (t) {
                if ("complete" === f.readyState || "loading" !== f.readyState && !f.documentElement.doScroll)
                  setTimeout(function () {
                    t(r)
                  }, 0);
                else {
                  var n = function i() {
                    f.removeEventListener("DOMContentLoaded", i, !1),
                      e.removeEventListener("load", i, !1),
                      t(r)
                  };
                  f.addEventListener("DOMContentLoaded", n, !1),
                    e.addEventListener("load", n, !1)
                }
                return this
              },
              get: function (e) {
                return e === t ? d.call(this) : this[e >= 0 ? e : e + this.length]
              },
              toArray: function () {
                return this.get()
              },
              size: function () {
                return this.length
              },
              remove: function () {
                return this.each(function () {
                  null != this.parentNode && this.parentNode.removeChild(this)
                })
              },
              each: function (e) {
                return c.every.call(this, function (t, n) {
                  return !1 !== e.call(t, n, t)
                }),
                  this
              },
              filter: function (e) {
                return j(e) ? this.not(this.not(e)) : r(l.call(this, function (t) {
                  return C.matches(t, e)
                }))
              },
              add: function (e, t) {
                return r(s(this.concat(r(e, t))))
              },
              is: function (e) {
                return "string" == typeof e ? this.length > 0 && C.matches(this[0], e) : e && this.selector == e.selector
              },
              not: function (e) {
                var n = [];
                if (j(e) && e.call !== t)
                  this.each(function (t) {
                    e.call(this, t) || n.push(this)
                  });
                else {
                  var i = "string" == typeof e ? this.filter(e) : N(e) && j(e.item) ? d.call(e) : r(e);
                  this.forEach(function (e) {
                    i.indexOf(e) < 0 && n.push(e)
                  })
                }
                return r(n)
              },
              has: function (e) {
                return this.filter(function () {
                  return I(e) ? r.contains(this, e) : r(this).find(e).size()
                })
              },
              eq: function (e) {
                return -1 === e ? this.slice(e) : this.slice(e, +e + 1)
              },
              first: function () {
                var e = this[0];
                return e && !I(e) ? e : r(e)
              },
              last: function () {
                var e = this[this.length - 1];
                return e && !I(e) ? e : r(e)
              },
              find: function (e) {
                var t = this;
                return e ? "object" == (void 0 === e ? "undefined" : a(e)) ? r(e).filter(function () {
                  var e = this;
                  return c.some.call(t, function (t) {
                    return r.contains(t, e)
                  })
                }) : 1 == this.length ? r(C.qsa(this[0], e)) : this.map(function () {
                  return C.qsa(this, e)
                }) : r()
              },
              closest: function (e, t) {
                var n = []
                  , i = "object" == (void 0 === e ? "undefined" : a(e)) && r(e);
                return this.each(function (r, a) {
                  for (; a && !(i ? i.indexOf(a) >= 0 : C.matches(a, e));)
                    a = a !== t && !M(a) && a.parentNode;
                  a && n.indexOf(a) < 0 && n.push(a)
                }),
                  r(n)
              },
              parents: function (e) {
                for (var t = [], n = this; n.length > 0;)
                  n = r.map(n, function (e) {
                    if ((e = e.parentNode) && !M(e) && t.indexOf(e) < 0)
                      return t.push(e),
                        e
                  });
                return U(t, e)
              },
              parent: function (e) {
                return U(s(this.pluck("parentNode")), e)
              },
              children: function (e) {
                return U(this.map(function () {
                  return V(this)
                }), e)
              },
              contents: function () {
                return this.map(function () {
                  return this.contentDocument || d.call(this.childNodes)
                })
              },
              siblings: function (e) {
                return U(this.map(function (e, t) {
                  return l.call(V(t.parentNode), function (e) {
                    return e !== t
                  })
                }), e)
              },
              empty: function () {
                return this.each(function () {
                  this.innerHTML = ""
                })
              },
              pluck: function (e) {
                return r.map(this, function (t) {
                  return t[e]
                })
              },
              show: function () {
                return this.each(function () {
                  var e, t, n;
                  "none" == this.style.display && (this.style.display = ""),
                  "none" == getComputedStyle(this, "").getPropertyValue("display") && (this.style.display = (e = this.nodeName,
                  p[e] || (t = f.createElement(e),
                    f.body.appendChild(t),
                    n = getComputedStyle(t, "").getPropertyValue("display"),
                    t.parentNode.removeChild(t),
                  "none" == n && (n = "block"),
                    p[e] = n),
                    p[e]))
                })
              },
              replaceWith: function (e) {
                return this.before(e).remove()
              },
              wrap: function (e) {
                var t = j(e);
                if (this[0] && !t)
                  var n = r(e).get(0)
                    , i = n.parentNode || this.length > 1;
                return this.each(function (a) {
                  r(this).wrapAll(t ? e.call(this, a) : i ? n.cloneNode(!0) : n)
                })
              },
              wrapAll: function (e) {
                if (this[0]) {
                  var t;
                  for (r(this[0]).before(e = r(e)); (t = e.children()).length;)
                    e = t.first();
                  r(e).append(this)
                }
                return this
              },
              wrapInner: function (e) {
                var t = j(e);
                return this.each(function (n) {
                  var i = r(this)
                    , a = i.contents()
                    , o = t ? e.call(this, n) : e;
                  a.length ? a.wrapAll(o) : i.append(o)
                })
              },
              unwrap: function () {
                return this.parent().each(function () {
                  r(this).replaceWith(r(this).children())
                }),
                  this
              },
              clone: function () {
                return this.map(function () {
                  return this.cloneNode(!0)
                })
              },
              hide: function () {
                return this.css("display", "none")
              },
              toggle: function (e) {
                return this.each(function () {
                  var n = r(this);
                  (e === t ? "none" == n.css("display") : e) ? n.show() : n.hide()
                })
              },
              prev: function (e) {
                return r(this.pluck("previousElementSibling")).filter(e || "*")
              },
              next: function (e) {
                return r(this.pluck("nextElementSibling")).filter(e || "*")
              },
              html: function (e) {
                return 0 in arguments ? this.each(function (t) {
                  var n = this.innerHTML;
                  r(this).empty().append(q(this, e, t, n))
                }) : 0 in this ? this[0].innerHTML : null
              },
              text: function (e) {
                return 0 in arguments ? this.each(function (t) {
                  var n = q(this, e, t, this.textContent);
                  this.textContent = null == n ? "" : "" + n
                }) : 0 in this ? this.pluck("textContent").join("") : null
              },
              attr: function (e, r) {
                var i;
                return "string" != typeof e || 1 in arguments ? this.each(function (t) {
                  if (1 === this.nodeType)
                    if (I(e))
                      for (n in e)
                        Y(this, n, e[n]);
                    else
                      Y(this, e, q(this, r, t, this.getAttribute(e)))
                }) : 0 in this && 1 == this[0].nodeType && null != (i = this[0].getAttribute(e)) ? i : t
              },
              removeAttr: function (e) {
                return this.each(function () {
                  1 === this.nodeType && e.split(" ").forEach(function (e) {
                    Y(this, e)
                  }, this)
                })
              },
              prop: function (e, t) {
                return "string" != typeof (e = O[e] || e) || 1 in arguments ? this.each(function (r) {
                  if (I(e))
                    for (n in e)
                      this[O[n] || n] = e[n];
                  else
                    this[e] = q(this, t, r, this[e])
                }) : this[0] && this[0][e]
              },
              removeProp: function (e) {
                return e = O[e] || e,
                  this.each(function () {
                    delete this[e]
                  })
              },
              data: function (e, n) {
                var r = "data-" + e.replace(b, "-$1").toLowerCase()
                  , i = 1 in arguments ? this.attr(r, n) : this.attr(r);
                return null !== i ? H(i) : t
              },
              val: function (e) {
                return 0 in arguments ? (null == e && (e = ""),
                  this.each(function (t) {
                    this.value = q(this, e, t, this.value)
                  })) : this[0] && (this[0].multiple ? r(this[0]).find("option").filter(function () {
                  return this.selected
                }).pluck("value") : this[0].value)
              },
              offset: function (t) {
                if (t)
                  return this.each(function (e) {
                    var n = r(this)
                      , i = q(this, t, e, n.offset())
                      , a = n.offsetParent().offset()
                      , o = {
                      top: i.top - a.top,
                      left: i.left - a.left
                    };
                    "static" == n.css("position") && (o.position = "relative"),
                      n.css(o)
                  });
                if (!this.length)
                  return null;
                if (f.documentElement !== this[0] && !r.contains(f.documentElement, this[0]))
                  return {
                    top: 0,
                    left: 0
                  };
                var n = this[0].getBoundingClientRect();
                return {
                  left: n.left + e.pageXOffset,
                  top: n.top + e.pageYOffset,
                  width: Math.round(n.width),
                  height: Math.round(n.height)
                }
              },
              css: function (e, t) {
                if (arguments.length < 2) {
                  var i = this[0];
                  if ("string" == typeof e) {
                    if (!i)
                      return;
                    return i.style[o(e)] || getComputedStyle(i, "").getPropertyValue(e)
                  }
                  if (A(e)) {
                    if (!i)
                      return;
                    var a = {}
                      , s = getComputedStyle(i, "");
                    return r.each(e, function (e, t) {
                      a[t] = i.style[o(t)] || s.getPropertyValue(t)
                    }),
                      a
                  }
                }
                var c = "";
                if ("string" == P(e))
                  t || 0 === t ? c = F(e) + ":" + $(e, t) : this.each(function () {
                    this.style.removeProperty(F(e))
                  });
                else
                  for (n in e)
                    e[n] || 0 === e[n] ? c += F(n) + ":" + $(n, e[n]) + ";" : this.each(function () {
                      this.style.removeProperty(F(n))
                    });
                return this.each(function () {
                  this.style.cssText += ";" + c
                })
              },
              index: function (e) {
                return e ? this.indexOf(r(e)[0]) : this.parent().children().indexOf(this[0])
              },
              hasClass: function (e) {
                return !!e && c.some.call(this, function (e) {
                  return this.test(K(e))
                }, B(e))
              },
              addClass: function (e) {
                return e ? this.each(function (t) {
                  if ("className" in this) {
                    i = [];
                    var n = K(this)
                      , a = q(this, e, t, n);
                    a.split(/\s+/g).forEach(function (e) {
                      r(this).hasClass(e) || i.push(e)
                    }, this),
                    i.length && K(this, n + (n ? " " : "") + i.join(" "))
                  }
                }) : this
              },
              removeClass: function (e) {
                return this.each(function (n) {
                  if ("className" in this) {
                    if (e === t)
                      return K(this, "");
                    i = K(this),
                      q(this, e, n, i).split(/\s+/g).forEach(function (e) {
                        i = i.replace(B(e), " ")
                      }),
                      K(this, i.trim())
                  }
                })
              },
              toggleClass: function (e, n) {
                return e ? this.each(function (i) {
                  var a = r(this)
                    , o = q(this, e, i, K(this));
                  o.split(/\s+/g).forEach(function (e) {
                    (n === t ? !a.hasClass(e) : n) ? a.addClass(e) : a.removeClass(e)
                  })
                }) : this
              },
              scrollTop: function (e) {
                if (this.length) {
                  var n = "scrollTop" in this[0];
                  return e === t ? n ? this[0].scrollTop : this[0].pageYOffset : this.each(n ? function () {
                      this.scrollTop = e
                    }
                    : function () {
                      this.scrollTo(this.scrollX, e)
                    }
                  )
                }
              },
              scrollLeft: function (e) {
                if (this.length) {
                  var n = "scrollLeft" in this[0];
                  return e === t ? n ? this[0].scrollLeft : this[0].pageXOffset : this.each(n ? function () {
                      this.scrollLeft = e
                    }
                    : function () {
                      this.scrollTo(e, this.scrollY)
                    }
                  )
                }
              },
              position: function () {
                if (this.length) {
                  var e = this[0]
                    , t = this.offsetParent()
                    , n = this.offset()
                    , i = w.test(t[0].nodeName) ? {
                    top: 0,
                    left: 0
                  } : t.offset();
                  return n.top -= parseFloat(r(e).css("margin-top")) || 0,
                    n.left -= parseFloat(r(e).css("margin-left")) || 0,
                    i.top += parseFloat(r(t[0]).css("border-top-width")) || 0,
                    i.left += parseFloat(r(t[0]).css("border-left-width")) || 0,
                    {
                      top: n.top - i.top,
                      left: n.left - i.left
                    }
                }
              },
              offsetParent: function () {
                return this.map(function () {
                  for (var e = this.offsetParent || f.body; e && !w.test(e.nodeName) && "static" == r(e).css("position");)
                    e = e.offsetParent;
                  return e
                })
              }
            },
            r.fn.detach = r.fn.remove,
            ["width", "height"].forEach(function (e) {
              var n = e.replace(/./, function (e) {
                return e[0].toUpperCase()
              });
              r.fn[e] = function (i) {
                var a, o = this[0];
                return i === t ? L(o) ? o["inner" + n] : M(o) ? o.documentElement["scroll" + n] : (a = this.offset()) && a[e] : this.each(function (t) {
                  (o = r(this)).css(e, q(this, i, t, o[e]()))
                })
              }
            }),
            ["after", "prepend", "before", "append"].forEach(function (n, i) {
              var a = i % 2;
              r.fn[n] = function () {
                var n, o, s = r.map(arguments, function (e) {
                  var i = [];
                  return "array" == (n = P(e)) ? (e.forEach(function (e) {
                    return e.nodeType !== t ? i.push(e) : r.zepto.isZ(e) ? i = i.concat(e.get()) : void (i = i.concat(C.fragment(e)))
                  }),
                    i) : "object" == n || null == e ? e : C.fragment(e)
                }), c = this.length > 1;
                return s.length < 1 ? this : this.each(function (t, n) {
                  o = a ? n : n.parentNode,
                    n = 0 == i ? n.nextSibling : 1 == i ? n.firstChild : 2 == i ? n : null;
                  var u = r.contains(f.documentElement, o);
                  s.forEach(function (t) {
                    if (c)
                      t = t.cloneNode(!0);
                    else if (!o)
                      return r(t).remove();
                    o.insertBefore(t, n),
                    u && function i(e, t) {
                      t(e);
                      for (var n = 0, r = e.childNodes.length; n < r; n++)
                        i(e.childNodes[n], t)
                    }(t, function (t) {
                      if (!(null == t.nodeName || "SCRIPT" !== t.nodeName.toUpperCase() || t.type && "text/javascript" !== t.type || t.src)) {
                        var n = t.ownerDocument ? t.ownerDocument.defaultView : e;
                        n.eval.call(n, t.innerHTML)
                      }
                    })
                  })
                })
              }
                ,
                r.fn[a ? n + "To" : "insert" + (i ? "Before" : "After")] = function (e) {
                  return r(e)[n](this),
                    this
                }
            }),
            C.Z.prototype = W.prototype = r.fn,
            C.uniq = s,
            C.deserializeValue = H,
            r.zepto = C,
            r
        }(),
        e.Zepto = t,
      e.$ === undefined && (e.$ = t),
        function (t) {
          var n, r = 1, i = Array.prototype.slice, a = t.isFunction, o = function (e) {
            return "string" == typeof e
          }, s = {}, c = {}, u = "onfocusin" in e, l = {
            focus: "focusin",
            blur: "focusout"
          }, d = {
            mouseenter: "mouseover",
            mouseleave: "mouseout"
          };

          function f(e) {
            return e._zid || (e._zid = r++)
          }

          function p(e, t, n, r) {
            if ((t = h(t)).ns)
              var i = (a = t.ns,
                new RegExp("(?:^| )" + a.replace(" ", " .* ?") + "(?: |$)"));
            var a;
            return (s[f(e)] || []).filter(function (e) {
              return e && (!t.e || e.e == t.e) && (!t.ns || i.test(e.ns)) && (!n || f(e.fn) === f(n)) && (!r || e.sel == r)
            })
          }

          function h(e) {
            var t = ("" + e).split(".");
            return {
              e: t[0],
              ns: t.slice(1).sort().join(" ")
            }
          }

          function g(e, t) {
            return e.del && !u && e.e in l || !!t
          }

          function m(e) {
            return d[e] || u && l[e] || e
          }

          function v(e, r, i, a, o, c, u) {
            var l = f(e)
              , p = s[l] || (s[l] = []);
            r.split(/\s/).forEach(function (r) {
              if ("ready" == r)
                return t(document).ready(i);
              var s = h(r);
              s.fn = i,
                s.sel = o,
              s.e in d && (i = function (e) {
                  var n = e.relatedTarget;
                  if (!n || n !== this && !t.contains(this, n))
                    return s.fn.apply(this, arguments)
                }
              ),
                s.del = c;
              var l = c || i;
              s.proxy = function (t) {
                if (!(t = _(t)).isImmediatePropagationStopped()) {
                  t.data = a;
                  var r = l.apply(e, t._args == n ? [t] : [t].concat(t._args));
                  return !1 === r && (t.preventDefault(),
                    t.stopPropagation()),
                    r
                }
              }
                ,
                s.i = p.length,
                p.push(s),
              "addEventListener" in e && e.addEventListener(m(s.e), s.proxy, g(s, u))
            })
          }

          function y(e, t, n, r, i) {
            var a = f(e);
            (t || "").split(/\s/).forEach(function (t) {
              p(e, t, n, r).forEach(function (t) {
                delete s[a][t.i],
                "removeEventListener" in e && e.removeEventListener(m(t.e), t.proxy, g(t, i))
              })
            })
          }

          c.click = c.mousedown = c.mouseup = c.mousemove = "MouseEvents",
            t.event = {
              add: v,
              remove: y
            },
            t.proxy = function (e, n) {
              var r = 2 in arguments && i.call(arguments, 2);
              if (a(e)) {
                var s = function () {
                  return e.apply(n, r ? r.concat(i.call(arguments)) : arguments)
                };
                return s._zid = f(e),
                  s
              }
              if (o(n))
                return r ? (r.unshift(e[n], e),
                  t.proxy.apply(null, r)) : t.proxy(e[n], e);
              throw new TypeError("expected function")
            }
            ,
            t.fn.bind = function (e, t, n) {
              return this.on(e, t, n)
            }
            ,
            t.fn.unbind = function (e, t) {
              return this.off(e, t)
            }
            ,
            t.fn.one = function (e, t, n, r) {
              return this.on(e, t, n, r, 1)
            }
          ;
          var w = function () {
            return !0
          }
            , b = function () {
            return !1
          }
            , k = /^([A-Z]|returnValue$|layer[XY]$|webkitMovement[XY]$)/
            , E = {
            preventDefault: "isDefaultPrevented",
            stopImmediatePropagation: "isImmediatePropagationStopped",
            stopPropagation: "isPropagationStopped"
          };

          function _(e, r) {
            if (r || !e.isDefaultPrevented) {
              r || (r = e),
                t.each(E, function (t, n) {
                  var i = r[t];
                  e[t] = function () {
                    return this[n] = w,
                    i && i.apply(r, arguments)
                  }
                    ,
                    e[n] = b
                });
              try {
                e.timeStamp || (e.timeStamp = Date.now())
              } catch (i) {
              }
              (r.defaultPrevented !== n ? r.defaultPrevented : "returnValue" in r ? !1 === r.returnValue : r.getPreventDefault && r.getPreventDefault()) && (e.isDefaultPrevented = w)
            }
            return e
          }

          function T(e) {
            var t, r = {
              originalEvent: e
            };
            for (t in e)
              k.test(t) || e[t] === n || (r[t] = e[t]);
            return _(r, e)
          }

          t.fn.delegate = function (e, t, n) {
            return this.on(t, e, n)
          }
            ,
            t.fn.undelegate = function (e, t, n) {
              return this.off(t, e, n)
            }
            ,
            t.fn.live = function (e, n) {
              return t(document.body).delegate(this.selector, e, n),
                this
            }
            ,
            t.fn.die = function (e, n) {
              return t(document.body).undelegate(this.selector, e, n),
                this
            }
            ,
            t.fn.on = function (e, r, s, c, u) {
              var l, d, f = this;
              return e && !o(e) ? (t.each(e, function (e, t) {
                f.on(e, r, s, t, u)
              }),
                f) : (o(r) || a(c) || !1 === c || (c = s,
                s = r,
                r = n),
              c !== n && !1 !== s || (c = s,
                s = n),
              !1 === c && (c = b),
                f.each(function (n, a) {
                  u && (l = function (e) {
                      return y(a, e.type, c),
                        c.apply(this, arguments)
                    }
                  ),
                  r && (d = function (e) {
                      var n, o = t(e.target).closest(r, a).get(0);
                      if (o && o !== a)
                        return n = t.extend(T(e), {
                          currentTarget: o,
                          liveFired: a
                        }),
                          (l || c).apply(o, [n].concat(i.call(arguments, 1)))
                    }
                  ),
                    v(a, e, c, s, r, d || l)
                }))
            }
            ,
            t.fn.off = function (e, r, i) {
              var s = this;
              return e && !o(e) ? (t.each(e, function (e, t) {
                s.off(e, r, t)
              }),
                s) : (o(r) || a(i) || !1 === i || (i = r,
                r = n),
              !1 === i && (i = b),
                s.each(function () {
                  y(this, e, i, r)
                }))
            }
            ,
            t.fn.trigger = function (e, n) {
              return (e = o(e) || t.isPlainObject(e) ? t.Event(e) : _(e))._args = n,
                this.each(function () {
                  e.type in l && "function" == typeof this[e.type] ? this[e.type]() : "dispatchEvent" in this ? this.dispatchEvent(e) : t(this).triggerHandler(e, n)
                })
            }
            ,
            t.fn.triggerHandler = function (e, n) {
              var r, i;
              return this.each(function (a, s) {
                (r = T(o(e) ? t.Event(e) : e))._args = n,
                  r.target = s,
                  t.each(p(s, e.type || e), function (e, t) {
                    if (i = t.proxy(r),
                      r.isImmediatePropagationStopped())
                      return !1
                  })
              }),
                i
            }
            ,
            "focusin focusout focus blur load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select keydown keypress keyup error".split(" ").forEach(function (e) {
              t.fn[e] = function (t) {
                return 0 in arguments ? this.bind(e, t) : this.trigger(e)
              }
            }),
            t.Event = function (e, t) {
              o(e) || (e = (t = e).type);
              var n = document.createEvent(c[e] || "Events")
                , r = !0;
              if (t)
                for (var i in t)
                  "bubbles" == i ? r = !!t[i] : n[i] = t[i];
              return n.initEvent(e, r, !0),
                _(n)
            }
        }(t),
        function (t) {
          var n, r, i = +new Date, a = e.document, o = /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
            s = /^(?:text|application)\/javascript/i, c = /^(?:text|application)\/xml/i, u = "application/json",
            l = "text/html", d = /^\s*$/, f = a.createElement("a");

          function p(e, n, r, i) {
            if (e.global)
              return function (e, n, r) {
                var i = t.Event(n);
                return t(e).trigger(i, r),
                  !i.isDefaultPrevented()
              }(n || a, r, i)
          }

          function h(e, t) {
            var n = t.context;
            if (!1 === t.beforeSend.call(n, e, t) || !1 === p(t, n, "ajaxBeforeSend", [e, t]))
              return !1;
            p(t, n, "ajaxSend", [e, t])
          }

          function g(e, t, n, r) {
            var i = n.context;
            n.success.call(i, e, "success", t),
            r && r.resolveWith(i, [e, "success", t]),
              p(n, i, "ajaxSuccess", [t, n, e]),
              v("success", t, n)
          }

          function m(e, t, n, r, i) {
            var a = r.context;
            r.error.call(a, n, t, e),
            i && i.rejectWith(a, [n, t, e]),
              p(r, a, "ajaxError", [n, r, e || t]),
              v(t, n, r)
          }

          function v(e, n, r) {
            var i = r.context;
            r.complete.call(i, n, e),
              p(r, i, "ajaxComplete", [n, r]),
              function (e) {
                e.global && !--t.active && p(e, null, "ajaxStop")
              }(r)
          }

          function y() {
          }

          function w(e, t) {
            return "" == t ? e : (e + "&" + t).replace(/[&?]{1,2}/, "?")
          }

          function b(e, n, r, i) {
            return t.isFunction(n) && (i = r,
              r = n,
              n = undefined),
            t.isFunction(r) || (i = r,
              r = undefined),
              {
                url: e,
                data: n,
                success: r,
                dataType: i
              }
          }

          f.href = e.location.href,
            t.active = 0,
            t.ajaxJSONP = function (n, r) {
              if (!("type" in n))
                return t.ajax(n);
              var o, s, c = n.jsonpCallback, u = (t.isFunction(c) ? c() : c) || "Zepto" + i++,
                l = a.createElement("script"), d = e[u], f = function (e) {
                  t(l).triggerHandler("error", e || "abort")
                }, p = {
                  abort: f
                };
              return r && r.promise(p),
                t(l).on("load error", function (i, a) {
                  clearTimeout(s),
                    t(l).off().remove(),
                    "error" != i.type && o ? g(o[0], p, n, r) : m(null, a || "error", p, n, r),
                    e[u] = d,
                  o && t.isFunction(d) && d(o[0]),
                    d = o = undefined
                }),
                !1 === h(p, n) ? (f("abort"),
                  p) : (e[u] = function () {
                  o = arguments
                }
                  ,
                  l.src = n.url.replace(/\?(.+)=\?/, "?$1=" + u),
                  a.head.appendChild(l),
                n.timeout > 0 && (s = setTimeout(function () {
                  f("timeout")
                }, n.timeout)),
                  p)
            }
            ,
            t.ajaxSettings = {
              type: "GET",
              beforeSend: y,
              success: y,
              error: y,
              complete: y,
              context: null,
              global: !0,
              xhr: function () {
                return new e.XMLHttpRequest
              },
              accepts: {
                script: "text/javascript, application/javascript, application/x-javascript",
                json: u,
                xml: "application/xml, text/xml",
                html: l,
                text: "text/plain"
              },
              crossDomain: !1,
              timeout: 0,
              processData: !0,
              cache: !0,
              dataFilter: y
            },
            t.ajax = function (i) {
              var o, v, b = t.extend({}, i || {}), k = t.Deferred && t.Deferred();
              for (n in t.ajaxSettings)
                b[n] === undefined && (b[n] = t.ajaxSettings[n]);
              !function (e) {
                e.global && 0 == t.active++ && p(e, null, "ajaxStart")
              }(b),
              b.crossDomain || ((o = a.createElement("a")).href = b.url,
                o.href = o.href,
                b.crossDomain = f.protocol + "//" + f.host != o.protocol + "//" + o.host),
              b.url || (b.url = e.location.toString()),
              (v = b.url.indexOf("#")) > -1 && (b.url = b.url.slice(0, v)),
                function (e) {
                  e.processData && e.data && "string" != t.type(e.data) && (e.data = t.param(e.data, e.traditional)),
                  !e.data || e.type && "GET" != e.type.toUpperCase() && "jsonp" != e.dataType || (e.url = w(e.url, e.data),
                    e.data = undefined)
                }(b);
              var E = b.dataType
                , _ = /\?.+=\?/.test(b.url);
              if (_ && (E = "jsonp"),
              !1 !== b.cache && (i && !0 === i.cache || "script" != E && "jsonp" != E) || (b.url = w(b.url, "_=" + Date.now())),
              "jsonp" == E)
                return _ || (b.url = w(b.url, b.jsonp ? b.jsonp + "=?" : !1 === b.jsonp ? "" : "callback=?")),
                  t.ajaxJSONP(b, k);
              var T, S = b.accepts[E], R = {}, x = function (e, t) {
                  R[e.toLowerCase()] = [e, t]
                }, C = /^([\w-]+:)\/\//.test(b.url) ? RegExp.$1 : e.location.protocol, z = b.xhr(),
                O = z.setRequestHeader;
              if (k && k.promise(z),
              b.crossDomain || x("X-Requested-With", "XMLHttpRequest"),
                x("Accept", S || "*/*"),
              (S = b.mimeType || S) && (S.indexOf(",") > -1 && (S = S.split(",", 2)[0]),
              z.overrideMimeType && z.overrideMimeType(S)),
              (b.contentType || !1 !== b.contentType && b.data && "GET" != b.type.toUpperCase()) && x("Content-Type", b.contentType || "application/x-www-form-urlencoded"),
                b.headers)
                for (r in b.headers)
                  x(r, b.headers[r]);
              if (z.setRequestHeader = x,
                z.onreadystatechange = function () {
                  if (4 == z.readyState) {
                    z.onreadystatechange = y,
                      clearTimeout(T);
                    var e, n = !1;
                    if (z.status >= 200 && z.status < 300 || 304 == z.status || 0 == z.status && "file:" == C) {
                      if (E = E || ((r = b.mimeType || z.getResponseHeader("content-type")) && (r = r.split(";", 2)[0]),
                      r && (r == l ? "html" : r == u ? "json" : s.test(r) ? "script" : c.test(r) && "xml") || "text"),
                      "arraybuffer" == z.responseType || "blob" == z.responseType)
                        e = z.response;
                      else {
                        e = z.responseText;
                        try {
                          e = function (e, t, n) {
                            if (n.dataFilter == y)
                              return e;
                            var r = n.context;
                            return n.dataFilter.call(r, e, t)
                          }(e, E, b),
                            "script" == E ? (0,
                              eval)(e) : "xml" == E ? e = z.responseXML : "json" == E && (e = d.test(e) ? null : t.parseJSON(e))
                        } catch (i) {
                          n = i
                        }
                        if (n)
                          return m(n, "parsererror", z, b, k)
                      }
                      g(e, z, b, k)
                    } else
                      m(z.statusText || null, z.status ? "error" : "abort", z, b, k)
                  }
                  var r
                }
                ,
              !1 === h(z, b))
                return z.abort(),
                  m(null, "abort", z, b, k),
                  z;
              var A = !("async" in b) || b.async;
              if (z.open(b.type, b.url, A, b.username, b.password),
                b.xhrFields)
                for (r in b.xhrFields)
                  z[r] = b.xhrFields[r];
              for (r in R)
                O.apply(z, R[r]);
              return b.timeout > 0 && (T = setTimeout(function () {
                z.onreadystatechange = y,
                  z.abort(),
                  m(null, "timeout", z, b, k)
              }, b.timeout)),
                z.send(b.data ? b.data : null),
                z
            }
            ,
            t.get = function () {
              return t.ajax(b.apply(null, arguments))
            }
            ,
            t.post = function () {
              var e = b.apply(null, arguments);
              return e.type = "POST",
                t.ajax(e)
            }
            ,
            t.getJSON = function () {
              var e = b.apply(null, arguments);
              return e.dataType = "json",
                t.ajax(e)
            }
            ,
            t.fn.load = function (e, n, r) {
              if (!this.length)
                return this;
              var i, a = this, s = e.split(/\s/), c = b(e, n, r), u = c.success;
              return s.length > 1 && (c.url = s[0],
                i = s[1]),
                c.success = function (e) {
                  a.html(i ? t("<div>").html(e.replace(o, "")).find(i) : e),
                  u && u.apply(a, arguments)
                }
                ,
                t.ajax(c),
                this
            }
          ;
          var k = encodeURIComponent;
          t.param = function (e, n) {
            var r = [];
            return r.add = function (e, n) {
              t.isFunction(n) && (n = n()),
              null == n && (n = ""),
                this.push(k(e) + "=" + k(n))
            }
              ,
              function i(e, n, r, a) {
                var o, s = t.isArray(n), c = t.isPlainObject(n);
                t.each(n, function (n, u) {
                  o = t.type(u),
                  a && (n = r ? a : a + "[" + (c || "object" == o || "array" == o ? n : "") + "]"),
                    !a && s ? e.add(u.name, u.value) : "array" == o || !r && "object" == o ? i(e, u, r, n) : e.add(n, u)
                })
              }(r, e, n),
              r.join("&").replace(/%20/g, "+")
          }
        }(t),
        function (e, t) {
          var n, r, i, o, s, c, u, l, d, f, p = "", h = document.createElement("div"),
            g = /^((translate|rotate|scale)(X|Y|Z|3d)?|matrix(3d)?|perspective|skew(X|Y)?)$/i, m = {};

          function v(e) {
            return n ? n + e : e.toLowerCase()
          }

          void 0 === h.style.transform && e.each({
            Webkit: "webkit",
            Moz: "",
            O: "o"
          }, function (e, t) {
            if (void 0 !== h.style[e + "TransitionProperty"])
              return p = "-" + e.toLowerCase() + "-",
                n = t,
                !1
          }),
            r = p + "transform",
            m[i = p + "transition-property"] = m[o = p + "transition-duration"] = m[c = p + "transition-delay"] = m[s = p + "transition-timing-function"] = m[u = p + "animation-name"] = m[l = p + "animation-duration"] = m[f = p + "animation-delay"] = m[d = p + "animation-timing-function"] = "",
            e.fx = {
              off: void 0 === n && void 0 === h.style.transitionProperty,
              speeds: {
                _default: 400,
                fast: 200,
                slow: 600
              },
              cssPrefix: p,
              transitionEnd: v("TransitionEnd"),
              animationEnd: v("AnimationEnd")
            },
            e.fn.animate = function (t, n, r, i, a) {
              return e.isFunction(n) && (i = n,
                r = void 0,
                n = void 0),
              e.isFunction(r) && (i = r,
                r = void 0),
              e.isPlainObject(n) && (r = n.easing,
                i = n.complete,
                a = n.delay,
                n = n.duration),
              n && (n = ("number" == typeof n ? n : e.fx.speeds[n] || e.fx.speeds._default) / 1e3),
              a && (a = parseFloat(a) / 1e3),
                this.anim(t, n, r, i, a)
            }
            ,
            e.fn.anim = function (t, n, p, h, v) {
              var y, w, b, k = {}, E = "", _ = this, T = e.fx.transitionEnd, S = !1;
              if (void 0 === n && (n = e.fx.speeds._default / 1e3),
              void 0 === v && (v = 0),
              e.fx.off && (n = 0),
              "string" == typeof t)
                k[u] = t,
                  k[l] = n + "s",
                  k[f] = v + "s",
                  k[d] = p || "linear",
                  T = e.fx.animationEnd;
              else {
                for (y in w = [],
                  t)
                  g.test(y) ? E += y + "(" + t[y] + ") " : (k[y] = t[y],
                    w.push(y.replace(/([A-Z])/g, "-$1").toLowerCase()));
                E && (k[r] = E,
                  w.push(r)),
                n > 0 && "object" === (void 0 === t ? "undefined" : a(t)) && (k[i] = w.join(", "),
                  k[o] = n + "s",
                  k[c] = v + "s",
                  k[s] = p || "linear")
              }
              return b = function (t) {
                if (void 0 !== t) {
                  if (t.target !== t.currentTarget)
                    return;
                  e(t.target).unbind(T, b)
                } else
                  e(this).unbind(T, b);
                S = !0,
                  e(this).css(m),
                h && h.call(this)
              }
                ,
              n > 0 && (this.bind(T, b),
                setTimeout(function () {
                  S || b.call(_)
                }, 1e3 * (n + v) + 25)),
              this.size() && this.get(0).clientLeft,
                this.css(k),
              n <= 0 && setTimeout(function () {
                _.each(function () {
                  b.call(this)
                })
              }, 0),
                this
            }
            ,
            h = null
        }(t),
        t;
      var e, t
    }
      .call(t, n, t, e)) === undefined || (e.exports = r)
  }
  , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , function (e, t) {
  }
]);
