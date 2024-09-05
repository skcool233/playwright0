from module import *
from module.table import Table
from module.locators import Locators
from utils.my_date import *


class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""
        self.locators = Locators(self.page)

    def navigate(self):
        self.page.goto(self.url)

    def table(self, 唯一文字, 表格序号=-1):
        return Table(self.page, 唯一文字, 表格序号)

    def click_button(self, button_name, timeout=30_000):
        button_loc = self.page.locator("button")
        for 单字符 in button_name:
            button_loc = button_loc.filter(has_text=单字符)
        button_loc.click(timeout=timeout)

    def search(self, 搜索内容: str, placeholder=None):
        if placeholder:
            self.page.locator(f"//span[@class='ant-input-affix-wrapper']//input[contains(@placeholder,'{placeholder}')]").fill(搜索内容)
        else:
            self.page.locator(".ant-input-affix-wrapper input").fill(搜索内容)
        self.page.wait_for_load_state("networkidle")

    def 表单_文本框填写(self, 表单项名称: str, 需要填写的文本: str, 表单最上层定位: Locator = None, timeout: float = None):
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator("input,textarea").locator("visible=true").last.fill(需要填写的文本, timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("input,textarea").locator("visible=true").last.fill(需要填写的文本, timeout=timeout)

    def 表单_下拉框选择(self, 表单项名称: str, 需要选择的项: str, 表单最上层定位: Locator = None, timeout: float = None):
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator("visible=true").click(timeout=timeout)
            if 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator('//input[@type="search"]').count():
                表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator('//input[@type="search"]').fill(需要选择的项, timeout=timeout)
            self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true").click(timeout=timeout)
            if self.locators.表单项中包含操作元素的最上级div(表单项名称).locator('//input[@type="search"]').count():
                self.locators.表单项中包含操作元素的最上级div(表单项名称).locator('//input[@type="search"]').fill(需要选择的项, timeout=timeout)
            self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(timeout=timeout)
        expect(self.page.locator(".ant-select-dropdown")).to_be_hidden(timeout=timeout)

    def 表单_radio选择(self, 表单项名称: str, 需要选择的项: str, 表单最上层定位: Locator = None, timeout: float = None):
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator("label").locator("visible=true").filter(has_text=需要选择的项).locator("input").check(timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("label").locator("visible=true").filter(has_text=需要选择的项).locator("input").check(timeout=timeout)

    def 表单_switch开关(self, 表单项名称: str, 开关状态: str, 表单最上层定位: Locator = None, timeout: float = None):
        if "开" in 开关状态 or "是" in 开关状态:
            开关状态bool = True
        else:
            开关状态bool = False
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).get_by_role("switch").set_checked(开关状态bool, timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).get_by_role("switch").set_checked(开关状态bool, timeout=timeout)

    def 表单_日期(self, 表单项名称: str, 日期: str, 表单最上层定位: Locator = None, timeout: float = None):
        if 表单最上层定位:
            日期控件定位 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
        else:
            日期控件定位 = self.locators.表单项中包含操作元素的最上级div(表单项名称)
        日期列表 = 日期.split(",")
        for index, 单日期 in enumerate(日期列表):
            try:
                int(单日期)
                格式化后的日期 = 返回当前时间xxxx_xx_xx加N天(int(单日期))
            except:
                格式化后的日期 = 单日期
            日期控件定位.locator("input").nth(index).click(timeout=timeout)
            日期控件定位.locator("input").nth(index).fill(格式化后的日期, timeout=timeout)
            日期控件定位.locator("input").nth(index).blur(timeout=timeout)

    def 快捷操作_填写表单(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        for 表单项, 内容 in kwargs.items():
            if not 内容:
                continue
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-input").count():
                self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-select-selector").count():
                self.表单_下拉框选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-radio-group").count():
                self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).get_by_role("switch").count():
                self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-picker").count():
                self.表单_日期(表单项名称=表单项, 日期=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")

    def 快捷操作_填写表单_增加根据数据类确定唯一表单版(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        页面上已有的表单项列表 = []
        已经有唯一表单项 = False
        if 表单最上层定位:
            处理后的表单最上层定位 = 表单最上层定位
        else:
            for index, 表单项 in enumerate(kwargs.keys()):
                if index == 0:
                    try:
                        self.locators.表单项中包含操作元素的最上级div(表单项).last.wait_for(timeout=timeout)
                    except:
                        pass

                if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 0:
                    continue
                else:
                    if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 1:
                        已经有唯一表单项 = True
                    页面上已有的表单项列表.append(self.locators.表单项中包含操作元素的最上级div(表单项))
                if 已经有唯一表单项 and len(页面上已有的表单项列表) >= 2:
                    break

            包含可见表单项的loc = self.page.locator("*")
            for 已有表单项_loc in 页面上已有的表单项列表:
                包含可见表单项的loc = 包含可见表单项的loc.filter(has=已有表单项_loc)
            if 已经有唯一表单项:
                处理后的表单最上层定位 = 包含可见表单项的loc.last
            else:
                处理后的表单最上层定位 = min(包含可见表单项的loc.all(), key=lambda loc: len(loc.text_content()))

        for 表单项, 内容 in kwargs.items():
            if not 内容:
                continue
            if self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-input").count():
                self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-select-selector").count():
                self.表单_下拉框选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-radio-group").count():
                self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).get_by_role("switch").count():
                self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-picker").count():
                self.表单_日期(表单项名称=表单项, 日期=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")
