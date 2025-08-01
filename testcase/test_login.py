import allure
import pytest
from selenium.webdriver.common.by import By
from conftest import open_homepage
from po.event import Event
from settings import ENV
from common.log import log

class TestLogin:
    @pytest.mark.parametrize("username,password,result",[
        (ENV.username,ENV.password,'用户基础数据')
    ],ids=[
        'test_datacenters_01'
    ]
    )
    @allure.feature('登录')
    @allure.story('密码登录')
    def test_pwdlogin(self,username,password,result,open_homepage):
        driver=open_homepage
        Event.Event_pwdtologin(driver,username,password)
        text=driver.get_text((By.XPATH,"//div[@class='flex-box flex-ac']//div[1]"))
        assert result in text
        driver.sel_click(
            (By.XPATH, "//i[@class='el-icon']//*[name()='svg']//*[name()='path' and contains(@fill,'currentCol')]"))
        driver.sel_click((By.XPATH, "//span[contains(text(),'退出登录')]"))
        driver.click_element_ui_confirm()
        log.info('登录成功，断言通过')

    @pytest.mark.parametrize("username,verifycode,result", [
        ('','1234','请输入账号'),
        (ENV.username, '1234','用户基础数据'),
        ('bucunzai','1234','请输入正确的手机号'),
        (ENV.username, '123','验证码错误'),
        (ENV.username, '', '请输入正确的验证码'),
        ('18883228657', '1234', 'token格式错误'),

    ],ids=[
        'test_datacenters_02',
        'test_datacenters_03',
        'test_datacenters_04',
        'test_datacenters_05',
        'test_datacenters_06',
        'test_datacenters_07',

    ]
    )
    @allure.feature('登录')
    @allure.story('验证码登陆')
    def test_verifycodelogin(self,username,verifycode,result,open_homepage):
        driver=open_homepage
        driver.get(ENV.URL)
        Event.Event_verifycodetologin(driver,username,verifycode)
        if result == '请输入账号':
            text=driver.get_text((By.XPATH,"//div[@class='el-form-item__content']/div[@class='el-form-item__error']"))
            assert result in text
            log.info('请输入账号，断言通过')
        if result == '用户基础数据':
            text=driver.get_text((By.XPATH,"//div[@class='flex-box flex-ac']//div[1]"))
            assert result in text
            driver.sel_click(
                (By.XPATH, "//i[@class='el-icon']//*[name()='svg']//*[name()='path' and contains(@fill,'currentCol')]"))
            driver.sel_click((By.XPATH, "//span[contains(text(),'退出登录')]"))
            driver.click_element_ui_confirm()
            log.info('登录成功，断言通过')
        elif result == '请输入正确的手机号':
            text=driver.get_text((By.XPATH,"//div[@class='el-form-item__error' and contains(text(),'请输入正确的手机号')]"))
            assert result in text
            log.info('请输入正确的手机号，断言通过')
        elif result == '验证码错误':
            text=driver.alert_text()
            assert result in text
            log.info('弹窗验证码错误，断言通过')
        elif result == '请输入正确验证码':
            text=driver.get_text((By.XPATH,"//div[@class='el-form-item__content']/div[@class='el-form-item__error']"))
            assert result in text
            log.info('请输入正确的验证码，断言通过')
        elif result == 'token格式错误':
            text=driver.alert_text()
            assert result in text
            log.info('token格式错误，断言通过')