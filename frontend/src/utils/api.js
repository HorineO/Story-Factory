import axios from 'axios';
import { API_BASE_URL } from '../config';

// 创建 Axios 实例并设置基础配置
const apiClient = axios.create({
    baseURL: `${API_BASE_URL}/api`,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器：自动注入 Authorization 头部
apiClient.interceptors.request.use(
    (config) => {
        // 这里假设 Token 存储在 localStorage 中，可按需替换为 Cookie 或其他安全存储
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// 响应拦截器：统一处理错误码和异常弹窗
apiClient.interceptors.response.use(
    (response) => response.data, // 直接返回后端 data 字段，调用方拿到的就是业务数据
    (error) => {
        const response = error.response;
        const errorData = response?.data || {};
        const errorMessage = errorData.message || response?.statusText || error.message;
        console.error('API Error:', errorMessage, errorData);
        alert(`操作失败: ${errorMessage}`);
        return Promise.reject(error);
    }
);

/*
 * 封装常用请求方法，保持与旧 API 的调用方式一致
 * ------------------------------------------------------------------
 */
export const getNodes = () => apiClient.get('/nodes');
export const getEdges = () => apiClient.get('/edges');

export const addNodeApi = (nodeData) => apiClient.post('/nodes', nodeData);
export const addEdgeApi = (connection) => apiClient.post('/edges', connection);
export const deleteNodeApi = (nodeId) => apiClient.delete(`/nodes/${nodeId}`);
export const deleteRelatedEdgesApi = (nodeId) => apiClient.delete(`/edges/related_to/${nodeId}`);
export const updateNodeTextApi = (nodeId, text) => apiClient.put(`/nodes/${nodeId}/text`, { text });