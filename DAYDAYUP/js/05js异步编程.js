setTimeout(function () {
  console.log('yibu')
}, 3000);
console.log("xianzhixiang"); //

//promise
setTimeout(function () {
  console.log("First");
  setTimeout(function () {
    console.log("Second");
    setTimeout(function () {
      console.log("Third");
    }, 3000);
  }, 4000);
}, 1000);