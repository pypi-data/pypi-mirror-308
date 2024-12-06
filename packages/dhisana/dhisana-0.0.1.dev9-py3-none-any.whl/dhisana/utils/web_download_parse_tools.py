# Tools to download and parse web content

import logging
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from dhisana.utils.assistant_tool_tag import assistant_tool

@assistant_tool
async def get_html_content_from_url(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        logging.info(f"Requesting {url}")
        try:
            await page.goto(url, timeout=10000)
            html_content = await page.content()
            return await parse_html_content(html_content)
        except Exception as e:
            logging.info(f"Failed to fetch {url}: {e}")
            return ""
        finally:
            await browser.close()

@assistant_tool
async def parse_html_content(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    return soup.get_text(separator=' ', strip=True)


