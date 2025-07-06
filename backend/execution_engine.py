from typing import Dict, List, Any, Optional, Tuple, cast
from enum import Enum
import time
from backend.services import NodeService, EdgeService, GenerationService

class NodeStatus(Enum):
    """节点执行状态"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 正在执行
    COMPLETED = "completed"  # 执行完成
    FAILED = "failed"        # 执行失败
    SKIPPED = "skipped"      # 跳过执行

class NodeExecutor:
    """节点执行器 - 负责执行单个节点"""
    
    def __init__(self):
        self.node_service = NodeService()
        self.generation_service = GenerationService()
        # 注册不同类型节点的执行函数
        self._executors = {
            "text": self._execute_text_node,
            "generate": self._execute_generate_node,
            "start": self._execute_start_node,
            "end": self._execute_end_node,
            "default": self._execute_default_node,
        }
    
    def execute_node(self, node_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行单个节点"""
        if input_data is None:
            input_data = {}
            
        result = {
            "node_id": node_id,
            "status": NodeStatus.PENDING.value,
            "start_time": time.time(),
            "end_time": None,
            "output": {},  # 初始化为空字典而不是None
            "error": None
        }
        
        try:
            # 更新状态为运行中
            result["status"] = NodeStatus.RUNNING.value
            self.node_service.update_node_status(node_id, NodeStatus.RUNNING.value)
            
            # 获取节点数据
            node = self.node_service.get_node(node_id)
            if not node:
                raise ValueError(f"节点 {node_id} 不存在")
            
            # 执行对应的节点类型
            node_type = node["type"]
            executor = self._executors.get(node_type, self._execute_default_node)
            output = executor(node, input_data)
            
            # 更新结果
            result["output"] = output
            result["status"] = NodeStatus.COMPLETED.value
            self.node_service.update_node_status(node_id, NodeStatus.COMPLETED.value)
            
        except Exception as e:
            # 处理执行错误
            result["status"] = NodeStatus.FAILED.value
            result["error"] = str(e)
            self.node_service.update_node_status(node_id, NodeStatus.FAILED.value)
            
        finally:
            # 记录结束时间
            result["end_time"] = time.time()
            
        return result
    
    def _execute_text_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行文本节点"""
        text = ""
        if "data" in node and "text" in node["data"]:
            text = node["data"]["text"]
        return {
            "text": text,
            "type": "text"
        }
    
    def _execute_generate_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行生成节点"""
        # 从输入数据中获取文本
        input_text = input_data.get("text", "")
        if not input_text:
            raise ValueError("生成节点需要输入文本")
        
        # 调用生成服务
        generated_text = self.generation_service.generate_text(input_text)
        
        return {
            "generated_text": generated_text,
            "input_text": input_text,
            "type": "generated"
        }
    
    def _execute_start_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行开始节点"""
        return {
            "type": "start",
            "message": "工作流开始"
        }
    
    def _execute_end_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行结束节点"""
        return {
            "type": "end",
            "final_result": input_data,
            "message": "工作流结束"
        }
    
    def _execute_default_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行默认节点"""
        return {
            "type": "default",
            "data": node["data"],
            "input": input_data
        }

class DataFlowManager:
    """数据流管理器 - 处理节点间的数据传递"""
    
    def __init__(self):
        self.edge_service = EdgeService()
        self.node_service = NodeService()
    
    def get_node_inputs(self, node_id: str, executed_nodes: Dict[str, Any]) -> Dict[str, Any]:
        """获取节点的输入数据"""
        edges = self.edge_service.get_all_edges()
        
        # 找到所有指向当前节点的边
        input_edges = [edge for edge in edges if edge["target"] == node_id]
        
        inputs = {}
        for edge in input_edges:
            source_id = edge["source"]
            if source_id in executed_nodes and "output" in executed_nodes[source_id]:
                inputs[source_id] = executed_nodes[source_id]["output"]
        
        return self._merge_inputs(inputs)
    
    def get_next_nodes(self, node_id: str) -> List[str]:
        """获取下一个要执行的节点"""
        edges = self.edge_service.get_all_edges()
        output_edges = [edge for edge in edges if edge["source"] == node_id]
        return [edge["target"] for edge in output_edges]
    
    def _merge_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """合并多个输入数据"""
        if not inputs:
            return {}
        
        # 如果只有一个输入，直接返回
        if len(inputs) == 1:
            return list(inputs.values())[0]
        
        # 如果有多个输入，合并它们
        merged = {}
        for node_id, input_data in inputs.items():
            if isinstance(input_data, dict):
                merged.update(input_data)
            else:
                merged[f"input_{node_id}"] = input_data
        
        return merged

class WorkflowEngine:
    """工作流执行引擎"""
    
    def __init__(self):
        self.node_executor = NodeExecutor()
        self.data_flow_manager = DataFlowManager()
        self.node_service = NodeService()
        
        # 执行状态
        self.executed_nodes: Dict[str, Any] = {}  # 已执行节点的结果
        self.is_running = False
    
    def execute_workflow(self, start_node_id: Optional[str] = None) -> Dict[str, Any]:
        """执行工作流"""
        if self.is_running:
            return {"error": "工作流已在执行中", "success": False, "executed_nodes": {}}
        
        self.is_running = True
        self.executed_nodes = {}
        
        try:
            # 如果没有指定开始节点，找到类型为start的节点
            if start_node_id is None:
                nodes = self.node_service.get_all_nodes()
                start_nodes = [node["id"] for node in nodes if node["type"] == "start"]
                if not start_nodes:
                    raise ValueError("没有找到开始节点")
                start_node_id = start_nodes[0]
            
            # 从开始节点执行
            self._execute_node_and_successors(cast(str, start_node_id))
            
            # 返回执行结果
            return {
                "success": True,
                "executed_nodes": self.executed_nodes
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "executed_nodes": self.executed_nodes
            }
        
        finally:
            self.is_running = False
    
    def _execute_node_and_successors(self, node_id: str) -> None:
        """执行节点及其后续节点"""
        # 如果节点已执行，直接返回
        if node_id in self.executed_nodes:
            return
        
        # 获取节点输入
        inputs = self.data_flow_manager.get_node_inputs(node_id, self.executed_nodes)
        
        # 执行节点
        result = self.node_executor.execute_node(node_id, inputs)
        self.executed_nodes[node_id] = result
        
        # 如果执行失败，不继续执行后续节点
        if result["status"] == NodeStatus.FAILED.value:
            return
        
        # 获取后续节点并执行
        next_nodes = self.data_flow_manager.get_next_nodes(node_id)
        for next_node_id in next_nodes:
            self._execute_node_and_successors(next_node_id)
    
    def execute_single_node(self, node_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行单个节点"""
        if input_data is None:
            input_data = {}
            
        return self.node_executor.execute_node(node_id, input_data)
    
    def get_execution_status(self) -> Dict[str, Any]:
        """获取执行状态"""
        return {
            "is_running": self.is_running,
            "executed_nodes": {
                node_id: {
                    "status": result["status"],
                    "start_time": result["start_time"],
                    "end_time": result["end_time"],
                    "error": result["error"]
                }
                for node_id, result in self.executed_nodes.items()
            }
        } 