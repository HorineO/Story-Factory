# 节点系统规范文档

## 概述

本项目的节点系统已经进行了重构，实现了智能布局和多层结构支持。所有节点现在都基于 `BaseNodeTemplate` 实现，并统一使用 `NodeFactory` 进行配置管理，确保了一致性和可维护性。

## 架构设计

### 1. BaseNodeTemplate (基础模板) - 智能布局版

- **位置**: `BaseNodeTemplate.js`
- **作用**: 提供统一的节点渲染逻辑，支持智能布局
- **特性**:
  - 智能布局选择（单侧/双侧）
  - 多层结构支持
  - 连接点与内容层平行对齐
  - 数据验证和默认值处理
  - 统一的 Handle 渲染
  - 支持自定义头部和左右内容
  - 错误处理和类型验证
  - **自动从工厂获取连接点配置**

### 2. NodeFactory (节点工厂) - 统一配置中心

- **位置**: `NodeFactory.js`
- **作用**: 统一创建和验证节点实例，集中管理所有节点配置
- **特性**:
  - 集中管理节点配置（连接点、图标、默认标签等）
  - 数据验证
  - 默认值处理
  - 类型安全
  - **单一配置源，避免重复配置**

### 3. 具体节点实现

所有节点都使用 `BaseNodeTemplate` 实现，连接点配置统一在 `NodeFactory` 中管理：

- `StartNode.js` - 开始节点（单侧布局）
- `EndNode.js` - 结束节点（单侧布局）
- `TextNode.js` - 文本节点（单侧布局，只有输出）
- `ChapterNode.js` - 章节节点（双侧布局）
- `GenerateNode.js` - 生成节点（双侧布局）

## 统一配置系统

### 配置管理原则

1. **单一配置源**: 所有节点的连接点配置都在 `NodeFactory.nodeConfigs` 中定义
2. **避免重复**: 节点组件不再重复定义连接点配置
3. **统一管理**: 修改节点配置只需要在工厂中修改一处

### 配置示例

```javascript
// NodeFactory.js 中的统一配置
static nodeConfigs = {
    'text': {
        nodeType: 'text-node',
        handles: [
            { type: 'source', position: 'right', id: 'output' }
        ],
        icon: '📝',
        defaultLabel: '文本',
        defaultContent: '文本内容'
    },
    // ... 其他节点配置
};
```

## 智能布局系统

### 布局规则

#### 双侧布局（有输入有输出）

```
┌─────────────────────────────────────┐
│             节点头部                 │
├─────────────┬───────────────────────┤
│   左侧内容   │      右侧内容         │
│   区域      │       区域            │
│             │                       │
│  ┌─────────┐│ ┌─────────────────┐   │
│  │ 输入层1  ││ │    输出层1      │   │
│  └─────────┘│ └─────────────────┘   │
│             │                       │
│  ┌─────────┐│ ┌─────────────────┐   │
│  │ 输入层2  ││ │    输出层2      │   │
│  └─────────┘│ └─────────────────┘   │
└─────────────┴───────────────────────┘
    ●           ●           ●
  输入1        输入2        输出1
```

#### 单侧布局（只有输入或只有输出）

```
┌─────────────────────────────────────┐
│             节点头部                 │
├─────────────────────────────────────┤
│           单侧内容区域               │
│                                     │
│         ┌─────────────────┐         │
│         │    内容层       │         │
│         └─────────────────┘         │
│                                     │
└─────────────────────────────────────┘
                ●
              连接点
```

### 智能判断逻辑

- **双侧布局**: 当节点既有输入连接点又有输出连接点时使用
- **单侧布局**: 当节点只有输入连接点或只有输出连接点时使用
- **自动选择**: 组件会根据连接点配置自动选择合适的布局

## 节点类型配置

### 支持的节点类型

| 类型     | 图标 | 布局类型 | 输入层 | 输出层 | 默认标签 | 默认内容          |
| -------- | ---- | -------- | ------ | ------ | -------- | ----------------- |
| start    | ▶️   | 单侧     | 0      | 1      | 开始节点 | 开始输出          |
| end      | ⏹️   | 单侧     | 1      | 0      | 结束节点 | 结束输入          |
| text     | 📝   | 单侧     | 0      | 1      | 文本节点 | 文本输出          |
| chapter  | 📖   | 双侧     | 1      | 1      | 章节节点 | 章节输入/章节输出 |
| generate | 🤖   | 双侧     | 1      | 1      | 生成节点 | 生成输入/生成输出 |

