const jsdom = require('jsdom');
const fs = require('fs');
const { JSDOM } = jsdom;

let resourceLoader = new jsdom.ResourceLoader({
    strictSSL: false,
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    platform: "Win32"
});

let html = fs.readFileSync('./3.html').toString("utf8");
let dom = new JSDOM(html,
    {
        url: "http://www.fangdi.com.cn/",
        contentType: "text/html",
        includeNodeLocations: true,
        storageQuota: 10000000,
        resources: resourceLoader
    }
);
let window = dom.window;
let document = window.document;

// 重写XMLHttpRequest可用于获取请求参数
window.XMLHttpRequest.prototype.open = function () {
    console.log(arguments)
};

function randInt(x, y) {
    if (y <= x) {
        return y + Math.round(Math.random() * (x - y));
    } else {
        return x + Math.round(Math.random() * (y - x))
    }
}

function addEventListener(a, b) {
    if (!window[a] || typeof window[a] === 'function') {
        window[a] = [];
    }
    b.orignTarget = this
    window[a].push(b)
}

let PluginArray = function () {
}
let MimeTypeArray = function () {
}
let width = randInt(480, 800)
let height = randInt(720, 1278)

class Screen {
    constructor() {
        this.availWidth = width;
        this.availHeight = height;
        this.width = width;
        this.height = height;
        this.colorDepth = 24;
        this.pixelDepth = 24;
        this.availTop = 0;
        this.availLeft = 0;
        this.orientation = { angle: 0, type: "landscape-primary", onchange: null };
    }
}

document.documentElement.clientWidth = width;
document.body.clientWidth = width;
document.documentElement.clientHeight = height;
document.body.clientHeight = height;

function Image(x, y) {
    this.prototype = document.createElement('img');
    Object.defineProperty(this.prototype, "width", { value: x ? x : 300, writable: true, configurable: true });
    Object.defineProperty(this.prototype, "height", { value: y ? y : 150, writable: true, configurable: true });
    return this
}

global.Image = Image

let Storage = function () {
    this.getItem = function (t) {
        return this[t]
    }
    this.setItem = function (t, v) {
        this[t] = v
    }
}
let storage = new Storage();

function IDBFactory() {
    this.cmd = function () {
    }
    this.databases = function () {
    }
    this.deleteDatabase = function () {
    }
    this.open = function () {
    }
}

function modify(insert) {
    let querySelector = insert.querySelector
    function newQuerySelector() {
        let res = querySelector.apply(this, arguments);
        if (res) {
            Object.defineProperty(res, "addEventListener", {
                value: addEventListener,
                writable: true,
                configurable: true
            });
        }
        return res
    }

    Object.defineProperty(insert, "addEventListener", { value: addEventListener, writable: true, configurable: true });
    Object.defineProperty(insert, "querySelector", { value: newQuerySelector, writable: true, configurable: true });
    return insert
}

window.modify = modify

let newCreateElement = document.createElement;
let newGetElement = document.getElementById;
let newGetComputedStyle = window.getComputedStyle

function newCreate() {
    let insert = newCreateElement.apply(this, arguments);
    if (arguments[0] === "canvas") {
        let getContext = insert.getContext;

        function newGetContext() {
            let res = getContext.apply(this, arguments);
            if (arguments[0] === '2d' && res) {
                Object.defineProperty(res, "direction", { value: "ltr", writable: true, configurable: true });
            }
            return res ? res : {
                getSupportedExtensions: getSupportedExtensions,
                getExtension: getExtension,
                getParameter: getParameter
            }
        }
        Object.defineProperty(insert, "width", { value: 300, writable: true, configurable: true });
        Object.defineProperty(insert, "height", { value: 150, writable: true, configurable: true });
        Object.defineProperty(insert, "getContext", { value: newGetContext, writable: true, configurable: true });
        Object.defineProperty(insert, "toDataURL", { value: newToDataURL, writable: true, configurable: true });
    } else if (arguments[0] === "img") {
        if (!window.imageElements) {
            window.imageElements = []
        }
        window.imageElements.push(insert);
    }
    insert = modify(insert)
    Object.defineProperty(insert, "addEventListener", { value: addEventListener, writable: true, configurable: true });
    return insert
}

function newGetEle() {
    let insert = newGetElement.apply(this, arguments);
    if (insert) {
        // 可附加其它条件，如需要在某个id的标签加入监听事件，可进行arguments判断
    }
    return insert
}

let cssColor = {
    ActiveBorder: "rgb(255, 255, 255)", ActiveCaption: "rgb(204, 204, 204)",
    AppWorkspace: "rgb(255, 255, 255)", Background: "rgb(99, 99, 206)",
    ButtonFace: "rgb(221, 221, 221)", ButtonHighlight: "rgb(221, 221, 221)",
    ButtonShadow: "rgb(136, 136, 136)", ButtonText: "rgb(0, 0, 0)",
    CaptionText: "rgb(0, 0, 0)", GrayText: "rgb(128, 128, 128)",
    Highlight: "rgb(181, 213, 255)", HighlightText: "rgb(0, 0, 0)",
    InactiveBorder: "rgb(255, 255, 255)", InactiveCaption: "rgb(255, 255, 255)",
    InactiveCaptionText: "rgb(127, 127, 127)", InfoBackground: "rgb(251, 252, 197)",
    InfoText: "rgb(0, 0, 0)", Menu: "rgb(247, 247, 247)", MenuText: "rgb(0, 0, 0)",
    Scrollbar: "rgb(255, 255, 255)", ThreeDDarkShadow: "rgb(102, 102, 102)", ThreeDFace: "rgb(192, 192, 192)",
    ThreeDHighlight: "rgb(221, 221, 221)", ThreeDLightShadow: "rgb(192, 192, 192)", ThreeDShadow: "rgb(136, 136, 136)",
    Window: "rgb(255, 255, 255)", WindowFrame: "rgb(204, 204, 204)", WindowText: "rgb(0, 0, 0)"
};

