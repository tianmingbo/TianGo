// setTimeout(function () {
//   console.log('yibu')
// }, 3000);
// console.log("xianzhixiang"); //js是异步执行，所以会先执行这行，三秒后，再执行前边的
//
// //promise
// setTimeout(function () {
//   console.log("First");
//   setTimeout(function () {
//     console.log("Second");
//     setTimeout(function () {
//       console.log("Third");
//     }, 3000);
//   }, 4000);
// }, 1000);
//
// new Promise(function (resolve, reject) {
//   setTimeout(function () {
//     console.log('first');
//     resolve();
//   }, 1000)
// }).then(function () {
//   return new Promise(function (resolve, reject) {
//     setTimeout(function () {
//       console.log('second');
//       resolve();
//     }, 2000)
//   })
// }).then(function () {
//   setTimeout(function () {
//     console.log('third')
//   }, 2000);
// });
//
// //promise只有一个参数，是一个函数，这个函数在构造之后会直接被异步执行
// new Promise(function (resolve, reject) {
//   console.log('running');
// })
//
// new Promise(function (resolve, reject) {
//   let a = 1;
//   let b = 0;
//   if (b === 0) {
//     reject('divide zero')
//   } else {
//     resolve(a / b);
//   }
// }).then(function (value) {
//   //正常执行
//   console.log('a/b=', value);
// }).catch(function (err) {
//   //捕获到错误
//   console.log(err);
// }).finally(function () {
//   //无论如何,都会执行
//   console.log('end');
// })

//******************************await ,async
// function test(delay, message) {
//   return new Promise(function (resolve, reject) {
//     setTimeout(function () {
//       console.log(message);
//       resolve();
//     }, delay);
//   });
// }
// async function print(){
//   await test(1000,'1');
//   await test(1000,'2');
//   await test(1000,'3');
// }
// print()


//********************** try catch
async function asyncFunc() {
  try {
    await new Promise(function (resolve, reject) {
      reject('error');
    })
  } catch (e) {
    console.log(e);
  }
}

async function asyncFunc2() {
  let value = await new Promise(
    function (resolve, reject) {
      resolve("Return value");
    }
  );
  //正常返回，会获取到返回值
  console.log(value);
}

asyncFunc();
asyncFunc2()