var str1 = 'tian';
var str2 = 'dGlhbg==';
var strToBase64 = new Buffer(str1).toString('base64');
var base64Tostr = new Buffer(str2, 'base64').toString();
console.log(base64Tostr)