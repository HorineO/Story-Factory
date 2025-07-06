/**
 * @file ContextMenuHandler.js
 * @description 处理节点右键菜单的显示和交互
 */
import React, { useCallback } from 'react';
import ContextMenu from '../ContextMenu';
import useStore from '../../stores/useStore';
import { useReactFlow } from 'reactflow';

const ContextMenuHandler = ({ deleteNode }) => {
    const reactFlowInstance = useReactFlow();
    const menu = useStore((state) => state.contextMenu);
    const setContextMenu = useStore((state) => state.setContextMenu);

    const handleDelete = useCallback(() => {
        if (menu?.id) {
            deleteNode(menu.id);
            setContextMenu(null);
        }
    }, [menu, deleteNode, setContextMenu]);

    const handleDuplicate = useCallback(() => {
        if (menu?.id) {
            // Get the latest nodes directly from the store
            const currentNodes = useStore.getState().nodes;
            const nodeToDuplicate = currentNodes.find(n => n.id === menu.id);
            if (nodeToDuplicate) {
                const newNode = {
                    ...nodeToDuplicate,
                    id: `node_${Date.now()}`,
                    position: {
                        x: nodeToDuplicate.position.x + 50,
                        y: nodeToDuplicate.position.y + 50,
                    }
                };
                reactFlowInstance.setNodes(nds => nds.concat(newNode));
                setContextMenu(null);
            }
        }
    }, [menu, reactFlowInstance, setContextMenu]);

    if (!menu) {
        return null;
    }

    return (
        <ContextMenu
            {...menu}
            onDelete={handleDelete}
            onDuplicate={handleDuplicate}
            onClose={() => setContextMenu(null)}
        />
    );
};

export default ContextMenuHandler; 