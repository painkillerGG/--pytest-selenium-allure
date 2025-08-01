import logging as log
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import ENV
class Event:
    @staticmethod
    @allure.step('密码登录')
    def Event_pwdtologin(driver,username,password):
        try:
            driver.sel_click((By.XPATH,"//div[@class='tab tab-active' and contains(text(),'密码登录')]"))
            driver.sel_send_keys((By.XPATH,"//input[@placeholder='请输入账号']"),username)
            driver.sel_send_keys((By.XPATH,"//input[@placeholder='请输入密码']"),password)
            time.sleep(10)
            log.debug('等待输入验证码')
            driver.sel_click((By.XPATH,"//button[@type='button' and normalize-space(.)='登录']"))
        except Exception as e:
            log.error(f'发生异常为{e}')
            raise e

    @staticmethod
    @allure.step('验证码登录')
    def Event_verifycodetologin(driver,username=ENV.username,verifycode=1234):
       try:
           driver.sel_click((By.XPATH, "//div[contains(text(),'验证码登录')]"))
           driver.sel_send_keys((By.XPATH, "//input[@placeholder='请输入账号']"), username)
           driver.sel_click((By.XPATH, "//div[@class='code-btn' and contains(text(),'获取验证码')]"))
           driver.sel_send_keys((By.XPATH, "//input[@placeholder='请输入验证码']"), verifycode)
           time.sleep(1)
           driver.sel_click((By.XPATH, "//button[@type='button' and normalize-space(.)='登录']"))
       except Exception as e:
           log.error(f'发生异常为{e}')
           raise e

    @staticmethod
    @allure.step('发布政策')
    def Event_publishpolicy(driver,pname='test',category='人才政策',einstitution='test',hyphen='test11',detail='test',filerule=ENV.test_txt):
        try:
            driver.sel_click((By.XPATH, "//span[contains(text(),'发布中心')]"))
            driver.sel_click((By.XPATH, "//span[contains(text(),'我的发布')]"))
            driver.sel_click(
                (By.XPATH, "//div[contains(normalize-space(),'发布政策')]/../../div[contains(text(),'立即发布')]"))
            # 通过for的值来获取input
            driver.sel_send_keys((By.XPATH,"//input[@id=//label[contains(normalize-space(), '政策名称')]/@for]"),pname)
            driver.sel_click(
                (By.XPATH, "//span[contains(text(),'请选择你的类型')]"))
            driver.sel_click((By.XPATH, f"//*[contains(text(),'{category}')]"))
            driver.sel_click((By.XPATH, "//input[@placeholder='请选择时间']"))
            driver.time_confirm_click()
            driver.sel_send_keys((By.XPATH,"//input[@id=//label[contains(normalize-space(), '发布机构')]/@for]"),einstitution)
            driver.sel_send_keys((By.XPATH,"//input[@id=//label[contains(normalize-space(), '发文字号')]/@for]"),hyphen)
            driver.sel_send_keys((By.XPATH,"//div[@class='ql-editor ql-blank']"),detail)
            driver.push_file((By.XPATH,"//div[@class='upload-file-uploader']//input[@name='files']"))
            driver.sel_click((By.XPATH,"//button[contains(@class, 'el-button') and .//span[text()='保存']]"))
        except Exception as e:
            log.error(f'发生异常：{e}')
            raise e

    @staticmethod
    @allure.step('发布项目')
    def Event_publishproject(driver,title='test_project',category='其他类型',content='test_content',require='test_require',file=ENV.test_txt):
        try:
            driver.sel_click((By.XPATH, "//span[contains(text(),'发布中心')]"))
            driver.sel_click((By.XPATH, "//span[contains(text(),'我的发布')]"))
            driver.sel_click(
                (By.XPATH, "//div[contains(normalize-space(),'发布项目')]/../../div[contains(text(),'立即发布')]"))
            driver.sel_send_keys((By.XPATH, "//input[@id=//label[contains(normalize-space(), '项目')]/@for]"), title)
            driver.sel_click(
                (By.XPATH, "//span[contains(text(),'请选择你的类型')]"))
            driver.sel_click((By.XPATH, f"//*[contains(text(),'{category}')]"))
            driver.sel_send_keys((By.XPATH, "//div[@class='ql-editor ql-blank'][1]"), content)
            driver.sel_send_keys((By.XPATH, "//div[contains(@class, 'el-form-item') and .//div[contains(@class, 'el-form-item__label') and contains(., '项目需求')]]//div[contains(@class, 'ql-editor')]"), require)
            driver.push_file(file)
            driver.sel_click((By.XPATH, "//button[contains(@class, 'el-button') and .//span[text()='保存']]"))
        except Exception as e:
            log.error(f'发生异常:{e}')
            raise e

    @staticmethod
    @allure.step('发布课程')
    def Event_publishcourse(driver):
        try:
            driver.sel_click((By.XPATH, "//span[contains(text(),'发布中心')]"))
            driver.sel_click((By.XPATH, "//span[contains(text(),'我的发布')]"))
            driver.sel_click(
                (By.XPATH, "//div[contains(normalize-space(),'上传在线课程')]/../../div[contains(text(),'立即发布')]"))
            driver.sel_send_keys((By.XPATH, "//input[@id=//label[contains(normalize-space(), '课程名称')]/@for]"), 'test课程')
            driver.push_file((By.XPATH, "//div[@class='el-upload el-upload--picture-card']//input[@name='files']"),
                                 r'D:\python program\study\PythonProject\auto-ui-minjianPC\source\test.png')
            driver.sel_send_keys((By.XPATH, "//input[@id=//label[contains(normalize-space(), '学校名称')]/@for]"), 'test学院')
            driver.sel_send_keys((By.XPATH, "//input[@id=//label[contains(normalize-space(), '老师名字')]/@for]"), 'test教授')
            driver.sel_click(
                (By.XPATH, "//span[contains(text(),'请选择课程类型')]"))
            driver.sel_click((By.XPATH, f"//*[contains(text(),'其他类型')]"))
            driver.sel_send_keys((By.XPATH, "//div[@class='ql-editor ql-blank']"),'简介。。。。。')
            driver.sel_click((By.XPATH, "(//button[@type='button' and ./span[text()='添加章节合集']])"))
            driver.sel_click((By.XPATH, "//button[contains(@class, 'el-button') and .//span[text()='保存']]"))
            time.sleep(1)
        except Exception as e:
            log.error(f'发生异常:{e}')
            raise e