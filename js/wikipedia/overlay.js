function overlay () {
  function waitForIt() {
    return new Promise(resolve => {
      function raf() {
        const elem = document.querySelector('#mw-sopaOverlay');
        if (elem) {
          return resolve(elem);
        } else {
          window.requestAnimationFrame(raf);
        }
      }
      window.requestAnimationFrame(raf);
    });
  }
  return waitForIt()
    .then(overlay => overlay.innerText.startsWith('Imagine a World'));
}