## 尺寸规范

### 节点尺寸标准

- **最小宽度**: 160px
- **最大宽度**: 280px
- **最小高度**: 40px（双侧）/ 35px（单侧）
- **响应式调整**: 移动端最小宽度 140px，最大宽度 240px

### 内容层尺寸

- **标准层高度**: 18px
- **单层显示高度**: 20px
- **内边距**: 4px-8px（根据布局类型调整）

## 使用方法

### 1. 基础节点使用

```javascript
import { NodeFactory } from "./NodeTypes";

// 创建双侧节点
const bilateralNodeData = {
  label: "处理节点",
  leftLayers: [{ label: "输入层", content: "输入内容" }],
  rightLayers: [{ label: "输出层", content: "输出内容" }],
};

// 创建单侧节点
const unilateralNodeData = {
  label: "开始节点",
  rightLayers: [{ label: "输出层", content: "开始输出" }],
};
```

### 2. 多层节点使用

```javascript
// 创建多层节点
const multiLayerData = {
  label: "多层节点",
  leftLayers: [
    { label: "输入层1", content: "输入内容1" },
    { label: "输入层2", content: "输入内容2" },
    { label: "输入层3", content: "输入内容3" },
  ],
  rightLayers: [
    { label: "输出层1", content: "输出内容1" },
    { label: "输出层2", content: "输出内容2" },
  ],
};
```

### 3. 创建自定义节点

```javascript
import React from "react";
import BaseNodeTemplate from "./BaseNodeTemplate";

const CustomNode = ({ data }) => {
  // 定义连接点 - 组件会根据连接点自动选择布局
  const handles = [
    // 双侧节点示例
    {
      type: "target",
      position: "left",
      id: "input-1",
      label: "输入1",
      layerIndex: 0,
    },
    {
      type: "source",
      position: "right",
      id: "output-1",
      label: "输出1",
      layerIndex: 0,
    },
  ];

  const customHeader = (
    <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
      <span>🎯</span>
      <span>{data.label}</span>
    </div>
  );

  return (
    <BaseNodeTemplate
      data={data}
      nodeType="text-node"
      handles={handles}
      customHeader={customHeader}
    />
  );
};
```

## 数据规范

### 标准数据字段

```javascript
const nodeData = {
  label: "节点标题", // 显示在头部
  leftLayers: [
    // 左侧内容层数组（可选）
    {
      label: "层标签",
      content: "层内容",
    },
  ],
  rightLayers: [
    // 右侧内容层数组（可选）
    {
      label: "层标签",
      content: "层内容",
    },
  ],
  // ... 其他自定义字段
};
```

### 连接点配置

```javascript
const handles = [
  {
    type: "target", // 'target' 或 'source'
    position: "left", // 'left' 或 'right'
    id: "unique-id", // 唯一标识符
    label: "连接点标签", // 可选，显示标签
    layerIndex: 0, // 对应内容层的索引
  },
];
```

### 布局选择规则

```javascript
// 双侧布局 - 既有输入又有输出
const bilateralHandles = [
  { type: "target", position: "left", id: "input" },
  { type: "source", position: "right", id: "output" },
];

// 单侧布局 - 只有输入
const inputOnlyHandles = [{ type: "target", position: "left", id: "input" }];

// 单侧布局 - 只有输出
const outputOnlyHandles = [{ type: "source", position: "right", id: "output" }];
```

## 样式系统

### CSS 类名规范

- `.node-base` - 基础节点样式
- `.node-header` - 节点头部样式
- `.node-body` - 节点主体样式
- `.node-left-content` - 左侧内容区域（双侧布局）
- `.node-right-content` - 右侧内容区域（双侧布局）
- `.node-single-content` - 单侧内容区域（单侧布局）
- `.node-content-layer` - 内容层样式
- `.node-single-layer` - 单层内容样式（简化显示）
- `.node-handles-container` - 连接点容器
- `.node-left-handles` - 左侧连接点容器
- `.node-right-handles` - 右侧连接点容器
- `.text-node` - 文本节点样式
- `.chapter-node` - 章节节点样式
- `.generate-node` - 生成节点样式
- `.start-node` - 开始节点样式
- `.end-node` - 结束节点样式

