import React from 'react';
import TabPanel from './TabPanel'; // 导入 TabPanel 组件
import NewNodeTab from './tabs/NewNodeTab';
import DirectoryTab from './tabs/DirectoryTab';
import NodePropertiesTab from './tabs/NodePropertiesTab'; // 导入 NodePropertiesTab 组件
import OtherTab from './tabs/OtherTab';

const LeftPanel = () => {
    const onDragStart = (event, nodeType) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    // 定义标签页
    const tabs = [
        { id: 'tab2', label: '新建节点', content: <NewNodeTab onDragStart={onDragStart} /> },
        { id: 'tab4', label: '节点属性', content: <NodePropertiesTab /> }, // 添加节点属性标签页
        { id: 'tab3', label: '目录', content: <DirectoryTab /> },
        { id: 'tab5', label: '其他', content: <OtherTab /> },
    ];

    return (
        <div
            className="left-panel"
            style={{
                width: '250px',
                backgroundColor: 'rgb(75, 75, 75)',
                borderRight: '1px solid #ddd',
                border: '1px solid rgb(46, 46, 46)',
                display: 'flex', // 使用 flexbox 布局
                flexDirection: 'column', // 垂直方向排列
                height: '100%' // 填充父容器高度
            }}
        >
            {/* 将 TabPanel 组件放置在 LeftPanel 中 */}
            <TabPanel tabs={tabs} />
        </div>
    );
};

export default LeftPanel;