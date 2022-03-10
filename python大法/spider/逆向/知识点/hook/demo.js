(function () {
    'use strict';

    //hook object的attr对象
    function hook(object, attr) {
        var func = object[attr]
        //改写func输出内容
        object[attr] = function () {
            console.log("hooked", object, attr)
            //重新apply执行原来的函数，新函数接管了原来的函数，这就是hook
            var ret = func.apply(object, arguments)
            debugger
            return ret
        }
    }

    hook(window, 'btoa')
})();