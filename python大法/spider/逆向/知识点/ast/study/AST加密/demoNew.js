window["Date"]["prototype"]["format"] = function (formatStr) {
  var str = formatStr;
  var Week = ['日', '一', '二', '三', '四', '五', '六'];
  str = str["replace"](/yyyy|YYYY/, this["getFullYear"]());
  str = str["replace"](/MM/, this["getMonth"]() + (915611 ^ 915610) > (535403 ^ 535394) ? (this["getMonth"]() + (281720 ^ 281721))["toString"]() : '0' + (this["getMonth"]() + (956931 ^ 956930)));
  str = str["replace"](/dd|DD/, this["getDate"]() > (651014 ^ 651023) ? (this["getDate"]() + (215051 ^ 215050))["toString"]() : '0' + this["getDate"]());
  return str;
};

console["log"](new window["Date"]()["format"]('yyyy-MM-dd'));