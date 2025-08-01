import os
import re
from time import sleep
import time
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from common.log import log
from settings import ENV
from config.conf import ALLURE_IMAGE_DIR
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Base:
    """初始化driver、清除数据、封装selenium操作（第3层:操作层）"""

    def __init__(self, driver=None):
        if driver:
            self.driver = driver
        else:
            service = Service(r'D:\python program\project\auto-ui-share\.venv\Scripts\chromedriver.exe')
            self.driver = webdriver.Chrome(service=service)
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            # MysqlAuto().execute(DBsql.sql_list)

    def get(self, url):
        try:
            self.driver.get(url)
            log.info(f"进入{url}")
        except Exception as e:
            log.error(e)
            raise e

    def quit(self):
        try:
            self.driver.quit()
        except Exception as e:
            log.error(e)
            raise e

    def click_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception as e:
            log.error(e)
            raise e

    @allure.step('鼠标左键单击')
    def sel_click(self, sel, timeout=20):
        selen = re.sub('[^\u4e00-\u9fa5]+', '', str(sel))
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(sel)).click()
            sleep(0.2)
            if len(selen) > 0:
                log.info(f'点击：{selen}')
            else:
                log.info(f'点击{sel}')
            return True
        except Exception as e:
            log.error(f"无法定位到该元素：{selen}.异常为：\n{e}")
            raise e

    @allure.step('输入内容')
    def sel_send_keys(self, sel, value, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(sel)).clear()
            sleep(0.2)
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(sel)).send_keys(value)
            sleep(0.2)
            selen = re.sub('[^\u4e00-\u9fa5]+', '', str(sel))
            if len(selen) > 0:
                log.info(f'点击：{selen},并输入值：{value}')
            return True
        except Exception as e:
            log.error(f'无法定位到该元素{sel}.异常为：\n{e}')
            raise e

    @allure.step('获取指定元素的text值')
    def get_text(self, els, timeout=10, mode=0):
        # 获取指定元素的text值
        try:
            # 等待袁术在页面上显示
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(els)
            )
            if mode == 0:
                log.info(element.text)
                return element.text
            else:
                log.info(element.get_attribute('textContent'))
                return element.get_attribute('textContent')
        except Exception as e:
            print(f'错误：{e}')
            return None

    def allure_save_screenshot(self, name):
        with open(self.chrom_save_screenshot(), 'rb') as f:
            log.info('网页截图')
            allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.JPG)

    @allure.step('chrome自带截图')
    def chrom_save_screenshot(self):
        try:
            img_dir = ALLURE_IMAGE_DIR
            str_time = str(time.time())[:10]
            img_file = ALLURE_IMAGE_DIR + f'\\tmp_chrome_save_screenshot{str_time}.jpg'
            if not os.path.isdir(img_dir):
                os.makedirs(img_dir)
                log.info(f'创建目录：{img_dir}')
            sleep(1)
            self.driver.save_screenshot(img_file)
            return img_file
        except Exception as e:
            log.error(f'截图发生异常{e}')
            raise e


    @allure.step('点击Element UI弹窗的确定按钮')
    def click_element_ui_confirm(self):
        """点击Element UI弹窗的确定按钮"""
        try:
            # 等待弹窗完全加载
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='el-message-box' and .//span[text()='提示']]"))
            )

            # 定位确定按钮的多种策略
            confirm_locators = [
                # 策略1：通过按钮文本定位
                "//div[@class='el-message-box__btns']/button[span='确定']",

                # 策略2：通过主要按钮样式定位
                "//div[@class='el-message-box__btns']/button[contains(@class, 'el-button--primary')]",

                # 策略3：通过按钮顺序定位（确定按钮通常是第二个）
                "//div[@class='el-message-box__btns']/button[2]",

                # 策略4：通过完整路径定位
                "//div[@class='el-message-box']//div[@class='el-message-box__btns']/button[span='确定']"
            ]

            # 尝试所有定位策略
            for locator in confirm_locators:
                try:
                    confirm_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, locator))
                    )

                    # 高亮按钮（调试用）
                    self.driver.execute_script("arguments[0].style.border='2px solid red';", confirm_btn)

                    # 滚动到视图中心
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_btn)

                    confirm_btn.click()
                    log.info(f"成功点击确定按钮，使用定位器: {locator}")
                    return True
                except Exception as e:
                    log.info(f'所有策略都失败：{e}')
                    continue

            # 如果所有策略都失败
            raise Exception("所有定位策略均失败")

        except Exception as e:
            # 错误处理和调试
            print(f"点击确定按钮时出错: {str(e)}")
            self.driver.save_screenshot("confirm_error.png")

            # 保存当前页面HTML用于调试
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)

            raise

    @allure.step('获取弹窗提示')
    def alert_text(self,mode=0):
        try:
            element=(WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH,"(//p[@class='el-message__content'])[1]"))
            ))
            if mode == 0:
                log.info(f'弹窗显示：{element.text}')
                return element.text
            else:
                log.info(element.get_attribute('textContent'))
                return element.get_attribute('textContent')
        except Exception as e:
            log.error(f'获取弹窗异常:{e}')
            raise e

    @allure.step('点击此刻按钮')
    def time_confirm_click(self):
        try:
            (WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='el-button el-button--small is-text el-picker-panel__link-btn']")))).click()
        except Exception as e:
            log.error(f'发生异常：{e}')
            raise e
    @allure.step('上传文件')
    def push_file(self,sel,file_rule=ENV.test_txt):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(sel)
            )
            element.send_keys(file_rule)
            time.sleep(2)
            log.info(f'上传文件成功')
        except Exception as e:
            log.error(f'发生异常：{e}')
            raise e
