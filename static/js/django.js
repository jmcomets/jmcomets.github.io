"use strict";

var django = {
  static: function(url, encode) {
    if (encode == undefined) { encode = false; }
    if (url[0] != '/') { url = '/' + url };
    url = '/static' + url;
    if (encode) { url = encodeURI(url); }
    return url;
  }
};
