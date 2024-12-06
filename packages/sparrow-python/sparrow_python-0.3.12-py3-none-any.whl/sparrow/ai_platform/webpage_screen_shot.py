# pip install playwright
# playwright install

import asyncio
from playwright.async_api import async_playwright
from PIL import Image
from io import BytesIO


class ScreenshotTaker:
    def __init__(self, viewport_width=1920, viewport_height=1080):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.browser = None

    async def _initialize_browser(self):
        """Initialize the browser if not already done."""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)

    async def capture_screenshot(self, url, screenshot_path=None):
        """Capture a full-page screenshot of a single URL."""
        await self._initialize_browser()

        # 创建新的页面
        page = await self.browser.new_page()

        # 设置页面视口
        await page.set_viewport_size({"width": self.viewport_width, "height": self.viewport_height})

        # 访问目标URL
        await page.goto(url, wait_until="networkidle")

        # 滚动页面底部确保内容完全加载
        await page.evaluate("""() => {
            window.scrollTo(0, document.body.scrollHeight);
        }""")

        # 等待几秒钟以确保页面和iframe中的内容加载完成
        await asyncio.sleep(2)

        # 处理页面中的所有 iframe
        for iframe_element in await page.query_selector_all("iframe"):
            try:
                # 获取 iframe 中的内容
                frame = await iframe_element.content_frame()
                if frame:
                    # 将 iframe 的高度设为内容高度
                    frame_height = await frame.evaluate("document.body.scrollHeight")
                    await iframe_element.evaluate(f"el => el.style.height = '{frame_height}px'")
            except Exception as e:
                print(f"Error handling iframe: {e}")

        # 截图整个页面并存入字节流
        screenshot_bytes = await page.screenshot(full_page=True)
        image = Image.open(BytesIO(screenshot_bytes))

        # 保存截图到文件（如果指定了保存路径）
        if screenshot_path:
            image.save(screenshot_path)
            print(f"Screenshot saved at {screenshot_path}")

        # 关闭页面
        await page.close()

        # 返回 PIL 图像对象
        return image

    async def capture_multiple_screenshots(self, urls, screenshot_paths=None):
        """
        Capture screenshots for multiple URLs.

        Parameters:
        - urls: list of URLs to capture
        - screenshot_paths: optional list of paths to save each screenshot.
                            If None, screenshots will not be saved to files.

        Returns:
        - List of PIL image objects for each URL.
        """
        tasks = []
        screenshot_paths = screenshot_paths or [None] * len(urls)

        # 批量创建截图任务
        for url, path in zip(urls, screenshot_paths):
            tasks.append(self.capture_screenshot(url, path))

        # 等待所有任务完成
        images = await asyncio.gather(*tasks)
        return images

    async def close(self):
        """Close the browser if it's open."""
        if self.browser:
            await self.browser.close()
            self.browser = None



if __name__ == "__main__":
    async def main():
        screenshot_taker = ScreenshotTaker()
        url = "https://sjh.baidu.com/site/dzfmws.cn/da721a31-476d-42ed-aad1-81c2dc3a66a3"
        urls = ["https://www.baidu.com", url]
        paths = ["example_screenshot.png", "another_example_screenshot.png"]

        # 批量截图并获取 PIL 图像对象列表
        images = await screenshot_taker.capture_multiple_screenshots(urls, paths)
        # 关闭浏览器
        await screenshot_taker.close()
        return images


    asyncio.run(main())

