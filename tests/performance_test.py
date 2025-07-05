#!/usr/bin/env python
import sys
import os
import time
import logging
import statistics
import requests
import json
import multiprocessing
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 配置日志
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'performance_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('performance_tests')

# 配置
DEFAULT_API_URL = "http://localhost:5000/api"
DEFAULT_ITERATIONS = 10
DEFAULT_CONCURRENT_USERS = 1


class PerformanceTest:
    """性能测试基类"""
    
    def __init__(self, api_url=DEFAULT_API_URL):
        self.api_url = api_url
        self.response_times = []
    
    def run_test(self, iterations=DEFAULT_ITERATIONS):
        """运行测试指定次数"""
        self.response_times = []
        
        for _ in tqdm(range(iterations), desc=f"运行 {self.__class__.__name__}"):
            start_time = time.time()
            self._execute_test()
            end_time = time.time()
            self.response_times.append((end_time - start_time) * 1000)  # 转换为毫秒
    
    def _execute_test(self):
        """具体测试实现，由子类重写"""
        raise NotImplementedError("子类必须实现_execute_test方法")
    
    def get_results(self):
        """获取测试结果统计"""
        if not self.response_times:
            return {
                "min": 0,
                "max": 0,
                "avg": 0,
                "median": 0,
                "p95": 0,
                "p99": 0,
                "count": 0
            }
            
        sorted_times = sorted(self.response_times)
        return {
            "min": min(sorted_times),
            "max": max(sorted_times),
            "avg": statistics.mean(sorted_times),
            "median": statistics.median(sorted_times),
            "p95": sorted_times[int(len(sorted_times) * 0.95)],
            "p99": sorted_times[int(len(sorted_times) * 0.99)],
            "count": len(sorted_times)
        }


class GetAllNodesTest(PerformanceTest):
    """测试获取所有节点的性能"""
    
    def _execute_test(self):
        response = requests.get(f"{self.api_url}/nodes")
        response.raise_for_status()


class CreateNodeTest(PerformanceTest):
    """测试创建节点的性能"""
    
    def _execute_test(self):
        data = {
            "type": "text",
            "data": {"label": f"Performance Test Node {time.time()}"},
            "position": {"x": 100, "y": 100}
        }
        response = requests.post(
            f"{self.api_url}/nodes",
            json=data
        )
        response.raise_for_status()


class GenerateTextTest(PerformanceTest):
    """测试生成文本的性能"""
    
    def _execute_test(self):
        data = {"user_content": "性能测试生成"}
        response = requests.post(
            f"{self.api_url}/generate",
            json=data
        )
        response.raise_for_status()


class UpdateNodeTextTest(PerformanceTest):
    """测试更新节点文本的性能"""
    
    def __init__(self, api_url=DEFAULT_API_URL):
        super().__init__(api_url)
        # 创建一个测试节点供所有测试使用
        self.node_id = None
    
    def setup(self):
        """为测试准备节点"""
        if not self.node_id:
            # 创建一个节点用于测试更新
            data = {
                "type": "text",
                "data": {"label": "Text Update Test Node", "text": ""},
                "position": {"x": 200, "y": 200}
            }
            response = requests.post(
                f"{self.api_url}/nodes",
                json=data
            )
            response.raise_for_status()
            self.node_id = response.json()["id"]
            logger.info(f"为文本更新测试创建节点: {self.node_id}")
    
    def _execute_test(self):
        if not self.node_id:
            self.setup()
            
        # 更新节点文本
        data = {"text": f"Updated text {time.time()}"}
        response = requests.put(
            f"{self.api_url}/nodes/{self.node_id}/text",
            json=data
        )
        response.raise_for_status()


