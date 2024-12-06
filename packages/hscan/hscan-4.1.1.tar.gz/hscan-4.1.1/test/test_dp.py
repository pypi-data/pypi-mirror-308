import json
from hashlib import md5

from scan import crawl, logger


def product(url):

    proxy = "http://127.0.0.1:7890"
    resp = crawl.open(
        "https://www.crocs.com/",
        # "https://rucaptcha.com/42",
        # "https://www.perplexity.ai/",
        # "https://milled.com/pricing",
        # "https://nopecha.com/demo/cloudflare",
        timeout=10,
        is_cloudflare=True,
        load_mode="none"
    )
    print("111", resp.response.cookies)
    # resp2 = crawl.open(
    #     "https://www.perplexity.ai",
    #     is_cloudflare=True
    # )
    # print("222", resp2.response.cookies)
    # resp3 = crawl.open(
    #     "https://nopecha.com/demo/cloudflare",
    #     is_cloudflare=True
    # )
    # print("333", resp3.response.cookies)
    # print("333 text", resp3.text())
    # print(resp.text())
    # print(resp2.response.cookies)
    # print(resp3.response.cookies)
    # crawl.close_dp()
    # print("22222",  resp.text())
    # resp = await crawl.fetch(url)
    crawl.close_dp()


if __name__ == "__main__":
    product("https://www.perplexity.ai/")

