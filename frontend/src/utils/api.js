import { API_BASE_URL } from '../config';

const BASE_URL = `${API_BASE_URL}/api`;

const handleResponse = async (response) => {
    if (!response.ok) {
        let errorData = {};
        try {
            errorData = await response.json();
        } catch (e) {
            // If response is not JSON, use status text
            errorData = { message: response.statusText };
        }
        const errorMessage = errorData.message || `HTTP error! status: ${response.status}`;
        console.error('API Error:', errorMessage, errorData);
        alert(`操作失败: ${errorMessage}`); // 用户通知
        throw new Error(errorMessage);
    }
    return response.json();
};

const apiCall = async (endpoint, options = {}) => {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        return await handleResponse(response);
    } catch (error) {
        console.error('Network or unexpected error:', error);
        alert(`网络错误或请求失败: ${error.message}`); // 用户通知
        throw error;
    }
};

export const getNodes = () => apiCall('/nodes');
export const getEdges = () => apiCall('/edges');

export const addNodeApi = (nodeData) => apiCall('/nodes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(nodeData),
});

export const addEdgeApi = (connection) => apiCall('/edges', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(connection),
});

export const deleteNodeApi = (nodeId) => apiCall(`/nodes/${nodeId}`, {
    method: 'DELETE',
});

export const deleteRelatedEdgesApi = (nodeId) => apiCall(`/edges/related_to/${nodeId}`, {
    method: 'DELETE',
});

export const updateNodeTextApi = (nodeId, text) => apiCall(`/nodes/${nodeId}/text`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
});