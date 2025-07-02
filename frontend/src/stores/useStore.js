
import { create } from 'zustand';
import {
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';
import { io } from 'socket.io-client';

const socket = io('http://127.0.0.1:5000');

const useStore = create((set, get) => ({
  nodes: [],
  edges: [],
  activeTab: 'tab1', // 默认标签页
  setActiveTab: (tabId) => set({ activeTab: tabId }),
  fetchNodesAndEdges: async () => {
    try {
      const nodesResponse = await fetch('http://127.0.0.1:5000/api/nodes');
      const nodesData = await nodesResponse.json();
      set({ nodes: nodesData });

      const edgesResponse = await fetch('http://127.0.0.1:5000/api/edges');
      const edgesData = await edgesResponse.json();
      set({ edges: edgesData });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  },

  addNode: async (nodeData) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/nodes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(nodeData),
      });
      const newNode = await response.json();
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
      await fetch('http://127.0.0.1:5000/api/edges', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(connection),
      });
    } catch (error) {
      console.error('Error adding edge:', error);
    }
  },

  deleteNode: async (nodeId) => {
    try {
      await fetch(`http://127.0.0.1:5000/api/nodes/${nodeId}`, {
        method: 'DELETE',
      });
      await fetch(`http://127.0.0.1:5000/api/edges/related_to/${nodeId}`, {
        method: 'DELETE',
      });

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
      const response = await fetch(`http://127.0.0.1:5000/api/nodes/${nodeId}/text`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      if (!response.ok) {
        console.error('Failed to update node text on backend.');
        // Revert the state if the backend update fails
        set((state) => ({
          nodes: state.nodes.map((node) =>
            node.id === nodeId ? { ...node, data: { ...node.data, text: originalText } } : node
          ),
        }));
      }
    } catch (error) {
      console.error('Error updating node text:', error);
      // Revert the state if there's a network error
      set((state) => ({
        nodes: state.nodes.map((node) =>
          node.id === nodeId ? { ...node, data: { ...node.data, text: originalText } } : node
        ),
      }));
    }
  },
}));

export default useStore;
