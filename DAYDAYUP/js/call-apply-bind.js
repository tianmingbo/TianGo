/**
 * https://mp.weixin.qq.com/s/_-9Ib6H51rWGK60X_g2n1g
 *
 * call() 方法会立即执行这个函数，接受一个多个参数，参数之间用逗号隔开；
 * function.call(thisArg, arg1, arg2, ...)
 * 第一个参数 thisArg 指定了函数体内 this 对象的指向，
 * 如果这个函数处于非严格模式下，指定为 null 或 undefined 时会自动替换为指向全局对象（浏览器中就是 window 对象），
 * 在严格模式下，函数体内的 this 还是为 null。从第二个参数开始往后，每个参数被依次传入函数，
 */
function test() {
  console.log(this.firstName + " " + this.lastName)
}

var data = {firstName: "John", lastName: "Doe"}
test.call(data)  // John Doe 给定了thisArg，函数中的this对象指向了data

/**
 *
 *
 * apply() 方法会立即执行这个函数，接受一个包含多个参数的数组；
 * function.apply(thisArg, [arg1, arg2, ...])
 *
 * 第一个参数 thisArg 与 call() 方法一致，第二个参数为一个带下标的集合，
 * 从 ECMAScript 第5版开始，这个集合可以为数组，也可以为类数组，apply() 方法把这个集合中的元素作为参数传递给被调用的函数.
 */
function test(a, b, c) {
  console.log(a + b + c)
}

test.apply(null, [1, 2, 3])  // 6 第二个参数是数组

function test() {
  console.log(this.firstName + " " + this.lastName)
}

var data = {firstName: "John", lastName: "Doe"}
test.apply(data)  // John Doe test中的this指向data


/**
 * bind() 方法不会立即执行这个函数，返回的是一个修改过后的函数，便于稍后调用，接受的参数和 call() 一样。
 *function.bind(thisArg, arg1, arg2, ...)
 *
 * **/

function test(a, b, c) {
  console.log(a + b + c)
}

test.bind(null, 1, 2, 3)()  // 6

  //把arguments改为真正的数组*************************
  //arguments没有slice方法，通过apply，等于把Array的slice给arguments用了
  (function fun() {
    // console.log(arguments.concat([3]))//报错
    const arr = Array.prototype.slice.apply(arguments);
    console.log(arr.concat([3]))//[1,2,3]
  })(1, 2)

