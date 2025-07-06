/**
 * @file FileSystemHandler.js
 * @description 处理文件系统操作的组件
 */
import React from 'react';
import useStore from '../stores/useStore';
import useFileOperations from '../components/FileOperations';

const FileSystemHandler = ({ children }) => {
    const { nodes, edges, setNodesAndEdges } = useStore();

    // 使用文件操作自定义 hook
    const { handleSave, handleOpen } = useFileOperations({
        nodes,
        edges,
        setNodesAndEdges
    });

    // 构建传递给子组件的属性
    const fileProps = {
        handleSave,
        handleOpen
    };

    return children(fileProps);
};

export default FileSystemHandler; 