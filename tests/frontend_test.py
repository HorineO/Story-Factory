#!/usr/bin/env python
import os
import sys
import time
import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 配置日志
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'frontend_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('frontend_tests')


class FrontendTest(unittest.TestCase):
    """前端UI组件测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试前准备：启动浏览器"""
        logger.info("启动浏览器")
        try:
            chrome_options = Options()
            # 根据环境变量决定是否使用无头模式
            if os.environ.get('CI') == 'true':
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
            cls.driver.maximize_window()
            cls.driver.get("http://localhost:3000")  # 假设前端运行在3000端口
            
            # 等待页面加载
            WebDriverWait(cls.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".react-flow"))
            )
            
            logger.info("浏览器初始化完成")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            if hasattr(cls, 'driver') and cls.driver:
                cls.driver.quit()
            raise
    
    @classmethod
    def tearDownClass(cls):
        """测试后清理：关闭浏览器"""
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()
            logger.info("浏览器已关闭")
    
    def setUp(self):
        """每个测试前的准备"""
        # 刷新页面以保证每个测试在干净的环境中运行
        self.driver.refresh()
        # 等待页面加载
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".react-flow"))
        )
    
    def test_navigation_bar_presence(self):
        """测试导航栏是否存在"""
        logger.info("测试导航栏是否存在")
        try:
            navbar = self.driver.find_element(By.CSS_SELECTOR, ".navbar")
            self.assertTrue(navbar.is_displayed(), "导航栏未显示")
            
            # 检查导航栏菜单项
            menu_items = ["文件", "编辑", "帮助"]
            for item in menu_items:
                menu_element = self.driver.find_element(By.XPATH, f"//div[contains(@class, 'navbar')]//div[text()='{item}']")
                self.assertTrue(menu_element.is_displayed(), f"导航栏菜单项'{item}'未显示")
            
        except NoSuchElementException as e:
            self.fail(f"导航栏元素未找到: {e}")
    
    def test_left_panel_functionality(self):
        """测试左侧面板功能"""
        logger.info("测试左侧面板功能")
        try:
            # 检查左侧面板是否存在
            left_panel = self.driver.find_element(By.CSS_SELECTOR, ".left-panel")
            self.assertTrue(left_panel.is_displayed(), "左侧面板未显示")
            
            # 检查标签页是否存在
            tab_buttons = left_panel.find_elements(By.CSS_SELECTOR, ".tab-button")
            self.assertGreaterEqual(len(tab_buttons), 1, "左侧面板应至少有一个标签页")
            
            # 切换标签页并验证内容变化
            for i, tab in enumerate(tab_buttons):
                tab.click()
                time.sleep(0.5)  # 等待标签内容加载
                tab_content = left_panel.find_element(By.CSS_SELECTOR, ".tab-content")
                self.assertTrue(tab_content.is_displayed(), f"标签页 {i} 内容未显示")
        
        except NoSuchElementException as e:
            self.fail(f"左侧面板元素未找到: {e}")
    
    def test_flow_canvas_interaction(self):
        """测试流程画布交互"""
        logger.info("测试流程画布交互")
        try:
            # 检查流程画布是否存在
            flow_canvas = self.driver.find_element(By.CSS_SELECTOR, ".react-flow")
            self.assertTrue(flow_canvas.is_displayed(), "流程画布未显示")
            
            # 检查添加节点功能
            # 假设有一个"添加文本节点"按钮
            add_node_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '文本节点') or contains(@title, '文本节点')]")
            add_node_button.click()
            
            # 验证节点是否添加到画布
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".react-flow__node"))
            )
            
            nodes = self.driver.find_elements(By.CSS_SELECTOR, ".react-flow__node")
            self.assertGreaterEqual(len(nodes), 1, "节点未成功添加到画布")
            
            # 测试节点选择
            nodes[0].click()
            time.sleep(0.5)  # 等待选择效果应用
            
            # 检查是否触发了节点选择事件（通过检查节点是否有选中样式或属性面板是否更新）
            try:
                selected_node = self.driver.find_element(By.CSS_SELECTOR, ".react-flow__node.selected")
                self.assertTrue(selected_node.is_displayed(), "节点未被选中")
            except NoSuchElementException:
                self.fail("未找到选中的节点")
        
        except NoSuchElementException as e:
            self.fail(f"流程画布元素未找到: {e}")
        
        except TimeoutException:
            self.fail("添加节点后未能在画布上找到节点")
    
    def test_context_menu(self):
        """测试上下文菜单"""
        logger.info("测试上下文菜单")
        try:
            # 先添加一个节点
            add_node_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '文本节点') or contains(@title, '文本节点')]")
            add_node_button.click()
            
            # 等待节点添加到画布
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".react-flow__node"))
            )
            
            # 获取节点
            node = self.driver.find_element(By.CSS_SELECTOR, ".react-flow__node")
            
            # 右键点击节点
            webdriver.ActionChains(self.driver).context_click(node).perform()
            
            # 等待上下文菜单出现
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".context-menu"))
            )
            
            # 验证上下文菜单是否显示
            context_menu = self.driver.find_element(By.CSS_SELECTOR, ".context-menu")
            self.assertTrue(context_menu.is_displayed(), "上下文菜单未显示")
            
            # 检查菜单项
            menu_items = context_menu.find_elements(By.CSS_SELECTOR, ".menu-item")
            self.assertGreaterEqual(len(menu_items), 1, "上下文菜单应至少有一个菜单项")
            
            # 测试点击菜单项（例如"删除"）
            delete_item = None
            for item in menu_items:
                if "删除" in item.text:
                    delete_item = item
                    break
            
            if delete_item:
                delete_item.click()
                time.sleep(1)  # 等待删除操作完成
                
                # 验证节点是否被删除
                nodes = self.driver.find_elements(By.CSS_SELECTOR, ".react-flow__node")
                self.assertEqual(len(nodes), 0, "节点未被删除")
        
        except NoSuchElementException as e:
            self.fail(f"上下文菜单元素未找到: {e}")
        
        except TimeoutException:
            self.fail("上下文菜单未显示")
    
    def test_node_properties_panel(self):
        """测试节点属性面板"""
        logger.info("测试节点属性面板")
        try:
            # 添加一个节点
            add_node_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '文本节点') or contains(@title, '文本节点')]")
            add_node_button.click()
            
            # 等待节点添加到画布
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".react-flow__node"))
            )
            
            # 选中节点
            node = self.driver.find_element(By.CSS_SELECTOR, ".react-flow__node")
            node.click()
            
            # 等待属性面板更新
            time.sleep(1)
            
            # 切换到属性标签页（如果需要）
            props_tab = self.driver.find_element(By.XPATH, "//div[contains(@class, 'tab-button') and contains(text(), '属性')]")
            props_tab.click()
            
            # 等待属性面板加载
            time.sleep(0.5)
            
            # 检查属性面板是否显示
            props_panel = self.driver.find_element(By.CSS_SELECTOR, ".node-properties-tab")
            self.assertTrue(props_panel.is_displayed(), "节点属性面板未显示")
            
            # 更新节点标签
            label_input = self.driver.find_element(By.XPATH, "//input[@name='label']")
            label_input.clear()
            label_input.send_keys("测试标签")
            
            # 点击应用或保存按钮（如果有）
            apply_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '应用') or contains(text(), '保存')]")
            apply_button.click()
            
            # 等待更改应用
            time.sleep(1)
            
            # 验证节点标签是否更新
            updated_node = self.driver.find_element(By.CSS_SELECTOR, ".react-flow__node")
            node_label = updated_node.find_element(By.CSS_SELECTOR, ".node-label")
            self.assertEqual(node_label.text, "测试标签", "节点标签未更新")
        
        except NoSuchElementException as e:
            self.fail(f"节点属性面板元素未找到: {e}")
        
        except TimeoutException:
            self.fail("节点属性面板未显示")


if __name__ == "__main__":
    unittest.main() 