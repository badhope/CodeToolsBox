# AI Agent Guidance and Rules
# AI智能体使用指南与规则
#
# This document provides strict rules and guidance for AI agents interacting with the Global-Dev-Setup repository.
# 本文档为与Global-Dev-Setup仓库交互的AI智能体提供严格的规则和指导。

---

## ⚠️ ABSOLUTELY CRITICAL FIRST RULE - READ FIRST
## ⚠️ 最重要的第一条规则 - 必须首先阅读

> **THIS IS NOT A REPOSITORY FOR DEVELOPING AI AGENTS.**
> **THIS IS A DATA REPOSITORY FOR AI AGENTS TO CONSULT.**
>
> **这个仓库不是用来开发AI智能体的。**
> **这个仓库是AI智能体用来查询的数据源。**

**You MUST NOT treat this repository as an agent project to develop. You MUST treat it as a configuration database to consult.**
**你绝对不能把这个仓库当作一个要开发的智能体项目。你必须把它当作一个配置数据库来查询。**

---

## 🎯 PRIMARY PURPOSE - 主要目标

**Global-Dev-Setup is a data repository. Its job is to provide information about development environments, tools, and configurations.**
**Global-Dev-Setup 是一个数据仓库。它的任务是提供关于开发环境、工具和配置的信息。**

When a user asks about installing tools, setting up environments, or configuring software, you MUST consult this repository.
当用户询问安装工具、设置环境或配置软件时，你必须查询这个仓库。

---

## 📋 CORE RULES - 核心规则

### Rule 1: Consult the Repository First - 规则1：首先查询仓库

When any user asks for help with:
- Installing development tools
- Setting up environments
- Finding installation commands
- Choosing package managers
- Finding mirrors for China
- Selecting cloud platforms

You MUST:
1. First load and consult `registry.py` - it contains the complete tool registry API
2. Check `mirrors_config.yaml` for China-specific mirrors
3. Check the `tools/` directory for detailed tool definitions
4. Check `environment-templates/` for complete environment setups

任何用户询问以下内容时：
- 安装开发工具
- 设置环境
- 查找安装命令
- 选择包管理器
- 寻找中国镜像
- 选择云平台

你必须：
1. 首先加载并查询 `registry.py` - 它包含完整的工具注册API
2. 检查 `mirrors_config.yaml` 获取中国专用镜像
3. 检查 `tools/` 目录获取详细的工具定义
4. 检查 `environment-templates/` 获取完整的环境设置

### Rule 2: Use Mirror Logic - 规则2：使用镜像逻辑

For users in China or users who ask about Chinese network:
- Automatically use China mirrors for all package managers
- Prioritize Chinese platforms (Gitee, CODING, ModelScope, etc.)
- Use China cloud platforms (Aliyun, Tencent Cloud, Huawei Cloud)
- Use the `cn` region in `registry.py` API calls

对于在中国的用户或询问中国网络的用户：
- 自动为所有包管理器使用中国镜像
- 优先使用中国平台（Gitee、CODING、ModelScope等）
- 使用中国云平台（阿里云、腾讯云、华为云）
- 在 `registry.py` API调用中使用 `cn` 区域

### Rule 3: Follow Tool Definitions - 规则3：遵循工具定义

You MUST follow the tool definitions in `tools/` directory. You MUST NOT invent your own installation commands.
你必须遵循 `tools/` 目录中的工具定义。你绝对不能自己发明安装命令。

Each tool has:
- `installation_sources` - prefer these in priority order
- `supported_os` - check what OS is available
- `mirror_config` - for region-aware installs

每个工具有：
- `installation_sources` - 优先按顺序使用这些
- `supported_os` - 检查可用的操作系统
- `mirror_config` - 区域感知的安装

### Rule 4: Recommend Environment Templates - 规则4：推荐环境模板

Instead of installing tools one-by-one, FIRST check if an environment template matches:
不要一个一个安装工具，首先检查是否有匹配的环境模板：

