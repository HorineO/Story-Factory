# 节点组件系统

## 概述

这个目录包含了 Story Factory 应用中所有 React Flow 节点的组件。我们使用了一个模块化的样式系统，让所有节点都可以继承基础样式模板。

## 样式系统架构

### 基础样式模板 (`NodeStyles.css`)

所有节点都基于以下基础样式：

- **`.node-base`** - 基础节点容器样式
- **`.node-header`** - 节点头部样式
- **`.node-body`** - 节点主体样式
- **`.node-text`** - 节点文本样式

### 节点类型样式

每种节点类型都有自己的 CSS 变量定义：

```css
.text-node {
  --node-border-color: #17a2b8;
  --node-header-bg: #17a2b8;
  --node-type: "text";
}
```

### 工具类

提供了一些实用的工具类：

- **`.node-compact`** - 紧凑型节点
- **`.node-large`** - 大型节点
- **`.node-rounded`** - 圆角节点
- **`.node-flat`** - 扁平化节点

## 现有节点类型

| 节点类型   | 组件文件          | 颜色主题       | 描述         |
| ---------- | ----------------- | -------------- | ------------ |
| `default`  | `DefaultNode.js`  | 灰色 (#6c757d) | 默认节点类型 |
| `text`     | `TextNode.js`     | 蓝色 (#17a2b8) | 文本节点     |
| `chapter`  | `ChapterNode.js`  | 紫色 (#6f42c1) | 章节节点     |
| `generate` | `GenerateNode.js` | 黄色 (#ffc107) | 生成节点     |
| `start`    | `StartNode.js`    | 绿色 (#28a745) | 开始节点     |
| `end`      | `EndNode.js`      | 红色 (#dc3545) | 结束节点     |
| `input`    | `InputNode.js`    | 橙色 (#fd7e14) | 输入节点     |
| `output`   | `OutputNode.js`   | 青色 (#20c997) | 输出节点     |

## 创建新节点类型

### 方法 1: 使用 BaseNodeTemplate (推荐)

```javascript
import React from "react";
import BaseNodeTemplate from "./BaseNodeTemplate";

const MyCustomNode = ({ data }) => {
  const handles = [
    { type: "target", position: "left" },
    { type: "source", position: "right" },
  ];

  return (
    <BaseNodeTemplate
      data={data}
      nodeType="text-node" // 使用现有样式
      handles={handles}
      customHeader={<div>🚀 {data.label}</div>}
      additionalClasses="node-compact"
    />
  );
};

export default MyCustomNode;
```

### 方法 2: 手动创建

```javascript
import React from "react";
import { Handle, Position } from "reactflow";
import "./NodeStyles.css";

const MyCustomNode = ({ data }) => {
  return (
    <div className="node-base text-node node-compact">
      <Handle type="target" position={Position.Left} />
      <div className="node-header">{data.label}</div>
      <div className="node-body">
        <div className="node-text">{data.content}</div>
      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default MyCustomNode;
```

### 方法 3: 创建新的样式主题

在 `NodeStyles.css` 中添加新的样式：

```css
.my-custom-node {
  --node-border-color: #your-color;
  --node-header-bg: #your-color;
  --node-type: "my-custom";
}

.my-custom-node .node-header {
  background-color: var(--node-header-bg);
}
```

## 节点数据格式

所有节点都期望接收以下数据格式：

```javascript
{
    label: "节点标签",
    content: "节点内容", // 或 text
    // 其他自定义属性...
}
```

## 连接点配置

连接点可以通过以下方式配置：

```javascript
const handles = [
  { type: "target", position: "left", id: "input1" },
  { type: "source", position: "right", id: "output1" },
  { type: "source", position: "bottom", id: "output2" },
];
```

## 响应式设计

节点样式已经包含了响应式设计：

- 在小屏幕上自动调整字体大小和间距
- 支持触摸设备的交互优化

## 动画效果

节点包含以下动画效果：

- 出现动画 (`nodeAppear`)
- 悬停效果
- 选择状态高亮
- 连接点悬停缩放

## 最佳实践

1. **使用 BaseNodeTemplate** - 对于大多数新节点类型，推荐使用 BaseNodeTemplate
2. **保持一致性** - 使用现有的颜色主题和样式模式
3. **响应式设计** - 确保节点在不同屏幕尺寸下都能正常显示
4. **性能优化** - 避免在节点组件中使用复杂的计算或大量 DOM 操作
5. **可访问性** - 确保节点有适当的标签和键盘导航支持
