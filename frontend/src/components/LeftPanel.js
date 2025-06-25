import React from 'react';
import TabPanel from './TabPanel'; // 导入 TabPanel 组件

const LeftPanel = () => {
    const onDragStart = (event, nodeType) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    // 定义标签页数据
    const tabs = [
        { id: 'tab1', label: '节点属性', content: <div>选择节点，就可以修改节点属性了</div> },
        {
            id: 'tab2', label: '新建节点', content: (
                <div>
                    <div className="dndnode" onDragStart={(event) => onDragStart(event, 'default')} draggable>
                        Default Node
                    </div>
                    {/* 可以添加更多类型的节点 */}
                </div>
            )
        },
        { id: 'tab3', label: '目录', content: <div>目录内容</div> },
        { id: 'tab4', label: '物品', content: <div>物品内容</div> },
        { id: 'tab5', label: '其他', content: <div>其他内容</div> },
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