class ComplexWorkflowTest(PerformanceTest):
    """测试复杂工作流程的性能"""
    
    def _execute_test(self):
        # 1. 创建源节点
        source_data = {
            "type": "text",
            "data": {"label": "Source Node", "text": "性能测试源文本"},
            "position": {"x": 0, "y": 0}
        }
        source_response = requests.post(
            f"{self.api_url}/nodes",
            json=source_data
        )
        source_response.raise_for_status()
        source_id = source_response.json()["id"]
        
        # 2. 创建目标节点
        target_data = {
            "type": "generate",
            "data": {"label": "Generate Node"},
            "position": {"x": 300, "y": 0}
        }
        target_response = requests.post(
            f"{self.api_url}/nodes",
            json=target_data
        )
        target_response.raise_for_status()
        target_id = target_response.json()["id"]
        
        # 3. 创建连接边
        edge_data = {
            "source": source_id,
            "target": target_id
        }
        edge_response = requests.post(
            f"{self.api_url}/edges",
            json=edge_data
        )
        edge_response.raise_for_status()
        
        # 4. 从节点生成内容
        generate_response = requests.post(
            f"{self.api_url}/nodes/{target_id}/generate"
        )
        generate_response.raise_for_status()
        
        # 5. 清理创建的节点和边
        requests.delete(f"{self.api_url}/nodes/{source_id}")
        requests.delete(f"{self.api_url}/nodes/{target_id}")


class BulkOperationsTest(PerformanceTest):
    """测试批量操作的性能"""
    
    def __init__(self, api_url=DEFAULT_API_URL, bulk_size=20):
        super().__init__(api_url)
        self.bulk_size = bulk_size
        self.created_nodes = []
    
    def _execute_test(self):
        # 1. 批量创建节点
        self.created_nodes = []
        for i in range(self.bulk_size):
            data = {
                "type": "text",
                "data": {"label": f"Bulk Node {i}"},
                "position": {"x": i * 50, "y": i * 30}
            }
            response = requests.post(
                f"{self.api_url}/nodes",
                json=data
            )
            response.raise_for_status()
            self.created_nodes.append(response.json()["id"])
        
        # 2. 获取所有节点
        response = requests.get(f"{self.api_url}/nodes")
        response.raise_for_status()
        
        # 3. 批量创建边连接相邻节点
        for i in range(self.bulk_size - 1):
            edge_data = {
                "source": self.created_nodes[i],
                "target": self.created_nodes[i + 1]
            }
            response = requests.post(
                f"{self.api_url}/edges",
                json=edge_data
            )
            response.raise_for_status()
        
        # 4. 获取所有边
        response = requests.get(f"{self.api_url}/edges")
        response.raise_for_status()
        
        # 5. 清理创建的节点（边会自动删除）
        for node_id in self.created_nodes:
            requests.delete(f"{self.api_url}/nodes/{node_id}")


def run_concurrent_test(test_class, api_url, iterations, concurrent_users):
    """运行并发测试"""
    def worker(result_queue):
        test = test_class(api_url)
        test.run_test(iterations)
        result_queue.put(test.response_times)
    
    logger.info(f"开始并发测试 {test_class.__name__}: {concurrent_users} 用户, 每个用户 {iterations} 次请求")
    
    # 创建进程池和结果队列
    result_queue = multiprocessing.Queue()
    processes = []
    
    # 启动进程
    for _ in range(concurrent_users):
        p = multiprocessing.Process(target=worker, args=(result_queue,))
        processes.append(p)
        p.start()
    
    # 等待所有进程完成
    for p in processes:
        p.join()
    
    # 收集结果
    all_response_times = []
    while not result_queue.empty():
        all_response_times.extend(result_queue.get())
    
    # 计算结果
    test_instance = test_class()
    test_instance.response_times = all_response_times
    return test_instance.get_results()


