from scan import logger, crawl
import time
from scan.common import Settings

Settings.dp_request_wait_times = 5
Settings.dp_max_tabs_count = 20


def dp_crawl():
    while True:
        try:
            # crawl.create_dp(
            #     # headless=True,
            #     # local_port=9222
            # )
            crawl.open("https://www.google.com", load_mode="none")
            # crawl.clear_dp_cache(cache=True, cookies=True)
            resp = crawl.open(
                "https://rucaptcha.com/42",
                # proxies="127.0.0.1:7897",
                is_cloudflare=True,
                load_mode="none",
            )
            print(resp.status_code, resp.response.url)
            # resp = crawl.open(url=url, is_cloudflare=True, load_mode="none")
            _code = resp.status_code
            real_url = resp.response.url
            text = resp.text()
            history = {'code': _code, 'url': real_url}
            print(_code, real_url, text[:20], history)

            logger.debug(f"resp cookie: {resp.response.cookies}")
            logger.debug(f"resp text: {resp.text()[:1000]}")
            resp2 = crawl.open(
                "https://www.perplexity.ai", is_cloudflare=True, load_mode="none"
            )
            logger.debug(f"resp2 cookie: {resp2.response.cookies}")
            resp3 = crawl.open(
                url="https://nopecha.com/demo/cloudflare", is_cloudflare=True, load_mode="none"
            )
            logger.debug(f"resp3 cookie: {resp3.response.cookies}")
            logger.debug(f"resp3 text: {resp3.text()[:1000]}")
        except Exception as e:
            logger.debug(f"error: {str(e)}")
            # raise
        time.sleep(3)

    # crawl.close_dp()


if __name__ == "__main__":
    dp_crawl()
