import React, { useState } from 'react';
import './NewNodeTab.css';

const NewNodeTab = ({ onDragStart }) => {
    const [isReactNodesCollapsed, setIsReactNodesCollapsed] = useState(false);
    const [isBasicNodesCollapsed, setIsBasicNodesCollapsed] = useState(false);

    return (
        <div>
            <div
                className="collapsible-header"
                onClick={() => setIsReactNodesCollapsed(!isReactNodesCollapsed)}
            >
                React自带节点 {isReactNodesCollapsed ? '▼' : '▲'}
            </div>
            {!isReactNodesCollapsed && (
                <div className="collapsible-content">
                    <div className="dndnode" onDragStart={(event) => onDragStart(event, 'default')} draggable>
                        默认节点
                    </div>
                    <div className="dndnode" onDragStart={(event) => onDragStart(event, 'input')} draggable>
                        输入节点
                    </div>
                    <div className="dndnode" onDragStart={(event) => onDragStart(event, 'output')} draggable>
                        输出节点
                    </div>
                    {/* 可以添加更多类型的节点 */}
                </div>
            )}
            <div
                className="collapsible-header"
                onClick={() => setIsBasicNodesCollapsed(!isBasicNodesCollapsed)}
            >
                基础节点 {isBasicNodesCollapsed ? '▼' : '▲'}
            </div>
            {!isBasicNodesCollapsed && (
                <div className="collapsible-content">
                    <div className="dndnode" draggable>
                        生成节点
                    </div>
                    <div className="dndnode" draggable>
                        文本节点
                    </div>
                    <div className="dndnode" draggable>
                        章节节点
                    </div>
                    {/* 可以添加更多类型的节点 */}
                </div>
            )}
        </div>
    );
};

export default NewNodeTab;