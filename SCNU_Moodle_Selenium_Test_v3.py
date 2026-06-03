# ============================================================
# 功能：华南师范大学砺儒云课堂(Moodle)自动化测试脚本
# 作者：刘湘荣
# 版本：v3.0（稳定版）
# 环境：Windows11 / Python3.10 / Selenium4.x / Chrome
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

    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)

    wait_page(driver)

    shot(driver, "00_homepage.png")
    print("[PASS] 浏览器初始化成功")

    return driver


def test_navigation(driver):
    print("\n===== 导航测试 =====")

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

    driver.back()
    wait_page(driver)

    print("[PASS] 前进后退完成")


def test_window_operation(driver):
    print("\n===== 窗口测试 =====")

    driver.maximize_window()
    time.sleep(1)

    driver.set_window_size(1280, 900)
    time.sleep(1)

    shot(driver, "03_window_resize.png")

    print("[PASS] 窗口操作完成")


def open_login(driver):
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    shot(driver, "04_login_page.png")


def test_text(driver):

    print("\n===== 文本获取测试 =====")

    driver.get(BASE_URL)
    wait_page(driver)

    try:
        text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text[:200]

        print("页面文本获取成功")
        print(text[:50])

    except Exception:
        print(driver.title)

    shot(driver, "05_text.png")


def test_input_and_button(driver):

    print("\n===== 文本框与按钮测试 =====")

    open_login(driver)

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.clear()
    username.send_keys("test_user")

    password.clear()
    password.send_keys("123456")

    print("用户名：", username.get_attribute("value"))

    login_btn = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit'],input[type='submit']"
    )

    print("按钮状态：", login_btn.is_enabled())

    shot(driver, "06_input_button.png")


def test_checkbox(driver):

    print("\n===== 复选框测试 =====")

    driver.get("about:blank")

    driver.execute_script("""
    document.body.innerHTML=
    '<h2>Checkbox Demo</h2><input type="checkbox" id="cb">';
    """)

    checkbox = driver.find_element(By.ID, "cb")

    print("初始状态:", checkbox.is_selected())

    checkbox.click()

    print("点击后状态:", checkbox.is_selected())

    shot(driver, "07_checkbox.png")


def test_keyboard(driver):

    print("\n===== 键盘测试 =====")

    open_login(driver)

    username = driver.find_element(By.NAME, "username")

    username.clear()
    username.send_keys("20230000001")

    username.send_keys(Keys.CONTROL, "a")
    username.send_keys(Keys.CONTROL, "c")

    username.send_keys(Keys.END)
    username.send_keys("_test")

    shot(driver, "08_keyboard.png")

    print("[PASS] 键盘操作完成")


def test_mouse(driver):

    print("\n===== 鼠标测试 =====")

    open_login(driver)

    btn = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit'],input[type='submit']"
    )

    actions = ActionChains(driver)

    actions.move_to_element(btn).perform()

    actions.context_click(btn).perform()

    shot(driver, "09_mouse_right.png")

    actions.double_click(btn).perform()

    shot(driver, "10_mouse_double.png")

    print("[PASS] 鼠标操作完成")


def test_alert(driver):

    print("\n===== Alert测试 =====")

    driver.get(LOGIN_URL)

    # ---------- Alert确定 ----------
    driver.execute_script(
        "alert('测试确定按钮');"
    )

    alert = WebDriverWait(driver,5).until(
        EC.alert_is_present()
    )

    print(alert.text)

    alert.accept()

    time.sleep(1)

    # 截图
    shot(driver, "11_alert_accept.png")

    # ---------- Confirm取消 ----------
    driver.execute_script(
        "confirm('测试取消按钮');"
    )

    alert = WebDriverWait(driver,5).until(
        EC.alert_is_present()
    )

    print(alert.text)

    alert.dismiss()

    time.sleep(1)

    # 截图
    shot(driver, "12_alert_dismiss.png")

    print("[PASS] Alert完成")

def test_window_switch(driver):

    print("\n===== 窗口切换测试 =====")

    original = driver.current_window_handle

    driver.execute_script(
        "window.open('https://moodle.scnu.edu.cn/')"
    )

    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > 1
    )

    for handle in driver.window_handles:
        if handle != original:
            driver.switch_to.window(handle)
            break

    wait_page(driver)

    shot(driver, "13_new_window.png")

    driver.close()

    driver.switch_to.window(original)

    print("[PASS] 窗口切换完成")


def test_frame(driver):

    print("\n===== Frame测试 ====")
    driver.get("about:blank")
    driver.execute_script("""
        document.body.innerHTML =
        '<h1>Frame测试页面</h1>' +
        '<iframe id="testFrame"></iframe>';

        var iframe = document.getElementById('testFrame');

        iframe.srcdoc =
        '<html><body><h2>这是Frame内部内容</h2></body></html>';
        """)
    shot(driver, "14_frame.png")

    driver.switch_to.frame("testFrame")

    print("进入Frame成功")

    driver.switch_to.default_content()
    shot(driver,"15_frame_inside.png")
    print("[PASS] Frame切换完成")


def test_element_screenshot(driver):

    print("\n===== 元素截图测试 =====")

    open_login(driver)

    form = driver.find_element(By.TAG_NAME, "form")

    form.screenshot(
        os.path.join(
            SCREENSHOT_DIR,
            "16_login_form.png"
        )
    )

    print("[PASS] 元素截图完成")


def test_captcha(driver):

    print("\n===== 验证码检测 =====")

    open_login(driver)

    selectors = [
        "img.captcha",
        "#captchaImg",
        "img[src*='captcha']"
    ]

    found = False

    for selector in selectors:
        elements = driver.find_elements(
            By.CSS_SELECTOR,
            selector
        )

        if elements:
            elements[0].screenshot(
                os.path.join(
                    SCREENSHOT_DIR,
                    "17_captcha.png"
                )
            )
            found = True
            break

    if not found:
        print("当前页面无验证码")
        shot(driver, "18_no_captcha.png")

    print("[PASS] 验证码检测完成")


def main():

    driver = init_browser()

    try:
        test_navigation(driver)
        test_window_operation(driver)
        test_text(driver)
        test_input_and_button(driver)
        test_checkbox(driver)
        test_keyboard(driver)
        test_mouse(driver)
        test_alert(driver)
        test_window_switch(driver)
        test_frame(driver)
        test_element_screenshot(driver)
        test_captcha(driver)

        print("\n全部测试完成")

    finally:
        time.sleep(2)
        driver.quit()
        print("浏览器关闭")


if __name__ == "__main__":
    main()
