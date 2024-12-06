from DrissionPage import ChromiumPage, ChromiumOptions
import time


def turnstile_challenge(page):
    for i in range(6):
        try:
            curr_title = page.title
            if all(
                ["just a moment" not in curr_title.lower(), "请稍候" not in curr_title]
            ):
                break

            print(f"第 {i + 1} 次尝试")
            if i == 0:
                time.sleep(2)
            else:
                time.sleep(0.5)

            challengeSolution = page.ele(
                "@name=cf-turnstile-response", timeout=1
            )
            challengeWrapper = challengeSolution.parent()
            challengeIframe = challengeWrapper.shadow_root.ele(
                "tag:iframe", timeout=1
            )
            challengeIframeBody = challengeIframe.ele(
                "tag:body", timeout=1
            ).shadow_root
            challengeButton = challengeIframeBody.ele("tag:input", timeout=1)
            challengeButton.focus()
            challengeButton.click()
        except Exception:
            pass


while True:
    try:
        co = ChromiumOptions()
        co.set_local_port(9223)
        co.headless(True)
        co.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
        co.set_argument('--no-sandbox')
        co.set_argument("--disable-gpu")
        driver = ChromiumPage(co)
        driver.clear_cache(cache=True, cookies=True)

        page = driver.new_tab()
        page.get("https://www.dogalecza.com.tr/selfish-drop-cilt-bakimi-2913?ttclid=E_C_P_CscBCl2ZJ5wkz8R7QIa1piD55ZM8JYXCDoOa7wRFOHpqjQs3txTqaEkaQxXL5uYUNmmeRvb58jEdsKvmu0v23IVK1CF84csU2VTLa23pObxOzm5kzUkH7oW7nZzSBl9u8aTQgRN5xd427Mg0XDVsPxj5If5Tw2utodBUcY_nVohK-73lsz9wzgwKblGPOqZizZjapSASoPy0XDtfyYFJF4t2luQy6q0FVp16UPSXbmkk-XZOKdTCDz9e1yiZU3jP5bEdtJ7DxX26NhIEdjIuMBog-8OcfL6JTr7MfEutOZBFg-_iBYQ8jx5c26VUrSHYyaM")
        turnstile_challenge(page)
        print(f"page 的标题为：{page.title}")
        page.close()
    except Exception as e:
        if "无法操作当前存储数据" in str(e):
            pass
        else:
            print(str(e))
            raise
