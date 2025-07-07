import React, { useEffect } from 'react';
import { Menu, Item, useContextMenu } from 'react-contexify';
import 'react-contexify/dist/ReactContexify.css';

// Context menu ID shared between trigger and menu component
const MENU_ID = 'node-context-menu';

/**
 * Node context menu implemented with react-contexify.
 * It is **displayed imperatively** when the parent handler calls `setContextMenu({ id, event })`.
 *
 * Props:
 *   event        – the native context-menu mouse event (required for positioning)
 *   id           – id of the node on which the menu was opened
 *   onDuplicate  – callback to duplicate node
 *   onDelete     – callback to delete node
 */
const ContextMenu = ({ event, id, onDuplicate, onDelete }) => {
    // Obtain the imperative show function from the hook
    const { show } = useContextMenu({ id: MENU_ID });

    // Show the menu once the component is mounted / props change
    useEffect(() => {
        if (event) {
            show({ event, props: { nodeId: id } });
        }
        // The dependency array purposefully excludes `show` (stable) to avoid unnecessary re-invocation.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [event, id]);

    // The Menu is rendered (invisibly) once – `show` controls its visibility.
    return (
        <Menu id={MENU_ID} theme="dark" animation={{ enter: 'fade', exit: 'fade' }}
            className="bg-gray-700 border border-gray-600 rounded shadow-lg text-sm text-gray-200">
            <Item onClick={onDuplicate} className="px-3 py-1 hover:bg-gray-600 focus:outline-none focus-visible:ring focus-visible:ring-white/50">复制节点</Item>
            <Item onClick={onDelete} className="px-3 py-1 hover:bg-gray-600 focus:outline-none focus-visible:ring focus-visible:ring-white/50">删除</Item>
        </Menu>
    );
};

export default ContextMenu;