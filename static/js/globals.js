"use strict";

function assert(expr, obj) {
  if (!expr) {
    throw obj || "Assertion failed";
  }
}

function staticURI(url, encode) {
  if (encode == undefined) { encode = false; }
  if (url[0] != '/') { url = '/' + url };
  url = '/static' + url;
  if (encode) { url = encodeURI(url); }
  return url;
}

(function($) {
  $('a.disabled').on('click', function() {
    return false;
  });
}) (jQuery);
