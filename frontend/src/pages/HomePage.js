/**
 * @file 定义了应用的主页组件。
 * @description 该组件集成了流程图画布和相关工具，用于展示和编辑流程图。
 */
// frontend/src/pages/HomePage.js
// 此文件作为Homepage应用程序的主入口点，负责导入和组合各个模块。
import React from 'react';
import { ReactFlowProvider } from 'reactflow';
import NavigationBar from '../components/NavigationBar';
import FlowCanvas from '../components/FlowCanvas';
import NodeStateManager from './NodeStateManager';
import FileSystemHandler from './FileSystemHandler';

const HomePage = () => {
    return (
        <ReactFlowProvider>
            <NodeStateManager>
                {(nodeProps) => (
                    <FileSystemHandler>
                        {(fileProps) => (
                            <>
                                <NavigationBar
                                    onSave={fileProps.handleSave}
                                    onOpen={fileProps.handleOpen}
                                />
                                <FlowCanvas {...nodeProps} />
                            </>
                        )}
                    </FileSystemHandler>
                )}
            </NodeStateManager>
        </ReactFlowProvider>
    );
};

export default HomePage;
