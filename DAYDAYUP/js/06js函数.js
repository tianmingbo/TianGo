(function () {
  console.log('myself')
})();//自调用函数

const x = (x, y) => x * y; //箭头函数
console.log(x(1, 2))


//获取最大值
a = findMax(1, 123, 500, 115, 44, 88);

function findMax() {
  let i, max = arguments[0];

  if (arguments.length < 2) return max;

  for (i = 0; i < arguments.length; i++) {
    if (arguments[i] > max) {
      max = arguments[i];
    }
  }
  return max;
}
var add = (function () {
    var counter = 0;
    return function () {return counter += 1;}
})();

console.log(add())
console.log(add())
console.log(add())
add();
add();
add();