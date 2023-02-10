/** apply 作用
 * 改变this指向
 * 将数组入参变为一般入参
 * */
let person = {
  fullName: function () {
    return this.firstName + " " + this.lastName;
  }
}

let personInfo = {
  firstName: "t",
  lastName: 'm'
}

// 当apply调用时，调用apply的函数是谁？(person.fullName)，把这个函数分享给personInfo，让personInfo去调用。

console.log(person.fullName.apply(personInfo))


// call 和 apply的区别 ***********************************
// apply的第二个参数接受的是数组，call不是
person = {
  fullName: function (city, country) {
    return this.firstName + " " + this.lastName + "," + city + "," + country;
  }
}
person1 = {
  firstName: "John",
  lastName: "Doe"
}
console.log(person.fullName.apply(person1, ["Oslo", "Norway"]));
// ********************************************
person = {
  fullName: function (city, country) {
    return this.firstName + " " + this.lastName + "," + city + "," + country;
  }
}
person1 = {
  firstName: "John",
  lastName: "Doe"
}
console.log(person.fullName.call(person1, "Oslo", "Norway"));

//把arguments改为真正的数组*************************
//arguments没有slice方法，通过apply，等于把Array的slice给arguments用了
(function fun() {
  // console.log(arguments.concat([3]))//报错
  const arr = Array.prototype.slice.apply(arguments);
  console.log(arr.concat([3]))//[1,2,3]
})(1, 2)

