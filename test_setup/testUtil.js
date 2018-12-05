class $TU {

  static async traverseChildrenUntil(parent, condition, delay = 1000) {
    let nextSibling = parent.children[0];
    let test = false;
    while (nextSibling) {
      $TU.scrollElemIntoView(nextSibling);
      test = condition();
      if (test) {
        return test;
      }
      await $TU.delay(delay);
      nextSibling = nextSibling.nextElementSibling;
    }
    return test;
  }

  static xpath(xpathQuery, startElem) {
    if (startElem == null) {
      startElem = document;
    }
    const snapShot = document.evaluate(
      xpathQuery,
      startElem,
      null,
      XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
      null
    );
    const elements = [];
    let i = 0;
    let len = snapShot.snapshotLength;
    while (i < len) {
      elements.push(snapShot.snapshotItem(i));
      i += 1;
    }
    return elements;
  }

  static scrollElemIntoView(elem) {
    elem.scrollIntoView({
      behavior: 'auto',
      block: 'center',
      inline: 'center'
    });
  }

  /**
   *
   * @param {function(): boolean} fn
   * @param {function(boolean)} cb
   * @returns {Promise<boolean>}
   */
  static runTestFNForSelenium(fn, cb) {
    return Promise.resolve().then(fn).then(cb).catch(() => cb(false));
  }


  /**
   * @desc Wrapper around querySelectorAll that returns an Array not NodeList
   * @param {string} selector
   * @returns {HTMLElement[]}
   */
  static qsa(selector) {
    return Array.from(document.querySelectorAll(selector));
  }

  /**
   * @desc Retrieve an element by either id or querySelector
   * @param {string} selectorOrId
   * @returns {?HTMLElement}
   */
  static elem(selectorOrId) {
    const elem = document.querySelector(selectorOrId);
    if (elem) return elem;
    return document.getElementById(selectorOrId);
  }

  /**
   *
   * @param selectorOrId
   * @returns {?string}
   */
  static elemText(selectorOrId) {
    const elem = $TU.elem(selectorOrId);
    if (elem == null) return null;
    return elem.innerText
  }

  /**
   *
   * @param selectorOrId
   * @returns {boolean}
   */
  static elemExists(selectorOrId) {
    return $TU.elem(selectorOrId) != null
  }

  /**
   *
   * @param selectorOrId
   * @returns {function(): boolean}
   */
  static elemExistsPredicate(selectorOrId) {
    return () => $TU.elemExists(selectorOrId)
  }

  /**
   *
   * @param selectorOrId
   * @returns {Promise<boolean>}
   */
  static waitForElement(selectorOrId) {
    return $TU.waitForPredicate($TU.elemExistsPredicate(selectorOrId))
  }

  /**
   *
   * @param expectedTitle
   * @returns {boolean}
   */
  static pageTitleEquals(expectedTitle) {
    return document.title === expectedTitle
  }

  /**
   *
   * @param selectorOrId
   * @param attr
   * @param expected
   * @returns {boolean}
   */
  static elemAttrOrPropEquals(selectorOrId, attr, expected) {
    const elem = $TU.elem(selectorOrId);
    if (!elem) throw new Error(`Element identified by ${selectorOrId} does not exist`);
    const test = elem.getAttribute(attr) === expected;
    return test ? test : elem[attr] === expected;
  }

  /**
   *
   * @param selectorOrId
   * @param timeout
   * @returns {Promise<boolean>}
   */
  static mediaElementShouldPlay(selectorOrId, timeout = 10000) {
    const elem = $TU.elem(selectorOrId);
    if (!elem) return Promise.resolve(false);
    return Promise.race([
      new Promise(resolve => {
        setTimeout(() => resolve(false), timeout);
        elem.onplaying = function () {
          resolve(true);
        };
        elem.onplay = function () {
          resolve(true);
        };
      }),
      elem.play().then(() => true).catch(e => false)
    ]);
  }

  /**
   *
   * @param selectorOrId
   * @param timeout
   * @returns {Promise<boolean>}
   */
  static async scrollUntilElement(selectorOrId, timeout = 25000) {
    let success = await $TU.scrollUntilPredicate($TU.elemExistsPredicate(selectorOrId), timeout);
    if (success) {
      $TU.scrollElemIntoView(selectorOrId);
    }
    return success;
  }

  static selectChildOf(parentSelectorOrId, childSelector) {
    const elem = $TU.elem(parentSelectorOrId);
    if (elem) return elem.querySelector(childSelector);
    return elem;
  }

  static selectChildrenOf(parentSelectorOrId, childrenSelector) {
    const elem = $TU.elem(parentSelectorOrId);
    if (elem) return Array.from(elem.querySelectorAll(childrenSelector));
    return elem;
  }

  static waitForChildToExist(parentSelectorOrId, childSelector) {
    return $TU.waitForPredicate(() => $TU.selectChildOf(parentSelectorOrId, childSelector) != null)
  }

  /**
   * @desc Determine if an element, retrieved by id or select, has the supplied CSS class
   * @param {string} selectorOrId
   * @param {string} clazz
   * @returns {boolean}
   */
  static elemHasClass(selectorOrId, clazz) {
    const elem = $TU.elem(selectorOrId);
    if (elem != null) return elem.classList.contains(clazz);
    return false;
  }

  /**
   * @desc Applies a function to every element selected by the supplied selector
   * @param {string} selector
   * @param {function(HTMLElement)} fn
   * @returns {HTMLElement[]}
   */
  static selectAllApply(selector, fn) {
    return $TU.qsa(selector).map(fn);
  }

  /**
   * @desc Filters the list of elements returned by querySelectorAll by the supplied selector
   * @param {string} selector
   * @param {function(HTMLElement)} predicate
   * @returns {HTMLElement[]}
   */
  static selectAllPreicate(selector, predicate) {
    return $TU.qsa(selector).filter(predicate);
  }

  /**
   * @desc Scroll the page until the supplied predicate returns true
   * @param {function(): boolean} predicate
   * @param {number} [timeout = 45000]
   * @returns {Promise<boolean>}
   */
  static scrollUntilPredicate(predicate, timeout = 30000) {
    return new Promise((resolve, reject) => {
      let to;
      let scrollInterval;
      if (predicate()) {
        return resolve(true);
      }
      const scroller = () => {
        window.scrollBy(0, 200);
        const sucess = predicate();
        if (sucess) {
          clearTimeout(to);
          clearInterval(scrollInterval);
          return resolve(sucess);
        }
        let scrollPos = window.scrollY + window.innerHeight;
        let maxScroll = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
        if (scrollPos >= maxScroll) {
          clearInterval(scrollInterval);
          return resolve(false);
        }
      };
      to = setTimeout(() => {
        window.clearInterval(scrollInterval);
        resolve(false);
      }, timeout);
      scrollInterval = window.setInterval(scroller, 1000);
    });
  }

  /**
   * @desc Click on an element retrieved via an selector or id
   * @param {string} selectorOrId
   * @returns {boolean}
   */
  static clickElem(selectorOrId) {
    const elem = $TU.elem(selectorOrId);
    if (elem) {
      elem.click();
      return true;
    }
    return false;
  }

  /**
   * @desc Wait for a predicate to be true via request animation frame, setInterval, or DOM mutation
   * @param {function(): boolean} predicate
   * @param {number} [timeout = 45000]
   * @returns {Promise<boolean>}
   */
  static waitForPredicate(predicate, timeout = 45000) {
    if (predicate()) {
      return Promise.resolve(true);
    }
    return new Promise((resolve, reject) => {
      let to;
      let interval = setInterval(() => {
        if (predicate()) {
          clearTimeout(to);
          clearInterval(interval);
          return resolve(true);
        }
      }, 1000);
      to = setTimeout(() => {
        clearInterval(interval);
        resolve(false);
      }, timeout);
    });
  }

  static delay(time = 1000) {
    return new Promise(r => setTimeout(r, time));
  }
}
