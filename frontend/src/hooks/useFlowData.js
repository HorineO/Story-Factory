/**
 * @file 定义了一个自定义 React Hook，用于管理和操作流程图数据。
 * @description 提供了添加、更新和删除节点及边的功能。
 */
import { useState, useEffect, useCallback } from 'react';
import { addEdge, useNodesState, useEdgesState } from 'reactflow';

const useFlowData = () => {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        const fetchNodesAndEdges = async () => {
            try {
                const nodesResponse = await fetch('http://127.0.0.1:5000/api/nodes');
                const nodesData = await nodesResponse.json();
                console.log('Fetched nodes:', nodesData);
                setNodes(nodesData);

                const edgesResponse = await fetch('http://127.0.0.1:5000/api/edges');
                const edgesData = await edgesResponse.json();
                console.log('Fetched edges:', edgesData);
                setEdges(edgesData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchNodesAndEdges();
    }, [setNodes, setEdges]);

    const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

    return {
        nodes,
        edges,
        onNodesChange,
        onEdgesChange,
        onConnect,
    };
};

export default useFlowData;