import { create } from 'zustand';
import {
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';
import { io } from 'socket.io-client';
import {
  getNodes,
  getEdges,
  addNodeApi,
  addEdgeApi,
  deleteNodeApi,
  deleteRelatedEdgesApi,
  updateNodeTextApi,
} from '../utils/api';

import { API_BASE_URL } from '../config';

const socket = io(API_BASE_URL);

// IO 映射：定义每种节点类型的输入/输出字段
const IO_MAPPINGS = {
  text: { output: 'text' },
  generate: { input: 'text', output: 'generate' },
  chapter: { input: 'text', output: 'text' },
};

const useStore = create((set, get) => ({
  nodes: [],
  edges: [],
  activeTab: 'tab2', // 默认标签页（新建节点）
  selectedNode: null, // 新增 selectedNode 状态
  contextMenu: null, // 右键菜单状态
  setActiveTab: (tabId) => set({ activeTab: tabId }),
  setSelectedNode: (node) => set({ selectedNode: node }),
  setContextMenu: (menuData) => set({ contextMenu: menuData }),
  onNodeClick: (event, node) => set({ selectedNode: node, activeTab: 'tab4' }),
  onPaneClick: () => set({ selectedNode: null }),
  fetchNodesAndEdges: async () => {
    try {
      const nodesData = await getNodes();
      set({ nodes: nodesData });

      const edgesData = await getEdges();
      set({ edges: edgesData });
    } catch (error) {
      // 错误已在api.js中处理，此处仅为捕获可能发生的意外错误
      console.error('Error fetching nodes and edges:', error);
    }
  },

  addNode: async (nodeData) => {
    try {
      const newNode = await addNodeApi(nodeData);
      set((state) => ({
        nodes: state.nodes.concat(newNode),
      }));
      return newNode;
    } catch (error) {
      console.error('Error adding node:', error);
      return null;
    }
  },

  onNodesChange: (changes) => {
    const nodes = applyNodeChanges(changes, get().nodes);
    set({ nodes });

    // 发送节点位置更新到后端
    changes.forEach(change => {
      if (change.type === 'position' && change.dragging) {
        const node = nodes.find(n => n.id === change.id);
        if (node) {
          socket.emit('node_move', {
            nodeId: node.id,
            x: Math.round(node.position.x * 1000) / 1000,
            y: Math.round(node.position.y * 1000) / 1000
          });
        }
      }
    });
  },

  onEdgesChange: (changes) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },

  onConnect: async (connection) => {
    try {
      await addEdgeApi(connection);

      // 在本地状态中根据连接关系传递数据
      const { source: sourceId, target: targetId } = connection;
      const nodes = get().nodes;

      const sourceNode = nodes.find((n) => n.id === sourceId);
      const targetNode = nodes.find((n) => n.id === targetId);

      if (!sourceNode || !targetNode) return;

      // 解析输入/输出字段
      const sourceMapping = sourceNode.source || IO_MAPPINGS[sourceNode.type] || {};
      const targetMapping = targetNode.source || IO_MAPPINGS[targetNode.type] || {};

      const outputKey = sourceMapping.output;
      const inputKey = targetMapping.input;

      if (!outputKey || !inputKey) return;

      const valueToTransfer = sourceNode.data?.[outputKey];

      if (typeof valueToTransfer === 'undefined') return;

      // 更新目标节点数据
      const updatedNodes = nodes.map((node) => {
        if (node.id === targetId) {
          return {
            ...node,
            data: {
              ...node.data,
              [inputKey]: valueToTransfer,
            },
          };
        }
        return node;
      });

      // 更新节点集合，同时如果当前选中的节点被修改，也同步更新 selectedNode
      const { selectedNode } = get();
      const newSelectedNode = selectedNode && selectedNode.id === targetId
        ? updatedNodes.find(n => n.id === targetId)
        : selectedNode;

      set({ nodes: updatedNodes, selectedNode: newSelectedNode });

      // 将数据同步到后端，确保刷新后目标节点仍保留该字段
      try {
        if (inputKey === 'text') {
          // 专门的文本字段更新接口
          await updateNodeTextApi(targetId, valueToTransfer);
        } else {
          // TODO: 如果未来需要支持其他字段，可在此添加通用更新逻辑
        }
      } catch (syncError) {
        console.error('Failed to persist node data to backend:', syncError);
      }
    } catch (error) {
      console.error('Error adding edge:', error);
    }
  },

  deleteNode: async (nodeId) => {
    try {
      await deleteNodeApi(nodeId);
      await deleteRelatedEdgesApi(nodeId);

      set((state) => ({
        nodes: state.nodes.filter((node) => node.id !== nodeId),
        edges: state.edges.filter((edge) => edge.source !== nodeId && edge.target !== nodeId),
      }));
    } catch (error) {
      console.error('Error deleting node:', error);
    }
  },

  updateNodeStatus: (nodeId, status) => {
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === nodeId ? { ...node, data: { ...node.data, status } } : node
      ),
    }));
    // 通过WebSocket发送状态更新
    socket.emit('node_status_update', { nodeId, status });
  },

  // 初始化WebSocket监听
  initSocketListeners: () => {
    socket.on('node_status_push', (data) => {
      set((state) => ({
        nodes: state.nodes.map((node) =>
          node.id === data.nodeId ? { ...node, data: { ...node.data, status: data.status } } : node
        ),
      }));
    });

    socket.on('nodes_update', (data) => {
      set({ nodes: data.nodes });
    });

    socket.on('node_updated', (data) => {
      set(state => ({
        nodes: state.nodes.map(node =>
          node.id === data.nodeId
            ? { ...node, position: { x: data.x, y: data.y } }
            : node
        )
      }));
    });

    socket.on('edges_update', (data) => {
      set({ edges: data.edges });
    });

    socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });
  },

  setNodesAndEdges: (nodes, edges) => {
    set({ nodes, edges });
  },

  updateNodeText: async (nodeId, text) => {
    const originalNodes = get().nodes; // Store current nodes for potential rollback
    const originalText = originalNodes.find(node => node.id === nodeId)?.data?.text;

    // Optimistically update the node text in the store
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === nodeId ? { ...node, data: { ...node.data, text: text } } : node
      ),
    }));

    try {
      await updateNodeTextApi(nodeId, text);
    } catch (error) {
      console.error('Error updating node text:', error);
      // Revert the state if the backend update fails or there's a network error
      set((state) => ({
        nodes: state.nodes.map((node) =>
          node.id === nodeId ? { ...node, data: { ...node.data, text: originalText } } : node
        ),
      }));
    }
  },

  // 添加新的方法以在前端存储生成结果
  updateNodeGenerate: (nodeId, generatedText) => {
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === nodeId ? { ...node, data: { ...node.data, generate: generatedText } } : node
      ),
      // 同步更新 selectedNode（如果当前选中）
      selectedNode: state.selectedNode && state.selectedNode.id === nodeId
        ? { ...state.selectedNode, data: { ...state.selectedNode.data, generate: generatedText } }
        : state.selectedNode,
    }));
    // TODO: 如果后端未来支持存储 generate 字段，可在此处添加 API 调用
  },
}));

export default useStore;
