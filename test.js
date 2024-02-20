function test(a, b, c) {
  let d = "", e, f, h, m, k = 187, l = 187;
  f = a.length;
  h = b.length;
  m = c.length;
  e = f > h ? f : h;
  for (var g = 0; g < e; g++)
    l = k = 187,
      g >= f ? l = b.charCodeAt(g) : g >= h ? k = a.charCodeAt(g) : (k = a.charCodeAt(g),
        l = b.charCodeAt(g)),
      d += c.charAt((k ^ l) % m);
  return d;
}

