/**
 * 原型链的终点是Object
 *
 * prototype属性 js中函数独有的
 * 每个函数的prototype都指向实例的原型对象,
 * 一个函数实例的__proto__就是该函数的 prototype
 *
 *
 * __proto__属性
 * 每个对象（除了null）都有__proto__，这个属性会指向自身的原型对象。在访问一个对象
 * 属性时，如果这个对象的内部不存在这个属性，就会经过__proto__属性到原型对象中寻找.
 * 直到Object
 *
 *
 * constructor属性
 *
 * 每个对象都有constructor属性，如果没有显示定义，就是通过__proto__从原型对象继承而来。
 *
 * 实例对象.__proto__ === 函数.prototype
 * 函数.prototype.constructor === 函数本身
 * */
function Test() {
}

var test = new Test()
console.log(test.__proto__ === Test.prototype) //true
console.log(Test.prototype.constructor === Test)  //true
Test.prototype.name = 'tian';
console.log(test.name) //tian