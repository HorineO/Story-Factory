/**
 * @file ReactFlowWrapper.js
 * @description 封装ReactFlow组件，处理流程图的核心渲染和交互逻辑
 */
import React, { useCallback, useRef } from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    useReactFlow,
} from 'reactflow';
import nodeTypes from '../nodes/NodeTypes';
import useStore from '../../stores/useStore';
import FlowControls from './FlowControls';
import 'reactflow/dist/style.css';

// 定义各节点类型的输入/输出字段映射
// key 为节点 type，value 为 { input, output }
// 若无对应映射，则默认为空对象
const IO_MAPPINGS = {
    text: { output: 'text' },
    generate: { input: 'text', output: 'generate' },
    chapter: { input: 'text', output: 'text' }
};

const ReactFlowWrapper = ({
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    onNodeClick,
    onPaneClick
}) => {
    const reactFlowInstance = useReactFlow();
    const flowRef = useRef(null);
    const addNode = useStore((state) => state.addNode);

    const handleNodeContextMenu = useCallback((event, node) => {
        // Prevent default browser menu
        event.preventDefault();

        // Persist the event so we can use it asynchronously (react pools synthetic events)
        event.persist();

        // Store the native event and node id for the ContextMenuHandler
        useStore.getState().setContextMenu({
            id: node.id,
            event: event.nativeEvent || event,
        });
    }, []);

    const handlePaneClickInternal = useCallback(() => {
        useStore.getState().setContextMenu(null);
        onPaneClick();
    }, [onPaneClick]);

    const handleNodeClickInternal = useCallback((event, node) => {
        onNodeClick(event, node);
    }, [onNodeClick]);

    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback(async (event) => {
        event.preventDefault();

        const type = event.dataTransfer.getData('application/reactflow');
        if (typeof type === 'undefined' || !type) {
            return;
        }

        const position = reactFlowInstance.screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
        });

        // Round position coordinates to 3 decimal places for reasonable precision
        position.x = Math.round(position.x * 1000) / 1000;
        position.y = Math.round(position.y * 1000) / 1000;

        const newNodeData = {
            type,
            position,
            data: { label: `${type} Node` },
            // 为新节点添加 source 映射，用于后续数据流转
            source: IO_MAPPINGS[type] || {},
        };

        const newNode = await addNode(newNodeData);
        if (newNode) {
            reactFlowInstance.setNodes((nds) => nds.concat(newNode));
        }
    }, [reactFlowInstance, addNode]);

    return (
        <ReactFlow
            ref={flowRef}
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeContextMenu={handleNodeContextMenu}
            onPaneClick={handlePaneClickInternal}
            onNodeClick={handleNodeClickInternal}
            onDragOver={onDragOver}
            onDrop={onDrop}
            nodeTypes={nodeTypes}
            fitView
            className="w-full h-full bg-gray-900"
            proOptions={{ hideAttribution: true }}
        >
            <FlowControls />
        </ReactFlow>
    );
};

export default ReactFlowWrapper; 