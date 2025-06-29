import React, { useState } from 'react';
import './NewNodeTab.css';

const NewNodeTab = ({ onDragStart }) => {
    const [isReactNodesCollapsed, setIsReactNodesCollapsed] = useState(true);
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
                    <div className="dndnode" data-type="default" onDragStart={(event) => onDragStart(event, 'default')} draggable>
                        默认节点
                    </div>
                    <div className="dndnode" data-type="input" onDragStart={(event) => onDragStart(event, 'input')} draggable>
                        输入节点
                    </div>
                    <div className="dndnode" data-type="output" onDragStart={(event) => onDragStart(event, 'output')} draggable>
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
                    <div className="dndnode" data-type="generate" onDragStart={(event) => onDragStart(event, 'generate')} draggable>
                        生成节点
                    </div>
                    <div className="dndnode" data-type="text" onDragStart={(event) => onDragStart(event, 'text')} draggable>
                        文本节点
                    </div>
                    <div className="dndnode" data-type="chapter" onDragStart={(event) => onDragStart(event, 'chapter')} draggable>
                        章节节点
                    </div>
                    <div className="dndnode" data-type="start" onDragStart={(event) => onDragStart(event, 'start')} draggable>
                        开始节点
                    </div>
                    <div className="dndnode" data-type="end" onDragStart={(event) => onDragStart(event, 'end')} draggable>
                        结束节点
                    </div>
                    {/* 可以添加更多类型的节点 */}
                </div>
            )}
        </div>
    );
};

export default NewNodeTab;