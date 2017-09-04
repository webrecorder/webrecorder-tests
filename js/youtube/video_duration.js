video = window.frames[0].document.getElementsByTagName("video")[0];

// async function get_duration() {
//   var duration = new Promise(resolve => {
//     video.addEventListener("loadedmetadata", function() {
//       resolve(video.duration);
//     });
//   });
//   return await duration;
// }

// get_duration().then(v => {
//    return v;
// });


var callback = arguments[arguments.length - 1];

video.onloadedmetadata = function() {
  callback(video.duration);
};

setTimeout(function() {
  callback(0);
}, 3000);
