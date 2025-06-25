import React from 'react';
import './NewNodeTab.css';

const NewNodeTab = ({ onDragStart }) => {
    return (
        <div>
            <div className="dndnode" onDragStart={(event) => onDragStart(event, 'default')} draggable>
                默认节点
            </div>
            <div className="dndnode" onDragStart={(event) => onDragStart(event, 'input')} draggable>
                输入节点
            </div>
            <div className="dndnode" onDragStart={(event) => onDragStart(event, 'default')} draggable>
                生成节点 (Default)
            </div>
            <div className="dndnode" onDragStart={(event) => onDragStart(event, 'output')} draggable>
                输出节点
            </div>
            {/* 可以添加更多类型的节点 */}
        </div>
    );
};

export default NewNodeTab;