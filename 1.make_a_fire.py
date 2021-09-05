from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
import time
import os


class Room:
    def __init__(self):
        # 创建浏览器对象
        self.driver = webdriver.Chrome()
        self.driver.get('http://adarkroom.doublespeakgames.com/?lang=zh_cn')
        # self.driver.get("file:///G:/Code/LearnPython/AutoScriptOnADarkRoom/adarkroom/index.html?lang=zh_cn")
        self.driver.implicitly_wait(3)  # 隐藏等待
        self.star()

    def open_url(self):
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.driver.get(os.path.normpath('file:///{0}/adarkroom/index.html?lang=zh_cn'.format(project_path)))  # 加载到小黑屋
        time.sleep(2)

    def click(self, by, value):
        """
        根据id，元素点击封装
        """
        self.driver.find_element(by, value).click()

    def click_id(self, id):
        """
        根据id定位元素并点击
        """
        self.click(By.ID, id)

    def click_id_event(self, id):
        """
        根据id定位元素并点击,如果元素还未出现或不可点击，则跳过；
        若遇见意外弹出导致元素无法点击，则处理弹窗事件后再次点击该元素
        """
        try:
            self.click_id(id)
        except NoSuchElementException:
            print("找不到元素：", id)
        except ElementClickInterceptedException:
            pass
        except ElementNotInteractableException:
            self.event()
            self.click_id(id)
        except EOFError as e:
            print("click_id_event", e)
            pass

    def click_css(self, css):
        """
        根据css定位元素并点击
        """
        self.click(By.CSS_SELECTOR, css)

    def element(self, by, value):
        """
        定位至元素
        """
        return self.driver.find_element(by, value)

    def element_css(self, css):
        """
        根据css定位元素
        """
        self.element(By.CSS_SELECTOR, css)

    def get_number(self, css):
        """
        利用css_selector获取对应物资数据，若不存在则返回0
        """
        try:
            number = int(self.element_css(css).get_attribute('textContent'))
            return number
        except EOFError as e:
            print("get_number:", e)
            return 0

    def get_text(self, css, type):
        """
        获取元素文本内容
        """
        try:
            return self.element_css(css).get_attribute(type)
        except NoSuchElementException:
            print("No text found")

    def sound(self):
        """
        出现声音弹窗是选择是
        """
        self.click_id('yes')
        time.sleep(1)

    def speed(self):
        """
        通过下面的菜单项选择游戏加速
        """
        self.click_css('.hyper')
        self.click_css('.hyper')
        self.click_id('yes')
        print("已加速")

    def keep(self):
        """
        游戏保存
        """
        self.click_css('.menu > span:nth-child(8)')  # 定位至保存
        self.click_id('export')  # 子弹窗选择导出游戏进度
        # 获取游戏进度文本
        text = self.get_text('#description > textarea', 'value')
        # 打开空文本文本并赋予读写
        with open("RoomKeep.txt", 'w') as f:
            f.write(text)
        print(text)
        self.click_id('done')  # 完成

    def input(self):
        """
        游戏导入
        """
        try:
            # 读取文本
            with open("RoomKeep.txt") as f:
                text = f.read()
            self.click_css('.menu > span:nth-child(8)')  # 定位至保存
            self.click_id('import')  # 子弹窗选择导入游戏进度
            self.click_id('yes')  # 确定导入
            # 写入游戏进度文本
            self.element_css('#description > textarea').send_keys(text)
            self.click_id('okay')  # 完成
            # time.sleep(1)
        except FileNotFoundError:
            print("RoomKeep.txt not found!")

    def event(self):
        # 判断意外弹窗
        self.driver.implicitly_wait(1)
        title = self.driver.find_element_by_class_name('eventTitle').get_attribute('textContent')
        print(title)
        if title == 'Penrose':
            self.event_Penrose()

    def event_Penrose(self):
        self.click_id('give in')
        time.sleep(3)
        handles = self.driver.window_handles  # 获取当前打开的所有窗口的句柄
        self.driver.switch_to.window(handles[1])
        self.driver.close()  # 关闭新窗口
        self.driver.switch_to.window(handles[0])

    def firewood(self):
        # 循环烧柴
        for _ in range(4):
            self.click_id_event('stokeButton')  # 烧柴
            time.sleep(5)

    def address_action(self, address_id, action_id):
        """
        跳转至地址并点击操作
        """
        self.click_id_event(address_id)
        time.sleep(1)
        self.click_id_event(action_id)

    # 循环动作
    def fire_cut_trapd(self):
        """
        循环完成烧火，砍柴，看陷阱
        """
        for _ in range(5):
            self.address_action('location_outside', 'gatherButton')  # 静谧森林伐木
            self.address_action('location_outside', 'trapsButton')  # 静谧森林看陷阱
            self.address_action('location_room', 'stokeButton')  # 生活间烧柴

    def star(self):
        self.sound()
        self.speed()
        self.click_id('lightButton')
        self.firewood()
        for _ in range(10):
            self.fire_cut_trapd()


if __name__ == '__main__':
    room = Room()
    # room.fire_cut_trapd()
    room.driver.quit()
