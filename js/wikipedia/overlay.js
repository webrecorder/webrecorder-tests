async function overlay () {
  await $TU.waitForElement('#mw-sopaOverlay');
  const text = $TU.elemText('#mw-sopaOverlay');
  return text != null ? text.startsWith('Imagine a World') : false
}
