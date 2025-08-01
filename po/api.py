import allure
import requests
from settings import ENV
from common.log import log


class Api:
    @allure.step('获取该用户的政策')
    def get_policy_list(self):
        try:
            url=f'{ENV.APIURL}/api/admin/policy/article/page'
            data = {
                'userId':'198',
                'totalElements' :'true'
            }
            response = requests.get(url, headers=ENV.headers, params=data)
            jsons = response.json()['list']
            log.info(f'获取政策列表：{jsons}')
            return jsons
        except Exception as e:
            log.error(f'获取政策列表失败：{e}')
            raise e
    @allure.step('删除所有政策')
    def delete_all_policy(self):
        try:
            url = f'{ENV.APIURL}/api/admin/policy/article/delete'
            #获取政策id
            datas=self.get_policy_list()
            if  len(datas)>0:
                for data in datas:
                    pid=data["id"]
                    log.debug(pid)
                    code=requests.get(url,headers=ENV.headers,params={'id':f'{pid}'}).status_code
                    log.debug(f"删除{pid}成功状态码：{code}")
            else:
                log.info("没有政策可删除")
        except  Exception as e:
            log.info(f'发生异常：{e}')
            raise e
    @allure.step('获取该用户的项目')
    def get_myproject_list(self):
        try:
            url = f'{ENV.APIURL}/api/admin/project/page'
            data = {
                'userId': '198',
                'totalElements': 'true',
                'size': '50',
                'page':'1'
            }
            response = requests.get(url, headers=ENV.headers, params=data)
            jsons = response.json()['list']
            log.info(f'获取项目列表：{jsons}')
            return jsons
        except Exception as e:
            log.error(f'获取项目列表失败：{e}')
            raise e

    @allure.step('删除所有项目')
    def delete_all_project(self):
        try:
            url = f'{ENV.APIURL}/api/admin/project/batch/delete'
            # 获取项目id
            datas = self.get_myproject_list()
            if len(datas) > 0:
                for data in datas:
                    pid = data["id"]
                    log.debug(pid)
                    code=requests.post(url, headers=ENV.headers, json={
                        'ids':[pid]
                    }).status_code
                    log.debug(f"删除{pid}成功,状态码：{code}")
            else:
                log.info("没有项目可删除")
        except  Exception as e:
            log.info(f'发生异常：{e}')
            raise e
    @allure.step('获取该用户的课程')
    def get_mycourse_list(self):
        try:
            url = f'{ENV.APIURL}/api/admin/course/page'
            data = {
                'userId': '198',
                'totalElements': 'true'
            }
            response = requests.get(url, headers=ENV.headers, params=data)
            jsons = response.json()['list']
            log.info(f'获取课程列表：{jsons}')
            return jsons
        except Exception as e:
            log.error(f'获取课程列表失败：{e}')
            raise e

    @allure.step('删除所有课程')
    def delete_all_course(self):
        try:
            url = f'{ENV.APIURL}/api/admin/course/delete'
            # 获取项目id
            datas = self.get_mycourse_list()
            if len(datas) > 0:
                for data in datas:
                    cid = data["id"]
                    log.debug(cid)
                    code=requests.get(url, headers=ENV.headers, params={'id':f'{cid}'}).status_code
                    log.debug(f"删除{cid}成功,状态码：{code}")
            else:
                log.info("没有课程可删除")
        except  Exception as e:
            log.info(f'发生异常：{e}')
            raise e

    @allure.step('获取校企合作')
    def get_cooperation_list(self):
        try:
            url = f'{ENV.APIURL}/api/admin/information/page'
            data = {
                'totalElements': 'true',
                'title': '校企合作666',
                'type':'SCHOOL_ORG_COOPERATION_ARTICLE',
                'page':'1',
                'size':'50'
            }
            response = requests.get(url, headers=ENV.headers, params=data)
            jsons = response.json()['list']
            log.info(f'获取课程列表：{jsons}')
            return jsons
        except Exception as e:
            log.error(f'获取课程列表失败：{e}')
            raise e

    @allure.step('删除所有校企合作')
    def delete_all_cooperation(self):
        try:
            url = f'{ENV.APIURL}/api/admin/information/delete'
            # 获取项目id
            datas = self.get_cooperation_list()
            if len(datas) > 0:
                for data in datas:
                    cid = data["id"]
                    log.debug(cid)
                    code = requests.get(url, headers=ENV.headers, params={'id': f'{cid}'}).status_code
                    log.debug(f"删除{cid}成功,状态码：{code}")
            else:
                log.info("没有课程可删除")
        except  Exception as e:
            log.info(f'发生异常：{e}')
            raise e


if  __name__ == '__main__':
    api = Api()
    # json=api.get_policy_list()
    # api.delete_all_policy()
    # projects=api.get_myproject_list()
    # api.delete_all_project()
    # api.get_mycourse_list()
    # api.delete_all_course()
    api.get_cooperation_list()
    api.delete_all_cooperation()