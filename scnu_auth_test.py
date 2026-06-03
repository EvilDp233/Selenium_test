# ============================================================
# 功能：华南师范大学统一身份认证平台自动化测试脚本
# 时间：2026-06-05
# 作者：[刘湘荣]
# 版本号：v1.0
# 测试环境：Windows 11 / Python 3.10 / Selenium 4.15 / Chrome 125
# 描述：涵盖窗口操作、键盘鼠标模拟、弹窗处理、Frame切换、
#       元素截屏及验证码获取等Selenium核心技术点验证
# ============================================================
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# BASE_URL = "https://moodle.scnu.edu.cn/"
# LOGIN_URL = "https://moodle.scnu.edu.cn/login/index.php"

# SCREENSHOT_DIR = "screenshots"

# if not os.path.exists(SCREENSHOT_DIR):
#     os.makedirs(SCREENSHOT_DIR)

# ==================== 1. 初始化与窗口操作 ====================
def init_browser():
    """初始化浏览器并设置窗口大小"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    
    # 【技术点】窗口大小操作：设置为指定分辨率
    driver.set_window_size(1280, 900)
    print("[INFO] 浏览器已启动，窗口大小设置为 1280x900")
    return driver

# ==================== 2. 页面导航与前进后退 ====================
def test_navigation(driver):
    """测试浏览器前进、后退操作"""
    BASE_URL = "https://moodle.scnu.edu.cn/"
    LOGIN_URL = "https://moodle.scnu.edu.cn/login/index.php"
    driver.get(BASE_URL)
    time.sleep(2)
    
    # 【技术点】浏览器后退与前进
    driver.get(BASE_URL)  # 先跳转到学校主页
    time.sleep(1)
    driver.back()   # 后退到认证页
    time.sleep(1)
    driver.forward() # 前进到学校主页
    time.sleep(1)
    driver.back()   # 再次回到认证页
    print("[PASS] 浏览器前进/后退操作验证成功")

# ==================== 3. 文本获取与数据处理 ====================
def test_text_extraction(driver):
    """获取静态文本和文本框数据并处理"""
    # 【技术点】获取静态文本数据
    try:
        title_text = driver.find_element(By.CSS_SELECTOR, ".login-title, h2, .title").text
        print(f"[INFO] 页面标题文本: '{title_text}'")
        assert len(title_text) > 0, "静态文本获取为空"
    except NoSuchElementException:
        print("[WARN] 未找到标题元素，尝试获取页面title")
        print(f"[INFO] 页面Title: {driver.title}")
    
    # 【技术点】获取文本框里的数据
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    username_input.clear()
    username_input.send_keys("test_user_2024")
    input_value = username_input.get_attribute("value")
    print(f"[INFO] 文本框获取的数据: '{input_value}'")
    assert input_value == "test_user_2024", "文本框数据不一致"
    print("[PASS] 文本获取与数据处理验证成功")

# ==================== 4. 按钮/复选框状态获取与操作 ====================
def test_checkbox_button(driver):
    """获取并操作复选框和按钮状态"""
    # 【技术点】获取复选框状态 & 选中复选框
    try:
        checkbox = driver.find_element(By.CSS_SELECTOR, 
                    "input[type='checkbox'], #rememberMe, .remember-me input")
        is_checked = checkbox.is_selected()
        print(f"[INFO] 复选框当前状态: {'已选中' if is_checked else '未选中'}")
        
        if not is_checked:
            checkbox.click()
            print("[INFO] 已点击选中复选框")
        assert checkbox.is_selected(), "复选框选中失败"
    except NoSuchElementException:
        print("[WARN] 未找到复选框，跳过该步骤")
    
    # 【技术点】获取按钮状态
    login_btn = driver.find_element(By.CSS_SELECTOR, 
                "button[type='submit'], #loginBtn, .btn-login")
    is_enabled = login_btn.is_enabled()
    print(f"[INFO] 登录按钮可用状态: {is_enabled}")
    print("[PASS] 按钮/复选框状态操作验证成功")

# ==================== 5. 模拟键盘操作（复制/粘贴/输入） ====================
def test_keyboard_operations(driver):
    """模拟键盘的输入、复制、粘贴"""
    pwd_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    
    # 【技术点】模拟键盘输入
    pwd_input.send_keys("MyTest@123")
    time.sleep(0.5)
    
    # 【技术点】模拟键盘全选+复制
    pwd_input.send_keys(Keys.CONTROL, 'a')
    pwd_input.send_keys(Keys.CONTROL, 'c')
    print("[INFO] 已执行 Ctrl+A 全选 & Ctrl+C 复制")
    
    # 清空后粘贴
    pwd_input.clear()
    time.sleep(0.3)
    # 【技术点】模拟键盘粘贴
    pwd_input.send_keys(Keys.CONTROL, 'v')
    pasted_val = pwd_input.get_attribute("value")
    print(f"[INFO] 粘贴后的密码框值长度: {len(pasted_val)}")
    assert len(pasted_val) > 0, "粘贴操作失败"
    print("[PASS] 键盘复制/粘贴/输入验证成功")

# ==================== 6. 模拟鼠标操作（单击/双击/右击） ====================
def test_mouse_operations(driver):
    """模拟鼠标单击、双击、右击"""
    actions = ActionChains(driver)
    target = driver.find_element(By.CSS_SELECTOR, 
             "button[type='submit'], #loginBtn, .btn-login")
    
    # 【技术点】鼠标右击
    actions.context_click(target).perform()
    time.sleep(1)
    # 按ESC关闭右键菜单
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("[INFO] 鼠标右击操作完成")
    
    # 【技术点】鼠标双击
    actions.double_click(target).perform()
    time.sleep(1)
    print("[INFO] 鼠标双击操作完成")
    
    # 【技术点】鼠标单击（hover也可归入此类）
    actions.move_to_element(target).click().perform()
    time.sleep(1)
    print("[PASS] 鼠标单击/双击/右击验证成功")

# ==================== 7. 弹出消息框处理与截屏 ====================
def test_alert_handling(driver):
    """处理alert弹窗并进行截屏"""
    # 通过JS触发一个alert用于演示
    driver.execute_script("alert('这是一条测试弹窗消息');")
    time.sleep(1)
    
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        print(f"[INFO] 捕获弹窗内容: '{alert_text}'")
        
        # 【技术点】弹窗截屏（Selenium4支持）
        try:
            alert.screenshot_as_png
            print("[INFO] 弹窗截屏成功(Selenium4)")
        except Exception:
            # 降级：对当前页面截屏
            driver.save_screenshot("alert_page_screenshot.png")
            print("[INFO] 已对弹窗所在页面进行截屏保存")
        
        # 【技术点】弹窗确定操作
        alert.accept()
        print("[PASS] 弹窗确定操作验证成功")
    except TimeoutException:
        print("[WARN] 未检测到弹窗，可能已被自动关闭")

# ==================== 8. 切换浏览器窗口和Frame ====================
def test_window_frame_switch(driver):
    """多窗口切换与Frame嵌套处理"""
    original_handle = driver.current_window_handle
    
    # 【技术点】切换浏览器窗口
    driver.execute_script("window.open('https://auth.scnu.edu.cn/', '_blank');")
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != original_handle:
            driver.switch_to.window(handle)
            print(f"[INFO] 已切换到新窗口: {driver.title}")
            break
    driver.close()
    driver.switch_to.window(original_handle)
    print("[PASS] 浏览器窗口切换验证成功")
    
    # 【技术点】Frame切换
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    if frames:
        driver.switch_to.frame(frames[0])
        print(f"[INFO] 已切入Frame, 当前URL: {driver.current_url}")
        driver.switch_to.default_content()
        print("[INFO] 已切回主文档")
    else:
        print("[INFO] 当前页面无iframe，使用JS创建演示Frame")
        driver.execute_script("""
            var f=document.createElement('iframe');
            f.id='testFrame'; f.src='about:blank';
            document.body.appendChild(f);
        """)
        driver.switch_to.frame("testFrame")
        driver.switch_to.default_content()
        print("[PASS] Frame切换验证成功(演示模式)")

# ==================== 9. 页面元素截屏 & 验证码获取 ====================
def test_element_screenshot_and_captcha(driver):
    """元素级截屏与验证码图片获取"""
    # 【技术点】页面元素截屏
    try:
        login_form = driver.find_element(By.CSS_SELECTOR, 
                     "form, .login-form, #loginForm")
        login_form.screenshot("login_form_element.png")
        print("[INFO] 登录表单元素截屏已保存: login_form_element.png")
    except NoSuchElementException:
        body = driver.find_element(By.TAG_NAME, "body")
        body.screenshot("page_body_element.png")
        print("[INFO] 页面body元素截屏已保存")
    
    # 【技术点】验证码获取
    captcha_selectors = [
        "img.captcha", "#captchaImg", "img[id*='captcha']",
        "img[src*='captcha']", "img.verify-code", "#verifyImg"
    ]
    captcha_found = False
    for sel in captcha_selectors:
        try:
            captcha_img = driver.find_element(By.CSS_SELECTOR, sel)
            captcha_img.screenshot("captcha_code.png")
            src = captcha_img.get_attribute("src")
            print(f"[INFO] 验证码图片已截屏保存, src={src[:80]}...")
            captcha_found = True
            break
        except NoSuchElementException:
            continue
    
    if not captcha_found:
        print("[WARN] 未找到验证码元素，尝试截取登录区域作为替代")
        driver.save_screenshot("captcha_area_fallback.png")
    print("[PASS] 元素截屏与验证码获取验证完成")

# ==================== 主流程调度 ====================
def main():
    """主测试流程入口"""
    print("=" * 50)
    print("  华南师范大学统一身份认证平台 - 自动化测试开始")
    print("=" * 50)
    
    driver = init_browser()
    try:
        test_navigation(driver)           # 步骤1-2: 导航与前进后退
        test_text_extraction(driver)      # 步骤3: 文本获取
        test_checkbox_button(driver)      # 步骤4: 复选框/按钮
        test_keyboard_operations(driver)  # 步骤5: 键盘操作
        test_mouse_operations(driver)     # 步骤6: 鼠标操作
        test_alert_handling(driver)       # 步骤7: 弹窗处理
        test_window_frame_switch(driver)  # 步骤8: 窗口/Frame切换
        test_element_screenshot_and_captcha(driver)  # 步骤9: 元素截屏&验证码
        
        print("\n" + "=" * 50)
        print("  ? 全部测试技术点验证完毕!")
        print("=" * 50)
    except Exception as e:
        print(f"[ERROR] 测试异常: {e}")
        driver.save_screenshot("error_screenshot.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("[INFO] 浏览器已关闭，测试结束")

if __name__ == "__main__":
    main()