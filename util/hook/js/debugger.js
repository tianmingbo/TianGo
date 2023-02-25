// ==UserScript==
// @name         Hook debugger
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function () {
  console.log("hook debugger注入");
  var _setInterval = setInterval;
  setInterval = function (a, b) {
    return null;
  };

  var _constructor = Function.prototype.constructor;
  Function.prototype.constructor = function (data) {
    if ("debugger" === data) {
      console.log('fake debugger');
      return null;
    }
    return _constructor(data)
  };
})();