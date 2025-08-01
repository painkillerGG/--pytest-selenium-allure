import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'log')
ALLURE_IMAGE_DIR=os.path.join(LOG_DIR, 'images_allure')#allure报告截图目录
if __name__ == '__main__':
    print(BASE_DIR)
    print(LOG_DIR)
    print(ALLURE_IMAGE_DIR)