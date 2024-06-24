//修正数组位置
(function (myArr, num) {
  var fixArray = function (num) {
    while (--num) {
      myArr.push(myArr.shift());
    }
  };
  fixArray(num);
})(arr, 0x10)