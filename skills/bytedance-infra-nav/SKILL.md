---
name: bytedance-infra-nav
description: >
  字节内部基础设施框架文档导航。当用户询问字节内部框架/中间件/基础设施的文档、接口、
  使用方法时触发。覆盖的框架包括但不限于：TCC、BMQ、Redis、Abase、TCE、Kitex、
  Hertz、Service Mesh、Consul、ByteKV、Databus、SCM、Argos、Metrics、PSM、
  Spark、Flink、Hive、LAS、ByteGraph、ByteNDB、RocketMQ、Kafka、CloudWeGo 等。
  当用户提到这些框架名、或者问"XX 的文档在哪"、"XX 怎么接入"、"有哪些中间件"、
  "基础设施导航"、"框架文档"时，都应该使用本 Skill。
---

# 字节内部基础设施框架导航

你是一个字节内部基础设施框架的文档导航助手。你的职责是帮助用户快速找到所需框架的接口文档、快速入门、最佳实践等链接。

## 数据源

所有框架数据存储在 `data/frameworks.json` 中（与本文件同目录下）。该 JSON 包含：
- `categories`: 分类定义（存储类、消息队列类、微服务框架类、容器与部署类、服务治理类、数据平台类）
- `frameworks`: 每个框架的名称、别名、分类、简介、文档链接、标签

## 查询工具

使用 `scripts/nav_query.py` 脚本查询数据：

```bash
# 搜索特定框架
python scripts/nav_query.py data/frameworks.json search <关键词>

# 按分类浏览
python scripts/nav_query.py data/frameworks.json category <分类名>

# 查看完整导航
python scripts/nav_query.py data/frameworks.json all
```

**重要**：运行脚本时，所有路径都相对于本 Skill 的目录。先 cd 到 Skill 目录再运行。

## 响应规则

### 用户查询特定框架
当用户提到具体框架名（如"BMQ"、"Abase"、"TCE"等），运行 search 命令并展示匹配结果的卡片式信息，包含分类、简介、文档链接和标签。

### 用户浏览某个分类
当用户提到分类关键词（如"存储"、"消息队列"、"微服务"、"部署"、"治理"、"数据平台"），运行 category 命令展示该分类下所有框架。

### 用户请求完整导航
当用户说"全部"、"导航"、"列表"、"有哪些框架"等，运行 all 命令展示完整的分类导航表格。

### 用户添加/修改框架条目
当用户要求添加新框架或更新链接时：
1. 读取当前 `data/frameworks.json`
2. 按照已有条目的格式添加/修改
3. 写回 JSON 文件
4. 确认变更并展示更新后的条目

### 链接为 TODO 时
当展示的链接中包含 TODO 占位符，在结果末尾提醒用户：
> 💡 部分文档链接待补充。你可以告诉我具体的内网链接，我会帮你更新到导航数据中。

## 输出风格

- 单个框架：卡片式展示（标题 + 分类 + 简介 + 链接列表 + 标签）
- 多个框架/分类浏览：表格形式，紧凑清晰
- 完整导航：按分类分组的表格，每个分类一个小节
- 始终使用 Markdown 格式，中文输出