### 自定义样式

```css
/* 添加新的节点类型样式 */
.custom-node {
  --node-border-color: #ff6b6b;
  --node-header-bg: #ff6b6b;
}

.custom-node .node-header {
  background-color: var(--node-header-bg);
}

/* 自定义内容层样式 */
.custom-node .node-content-layer {
  background-color: rgba(255, 107, 107, 0.1);
  border-color: rgba(255, 107, 107, 0.3);
}

/* 自定义单层内容样式 */
.custom-node .node-single-layer {
  background-color: rgba(255, 107, 107, 0.15);
  border-color: rgba(255, 107, 107, 0.4);
}
```

## 最佳实践

### 1. 布局设计

- 根据节点的实际功能选择合适的连接点配置
- 只有输入或输出的节点使用单侧布局，避免空白区域
- 多层内容时使用清晰的标签和描述

### 2. 数据一致性

- 使用 `leftLayers` 和 `rightLayers` 数组定义内容层
- 通过 `layerIndex` 确保连接点与内容层正确对齐
- 提供有意义的默认值

### 3. 连接点设计

- 为每个连接点提供唯一的 `id`
- 使用 `label` 属性提高可读性
- 确保 `layerIndex` 与对应的内容层索引匹配

### 4. 多层结构

- 合理设计内容层数量，避免过于复杂
- 使用清晰的层标签和内容描述
- 考虑响应式设计，确保在小屏幕上也能正常显示

### 5. 性能优化

- 避免在节点组件中进行复杂计算
- 使用 `React.memo` 优化渲染性能
- 合理使用 `useCallback` 和 `useMemo`

### 6. 扩展性

- 通过 `NodeFactory.nodeConfigs` 添加新节点类型
- 使用 `BaseNodeTemplate` 创建自定义节点
- 保持向后兼容性

## 迁移指南

### 从旧版本迁移

1. **更新数据结构**:

   ```javascript
   // 旧版本
   const oldData = {
     label: "节点",
     content: "内容",
   };

   // 新版本 - 双侧节点
   const bilateralData = {
     label: "节点",
     leftLayers: [{ label: "输入", content: "内容" }],
     rightLayers: [{ label: "输出", content: "内容" }],
   };

   // 新版本 - 单侧节点
   const unilateralData = {
     label: "节点",
     rightLayers: [{ label: "输出", content: "内容" }],
   };
   ```

2. **更新连接点配置**:

   ```javascript
   // 旧版本
   const oldHandles = [{ type: "target", position: "left", id: "input" }];

   // 新版本
   const newHandles = [
     {
       type: "target",
       position: "left",
       id: "input",
       label: "输入",
       layerIndex: 0,
     },
   ];
   ```

3. **布局自动选择**:

   ```javascript
   // 组件会自动根据连接点选择布局
   // 无需手动指定布局类型
   <BaseNodeTemplate data={data} handles={handles} />
   ```

## 测试

使用 `NodeStyleTest.js` 组件可以测试所有节点类型的样式和功能：

```javascript
import NodeStyleTest from "./NodeStyleTest";

// 在开发环境中使用
<NodeStyleTest />;
```

## 总结

重构后的节点系统提供了：

1. **智能布局选择** - 根据节点类型自动选择最合适的布局
2. **规范化的尺寸** - 统一的节点大小和视觉一致性
3. **优化的单侧布局** - 只有输入或输出的节点更加简洁
4. **灵活的多层结构** - 支持复杂的节点逻辑和数据流
5. **精确的连接点对齐** - 每个连接点与对应内容层平行
6. **增强的视觉效果** - 更好的阴影、边框和交互效果
7. **完善的文档和示例** - 便于开发者理解和使用

重构后的节点系统不仅满足了当前需求，还为未来的功能扩展提供了良好的基础架构。
