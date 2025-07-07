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

        const newNodeData = {
            type,
            position,
            data: { label: `${type} Node` },
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
            className="bg-gray-900"
            proOptions={{ hideAttribution: true }}
        >
            <FlowControls />
        </ReactFlow>
    );
};

export default ReactFlowWrapper; 