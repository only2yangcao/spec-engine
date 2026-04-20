---
name: spec
description: 规格执行引擎 - 管理项目研发流程，从需求规格到代码交付
---

# /spec 命令

启动规格执行引擎，管理 .spec-versions 目录下的版本执行流程。

## 用法

```
/spec                    # 开始或恢复规格执行
/spec status [版本号]    # 查看版本状态
/spec versions           # 列出所有版本
```

## 功能

- **断点续传**: 自动检测并从断点恢复
- **多角色协作**: 自动分配任务给 system-architect、qa、code_developer、code_reviewer
- **人工审查节点**: 在关键步骤停下来征求用户决策
- **状态管理**: 通过 state.json 跟踪流程进展

## 工作流程

1. Step0 版本检查（前置）
2. Step1 需求初始化
3. Step2 工程化任务拆解
4. Step3 人工审查节点1
5. Step4 工程化测试验证
6. Step5 人工审查节点2
7. Step6 编码->代码验收（循环）
8. Step7 人工审查节点3
9. Step8 项目汇报

## 相关 Skills

- spec-executor: 规格执行引擎（本命令调用）
- spec-builder: 规格构建引擎
