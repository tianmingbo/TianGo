function callback() {
    n = "_aq_" + Math.floor(1e6 * Math.random());
    return n;
}

var navigator = [];
var screen = [];
var window = [];
var document = [];
var ie_activex = 'ie_activex';
gettokenid = function () {
    var _0x31cex51 = [];
    _0x31cex51['push'](navigator['userAgent']);
    _0x31cex51['push'](navigator['language']);
    _0x31cex51['push'](screen['colorDepth']);
    if (this['screen_resolution']) {
        var _0x31cex52 = this['getScreenResolution']();
        if (typeof _0x31cex52 !== 'undefined') {
            _0x31cex51['push'](_0x31cex52['join']('x'))
        }
    }
    ;
    _0x31cex51['push'](new Date()['getTimezoneOffset']());
    _0x31cex51['push'](this['hasSessionStorage']());
    _0x31cex51['push'](this['hasLocalStorage']());
    _0x31cex51['push'](!!window['indexedDB']);
    if (document['body']) {
        _0x31cex51['push'](typeof (document['body']['addBehavior']))
    } else {
        _0x31cex51['push'](typeof undefined)
    }
    ;
    _0x31cex51['push'](typeof (window['openDatabase']));
    _0x31cex51['push'](navigator['cpuClass']);
    _0x31cex51['push'](navigator['platform']);
    _0x31cex51['push'](navigator['doNotTrack']);
    _0x31cex51['push'](this['getPluginsString']());
    if (this['canvas'] && this['isCanvasSupported']()) {
        _0x31cex51['push'](this['getCanvasFingerprint']())
    }
    ;
    _0x31cex51['push'](this['getRandom']());
    if (this['hasher']) {
        return this['hasher'](_0x31cex51['join']('###'), 31)
    } else {
        return this['murmurhash3_32_gc'](_0x31cex51['join']('###'), 31)
    }
}
murmurhash3_32_gc = function (_0x31cex38, _0x31cex53) {
    var _0x31cex54, _0x31cex55, _0x31cex56, _0x31cex57, _0x31cex58, _0x31cex59, _0x31cex5a, _0x31cex3a;
    _0x31cex54 = _0x31cex38['length'] & 3;
    _0x31cex55 = _0x31cex38['length'] - _0x31cex54;
    _0x31cex56 = _0x31cex53;
    _0x31cex58 = 0xcc9e2d51;
    _0x31cex59 = 0x1b873593;
    _0x31cex3a = 0;
    while (_0x31cex3a < _0x31cex55) {
        _0x31cex5a = ((_0x31cex38['charCodeAt'](_0x31cex3a) & 0xff)) | ((_0x31cex38['charCodeAt'](++_0x31cex3a) & 0xff) << 8) | ((_0x31cex38['charCodeAt'](++_0x31cex3a) & 0xff) << 16) | ((_0x31cex38['charCodeAt'](++_0x31cex3a) & 0xff) << 24);
        ++_0x31cex3a;
        _0x31cex5a = ((((_0x31cex5a & 0xffff) * _0x31cex58) + ((((_0x31cex5a >>> 16) * _0x31cex58) & 0xffff) << 16))) & 0xffffffff;
        _0x31cex5a = (_0x31cex5a << 15) | (_0x31cex5a >>> 17);
        _0x31cex5a = ((((_0x31cex5a & 0xffff) * _0x31cex59) + ((((_0x31cex5a >>> 16) * _0x31cex59) & 0xffff) << 16))) & 0xffffffff;
        _0x31cex56 ^= _0x31cex5a;
        _0x31cex56 = (_0x31cex56 << 13) | (_0x31cex56 >>> 19);
        _0x31cex57 = ((((_0x31cex56 & 0xffff) * 5) + ((((_0x31cex56 >>> 16) * 5) & 0xffff) << 16))) & 0xffffffff;
        _0x31cex56 = (((_0x31cex57 & 0xffff) + 0x6b64) + ((((_0x31cex57 >>> 16) + 0xe654) & 0xffff) << 16))
    }
    ;
    _0x31cex5a = 0;
    switch (_0x31cex54) {
        case 3:
            _0x31cex5a ^= (_0x31cex38['charCodeAt'](_0x31cex3a + 2) & 0xff) << 16;
        case 2:
            _0x31cex5a ^= (_0x31cex38['charCodeAt'](_0x31cex3a + 1) & 0xff) << 8;
        case 1:
            _0x31cex5a ^= (_0x31cex38['charCodeAt'](_0x31cex3a) & 0xff);
            _0x31cex5a = (((_0x31cex5a & 0xffff) * _0x31cex58) + ((((_0x31cex5a >>> 16) * _0x31cex58) & 0xffff) << 16)) & 0xffffffff;
            _0x31cex5a = (_0x31cex5a << 15) | (_0x31cex5a >>> 17);
            _0x31cex5a = (((_0x31cex5a & 0xffff) * _0x31cex59) + ((((_0x31cex5a >>> 16) * _0x31cex59) & 0xffff) << 16)) & 0xffffffff;
            _0x31cex56 ^= _0x31cex5a
    }
    ;
    _0x31cex56 ^= _0x31cex38['length'];
    _0x31cex56 ^= _0x31cex56 >>> 16;
    _0x31cex56 = (((_0x31cex56 & 0xffff) * 0x85ebca6b) + ((((_0x31cex56 >>> 16) * 0x85ebca6b) & 0xffff) << 16)) & 0xffffffff;
    _0x31cex56 ^= _0x31cex56 >>> 13;
    _0x31cex56 = ((((_0x31cex56 & 0xffff) * 0xc2b2ae35) + ((((_0x31cex56 >>> 16) * 0xc2b2ae35) & 0xffff) << 16))) & 0xffffffff;
    _0x31cex56 ^= _0x31cex56 >>> 16;
    return _0x31cex56 >>> 0
}
hasLocalStorage = function () {
    try {
        return !!window['localStorage']
    } catch (e) {
        return true
    }
}
hasSessionStorage = function () {
    try {
        return !!window['sessionStorage']
    } catch (e) {
        return true
    }
}
isCanvasSupported = function () {
    var _0x31cex5b = document['createElement']('canvas');
    return !!(_0x31cex5b['getContext'] && _0x31cex5b['getContext']('2d'))
}
isIE = function () {
    if (navigator['appName'] === 'Microsoft Internet Explorer') {
        return true
    } else {
        if (navigator['appName'] === 'Netscape' && /Trident/ ['test'](navigator['userAgent'])) {
            return true
        }
    }
    ;
    return false
}
getPluginsString = function () {
    if (this['isIE']() && ie_activex) {
        return this['getIEPluginsString']()
    } else {
        return this['getRegularPluginsString']()
    }
}
getRegularPluginsString = function () {
    return this['map'](navigator['plugins'],
        function (_0x31cexb) {
            var _0x31cex5c = this['map'](_0x31cexb,
                function (_0x31cex5d) {
                    return [_0x31cex5d['type'], _0x31cex5d['suffixes']]['join']('~')
                })['join'](',');
            return [_0x31cexb['name'], _0x31cexb['description'], _0x31cex5c]['join']('::')
        },
        this)['join'](';')
}
getIEPluginsString = function () {
    if (window['ActiveXObject']) {
        var _0x31cex5e = ['ShockwaveFlash.ShockwaveFlash', 'AcroPDF.PDF', 'PDF.PdfCtrl', 'QuickTime.QuickTime', 'rmocx.RealPlayer G2 Control', 'rmocx.RealPlayer G2 Control.1', 'RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)', 'RealVideo.RealVideo(tm) ActiveX Control (32-bit)', 'RealPlayer', 'SWCtl.SWCtl', 'WMPlayer.OCX', 'AgControl.AgControl', 'Skype.Detection'];
        return this['map'](_0x31cex5e,
            function (_0x31cex5f) {
                try {
                    new ActiveXObject(_0x31cex5f);
                    return _0x31cex5f
                } catch (e) {
                    return null
                }
            })['join'](';')
    } else {
        return ''
    }
}
getScreenResolution = function () {
    var _0x31cex52;
    if (this['screen_orientation']) {
        _0x31cex52 = (screen['height'] > screen['width']) ? [screen['height'], screen['width']] : [screen['width'], screen['height']]
    } else {
        _0x31cex52 = [screen['height'], screen['width']]
    }
    ;
    return _0x31cex52
}
getCanvasFingerprint = function () {
    var _0x31cex60 = document['createElement']('canvas');
    var _0x31cex61 = _0x31cex60['getContext']('2d');
    var _0x31cex62 = 'aq';
    _0x31cex61['textBaseline'] = 'top';
    _0x31cex61['font'] = '14px \'Arial\'';
    _0x31cex61['textBaseline'] = 'alphabetic';
    _0x31cex61['fillStyle'] = '#f60';
    _0x31cex61['fillRect'](125, 1, 62, 20);
    _0x31cex61['fillStyle'] = '#069';
    _0x31cex61['fillText'](_0x31cex62, 2, 15);
    _0x31cex61['fillStyle'] = 'rgba(102, 204, 0, 0.7)';
    _0x31cex61['fillText'](_0x31cex62, 4, 17);
    return _0x31cex60['toDataURL']()
}
getRandom = function () {
    var _0x31cex63 = +new Date();
    return _0x31cex63
}
this['map'] = function (_0x31cex4b, _0x31cex4c, _0x31cex4d) {
    var _0x31cex4e = [];
    if (_0x31cex4b == null) {
        return _0x31cex4e
    }
    ;
    if (_0x31cex4a && _0x31cex4b['map'] === _0x31cex4a) {
        return _0x31cex4b['map'](_0x31cex4c, _0x31cex4d)
    }
    ;
    this['each'](_0x31cex4b,
        function (_0x31cex3e, _0x31cex4f, _0x31cex50) {
            _0x31cex4e[_0x31cex4e['length']] = _0x31cex4c['call'](_0x31cex4d, _0x31cex3e, _0x31cex4f, _0x31cex50)
        });
    return _0x31cex4e
};