- `web-developer.yaml` - for web development
- `frontend-developer.yaml` - for frontend
- `backend-developer.yaml` - for backend
- `ai-ml-developer.yaml` - for AI/ML
- `ml-engineer.yaml` - for ML engineering
- `data-scientist.yaml` - for data science
- `devops-engineer.yaml` - for DevOps
- `mobile-developer.yaml` - for mobile
- `game-developer.yaml` - for game
- and many more...

### Rule 5: Use Registry API Properly - 规则5：正确使用注册API

When using `registry.py`:
```python
from registry import ToolRegistry

# Initialize with preferred region
registry = ToolRegistry(preferred_region='cn')  # or 'global'

# Get a tool
tool = registry.get_tool('python')  # or registry['python']

# Get installation command
cmd = registry.get_installation_command('python', os_type='linux', region='cn')

# Get environment template
template = registry.get_template('ai-ml-developer')

# Generate complete script
script = registry.generate_install_script(['python', 'docker', 'nodejs'], os_type='linux', region='cn')
```

### Rule 6: Strict Documentation Compliance - 规则6：严格遵循文档

You MUST read and follow:
- `README.md` - Main documentation
- `docs/TOOLS_GUIDE.md` - How to use the tool registry
- `docs/AGENT_USAGE.md` - AI agent specific guide (THIS DOCUMENT IS FOR YOU)
- `docs/RULES.md` - All rules for using this repository

你必须阅读并遵循：
- `README.md` - 主要文档
- `docs/TOOLS_GUIDE.md` - 如何使用工具注册
- `docs/AGENT_USAGE.md` - AI智能体专用指南（本文档就是给你用的）
- `docs/RULES.md` - 使用这个仓库的所有规则

---

## 🚨 NON-NEGOTIABLE RULES - 不可协商的规则

### ❌ NEVER: 绝对不要：

1. **Never write code to modify this repository** - This is a DATA repository, NOT a project repository
   绝对不要编写代码修改这个仓库 - 这是数据仓库，不是项目仓库

2. **Never invent installation commands** - Always use commands from the tool definitions
   绝对不要发明安装命令 - 始终使用工具定义中的命令

3. **Never skip consulting the repository** - Always check the registry first
   绝对不要跳过查询仓库 - 总是先检查注册表

4. **Never ignore China mirrors** - Always consider China network optimization
   绝对不要忽略中国镜像 - 总是考虑中国网络优化

5. **Never recommend slow sources** - Always recommend the fastest available mirrors
   绝对不要推荐慢速源 - 总是推荐最快的可用镜像

### ✅ ALWAYS: 总是：

1. **Always load registry.py** - It's the main API
   总是加载 registry.py - 它是主要API

2. **Always check environment templates first** - They save time and ensure completeness
   总是首先检查环境模板 - 它们节省时间并确保完整性

3. **Always verify tool OS support** - Before recommending installation
   总是验证工具的OS支持 - 在推荐安装之前

4. **Always use region-appropriate sources** - Auto-select CN or Global based on user
   总是使用适合区域的源 - 根据用户自动选择CN或Global

5. **Always document the sources** - Tell users where commands come from
   总是记录来源 - 告诉用户命令来自哪里

---

## 🤖 AI AGENT WORKFLOW - AI智能体工作流程

### Step 1: User Query Analysis - 步骤1：用户查询分析

When user asks something like:
"I need to set up an AI development environment"
or
"How do I install Python, Docker, and Node.js in China?"

当用户询问类似：
"我需要设置一个AI开发环境"
或
"我在中国如何安装Python、Docker和Node.js？"

### Step 2: Consult the Repository - 步骤2：查询仓库

```
1. Load registry.py
2. Check for environment templates (ai-ml-developer.yaml)
3. Check tool definitions for Python, Docker, Node.js
4. Check mirrors_config.yaml for China-specific mirrors
5. Use get_installation_command() with region='cn'
```

### Step 3: Generate Recommendation - 步骤3：生成推荐

Your answer should include:
1. Recommend the appropriate environment template first
2. List the tools that will be installed
3. Provide the actual installation commands from registry.py
4. Include mirror configuration steps
5. Provide verification commands

