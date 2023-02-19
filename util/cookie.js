(function () {
  'use strict';
  var org = document.cookie.__lookupSetter__('cookie');
  document.__defineSetter__("cookie", function (cookie) {
    if (cookie.indexOf('yuanren') > -1) {
      debugger;
    }
    org = cookie;
  });
  document.__defineGetter__("cookie", function () {
    return org;
  });
})();