# ============================================================
# 功能：华南师范大学砺儒云课堂(Moodle)自动化测试脚本
# 作者：刘湘荣
# 版本：v4.0 Final
# 环境：Windows11 / Python3.10+ / Selenium4.x / Chrome
# 网站：https://moodle.scnu.edu.cn/
# ============================================================

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://moodle.scnu.edu.cn/"
LOGIN_URL = "https://moodle.scnu.edu.cn/login/index.php"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def wait_page(driver, timeout=20):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def shot(driver, filename):
    path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    print(f"[截图] {path}")


def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    wait_page(driver)
    shot(driver, "00_homepage.png")
    return driver


def open_login(driver):
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    shot(driver, "04_login_page.png")


def test_navigation(driver):
    driver.get(BASE_URL)
    wait_page(driver)
    driver.get("https://www.baidu.com")
    wait_page(driver)

    driver.back()
    wait_page(driver)
    shot(driver, "01_back.png")

    driver.forward()
    wait_page(driver)
    shot(driver, "02_forward.png")


def test_window_operation(driver):
    driver.maximize_window()
    driver.set_window_size(1280, 900)
    shot(driver, "03_window_resize.png")


def test_text(driver):
    driver.get(BASE_URL)
    wait_page(driver)
    print(driver.find_element(By.TAG_NAME, "body").text[:100])
    shot(driver, "05_text.png")


def test_input_and_button(driver):
    open_login(driver)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.clear()
    username.send_keys("test_user")

    password.clear()
    password.send_keys("123456")

    print("按钮可用：", driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'],input[type='submit']"
    ).is_enabled())

    shot(driver, "06_input_button.png")


def test_checkbox(driver):
    driver.get("about:blank")
    driver.execute_script("""
    document.body.innerHTML =
    '<h2>Checkbox Demo</h2><input type="checkbox" id="cb">';
    """)
    cb = driver.find_element(By.ID, "cb")
    cb.click()
    shot(driver, "07_checkbox.png")


def test_keyboard(driver):
    open_login(driver)
    username = driver.find_element(By.NAME, "username")

    username.clear()
    username.send_keys("20230000001")
    username.send_keys(Keys.CONTROL, "a")
    username.send_keys(Keys.CONTROL, "c")
    username.send_keys(Keys.END)
    username.send_keys("_test")

    shot(driver, "08_keyboard.png")


def test_mouse(driver):
    driver.get("about:blank")
    driver.execute_script("""
    document.body.innerHTML =
    '<button id="btn">测试按钮</button>';
    """)

    btn = driver.find_element(By.ID, "btn")
    actions = ActionChains(driver)

    actions.click(btn).perform()
    shot(driver, "09_mouse_click.png")

    actions.double_click(btn).perform()
    shot(driver, "10_mouse_double.png")


def test_alert(driver):
    driver.get(LOGIN_URL)

    driver.execute_script("alert('测试确定按钮');")
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert.accept()
    shot(driver, "11_alert_accept.png")

    driver.execute_script("confirm('测试取消按钮');")
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert.dismiss()
    shot(driver, "12_alert_dismiss.png")


def test_window_switch(driver):
    original = driver.current_window_handle

    driver.execute_script("window.open('https://moodle.scnu.edu.cn/')")

    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > 1
    )

    for h in driver.window_handles:
        if h != original:
            driver.switch_to.window(h)
            break

    wait_page(driver)
    shot(driver, "13_new_window.png")

    driver.close()
    driver.switch_to.window(original)


def test_frame(driver):
    driver.get("about:blank")

    driver.execute_script("""
    document.body.innerHTML =
    '<h1>Frame测试页面</h1><iframe id="testFrame"></iframe>';

    document.getElementById("testFrame").srcdoc =
    '<html><body><h2>Frame内部页面</h2></body></html>';
    """)

    shot(driver, "14_frame_before.png")

    driver.switch_to.frame("testFrame")
    shot(driver, "15_frame_inside.png")
    driver.switch_to.default_content()


def test_element_screenshot(driver):
    open_login(driver)

    form = driver.find_element(By.TAG_NAME, "form")
    form.screenshot(
        os.path.join(SCREENSHOT_DIR, "16_login_form.png")
    )


def test_captcha(driver):
    open_login(driver)

    found = False

    for sel in [
        "img.captcha",
        "#captchaImg",
        "img[src*='captcha']"
    ]:
        els = driver.find_elements(By.CSS_SELECTOR, sel)

        if els:
            els[0].screenshot(
                os.path.join(SCREENSHOT_DIR, "17_captcha.png")
            )
            found = True
            break

    if not found:
        shot(driver, "17_no_captcha.png")


def safe_run(func, driver):
    try:
        print(f"\\n===== {func.__name__} =====")
        func(driver)
    except Exception as e:
        print(f"[ERROR] {func.__name__}: {e}")


def main():
    driver = init_browser()

    tests = [
        test_navigation,
        test_window_operation,
        test_text,
        test_input_and_button,
        test_checkbox,
        test_keyboard,
        test_mouse,
        test_alert,
        test_window_switch,
        test_frame,
        test_element_screenshot,
        test_captcha
    ]

    try:
        for t in tests:
            safe_run(t, driver)

        print("\\n全部测试完成")

    finally:
        time.sleep(2)
        driver.quit()
        print("浏览器关闭")


if __name__ == "__main__":
    main()
