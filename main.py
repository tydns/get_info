from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import aiohttp
from bs4 import BeautifulSoup

@register("server_info", "Your Name", "获取服务器信息并渲染为图片返回", "1.0.0")
class ServerInfoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def fetch_and_render_webpage(self, url: str) -> str:
        """
        获取网页内容并渲染为图片。
        """
        try:
            # 获取网页内容
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    html_content = await response.text()

            # 使用 BeautifulSoup 提取网页正文内容
            soup = BeautifulSoup(html_content, "html.parser")
            body_content = soup.body.get_text(separator="\n", strip=True) if soup.body else "无正文内容"

            # 定义 HTML 模板
            HTML_TEMPLATE = """
            <div style="font-size: 16px; font-family: Arial, sans-serif; padding: 20px;">
                <pre style="white-space: pre-wrap; word-wrap: break-word; color: #555;">{{ content }}</pre>
            </div>
            """

            # 渲染网页内容为图片
            image_url = await self.html_render(HTML_TEMPLATE, {"content": body_content})
            return image_url

        except Exception as e:
            print(f"处理网页时出错: {str(e)}")
            return None

    @filter.command("mc_info")
    async def mc_info(self, event: AstrMessageEvent):
        """
        通过 /mc_info 获取服务器 3 的信息并渲染为图片返回。
        """
        url = "http://154.204.177.235:8008/server/3"
        image_url = await self.fetch_and_render_webpage(url)
        if image_url:
            yield event.image_result(image_url)
        else:
            yield event.plain_result("无法获取服务器 3 的信息。")

    @filter.command("web_info")
    async def web_info(self, event: AstrMessageEvent):
        """
        通过 /web_info 获取服务器 4 的信息并渲染为图片返回。
        """
        url = "http://154.204.177.235:8008/server/4"
        image_url = await self.fetch_and_render_webpage(url)
        if image_url:
            yield event.image_result(image_url)
        else:
            yield event.plain_result("无法获取服务器 4 的信息。")
