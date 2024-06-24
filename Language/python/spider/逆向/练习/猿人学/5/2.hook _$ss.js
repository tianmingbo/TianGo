(function () {
  'use strict'
  Object.defineProperty(window, '_$ss', {
    set: function (val) {
      console.log('Hook捕获到_$ss的值->', val);
      debugger;
    },
  });
})();