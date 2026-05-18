# Global-Dev-Setup - Agent API Reference

## Overview

The Global-Dev-Setup provides a clean, agent-friendly API that allows external AI systems to:

- Query available tools and templates
- Get intelligent recommendations
- Execute installations
- Check system status
- Verify installations

## Quick Start

```python
from core.agent_interface import DevSetupAgent, AgentCommand

# Initialize the agent
agent = DevSetupAgent()

# Execute a command
result = agent.execute_command(AgentCommand.GET_STATUS, {})

print(result.status.value)  # "success"
print(result.data)           # Data returned
print(result.message)        # Human-readable message
```

## Commands

### LIST_TOOLS
List all available tools, optionally filtered by category.

**Parameters:**
- `category` (optional): "all", "programming-language", "database", "devops", "editor", "productivity"

**Example:**
```python
result = agent.execute_command(
    AgentCommand.LIST_TOOLS,
    {"category": "devops"}
)
```

### GET_TOOL_INFO
Get detailed information about a specific tool.

**Parameters:**
- `tool_name` (required): Name of the tool

**Example:**
```python
result = agent.execute_command(
    AgentCommand.GET_TOOL_INFO,
    {"tool_name": "python3"}
)
```

### RECOMMEND_TOOLS
Get intelligent tool recommendations based on user context.

**Parameters:**
- `style` (required): "full-stack", "frontend", "backend", "ai-ml", "devops", "mobile"
- `size` (optional): "small", "medium", "large" (default: "medium")
- `cloud` (optional): "none", "aws", "gcp", "azure" (default: "none")
- `existing` (optional): List of already installed tools
- `os` (optional): Auto-detected if not specified

**Example:**
```python
result = agent.execute_command(
    AgentCommand.RECOMMEND_TOOLS,
    {
        "style": "ai-ml",
        "size": "medium",
        "cloud": "aws",
        "existing": ["git"]
    }
)
```

### INSTALL_TOOL
Install a single tool.

**Parameters:**
- `tool_name` (required): Name of tool to install

**Example:**
```python
result = agent.execute_command(
    AgentCommand.INSTALL_TOOL,
    {"tool_name": "python3"}
)
```

### INSTALL_MULTIPLE
Install multiple tools.

**Parameters:**
- `tools` (required): List of tool names
- `parallel` (optional): Boolean, whether to install in parallel (default: false)

**Example:**
```python
result = agent.execute_command(
    AgentCommand.INSTALL_MULTIPLE,
    {
        "tools": ["git", "python3", "docker"],
        "parallel": true
    }
)
```

### LIST_TEMPLATES
List available environment templates.

**Example:**
```python
result = agent.execute_command(AgentCommand.LIST_TEMPLATES, {})
```

### APPLY_TEMPLATE
Apply an environment template.

**Parameters:**
- `template_name` (required): Name of template to apply

**Example:**
```python
result = agent.execute_command(
    AgentCommand.APPLY_TEMPLATE,
    {"template_name": "web-developer"}
)
```

### GET_STATUS
Get system status and installed tools.

**Example:**
```python
result = agent.execute_command(AgentCommand.GET_STATUS, {})
```

### VERIFY_INSTALL
Verify if specified tools are correctly installed.

**Parameters:**
- `tools` (required): List of tool names to verify

**Example:**
```python
result = agent.execute_command(
    AgentCommand.VERIFY_INSTALL,
    {"tools": ["git", "python3", "docker"]}
)
```

### GET_ENVIRONMENT
Get environment variables and tool versions.

**Example:**
```python
result = agent.execute_command(AgentCommand.GET_ENVIRONMENT, {})
```

## Quick Bootstrap

For convenience, there's also a direct `quick_bootstrap` method:

```python
# One-line setup for a specific development style
result = agent.quick_bootstrap("ai-ml")  # or "full-stack", "devops", etc.
```

## Response Object

All commands return an `AgentResponse` object with:

- `status`: ExecutionStatus (PENDING, RUNNING, SUCCESS, FAILED, PARTIAL)
- `data`: The returned data (dict, list, or None)
- `message`: Human-readable message
- `errors`: List of error strings (if any)
- `warnings`: List of warning strings (if any)
- `execution_time_ms`: Execution time in milliseconds

## Integration Pattern

Here's how an external AI agent would typically use this API:

```python
# 1. Initialize
agent = DevSetupAgent()

# 2. Check current state
status = agent.execute_command(AgentCommand.GET_STATUS, {})

# 3. Understand user's needs
# ... your AI's user understanding logic ...

# 4. Get recommendations
recommendations = agent.execute_command(
    AgentCommand.RECOMMEND_TOOLS,
    {
        "style": "full-stack",  # based on user needs
        "size": "small",
        "cloud": "none"
    }
)

# 5. Show plan to user, get confirmation
# ... your UI/confirmation logic ...

# 6. Execute installation
result = agent.execute_command(
    AgentCommand.INSTALL_MULTIPLE,
    {"tools": ["git", "python3", "docker"]}
)

# 7. Verify
verify_result = agent.execute_command(
    AgentCommand.VERIFY_INSTALL,
    {"tools": ["git", "python3", "docker"]}
)
```

## Available Styles

- `full-stack` - Full-stack web development
- `frontend` - Frontend-only development
- `backend` - Backend API development
- `ai-ml` - AI/ML and data science
- `devops` - DevOps and cloud native
- `mobile` - Mobile app development

## Available Templates

- `web-developer` - Full web development stack
- `ai-ml-developer` - AI/ML development environment
- `mobile-developer` - Mobile app development
- `devops-engineer` - DevOps and cloud native

## Error Handling

Always check the status:

```python
result = agent.execute_command(cmd, params)

if result.status == ExecutionStatus.SUCCESS:
    print("Success!", result.message)
elif result.status == ExecutionStatus.PARTIAL:
    print("Partial success:", result.message)
    # Check which worked
else:
    print("Failed:", result.message)
    for error in result.errors:
        print("  -", error)
```

## Security Considerations

- Installation may require sudo/admin privileges
- Tool definitions are in trusted files (tool.yaml)
- No arbitrary code execution from untrusted sources
- All commands logged for auditing
