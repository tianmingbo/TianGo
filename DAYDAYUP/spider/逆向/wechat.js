function p(e, t) {
    var n = (65535 & e) + (65535 & t);
    return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
}

function a(e, t, n, o, i, r) {
    return p((r = p(p(t, e), p(o, r))) << i | r >>> 32 - i, n)
}

function l(e, t, n, o, i, r, s) {
    return a(t & n | ~t & o, e, t, i, r, s)
}

function m(e, t, n, o, i, r, s) {
    return a(t & o | n & ~o, e, t, i, r, s)
}

function f(e, t, n, o, i, r, s) {
    return a(t ^ n ^ o, e, t, i, r, s)
}

function g(e, t, n, o, i, r, s) {
    return a(n ^ (t | ~o), e, t, i, r, s)
}

function s(e, t) {
    e[t >> 5] |= 128 << t % 32,
        e[14 + (t + 64 >>> 9 << 4)] = t;
    for (var n, o, i, r, s = 1732584193, a = -271733879, c = -1732584194, u = 271733878, d = 0; d < e.length; d += 16) s = l(n = s, o = a, i = c, r = u, e[d], 7, -680876936),
        u = l(u, s, a, c, e[d + 1], 12, -389564586),
        c = l(c, u, s, a, e[d + 2], 17, 606105819),
        a = l(a, c, u, s, e[d + 3], 22, -1044525330),
        s = l(s, a, c, u, e[d + 4], 7, -176418897),
        u = l(u, s, a, c, e[d + 5], 12, 1200080426),
        c = l(c, u, s, a, e[d + 6], 17, -1473231341),
        a = l(a, c, u, s, e[d + 7], 22, -45705983),
        s = l(s, a, c, u, e[d + 8], 7, 1770035416),
        u = l(u, s, a, c, e[d + 9], 12, -1958414417),
        c = l(c, u, s, a, e[d + 10], 17, -42063),
        a = l(a, c, u, s, e[d + 11], 22, -1990404162),
        s = l(s, a, c, u, e[d + 12], 7, 1804603682),
        u = l(u, s, a, c, e[d + 13], 12, -40341101),
        c = l(c, u, s, a, e[d + 14], 17, -1502002290),
        s = m(s, a = l(a, c, u, s, e[d + 15], 22, 1236535329), c, u, e[d + 1], 5, -165796510),
        u = m(u, s, a, c, e[d + 6], 9, -1069501632),
        c = m(c, u, s, a, e[d + 11], 14, 643717713),
        a = m(a, c, u, s, e[d], 20, -373897302),
        s = m(s, a, c, u, e[d + 5], 5, -701558691),
        u = m(u, s, a, c, e[d + 10], 9, 38016083),
        c = m(c, u, s, a, e[d + 15], 14, -660478335),
        a = m(a, c, u, s, e[d + 4], 20, -405537848),
        s = m(s, a, c, u, e[d + 9], 5, 568446438),
        u = m(u, s, a, c, e[d + 14], 9, -1019803690),
        c = m(c, u, s, a, e[d + 3], 14, -187363961),
        a = m(a, c, u, s, e[d + 8], 20, 1163531501),
        s = m(s, a, c, u, e[d + 13], 5, -1444681467),
        u = m(u, s, a, c, e[d + 2], 9, -51403784),
        c = m(c, u, s, a, e[d + 7], 14, 1735328473),
        s = f(s, a = m(a, c, u, s, e[d + 12], 20, -1926607734), c, u, e[d + 5], 4, -378558),
        u = f(u, s, a, c, e[d + 8], 11, -2022574463),
        c = f(c, u, s, a, e[d + 11], 16, 1839030562),
        a = f(a, c, u, s, e[d + 14], 23, -35309556),
        s = f(s, a, c, u, e[d + 1], 4, -1530992060),
        u = f(u, s, a, c, e[d + 4], 11, 1272893353),
        c = f(c, u, s, a, e[d + 7], 16, -155497632),
        a = f(a, c, u, s, e[d + 10], 23, -1094730640),
        s = f(s, a, c, u, e[d + 13], 4, 681279174),
        u = f(u, s, a, c, e[d], 11, -358537222),
        c = f(c, u, s, a, e[d + 3], 16, -722521979),
        a = f(a, c, u, s, e[d + 6], 23, 76029189),
        s = f(s, a, c, u, e[d + 9], 4, -640364487),
        u = f(u, s, a, c, e[d + 12], 11, -421815835),
        c = f(c, u, s, a, e[d + 15], 16, 530742520),
        s = g(s, a = f(a, c, u, s, e[d + 2], 23, -995338651), c, u, e[d], 6, -198630844),
        u = g(u, s, a, c, e[d + 7], 10, 1126891415),
        c = g(c, u, s, a, e[d + 14], 15, -1416354905),
        a = g(a, c, u, s, e[d + 5], 21, -57434055),
        s = g(s, a, c, u, e[d + 12], 6, 1700485571),
        u = g(u, s, a, c, e[d + 3], 10, -1894986606),
        c = g(c, u, s, a, e[d + 10], 15, -1051523),
        a = g(a, c, u, s, e[d + 1], 21, -2054922799),
        s = g(s, a, c, u, e[d + 8], 6, 1873313359),
        u = g(u, s, a, c, e[d + 15], 10, -30611744),
        c = g(c, u, s, a, e[d + 6], 15, -1560198380),
        a = g(a, c, u, s, e[d + 13], 21, 1309151649),
        s = g(s, a, c, u, e[d + 4], 6, -145523070),
        u = g(u, s, a, c, e[d + 11], 10, -1120210379),
        c = g(c, u, s, a, e[d + 2], 15, 718787259),
        a = g(a, c, u, s, e[d + 9], 21, -343485551),
        s = p(s, n),
        a = p(a, o),
        c = p(c, i),
        u = p(u, r);
    return [s,
        a,
        c,
        u]
}

function c(e) {
    for (var t = '', n = 0; n < 32 * e.length; n += 8) t += String.fromCharCode(e[n >> 5] >>> n % 32 & 255);
    return t
}

function u(e) {
    var t,
        n = [];
    for (n[(e.length >> 2) - 1] = void 0, t = 0; t < n.length; t += 1) n[t] = 0;
    for (t = 0; t < 8 * e.length; t += 8) n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
    return n
}

function o(e) {
    for (var t, n = '0123456789abcdef', o = '', i = 0; i < e.length; i += 1) t = e.charCodeAt(i),
        o += n.charAt(t >>> 4 & 15) + n.charAt(15 & t);
    return o
}

function i(e) {
    return unescape(encodeURIComponent(e))
}

function r(e) {
    return c(s(u(e = i(e)), 8 * e.length))
}

function d(e, t) {
    return function (e, t) {
        var n,
            o = u(e),
            i = [],
            r = [];
        for (i[15] = r[15] = void 0, 16 < o.length && (o = s(o, 8 * e.length)), n = 0; n < 16; n += 1) i[n] = 909522486 ^ o[n],
            r[n] = 1549556828 ^ o[n];
        return t = s(i.concat(u(t)), 512 + 8 * t.length),
            c(s(r.concat(t), 640))
    }(i(e), i(t))
}

function getPwd(e, t, n) {
    return t ? n ? d(t, e) : o(d(t, e)) : n ? r(e) : o(r(e))
}