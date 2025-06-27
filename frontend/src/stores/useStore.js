
import { create } from 'zustand';
import {
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';
 
const useStore = create((set, get) => ({
  nodes: [],
  edges: [],
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

  onNodesChange: (changes) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
  },

  onEdgesChange: (changes) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },

  onConnect: (connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
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
  },

  setNodesAndEdges: (nodes, edges) => {
    set({ nodes, edges });
  },
}));
 
export default useStore;
