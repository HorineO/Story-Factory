
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

const socket = io('http://127.0.0.1:5000');

const useStore = create((set, get) => ({
  nodes: [],
  edges: [],
  activeTab: 'tab1', // 默认标签页
  selectedNode: null, // 新增 selectedNode 状态
  setActiveTab: (tabId) => set({ activeTab: tabId }),
  setSelectedNode: (node) => set({ selectedNode: node }),
  onNodeClick: (event, node) => set({ selectedNode: node }),
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
            x: node.position.x,
            y: node.position.y
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
}));

export default useStore;
