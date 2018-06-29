function documentTitle() {
  return document.title === "Procrastination Polka by Dragan Espenschied (Live) - YouTube"
}

function videoSrc () {
  const video = document.getElementsByTagName('video')[0];
  return video.src ===  "https://r2---sn-nvopjoxu-25ve.googlevideo.com/videoplayback?lmt=1293668212190294&expire=1490092899&ratebypass=yes&ipbits=0&mime=video%2Fmp4&requiressl=yes&clen=8924242&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpcm2cms%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=2363750&pl=19&source=youtube&dur=116.471&mv=m&mt=1490071223&ms=au&ei=A6_QWLyRKe-A_APRtI7wDQ&id=o-ABvUC5LhDBxHMoY_fDgjpktcyl8manKZR09X3CE-g53X&mn=sn-nvopjoxu-25ve&mm=31&signature=D59DC089448E0C9FBBA80512A5C2D87A01AC75D1.65AF95645D26D34CDE542DFC13F0464F156F03C3&key=yt6&ip=75.101.62.254&gir=yes&upn=9P176uePWno&pcm2cms=yes&itag=18&cpn=JOlTjRyzZpdp9YNl&c=WEB&cver=1.20170316&ptk=youtube_none&pltype=contentugc";
}

function videoDuration() {
  const video = document.getElementsByTagName('video')[0];
  return video.duration === 116.471293;
}

function videoPlaying() {
  const video = document.getElementsByTagName('video')[0];
  return Promise.race([
    new Promise(resolve => {
      setTimeout(() => resolve(false), 5000);
      video.onplaying = function() {
        resolve(true);
      };
    }),
     video.play().then(() => true).catch((e) => e.toString())
  ]);
}