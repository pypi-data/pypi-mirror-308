from scan import logger, crawl
import time
import asyncio
from scan.common import Settings

Settings.dp_request_wait_times = 5
Settings.dp_max_tabs_count = 3


def dp_crawl():
    while True:
        try:
            # crawl.create_dp(
            #     # headless=True,
            #     # local_port=9222
            # )
            crawl.open("https://github.com", load_mode="none")
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


async def tdp(url):
    await asyncio.sleep(0.1)
    crawl.open(url, load_mode="none")


async def task():
    logger.info("开始执行任务...")
    task_list = []
    urls = [
        "https://github.com",
        "https://www.baidu.com",
        "https://www.google.com",
        "https://www.apple.com",
    ]
    for _ in urls:
        print("___", _)
        t = asyncio.create_task(tdp(_))
        task_list.append(t)
    await asyncio.gather(*task_list)
    logger.info("结束执行任务...")


if __name__ == "__main__":
    # asyncio.run(consume_image_tasks())
    asyncio.run(task())