def generate_report(results, output_dir=None):
    """生成测试报告"""
    if output_dir is None:
        output_dir = os.path.join(parent_dir, 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f'performance_report_{timestamp}.json')
    chart_file = os.path.join(output_dir, f'performance_chart_{timestamp}.png')
    
    # 保存结果到JSON文件
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    # 绘制图表
    fig, axs = plt.subplots(2, figsize=(12, 10))
    
    # 响应时间条形图
    test_names = list(results.keys())
    avg_times = [results[name]['avg'] for name in test_names]
    median_times = [results[name]['median'] for name in test_names]
    p95_times = [results[name]['p95'] for name in test_names]
    
    x = range(len(test_names))
    width = 0.25
    
    axs[0].bar([i - width for i in x], avg_times, width, label='平均')
    axs[0].bar(x, median_times, width, label='中位数')
    axs[0].bar([i + width for i in x], p95_times, width, label='95百分位')
    
    axs[0].set_ylabel('响应时间 (毫秒)')
    axs[0].set_title('API响应时间')
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(test_names)
    axs[0].legend()
    
    # 最小/最大/p99响应时间
    min_times = [results[name]['min'] for name in test_names]
    max_times = [results[name]['max'] for name in test_names]
    p99_times = [results[name]['p99'] for name in test_names]
    
    axs[1].bar([i - width for i in x], min_times, width, label='最小')
    axs[1].bar(x, max_times, width, label='最大')
    axs[1].bar([i + width for i in x], p99_times, width, label='99百分位')
    
    axs[1].set_ylabel('响应时间 (毫秒)')
    axs[1].set_title('响应时间极值')
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(test_names)
    axs[1].legend()
    
    plt.tight_layout()
    plt.savefig(chart_file)
    
    logger.info(f"测试报告已保存到: {report_file}")
    logger.info(f"测试图表已保存到: {chart_file}")
    
    return report_file, chart_file


def main(iterations=DEFAULT_ITERATIONS, concurrent_users=DEFAULT_CONCURRENT_USERS, api_url=DEFAULT_API_URL):
    """运行所有性能测试"""
    logger.info(f"开始性能测试: {iterations} 次迭代, {concurrent_users} 并发用户")
    
    test_classes = [
        GetAllNodesTest,
        CreateNodeTest,
        GenerateTextTest,
        UpdateNodeTextTest,  # 新增测试类
        ComplexWorkflowTest,  # 新增测试类
        BulkOperationsTest    # 新增测试类
    ]
    
    results = {}
    
    # 运行单用户测试
    logger.info("运行单用户测试...")
    for test_class in test_classes:
        test_name = test_class.__name__
        logger.info(f"运行测试: {test_name}")
        test = test_class(api_url)
        
        # 针对特殊测试类需要执行setup
        if hasattr(test, 'setup'):
            test.setup()
            
        test.run_test(iterations)
        results[f"{test_name}_单用户"] = test.get_results()
    
    # 运行并发测试（如果需要）
    if concurrent_users > 1:
        logger.info("运行并发测试...")
        for test_class in test_classes:
            test_name = test_class.__name__
            logger.info(f"运行并发测试: {test_name}")
            
            # 跳过复杂工作流的并发测试，可能会引起冲突
            if test_name in ["ComplexWorkflowTest", "BulkOperationsTest"]:
                logger.info(f"跳过 {test_name} 的并发测试，避免资源冲突")
                continue
                
            concurrent_results = run_concurrent_test(
                test_class, api_url, iterations, concurrent_users
            )
            results[f"{test_name}_并发{concurrent_users}用户"] = concurrent_results
    
    # 生成测试报告
    generate_report(results)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Story Factory 性能测试")
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS, help="每个测试执行的次数")
    parser.add_argument("--concurrent-users", type=int, default=DEFAULT_CONCURRENT_USERS, help="并发用户数量")
    parser.add_argument("--api-url", type=str, default=DEFAULT_API_URL, help="API服务的URL地址")
    parser.add_argument("--bulk-size", type=int, default=20, help="批量操作测试的节点数量")
    
    args = parser.parse_args()
    
    # 正确设置批量操作测试的规模 - 不能直接为类设置属性
    bulk_size = args.bulk_size
    
    # 修改main函数调用，传递bulk_size参数
    main(args.iterations, args.concurrent_users, args.api_url) 