overlay_text = window.frames[0].document.getElementById("mw-sopaOverlay")
  .innerText;
first_line = overlay_text.split(/\r?\n/)[0];
return first_line;