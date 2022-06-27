function CallSecretFunc() {
  Java.perform(function () {
    Java.choose('com.xjb.demo02.MainActivity', {
      onMatch: function (instance) {
        instance.secret();
      },
      onComplete: function () {
        console.log('done');
      }
    })
  })
}

function getTotalValue() {
  Java.perform(function () {
    var MainActivity = Java.use('com.xjb.demo02.MainActivity');
    //对象函数调用
    Java.choose('com.xjb.demo02.MainActivity', {
      onMatch: function (instance) {
        console.log('total value:', instance.total.value);
        console.log('secret func exec success');
      },
      onComplete: function () {
        console.log('search complete');
      }
    })
  })
}

// setImmediate(getTotalValue);
//rpc导出，导出名不可以有下划线和大写
rpc.exports = {
  callsecertfunc: CallSecretFunc,
  gettotalvalue: getTotalValue
}