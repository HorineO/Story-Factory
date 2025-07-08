/**
 * @file 定义了应用的主页组件。
 * @description 该组件集成了流程图画布和相关工具，用于展示和编辑流程图。
 */
// frontend/src/pages/HomePage.js
// 此文件作为Homepage应用程序的主入口点，负责导入和组合各个模块。
import React, { Suspense } from 'react';
import { ReactFlowProvider } from 'reactflow';
import NodeStateManager from './NodeStateManager';
import FileSystemHandler from './FileSystemHandler';

const NavigationBar = React.lazy(() => import('../components/NavigationBar'));
const FlowCanvas = React.lazy(() => import('../components/FlowCanvas'));

const HomePage = () => {
    return (
        <ReactFlowProvider>
            <NodeStateManager>
                {(nodeProps) => (
                    <FileSystemHandler>
                        {(fileProps) => (
                            <>
                                <div className="flex flex-col h-full">
                                    <Suspense fallback={<div className="text-white p-4">Loading UI...</div>}>
                                        <NavigationBar
                                            onSave={fileProps.handleSave}
                                            onOpen={fileProps.handleOpen}
                                        />
                                    </Suspense>
                                    <Suspense fallback={<div className="flex-1 flex items-center justify-center text-white">Loading Canvas...</div>}>
                                        <FlowCanvas {...nodeProps} />
                                    </Suspense>
                                </div>
                            </>
                        )}
                    </FileSystemHandler>
                )}
            </NodeStateManager>
        </ReactFlowProvider>
    );
};

export default HomePage;
