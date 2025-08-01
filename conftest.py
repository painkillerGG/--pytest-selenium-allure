import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from common.log import log
from po.event import Event
from po.home_page import HomePage
from settings import ENV


@pytest.fixture( scope='function')
def login():
    global driver
    driver=HomePage()
    driver.get(ENV.URL)
    Event.Event_verifycodetologin(driver)
    yield driver
    driver.quit()
    log.info("退出浏览器")
@pytest.fixture(scope='class')
def open_homepage():
    global driver
    driver=HomePage()
    driver.get(ENV.URL)
    log.debug("进入网页")
    yield driver
    driver.quit()

@pytest.fixture(scope='class')
def open_page():
    global driver
    service = Service(r'D:\python program\project\auto-ui-share\.venv\Scripts\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(ENV.URL)
    yield driver
    driver.quit()
    log.debug("退出浏览器")
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    log.info(f'test report: {result}')
    log.info(f"execution time-consuming:{round(call.duration,2)}second")
    if result.failed:
        try:
            log.info('error.screenshot.')
            driver.allure_save_screenshot('error.screenshot')
        except Exception as e:
            log.error(e)
            pass