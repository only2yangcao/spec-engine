---
name: spec-status
description: 查看规格版本状态
---

# /spec-status 命令

查看规格版本的执行状态。

## 用法

```
/spec-status              # 查看进行中的版本
/spec-status [版本号]     # 查看指定版本状态（可简写，如 001）
```

## 功能

- 无版本号参数：展示进行中的版本
- 有版本号参数：提供该版本的摘要，并展示项目汇报
- 版本号可简写（如 001 表示 v001）

## 示例

```
/spec-status
/spec-status 001
/spec-status v001-xgame-ad-monitor
```
