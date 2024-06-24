//提供一个接口
// exports.word = function () {
//     console.log('hello tmb')
// }


//********************************************************************

function Hello() {
    var name;
    this.SetName = function (theName) {
        name = theName;
    };
    this.sayHello = function () {
        console.log('hello ' + name);
    };
};
module.exports = Hello;