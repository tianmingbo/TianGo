var arg1 = "CAB0CFC6996C1B5EAB8602D5BE069C21DD3E0925";
var _0x4818 = ["csKHwqMI", "ZsKJwr8VeAsy", "UcKiN8O/wplwMA==", "JR8CTg==", "YsOnbSEQw7ozwqZKesKUw7kwX8ORIQ==", "w7oVS8OSwoPCl3jChMKhw6HDlsKXw4s/YsOG", "fwVmI1AtwplaY8Otw5cNfSgpw6M=", "OcONwrjCqsKxTGTChsOjEWE8PcOcJ8K6", "U8K5LcOtwpV0EMOkw47DrMOX", "HMO2woHCiMK9SlXClcOoC1k=", "asKIwqMDdgMuPsOKBMKcwrrCtkLDrMKBw64d", "wqImMT0tw6RNw5k=", "DMKcU0JmUwUv", "VjHDlMOHVcONX3fDicKJHQ==", "wqhBH8Knw4TDhSDDgMOdwrjCncOWwphhN8KCGcKqw6dHAU5+wrg2JcKaw4IEJcOcwrRJwoZ0wqF9YgAV", "dzd2w5bDm3jDpsK3wpY=", "w4PDgcKXwo3CkcKLwr5qwrY=", "wrJOTcOQWMOg", "wqTDvcOjw447wr4=", "w5XDqsKhMF1/", "wrAyHsOfwppc", "J3dVPcOxLg==", "wrdHw7p9Zw==", "w4rDo8KmNEw=", "IMKAUkBt", "w6bDrcKQwpVHwpNQwqU=", "d8OsWhAUw7YzwrU=", "wqnCksOeezrDhw==", "UsKnIMKWV8K/", "w4zDocK8NUZv", "c8OxZhAJw6skwqJj", "PcKIw4nCkkVb", "KHgodMO2VQ==", "wpsmwqvDnGFq", "wqLDt8Okw4c=", "w7w1w4PCpsO4wqA=", "wq9FRsOqWMOq", "byBhw7rDm34=", "LHg+S8OtTw==", "wqhOw715dsOH", "U8O7VsO0wqvDvcKuKsOqX8Kr", "Yittw5DDnWnDrA==", "YMKIwqUUfgIk", "aB7DlMODTQ==", "wpfDh8Orw6kk", "w7vCqMOrY8KAVk5OwpnCu8OaXsKZP3DClcKyw6HDrQ==", "wow+w6vDmHpsw7Rtwo98LC7CiG7CksORT8KlW8O5wr3Di8OTHsODeHjDmcKlJsKqVA==", "NwV+", "w7HDrcKtwpJawpZb", "wpQswqvDiHpuw6I=", "YMKUwqMJZQ==", "KH1VKcOqKsK1", "fQ5sFUkkwpI=", "wrvCrcOBR8Kk", "M3w0fQ==", "w6xXwqPDvMOFwo5d"];

(function (_0x4c97f0, _0x1742fd) {
  var _0x4db1c = function (_0x48181e) {
    while (--_0x48181e) {
      _0x4c97f0["push"](_0x4c97f0["shift"]());
    }
  };

  var _0x3cd6c6 = function () {
    var _0xb8360b = {
      "data": {
        "key": "cookie",
        "value": "timeout"
      },
      "setCookie": function (_0x20bf34, _0x3e840e, _0x5693d3, _0x5e8b26) {
        _0x5e8b26 = _0x5e8b26 || {};

        var _0xba82f0 = _0x3e840e + "=" + _0x5693d3;

        var _0x5afe31 = 0;

        for (var _0x5afe31 = 0, _0x178627 = _0x20bf34["length"]; _0x5afe31 < _0x178627; _0x5afe31++) {
          var _0x41b2ff = _0x20bf34[_0x5afe31];
          _0xba82f0 += "; " + _0x41b2ff;
          var _0xd79219 = _0x20bf34[_0x41b2ff];

          _0x20bf34["push"](_0xd79219);

          _0x178627 = _0x20bf34["length"];

          if (_0xd79219 !== !![]) {
            _0xba82f0 += "=" + _0xd79219;
          }
        }

        _0x5e8b26["cookie"] = _0xba82f0;
      },
      "removeCookie":function(){return "dev";},
      "getCookie": function (_0x4a11fe, _0x189946) {
        _0x4a11fe = _0x4a11fe || function (_0x6259a2) {
          return _0x6259a2;
        };

        var _0x25af93 = _0x4a11fe(new RegExp("(?:^|; )" + _0x189946["replace"](/([.$?*|{}()[]\/+^])/g, "$1") + "=([^;]*)"));

        var _0x52d57c = function (_0x105f59, _0x3fd789) {
          _0x105f59(++_0x3fd789);
        };

        _0x52d57c(_0x4db1c, _0x1742fd);

        return _0x25af93 ? decodeURIComponent(_0x25af93[1]) : undefined;
      }
    };

    var _0x4a2aed = function () {
      var _0x124d17 = new RegExp("\\w+ *\\(\\) *{\\w+ *['|\"].+['|\"];? *}");

      return _0x124d17["test"](_0xb8360b["removeCookie"]["toString"]()); //判断是不是格式化
    };

    _0xb8360b["updateCookie"] = _0x4a2aed;
    var _0x2d67ec = "";

    var _0x120551 = _0xb8360b["updateCookie"]();

    if (!_0x120551) {
      _0xb8360b["setCookie"](["*"], "counter", 1);
    } else if (_0x120551) {
      _0x2d67ec = _0xb8360b["getCookie"](null, "counter");
    } else {
      _0xb8360b["removeCookie"]();
    }
  };

  _0x3cd6c6();
})(_0x4818, 347);

console.log(_0x4818)