# Step1 需求初始化

## 任务描述

初始化版本目录，记录需求规格快照文档：
1. 阅读需求规格文档，生成版本号，类似`v001-{需求短名}`
2. 创建版本目录和子目录，创建`state.json`、`report.md`文档，初始化`state.json`文档
3. 需求规格文档拆解成`ARCHITECTURE.md`、`CONVENTIONS.md`、`SPEC.md`、`TEST-SCENARIOS.md`四个文件，存储到`spec/`目录

## 执行角色

项目经理

## 目录结构

```
.spec-versions/{version}/
├── spec/
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── SPEC.md
│   └── TEST-SCENARIOS.md
├── tasks/
├── tests/
├── reviews/
├── state.json
└── report.md
```

## state.json 初始格式

```json
{
    "version": "v001-{short-name}",
    "current_step": "Step1 需求初始化",
    "status": "进行中",
    "completed_steps": ["Step0 版本检查"],
    "tasks": [],
    "risks": []
}
```
