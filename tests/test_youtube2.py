import os
import sys
import pytest
from expects import expect, equal, be_empty

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.browser import create


@pytest.mark.asyncio
async def test_youtube():
    goto = 'http://localhost:8080/live/https://www.youtube.com/watch?v=L9Z2OcrZDZo'
    browser = await create(browser_exec='google-chrome-beta', headless=False)
    await browser.goto(goto, {'waitUntil': 'load'})
    expect(browser.top_url).to(equal(goto))
    expect(browser.replay_url).to(equal(goto.replace('live', 'live/mp_')))
    replay_title = await browser.replay_title()
    expect(replay_title).to(equal('Ferry Corsten pres. Gouryella 2.0 - Transmission Bangkok, 17-MAR-2018 - YouTube'))
    video_url = await browser.replay_eval("""() => { 
        return document.querySelector("#movie_player > div.html5-video-container > video").src; 
     }""")
    # expect(video_url).to(equal('blob:http://localhost:8080/90e6f874-53e4-4102-b2e2-01fb2cb3c183')) youtube is crazy changing this
    expect(video_url).to_not(be_empty)
    # print(video_url)
    await browser.close()
