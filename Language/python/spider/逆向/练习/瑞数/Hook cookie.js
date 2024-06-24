// ==UserScript==
// @name         Hook document.cookie
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       tian
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function () {
  var cookie_cache = document.cookie;
  Object.defineProperty(document, 'cookie', {
    get: function () {
      console.log("get cookie:", cookie_cache)
      return cookie_cache;
    },
    set: function (val) {
      console.log("setting cookie:", val);
      debugger;
      var cookie = val.split(";")[0];
      var ncookie = cookie.split("=");
      var flag = false;
      var cache = cookie_cache.split(";");
      cache = cache.map(function (a) {
        if (a.split("=")[0] == ncookie[0]) {
          flag = true;
          return cookie;
        }
        return a;
      })
      cookie_cache = cache.join(";");
      if (!flag) {
        cookie_cache += cookie + ";";
      }
      this._value = val;
      return cookie_cache;
    }
  });
})();