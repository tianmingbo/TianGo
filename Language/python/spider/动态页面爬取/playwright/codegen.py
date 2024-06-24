# playwright congen -o script.py -b firefox
import asyncio

from playwright.async_api import Playwright, async_playwright


async def run(playwright: Playwright) -> None:
    browser = await playwright.firefox.launch(headless=False)
    context = await browser.new_context()
    # Open new page
    page = await context.new_page()
    # Go to https://www.baidu.com/
    await page.goto("https://www.baidu.com/")
    # Click input[name="wd"]
    await page.locator("input[name=\"wd\"]").click()
    # Fill input[name="wd"]
    # async with page.expect_navigation(url="https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E9%99%88%E5%A4%A7%E5%8A%9B&fenlei=256&rsv_pq=fe8bdcd200067d45&rsv_t=52ca%2BTiegNpCopdeAFWx2begH%2FeXvn89Xa1bJxwbyegTc0pKvMvh%2B4ST4tk&rqlang=cn&rsv_enter=1&rsv_dl=ib&rsv_sug3=10&rsv_sug1=19&rsv_sug7=100"):
    async with page.expect_navigation():
        await page.locator("input[name=\"wd\"]").fill("陈大力")
    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
