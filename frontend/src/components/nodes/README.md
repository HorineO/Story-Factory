# 节点样式规范

## 概述

本文档定义了 Story Factory 项目中所有节点的样式规范，确保节点在视觉上保持一致性和专业性。

## 基础样式类

### node-base

所有节点都应该使用的基础样式类，包含：

- 圆角边框 (3px)
- 阴影效果
- 字体设置
- 颜色主题

### node-header

节点标题区域样式，包含：

- 白色文字
- 粗体字重
- 底部边框
- 弹性布局

### node-body

节点内容区域样式，包含：

- 深色背景
- 浅色文字
- 内边距

## 节点类型颜色方案

| 节点类型 | 主色调 | 边框颜色 | 用途         |
| -------- | ------ | -------- | ------------ |
| text     | 蓝色   | #17a2b8  | 文本内容节点 |
| chapter  | 紫色   | #6f42c1  | 章节节点     |
| generate | 黄色   | #ffc107  | 生成节点     |
| start    | 绿色   | #28a745  | 开始节点     |
| end      | 红色   | #dc3545  | 结束节点     |
| input    | 橙色   | #fd7e14  | 输入节点     |
| output   | 青色   | #20c997  | 输出节点     |
| default  | 灰色   | #6c757d  | 默认节点     |

## Handle 样式规范

所有 Handle 都应该使用以下类名：

- `react-flow__handle-left` - 左侧 Handle
- `react-flow__handle-right` - 右侧 Handle
- `react-flow__handle-top` - 顶部 Handle
- `react-flow__handle-bottom` - 底部 Handle

## 开发规范

### 1. 导入样式文件

```javascript
import "./NodeStyles.css";
```

### 2. 使用基础样式类

```javascript
// 对于有header和body的节点
<div className="node-base [node-type]-node">
    <div className="node-header">{data.label}</div>
    <div className="node-body">{content}</div>
</div>

// 对于简单节点
<div className="[node-type]-node">
    {content}
</div>
```

### 3. Handle 样式

```javascript
<Handle
  type="source"
  position={Position.Right}
  className="react-flow__handle-right"
/>
```

### 4. 添加新节点类型

1. 在`NodeStyles.css`中添加新的样式类
2. 遵循颜色方案选择适当的颜色
3. 确保样式与现有节点保持一致
4. 在`NodeTypes.js`中注册新节点

## 注意事项

1. **颜色一致性**: 新节点必须遵循既定的颜色方案
2. **尺寸统一**: 所有节点都应该有合适的最小宽度和高度
3. **字体统一**: 使用统一的字体族和大小
4. **间距统一**: 保持内边距和外边距的一致性
5. **响应式设计**: 确保节点在不同屏幕尺寸下都能正常显示

## 测试检查清单

- [ ] 节点在正常状态下显示正确
- [ ] 节点在选中状态下有高亮效果
- [ ] Handle 位置和样式正确
- [ ] 文字可读性良好
- [ ] 颜色对比度符合可访问性标准
- [ ] 在不同主题下显示正常
