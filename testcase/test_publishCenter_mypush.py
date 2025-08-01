import time
from time import sleep
import allure
from selenium.webdriver.common.by import By
from common.log import log
from conftest import open_homepage, login
from draft.Learnrequests import response
from po.event import Event
from settings import ENV
from po.api import Api
class Testpublish:
    @allure.feature('发布中心-我的发布')
    @allure.story('发布政策')
    def test_mypublish_policy(self, login):
        driver = login
        Api().delete_all_policy()
        pname = 'testname1'
        category = '居住政策'
        einstitution = '测试部'
        hyphen = 'test110'
        detail = 'testdetail'
        filerule = ENV.test_txt
        Event.Event_publishpolicy(driver, pname, category, einstitution, hyphen, detail, filerule)
        #弹窗断言
        result = driver.alert_text()
        assert '保存成功' in result
        log.info('保存成功，断言通过')
        #数据断言
        policies= Api().get_policy_list()
        result=policies[0]["title"]
        log.debug(result)
        assert pname in result
        log.info('查询到新增政策，断言通过')

    @allure.feature('发布中心-我的发布')
    @allure.story('发布项目')
    def test_mypublish_project(self,login):
        driver = login
        Api().delete_all_project()
        title = 'test_project'
        Event.Event_publishproject(driver,title=title)
        # 弹窗断言
        result = driver.alert_text()
        assert '保存成功' in result
        log.info('保存成功，断言通过')
        # 数据断言
        project = Api().get_myproject_list()
        result = project[0]["name"]
        log.debug(result)
        assert title in result
        log.info('查询到新增项目，断言通过')

    @allure.feature('发布中心-我的发布')
    @allure.story('上传在线课程')
    def test_mypublish_course(self, login):
        driver = login
        Api().delete_all_course()
        Event.Event_publishcourse(driver)
        result = driver.alert_text()
        assert '保存成功' in result
        log.info('保存成功，断言通过')