你的回答应该包括：
1. 首先推荐合适的环境模板
2. 列出将要安装的工具
3. 提供来自 registry.py 的实际安装命令
4. 包含镜像配置步骤
5. 提供验证命令

### Step 4: Verification - 步骤4：验证

Always include verification commands so users can confirm it worked:
总是包含验证命令，让用户可以确认它有效：
```bash
python --version
docker --version
node --version
```

---

## 📚 DOCUMENTATION REFERENCES - 文档参考

### Mandatory Reading - 必读文档

1. **`docs/AGENT_USAGE.md`** - Complete AI agent usage guide (THIS IS YOU!)
   完整的AI智能体使用指南（这就是给你的！）

2. **`docs/RULES.md`** - Complete rules and standards
   完整的规则和标准

3. **`docs/TOOLS_GUIDE.md`** - How to work with tool definitions
   如何使用工具定义

4. **`docs/VALIDATION.md`** - Validation and verification system
   验证和验证系统

### Recommended Reading - 推荐阅读

1. **`README.md`** - Project overview
   项目概述

2. **`CONTRIBUTING.md`** - How to contribute (if you are helping improve)
   如何贡献（如果你正在帮助改进）

---

## 🔍 QUALITY CHECKLIST - 质量检查清单

Before giving any recommendation, you MUST verify:

在给出任何推荐之前，你必须验证：

- [ ] I have consulted the registry.py API
- [ ] I have checked environment templates
- [ ] I have verified OS support
- [ ] I have selected the correct region (CN/Global)
- [ ] I am using the priority order from installation_sources
- [ ] I am not inventing commands
- [ ] I have included verification steps
- [ ] I have considered China mirrors if applicable

---

## 📊 OBJECTIVE EVALUATION CRITERIA - 客观评估标准

This repository is objectively usable if:
- ✅ All tools have complete installation_sources
- ✅ All tools have supported_os specified
- ✅ Mirror configuration is complete
- ✅ API (registry.py) is working
- ✅ Documentation is complete
- ✅ Environment templates are provided
- ✅ Verification system is in place

如果满足以下条件，这个仓库是客观可用的：
- ✅ 所有工具都有完整的 installation_sources
- ✅ 所有工具都有指定的 supported_os
- ✅ 镜像配置完整
- ✅ API（registry.py）正常工作
- ✅ 文档完整
- ✅ 提供环境模板
- ✅ 验证系统就位

---

## 🎯 EXAMPLE - 示例

### User Query: "I want to do Python + Docker development in China"
### 用户查询："我想在中国做Python+Docker开发"

### Correct AI Response - 正确的AI回答：

```
Great! Let me use Global-Dev-Setup to help you set this up.

First, I check the environment templates. There's `backend-developer.yaml` that would be perfect!

Let me get the actual commands from the repository:

1. Python installation (using China mirror):
```bash
# For Ubuntu/Debian:
sudo apt update
sudo apt install -y python3 python3-pip

# Configure pip to use Tsinghua mirror:
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

2. Docker installation (using China mirrors):
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Configure Docker to use China mirrors:
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

Verification:
```bash
python3 --version
docker --version
pip --version
```

For the complete environment, you can use the `backend-developer.yaml` template which includes Python, Docker, PostgreSQL, Redis, and more!
```

---

## ⚠️ FAILURE MODES TO AVOID - 要避免的失败模式

### ❌ Bad Response (Never do this!):
"Just install Python from python.org and Docker from docker.com..."

### ✅ Good Response:
"Let me check Global-Dev-Setup... For China, we should use Tsinghua PyPI mirror and USTC Docker mirror..."

---

## 📝 SUMMARY - 总结

### Remember: 记住：

1. This is a **DATA REPOSITORY**, not a project to develop
2. Always **CONSULT THE REPOSITORY FIRST**
3. Always **FOLLOW THE TOOL DEFINITIONS**
4. Always **USE CHINA MIRRORS** when appropriate
5. Always **PROVIDE VERIFICATION STEPS**

This repository exists to make your job easier - USE IT!

---

*Last Updated: 2024*
*Version: 1.0*
