async function scrollTimelinePlayVideo () {
  const selector = 'div[data-tweet-id="1025037046438453248"]';
  const good = await $TU.traverseChildrenUntil($TU.elem('stream-items-id'), $TU.elemExistsPredicate(selector), 500);
  if (!good) return good;
  const elem = $TU.elem(selector);
  $TU.scrollElemIntoView(elem);
  await $TU.delay();
  return $TU.mediaElementShouldPlay('video');
}

async function expandThread() {
  let result = $TU.clickElem('div[data-tweet-id="1029823824995471367"] > .content > .self-thread-tweet-cta > a');
  if (!result) return result;
  await $TU.delay(1000);
  const kids =  $TU.selectChildrenOf('div[class="PermalinkOverlay-modal"]', 'img').length === 13;
  const title = $TU.pageTitleEquals('Rhizome on Twitter: "More Paper Rad: an oral history of the collective via Jacob Ciocci, Jessica Ciocci and Ben Jones here: https://t.co/wgpY1HG6Wr… https://t.co/MLvzOrSXnE"');
  return kids && title;
}
