import React, { useEffect } from 'react';
// import './LeftPanel.css'; // Tailwind migration: old styles removed
import TabPanel from './TabPanel'; // 导入 TabPanel 组件
import NewNodeTab from './tabs/NewNodeTab';
import DirectoryTab from './tabs/DirectoryTab';
import NodePropertiesTab from './tabs/NodePropertiesTab'; // 导入 NodePropertiesTab 组件
import OtherTab from './tabs/OtherTab';
import useStore from '../stores/useStore';

const LeftPanel = () => {
    const onDragStart = (event, nodeType) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    const setActiveTab = useStore((state) => state.setActiveTab);

    // 定义标签页
    const tabs = [
        { id: 'tab2', label: '新建节点', content: <NewNodeTab onDragStart={onDragStart} /> },
        { id: 'tab4', label: '节点属性', content: <NodePropertiesTab /> }, // 添加节点属性标签页
        { id: 'tab3', label: '目录', content: <DirectoryTab /> },
        { id: 'tab5', label: '其他', content: <OtherTab /> },
    ];

    // 当组件挂载时，若当前 activeTab 与第一个 tab 不一致，则设置为默认（第一个）
    useEffect(() => {
        setActiveTab(tabs[0].id);
    }, []);

    return (
        <div
            className="w-64 bg-gray-700 border border-gray-600 flex flex-col h-full"
        >
            {/* 将 TabPanel 组件放置在 LeftPanel 中 */}
            <TabPanel tabs={tabs} />
        </div>
    );
};

export default LeftPanel;