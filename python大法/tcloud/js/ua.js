var At = (Math.round,
    Math.min,
    Math.max,
    Math.random,
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
    , Bt = function (t) {
    for (var e, o, n = String(t), a = 0, r = At, i = ""; n.charAt(0 | a) || (r = "=",
    a % 1); i += r.charAt(63 & e >> 8 - a % 1 * 8)) {
        if (o = n.charCodeAt(a += .75),
            o > 255)
            return "base64encode outside range";
        e = e << 8 | o
    }
    return i
}