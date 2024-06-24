!function (allModule) {
  function useModule(whichModule) {
    //模块加载器，确定使用哪个模块
    allModule[whichModule].call(null, "hello world!");
  }

  useModule(2)
}([
  function module0(param) {
    console.log("module0: " + param)
  },
  function module1(param) {
    console.log("module1: " + param)
  },
  function module2(param) {
    console.log("module2: " + param)
  },
]);