from pyppeteer.page import Page


async def get_document_title(page: Page) -> str:
    title = await page.evaluate('''() => document.title''')
    return title
