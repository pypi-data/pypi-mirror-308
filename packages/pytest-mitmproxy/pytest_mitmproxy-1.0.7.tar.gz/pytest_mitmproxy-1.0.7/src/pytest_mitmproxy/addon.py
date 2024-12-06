import logging
import sys
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)
mitm_log = Path(tempfile.gettempdir()) / "mitmdump.log"


class MyAddon:
    def __init__(self):
        self.log_file = mitm_log
        self.clear_log()
        self.url_filter = None
        # print(f"{sys.argv=}")
        for arg in sys.argv:
            if arg.startswith("url_filter="):
                self.url_filter = arg.split("=")[1]
                break

    def clear_log(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.truncate()

    def write_log(self, data):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{data}\n")

    def request(self, flow):
        request_url = flow.request.url
        if self.url_filter in request_url:
            print("*" * 80)
            display_url = f"Request Url: {request_url}"
            print(display_url)
            # 打印请求体（如果存在）
            if flow.request.content:
                content = flow.request.content.decode("utf-8", errors="ignore")
                display_content = f"Request Body: {content}"
                log_content = "\n".join([display_url, display_content, "*" * 80])
                self.write_log(f"{log_content}\n")
            else:
                display_content = "Request Body: None"
                log_content = "\n".join([display_url, display_content, "*" * 80])
                self.write_log(f"{log_content}\n")
            print("*" * 80)


addons = [MyAddon()]
