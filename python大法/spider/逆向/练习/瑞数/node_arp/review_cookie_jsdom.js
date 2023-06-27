const jsdom = require('jsdom');
const {JSDOM} = jsdom;

function getCookie(html_text, url, init_localStorage, last_cookie) {

  const dom = new JSDOM(html_text, {
    url: url,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    runScripts: 'dangerously',
    beforeParse(window) {
      // window.alert();
      window.setInterval = function (s, b) {
        eval(s)
      }
      //重写之后进行伪装
      window.setInterval.toString = function () {
        return "function setInterval() { [native code] }"
      }
      window.setTimeout = function (s, b) {
        eval(s)
      }
      window.setTimeout.toString = function () {
        return "function setTimeout() { [native code] }"
      }
      window.localStorage.setItem('$_f0', "bPDdOo9zc_ruy.7NU5ZzQJvtX80");
      window.localStorage.setItem('$_f1', "Dw3Au.0k5f2nKwZPxHMUiHhe47Q");
      window.localStorage.setItem('$_fh0', "t5vkmXwuUtqfnaX42LaFxHN6SJ9");

      if (init_localStorage !== undefined) {
        window.localStorage = init_localStorage;
      }
      if (last_cookie !== undefined) {
        window.document.cookie = last_cookie;
      }

      window.navigator.getBattery = function () {
        return {
          then: function (func) {

            func({level: 1, charging: true, chargingTime: 0, dischargingTime: Infinity,})

          }
        }
      }
    }
  });

  var cookie = dom.window.document.cookie;
  var localStorage = dom.window.localStorage;
  dom.window.close();

  return {
    'cookie': cookie,
    'localStorage': localStorage
  };

}


module.exports = {
  getCookie: getCookie
}
