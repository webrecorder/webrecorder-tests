var video = window.frames[0].document.getElementsByTagName("video")[0];
var callback = arguments[arguments.length - 1];

video.onplaying = function() {
  callback("play");
};

setTimeout(function() {
  callback("notplayed");
}, 4000);
