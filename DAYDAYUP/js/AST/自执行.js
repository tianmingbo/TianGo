//1
(function test() {
    console.log('自执行1')
})();

//2
(function test() {
    console.log('自执行2')
}());

//3
!function test() {
    console.log('自执行3')
}();