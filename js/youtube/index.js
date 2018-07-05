function documentTitle() {
  return document.title === "Procrastination Polka by Dragan Espenschied (Live) - YouTube"
}

function videoSrc () {
  const video = document.getElementsByTagName('video')[0];
  return video.src === "https://r5---sn-p5qs7n7l.googlevideo.com/videoplayback?mn=sn-p5qs7n7l%2Csn-p5qlsns6&ip=54.164.112.170&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cexpire&ratebypass=yes&clen=13016094&c=WEB&fvip=5&itag=43&mm=31%2C29&expire=1530569517&id=o-ABLAEsmN5cx8JE5sCvXSByZHCrEkLvw0NvxdOJVbk2zo&mt=1530547813&pl=20&mv=m&ei=zU46W7TECYeO8gTHvLvACw&ms=au%2Crdu&gir=yes&source=youtube&signature=3EE578799E79D4738F8B59BBD6D419FDE6AFA50A.5A2C6E7BC8ED0B73A65782AF01DB6ABF09846A97&requiressl=yes&mime=video%2Fwebm&initcwndbps=3831250&ipbits=0&fexp=23709359&lmt=1293670029100691&key=yt6&dur=0.000&cpn=jvLiqzfHKDw77Pyw&cver=2.20180628&ptk=youtube_none&pltype=contentugc";
}

function videoDuration() {
  const video = document.getElementsByTagName('video')[0];
  return video.duration === 116.455;
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