Object.defineProperty(window, "indexedDB", { value: new IDBFactory(), writable: true, configurable: true });
Object.defineProperty(window, "openDatabase", {
    value: function () {
    }, writable: true, configurable: true
});

Object.defineProperty(window, "setTimeout", { value: setTimeout, writable: true, configurable: true });
Object.defineProperty(window, "setInterval", { value: setInterval, writable: true, configurable: true });
Object.defineProperty(window, "setImmediate", { value: setTimeout, writable: true, configurable: true });
Object.defineProperty(document, "createElement", { value: newCreate, writable: true, configurable: true });
Object.defineProperty(document, "getElementById", { value: newGetEle, writable: true, configurable: true });
Object.defineProperty(document, "addEventListener", { value: addEventListener, writable: true, configurable: true });
Object.defineProperty(document, "compatMode", { value: "CSS1Compat" });  // BackCompat
Object.defineProperty(window, "addEventListener", { value: addEventListener, writable: true, configurable: true });
Object.defineProperty(window, "localStorage", { value: storage, writable: true, configurable: true });
Object.defineProperty(window, "sessionStorage", { value: storage, writable: true, configurable: true });
Object.defineProperty(window, "Storage", { value: storage, writable: true, configurable: true });
Object.defineProperty(window, "screen", { value: new Screen(), writable: true, configurable: true });
Object.defineProperty(window, "innerHeight", { value: height, writable: true, configurable: true });
Object.defineProperty(window, "innerWidth", { value: width, writable: true, configurable: true });
Object.defineProperty(window, "outerHeight", { value: height, writable: true, configurable: true });
Object.defineProperty(window, "outerWidth", { value: width, writable: true, configurable: true });
Object.defineProperty(window.navigator, "plugins", { value: new PluginArray(), writable: true, configurable: true });
Object.defineProperty(window.navigator, "mimeTypes", { value: new MimeTypeArray(), writable: true, configurable: true });
Object.defineProperty(window.navigator, "languages", { value: ["zh-CN", "en-US"], writable: true, configurable: true });
Object.defineProperty(window.navigator, "language", { value: "zh-CN", writable: true, configurable: true });
Object.defineProperty(window.navigator, "cpuClass", {value: "x86"});
Object.defineProperty(window.navigator, "vendor", { value: "Google Inc.", writable: true, configurable: true });
Object.defineProperty(window.navigator, "vendorSub", { value: "", writable: true, configurable: true });
let hard = [8, 12, 16, 24];
let hardware = hard[Math.floor((Math.random() * hard.length))];
Object.defineProperty(window.navigator, "hardwareConcurrency", { value: hardware, writable: true, configurable: true });
Object.defineProperty(window.navigator, "deviceMemory", { value: 32, writable: true, configurable: true });
Object.defineProperty(window.navigator, "maxTouchPoints", { value: 0, writable: true, configurable: true });
Object.defineProperty(window.navigator, "msManipulationViewsEnabled", {
    value: true,
    writable: true,
    configurable: true
});
Object.defineProperty(window.navigator, "connection", {
    value: { effectiveType: "WIFI", downlink: 10, rtt: 50 },
    writable: true,
    configurable: true
});
Object.defineProperty(window.navigator, "webdriver", { value: false, writable: true, configurable: true });
Object.defineProperty(window.navigator, "doNotTrack", { value: null, writable: true, configurable: true });
Object.defineProperty(window.navigator, "appVersion", {
    value: window.navigator.userAgent.split('/').slice(1).join('/'),
    writable: true,
    configurable: true
});
Object.defineProperty(window.navigator, "platform", { value: 'Win32', writable: true, configurable: true });


Object.assign(global, window);

let txt = fs.readFileSync('./3.js').toString('utf8')
window['$_ts'] = {};
eval.apply(global, [txt]);

let scripts = document.getElementsByTagName("script");
for (let i = 0; i < scripts.length; i++) {
    if (scripts[i] && scripts[i].getAttribute('r') === 'm') {
        let innerText = scripts[i].innerHTML
        eval.apply(global, [innerText])
    }
}



// Object.defineProperty(window, "setTimeout", { value: setTimeout, writable: true, configurable: true });
// Object.defineProperty(window, "setInterval", { value: setTimeout, writable: true, configurable: true });
// Object.defineProperty(window, "setImmediate", { value: setTimeout, writable: true, configurable: true });


console.log(document.cookie);
console.log(document.cookie.length);
let res = window.XMLHttpRequest.prototype.open('GET', './modules/top.jsp', false)
console.log(res)
return;