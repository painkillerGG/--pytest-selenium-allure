import re
from time import sleep
from selenium.webdriver.support import expected_conditions
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.log import log as logger


@allure.step('鼠标左键单击')
def sel_click(driver, sel, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(expected_conditions.element_to_be_clickable(sel)).click()
        sleep(0.2)
        selen = re.sub('[^\u4e00-\u9fa5]+', '', str(sel))
        if len(selen) > 0:
            logger.info(f'点击：{selen}')
        return True
    except Exception as e:
        logger.error(f'无法定位到该元素：{sel}.异常为：\n{e}')
        raise e

@allure.step('输入内容')
def sel_send_keys(driver, sel, value, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(expected_conditions.element_to_be_clickable(sel)).clear()
        sleep(0.2)
        WebDriverWait(driver, timeout).until(expected_conditions.element_to_be_clickable(sel)).send_keys(value)
        sleep(0.2)
        selen = re.sub('[^\u4e00-\u9fa5]+','', str(sel))
        if len(selen) > 0:
            logger.info(f'点击：{selen},并输入值：{value}')
        return True
    except Exception as e:
        logger.error(f'无法定位到该元素{sel}.异常为：\n{e}')
        raise e

@allure.step('获取指定元素的text值')
def get_text(driver, els, timeout=10, mode=0):
        #获取指定元素的text值
    try:
        #等待袁术在页面上显示
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(els)
        )
        if mode == 0:
            logger.info(element.text)
            return element.text
        else :
            logger.info(element.get_attribute('textContent'))
            return element.get_attribute('textContent')
    except Exception as e:
        print(f'错误：{e}')
        return None
