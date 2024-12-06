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
            # # crawl.open("https://www.baidu.com", load_mode="none")
            # crawl.clear_dp_cache(cache=True, cookies=True)
            resp = crawl.open(
                "https://personal-leadershop.com/?ttclid=E_C_P_CsQBbVH6Zbf-pWpCpYBiP1r98n99dTc2FqIkPMSFVNyO7kcEP5KvrLYbz2gOmKTpEv9QmBmU1PTuqYZ5IErOixQJtzohiWcwcHr9dsSwc4Rou-5pfcgfq_mUkZI9N2IW7WW449o_B_fyJBl8zMwN61EIgQsYCQ-KQOefgeDY7OQA1iZQRIuILdOoI7jtavFgdvVG7Dc9w7OHUZXyjiY2lLtzODIU9ePYLhUKrXXDV85QJXYfoqQFVg-VMLxw8j5WMlA1sNYSkRIEdjIuMBogRMhbunVDSnNHhAcX0lGWCIDWWLnXyx5PhCgiw_JVjF8",
                # proxies="127.0.0.1:7897",
                # is_cloudflare=True,
                load_mode="none",
            )
            print(resp.status_code, resp.response.url)
            print(resp.text())
            # # resp = crawl.open(url=url, is_cloudflare=True, load_mode="none")
            # _code = resp.status_code
            # real_url = resp.response.url
            # text = resp.text()
            # history = {'code': _code, 'url': real_url}
            # print(_code, real_url, text[:20], history)
            #
            # logger.debug(f"resp cookie: {resp.response.cookies}")
            # logger.debug(f"resp text: {resp.text()[:1000]}")
            # resp2 = crawl.open(
            #     "https://www.perplexity.ai", is_cloudflare=True, load_mode="none"
            # )
            # logger.debug(f"resp2 cookie: {resp2.response.cookies}")
            # resp3 = crawl.open(
            #     url="https://nopecha.com/demo/cloudflare", is_cloudflare=True, load_mode="none"
            # )
            # logger.debug(f"resp3 cookie: {resp3.response.cookies}")
            # logger.debug(f"resp3 text: {resp3.text()[:1000]}")
        except Exception as e:
            logger.debug(f"error: {str(e)}")
            # raise
        time.sleep(3)

    # crawl.close_dp()


if __name__ == "__main__":
    dp_crawl()
