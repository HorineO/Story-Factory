# 为了向后兼容，使用新创建的models和database
from backend.models import initial_nodes, initial_edges
from backend.database import get_all_nodes, get_all_edges

# 导出这些变量和函数以保持向后兼容
__all__ = ['initial_nodes', 'initial_edges', 'get_all_nodes', 'get_all_edges']
