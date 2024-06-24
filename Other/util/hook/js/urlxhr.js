(function () {
  'use strict';
  var open = window.XMLHttpRequest.prototype.open;
  window.XMLHttpRequest.prototype.open = function (method, url, async) {
    if (url.indexOf("app_id") > -1) {
      debugger;
    }
    return open.apply(this, arguments);
  };
})();