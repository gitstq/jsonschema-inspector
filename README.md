<div align="center">

# 🔍 JSONSchema-Inspector

**Lightweight JSON Schema Visualization & Intelligent Validation Engine**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](setup.py)
[![Tests](https://img.shields.io/badge/Tests-49%20passing-brightgreen)]()

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Project Introduction

JSONSchema-Inspector is a **zero-dependency** Python CLI tool designed for developers who work with JSON Schema on a daily basis. It provides a complete toolchain for schema validation, visualization, mock data generation, and schema comparison — all from your terminal.

**Inspiration**: While working with APIs and configuration systems, we noticed that existing JSON Schema tools are either too heavy (requiring dozens of dependencies) or too limited (only supporting validation). JSONSchema-Inspector bridges this gap by offering a lightweight, all-in-one solution.

**Key Differentiators**:
- 🚀 **Zero dependencies** — Pure Python standard library, no external packages required
- 🎨 **Terminal visualization** — Beautiful tree-like schema structure display
- 🤖 **Smart mock generation** — Generate realistic sample data from schemas
- 📊 **Schema diff engine** — Compare schemas and detect breaking changes
- 🌍 **Multi-draft support** — Draft 7, 2019-09, and 2020-12

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| ✅ **Schema Validation** | Full validation with detailed error reporting | Ready |
| 🎨 **Terminal Visualization** | Tree-like schema structure with colors | Ready |
| 🤖 **Mock Data Generation** | Generate realistic samples from schemas | Ready |
| 📊 **Schema Diff** | Compare schemas, detect breaking changes | Ready |
| 📝 **Auto Documentation** | Generate Markdown docs from schemas | Ready |
| 🔗 **$ref Resolution** | Local reference resolution | Ready |
| ⚡ **Zero Dependencies** | Pure Python standard library | Ready |

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/jsonschema-inspector.git
cd jsonschema-inspector

# Install
pip install -e .

# Or use directly without installation
python -m jsonschema_inspector --help
```

#### Basic Usage

```bash
# Validate JSON data against schema
jsonschema-inspector validate schema.json data.json

# Visualize schema structure
jsonschema-inspector visualize schema.json

# Generate mock data
jsonschema-inspector mock schema.json --count 5

# Compare two schemas
jsonschema-inspector diff old_schema.json new_schema.json

# Generate Markdown documentation
jsonschema-inspector doc schema.json --output api.md
```

### 📖 Detailed Usage Guide

#### Validation Command

```bash
# Basic validation
jsonschema-inspector validate examples/user.schema.json examples/user.valid.json

# With strict mode (warnings as errors)
jsonschema-inspector validate schema.json data.json --strict

# Save report to file
jsonschema-inspector validate schema.json data.json --output report.json
```

#### Mock Data Generation

```bash
# Generate single sample
jsonschema-inspector mock schema.json

# Generate multiple samples with seed for reproducibility
jsonschema-inspector mock schema.json --count 10 --seed 42
```

#### Schema Diff

```bash
# Text diff (default)
jsonschema-inspector diff v1.json v2.json

# JSON format output
jsonschema-inspector diff v1.json v2.json --format json

# Markdown report
jsonschema-inspector diff v1.json v2.json --format markdown --output changes.md
```

### 💡 Design Philosophy

**Why zero dependencies?**
- Faster installation and startup
- No dependency conflicts
- Easier to audit and trust
- Works in restricted environments

**Technology Choices**:
- Pure Python 3.8+ for maximum compatibility
- ANSI colors for terminal output (disable with `--no-color`)
- Modular architecture for easy extension

### 📦 Packaging & Deployment

```bash
# Build distribution
python setup.py sdist bdist_wheel

# Install from source
pip install .

# Run tests
python -m unittest discover tests/ -v
```

### 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="simplified-chinese"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

JSONSchema-Inspector 是一款**零依赖**的 Python CLI 工具，专为日常需要处理 JSON Schema 的开发者设计。它提供了完整的工具链，包括模式验证、可视化、模拟数据生成和模式对比——全部在终端中完成。

**灵感来源**：在处理 API 和配置系统时，我们发现现有的 JSON Schema 工具要么太重（需要几十个依赖），要么功能太有限（仅支持验证）。JSONSchema-Inspector 填补了这一空白，提供了一个轻量级的一站式解决方案。

**核心差异化亮点**：
- 🚀 **零依赖** — 纯 Python 标准库，无需外部包
- 🎨 **终端可视化** — 美观的树形结构展示
- 🤖 **智能模拟生成** — 从 Schema 生成逼真的样本数据
- 📊 **模式差异引擎** — 对比 Schema 并检测破坏性变更
- 🌍 **多草案支持** — 支持 Draft 7、2019-09 和 2020-12

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|---------|-------------|--------|
| ✅ **Schema 验证** | 完整验证并输出详细错误报告 | 已就绪 |
| 🎨 **终端可视化** | 带颜色的树形结构展示 | 已就绪 |
| 🤖 **模拟数据生成** | 从 Schema 生成逼真的样本 | 已就绪 |
| 📊 **Schema 差异对比** | 对比 Schema，检测破坏性变更 | 已就绪 |
| 📝 **自动文档生成** | 从 Schema 生成 Markdown 文档 | 已就绪 |
| 🔗 **$ref 解析** | 本地引用解析 | 已就绪 |
| ⚡ **零依赖** | 纯 Python 标准库 | 已就绪 |

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/jsonschema-inspector.git
cd jsonschema-inspector

# 安装
pip install -e .

# 或直接运行，无需安装
python -m jsonschema_inspector --help
```

#### 基本用法

```bash
# 验证 JSON 数据
jsonschema-inspector validate schema.json data.json

# 可视化 Schema 结构
jsonschema-inspector visualize schema.json

# 生成模拟数据
jsonschema-inspector mock schema.json --count 5

# 对比两个 Schema
jsonschema-inspector diff old_schema.json new_schema.json

# 生成 Markdown 文档
jsonschema-inspector doc schema.json --output api.md
```

### 📖 详细使用指南

#### 验证命令

```bash
# 基础验证
jsonschema-inspector validate examples/user.schema.json examples/user.valid.json

# 严格模式（警告视为错误）
jsonschema-inspector validate schema.json data.json --strict

# 保存报告到文件
jsonschema-inspector validate schema.json data.json --output report.json
```

#### 模拟数据生成

```bash
# 生成单个样本
jsonschema-inspector mock schema.json

# 生成多个样本，使用种子保证可复现
jsonschema-inspector mock schema.json --count 10 --seed 42
```

#### Schema 差异对比

```bash
# 文本差异（默认）
jsonschema-inspector diff v1.json v2.json

# JSON 格式输出
jsonschema-inspector diff v1.json v2.json --format json

# Markdown 报告
jsonschema-inspector diff v1.json v2.json --format markdown --output changes.md
```

### 💡 设计思路

**为什么选择零依赖？**
- 安装和启动更快
- 无依赖冲突
- 更易于审计和信任
- 在受限环境中也能工作

**技术选型原因**：
- Python 3.8+ 以获得最大兼容性
- ANSI 颜色输出（使用 `--no-color` 禁用）
- 模块化架构，便于扩展

### 📦 打包与部署

```bash
# 构建分发包
python setup.py sdist bdist_wheel

# 从源码安装
pip install .

# 运行测试
python -m unittest discover tests/ -v
```

### 🤝 贡献指南

欢迎贡献！请遵循以下规范：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="traditional-chinese"></a>
## 🇹🇼 繁體中文

### 🎉 項目介紹

JSONSchema-Inspector 是一款**零依賴**的 Python CLI 工具，專為日常需要處理 JSON Schema 的開發者設計。它提供了完整的工具鏈，包括模式驗證、可視化、模擬數據生成和模式對比——全部在終端中完成。

**靈感來源**：在處理 API 和配置系統時，我們發現現有的 JSON Schema 工具要么太重（需要幾十個依賴），要么功能太有限（僅支持驗證）。JSONSchema-Inspector 填補了這一空白，提供了一個輕量級的一站式解決方案。

**核心差異化亮點**：
- 🚀 **零依賴** — 純 Python 標準庫，無需外部套件
- 🎨 **終端可視化** — 美觀的樹形結構展示
- 🤖 **智能模擬生成** — 從 Schema 生成逼真的樣本數據
- 📊 **模式差異引擎** — 對比 Schema 並檢測破壞性變更
- 🌍 **多草案支持** — 支持 Draft 7、2019-09 和 2020-12

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|---------|-------------|--------|
| ✅ **Schema 驗證** | 完整驗證並輸出詳細錯誤報告 | 已就緒 |
| 🎨 **終端可視化** | 帶顏色的樹形結構展示 | 已就緒 |
| 🤖 **模擬數據生成** | 從 Schema 生成逼真的樣本 | 已就緒 |
| 📊 **Schema 差異對比** | 對比 Schema，檢測破壞性變更 | 已就緒 |
| 📝 **自動文檔生成** | 從 Schema 生成 Markdown 文檔 | 已就緒 |
| 🔗 ** 解析** | 本地引用解析 | 已就緒 |
| ⚡ **零依賴** | 純 Python 標準庫 | 已就緒 |

### 🚀 快速開始

#### 環境要求
- Python 3.8 或更高版本

#### 安裝

Obtaining file:///data/user/work/jsonschema-inspector/jsonschema-inspector
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'error'
usage: jsonschema-inspector [-h] [--version] [--no-color]
                            {validate,visualize,viz,mock,diff,doc} ...

🔍 JSONSchema-Inspector - Lightweight JSON Schema Visualization & Intelligent Validation Engine

positional arguments:
  {validate,visualize,viz,mock,diff,doc}
                        Available commands
    validate            Validate JSON data against schema
    visualize (viz)     Visualize schema structure
    mock                Generate mock data from schema
    diff                Compare two schemas
    doc                 Generate Markdown documentation

options:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --no-color            Disable colored output

Examples:
  jsonschema-inspector validate schema.json data.json
  jsonschema-inspector visualize schema.json
  jsonschema-inspector mock schema.json --count 3
  jsonschema-inspector diff old_schema.json new_schema.json
  jsonschema-inspector doc schema.json --output api.md
        

#### 基本用法



### 📖 詳細使用指南

#### 驗證命令



#### 模擬數據生成



#### Schema 差異對比



### 💡 設計思路

**為什麼選擇零依賴？**
- 安裝和啟動更快
- 無依賴衝突
- 更易於審計和信任
- 在受限環境中也能工作

**技術選型原因**：
- Python 3.8+ 以獲得最大兼容性
- ANSI 顏色輸出（使用  禁用）
- 模塊化架構，便於擴展

### 📦 打包與部署

running sdist
running egg_info
creating jsonschema_inspector.egg-info
writing jsonschema_inspector.egg-info/PKG-INFO
writing dependency_links to jsonschema_inspector.egg-info/dependency_links.txt
writing entry points to jsonschema_inspector.egg-info/entry_points.txt
writing top-level names to jsonschema_inspector.egg-info/top_level.txt
writing manifest file 'jsonschema_inspector.egg-info/SOURCES.txt'
reading manifest file 'jsonschema_inspector.egg-info/SOURCES.txt'
adding license file 'LICENSE'
writing manifest file 'jsonschema_inspector.egg-info/SOURCES.txt'
running check
creating jsonschema-inspector-1.0.0
creating jsonschema-inspector-1.0.0/jsonschema_inspector
creating jsonschema-inspector-1.0.0/jsonschema_inspector.egg-info
creating jsonschema-inspector-1.0.0/tests
copying files to jsonschema-inspector-1.0.0...
copying LICENSE -> jsonschema-inspector-1.0.0
copying README.md -> jsonschema-inspector-1.0.0
copying setup.py -> jsonschema-inspector-1.0.0
copying jsonschema_inspector/__init__.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector/__main__.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector/cli.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector/diff_engine.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector/mock_generator.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector/validator.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector/visualizer.py -> jsonschema-inspector-1.0.0/jsonschema_inspector
copying jsonschema_inspector.egg-info/PKG-INFO -> jsonschema-inspector-1.0.0/jsonschema_inspector.egg-info
copying jsonschema_inspector.egg-info/SOURCES.txt -> jsonschema-inspector-1.0.0/jsonschema_inspector.egg-info
copying jsonschema_inspector.egg-info/dependency_links.txt -> jsonschema-inspector-1.0.0/jsonschema_inspector.egg-info
copying jsonschema_inspector.egg-info/entry_points.txt -> jsonschema-inspector-1.0.0/jsonschema_inspector.egg-info
copying jsonschema_inspector.egg-info/top_level.txt -> jsonschema-inspector-1.0.0/jsonschema_inspector.egg-info
copying tests/__init__.py -> jsonschema-inspector-1.0.0/tests
copying tests/test_diff_engine.py -> jsonschema-inspector-1.0.0/tests
copying tests/test_mock_generator.py -> jsonschema-inspector-1.0.0/tests
copying tests/test_validator.py -> jsonschema-inspector-1.0.0/tests
copying tests/test_visualizer.py -> jsonschema-inspector-1.0.0/tests
Writing jsonschema-inspector-1.0.0/setup.cfg
creating dist
Creating tar archive
removing 'jsonschema-inspector-1.0.0' (and everything under it)
running bdist_wheel
running build
running build_py
creating build
creating build/lib
creating build/lib/jsonschema_inspector
copying jsonschema_inspector/mock_generator.py -> build/lib/jsonschema_inspector
copying jsonschema_inspector/visualizer.py -> build/lib/jsonschema_inspector
copying jsonschema_inspector/__main__.py -> build/lib/jsonschema_inspector
copying jsonschema_inspector/__init__.py -> build/lib/jsonschema_inspector
copying jsonschema_inspector/validator.py -> build/lib/jsonschema_inspector
copying jsonschema_inspector/cli.py -> build/lib/jsonschema_inspector
copying jsonschema_inspector/diff_engine.py -> build/lib/jsonschema_inspector
creating build/lib/tests
copying tests/test_visualizer.py -> build/lib/tests
copying tests/test_diff_engine.py -> build/lib/tests
copying tests/__init__.py -> build/lib/tests
copying tests/test_mock_generator.py -> build/lib/tests
copying tests/test_validator.py -> build/lib/tests
installing to build/bdist.linux-x86_64/wheel
running install
running install_lib
creating build/bdist.linux-x86_64
creating build/bdist.linux-x86_64/wheel
creating build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/mock_generator.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/visualizer.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/__main__.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/__init__.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/validator.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/cli.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
copying build/lib/jsonschema_inspector/diff_engine.py -> build/bdist.linux-x86_64/wheel/jsonschema_inspector
creating build/bdist.linux-x86_64/wheel/tests
copying build/lib/tests/test_visualizer.py -> build/bdist.linux-x86_64/wheel/tests
copying build/lib/tests/test_diff_engine.py -> build/bdist.linux-x86_64/wheel/tests
copying build/lib/tests/__init__.py -> build/bdist.linux-x86_64/wheel/tests
copying build/lib/tests/test_mock_generator.py -> build/bdist.linux-x86_64/wheel/tests
copying build/lib/tests/test_validator.py -> build/bdist.linux-x86_64/wheel/tests
running install_egg_info
Copying jsonschema_inspector.egg-info to build/bdist.linux-x86_64/wheel/jsonschema_inspector-1.0.0.egg-info
running install_scripts
adding license file "LICENSE" (matched pattern "LICEN[CS]E*")
creating build/bdist.linux-x86_64/wheel/jsonschema_inspector-1.0.0.dist-info/WHEEL
creating 'dist/jsonschema_inspector-1.0.0-py3-none-any.whl' and adding 'build/bdist.linux-x86_64/wheel' to it
adding 'jsonschema_inspector/__init__.py'
adding 'jsonschema_inspector/__main__.py'
adding 'jsonschema_inspector/cli.py'
adding 'jsonschema_inspector/diff_engine.py'
adding 'jsonschema_inspector/mock_generator.py'
adding 'jsonschema_inspector/validator.py'
adding 'jsonschema_inspector/visualizer.py'
adding 'tests/__init__.py'
adding 'tests/test_diff_engine.py'
adding 'tests/test_mock_generator.py'
adding 'tests/test_validator.py'
adding 'tests/test_visualizer.py'
adding 'jsonschema_inspector-1.0.0.dist-info/LICENSE'
adding 'jsonschema_inspector-1.0.0.dist-info/METADATA'
adding 'jsonschema_inspector-1.0.0.dist-info/WHEEL'
adding 'jsonschema_inspector-1.0.0.dist-info/entry_points.txt'
adding 'jsonschema_inspector-1.0.0.dist-info/top_level.txt'
adding 'jsonschema_inspector-1.0.0.dist-info/RECORD'
removing build/bdist.linux-x86_64/wheel
Processing /data/user/work/jsonschema-inspector
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: jsonschema-inspector
  Building wheel for jsonschema-inspector (pyproject.toml): started
  Building wheel for jsonschema-inspector (pyproject.toml): finished with status 'done'
  Created wheel for jsonschema-inspector: filename=jsonschema_inspector-1.0.0-py3-none-any.whl size=27505 sha256=9c75a10193a7a4e539aa7446e359857325f63a8b347fd08c383b5e2e5a162ca0
  Stored in directory: /root/.cache/pip/wheels/7b/28/5b/d111c910205c68128e48f8275314376fcc8086875b8fbc2987
Successfully built jsonschema-inspector
Installing collected packages: jsonschema-inspector
Successfully installed jsonschema-inspector-1.0.0

### 🤝 貢獻指南

歡迎貢獻！請遵循以下規範：

1. Fork 本倉庫
2. 創建功能分支 ()
3. 提交更改 (On branch feature/amazing-feature
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md
	jsonschema-inspector/

nothing added to commit but untracked files present (use "git add" to track))
4. 推送到分支 ()
5. 創建 Pull Request

### 📄 開源協議

本項目採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 文件。
