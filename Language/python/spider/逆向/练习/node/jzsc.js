var express = require('express');
var crypto = require('crypto-js')
const bodyParser = require("body-parser");
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.post('/data', function (req, res) {
  var t = req.body.t;
  var f = crypto.enc.Utf8.parse("jo8j9wGw%6HbxfFn"),
    m = crypto.enc.Utf8.parse("0123456789ABCDEF");
  var e = crypto.enc.Hex.parse(t)
    , n = crypto.enc.Base64.stringify(e)
    , a = crypto.AES.decrypt(n, f, {
    iv: m, mode: crypto.mode.CBC, padding: crypto.pad.Pkcs7
  }), r = a.toString(crypto.enc.Utf8);
  console.log('parse success')
  res.send(r.toString());
});

var server = app.listen(6666, function () {
  console.log('Listening on port %d', server.address().port);
});