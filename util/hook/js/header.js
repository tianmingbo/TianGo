(function () {
  'use strict';
  var org = window.XMLHttpRequest.prototype.setRequestHeader;
  window.XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
    if (key === 'lxlxlx') {
      debugger;
    }
    return org.apply(this, arguments);
  }
})();