import math
import re
import logging
from typing import Optional, Union

from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files

logger = logging.getLogger("mkdocs.plugins.timetoread_zh")


class TimeToReadZh(BasePlugin):
    """MkDocs plugin to add Chinese-friendly reading time estimates to pages."""

    page_time_dict: dict[str, Union[int, bool]] = {}

    config_scheme = (
        (
            "wpm",
            config_options.Type(
                int, default=300, help="Words per minute reading speed"
            ),
        ),
        (
            "allPages",
            config_options.Type(
                bool, default=True, help="Apply to all pages by default"
            ),
        ),
        (
            "textColor",
            config_options.Type(
                str, default="bdbdbd", help="Color of the reading time text"
            ),
        ),
        (
            "substitute",
            config_options.Type(str, default="</h1>", help="HTML tag to insert after"),
        ),
        (
            "template",
            config_options.Type(
                str,
                default="预计阅读时长 : {minutes} 分钟",
                help="Template for the reading time message",
            ),
        ),
        (
            "language",
            config_options.Type(
                str, default="zh", help="Language for the reading time message"
            ),
        ),
        (
            "min_time",
            config_options.Type(int, default=1, help="Minimum reading time to display"),
        ),
        (
            "round_method",
            config_options.Type(
                str, default="ceil", help="Rounding method: 'ceil', 'floor', or 'round'"
            ),
        ),
    )

    _translations = {
        "zh": "预计阅读时长 : {minutes} 分钟",
        "en": "Estimated reading time: {minutes} minutes",
        "ja": "推定読書時間：{minutes}分",
        "ko": "예상 읽기 시간: {minutes}분",
    }

    def calculate_time(self, text: str, wpm: int) -> int:
        """Calculate reading time in minutes."""
        try:
            # 分别计算中文和英文字数
            chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
            words = len(re.split(r"\W+", re.sub(r"[\u4e00-\u9fff]", "", text).strip()))

            # 中文阅读速度约为英文的1/2
            total_words = words + (chinese_chars * 2)
            minutes = total_words / wpm

            # Apply rounding method
            if self.config["round_method"] == "ceil":
                minutes = math.ceil(minutes)
            elif self.config["round_method"] == "floor":
                minutes = math.floor(minutes)
            else:  # round
                minutes = round(minutes)

            # Ensure minimum time
            return max(self.config["min_time"], minutes)
        except Exception as e:
            logger.error(f"Error calculating reading time: {e}")
            return self.config["min_time"]

    def get_template(self) -> str:
        """Get the template string based on language configuration."""
        language = self.config["language"]
        custom_template = self.config["template"]

        if custom_template != self._translations["zh"]:
            return custom_template

        return self._translations.get(language, self._translations["en"])

    def on_page_markdown(
        self, markdown: str, page: Page, config: Config, files: Files
    ) -> str:
        """Process the markdown content of each page."""
        logger.debug(f"Processing page: {page.url}")

        # Skip processing if explicitly disabled
        if page.meta.get("timetoread") is False:
            self.page_time_dict[page.url] = False
            return markdown

        # Process if globally enabled or explicitly enabled for this page
        if self.config["allPages"] or page.meta.get("timetoread") is True:
            reading_time = self.calculate_time(markdown, self.config["wpm"])
            self.page_time_dict[page.url] = reading_time
            logger.debug(
                f"Calculated reading time for {page.url}: {reading_time} minutes"
            )

        return markdown

    def on_post_page(self, output: str, page: Page, config: Config) -> str:
        """Modify the HTML output to include reading time."""
        reading_time = self.page_time_dict.get(page.url)
        if not reading_time:
            return output

        try:
            # Prepare the reading time HTML
            template = self.get_template()
            time_message = template.format(minutes=reading_time)

            text_color = self.config["textColor"]
            time_html = (
                f'</h1><p style="color:#{text_color}">' f"<i>{time_message}</i></p>\n"
            )

            # Insert the reading time
            sub = self.config["substitute"]
            if sub in output:
                where = output.find(sub)
                if where != -1:
                    return output[:where] + output[where:].replace(sub, time_html, 1)

            logger.warning(f"Substitute tag '{sub}' not found in {page.url}")
            return output

        except Exception as e:
            logger.error(f"Error processing page {page.url}: {e}")
            return output

    def on_config(self, config: Config) -> Config:
        """Validate configuration on startup."""
        if self.config["round_method"] not in ["ceil", "floor", "round"]:
            logger.warning(
                f"Invalid round_method '{self.config['round_method']}'. "
                "Using 'ceil' as default."
            )
            self.config["round_method"] = "ceil"
        return config
