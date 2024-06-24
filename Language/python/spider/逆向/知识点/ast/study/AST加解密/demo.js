  Date.prototype.format = function (formatStr) {
    var str = formatStr;
    var Week = ['日', '一', '二', '三', '四', '五', '六']; //ASCIIEncrypt
    str = str.replace(/yyyy|YYYY/, this.getFullYear()); //Base64Encrypt
    str = str.replace(/MM/, (this.getMonth() + 1 > 9 ? (this.getMonth() + 1).toString() : '0' + (this.getMonth() + 1)))
    str = str.replace(/dd|DD/, this.getDate() > 9 ? (this.getDate() + 1).toString() : '0' + this.getDate());
    return str;
  }

  console.log(new Date().format('yyyy-MM-dd'));