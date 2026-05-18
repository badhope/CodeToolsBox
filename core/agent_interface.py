"""
Global-Dev-Setup - Agent Interface for External Integration
Provides API for external AI agents to access and control the setup system.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path

from core.models.models import Tool
from core.config.config import ConfigManager
from core.engine.smart_recommender import SmartRecommender, UserContext, DevelopmentStyle, ProjectSize, CloudProvider
from core.engine.smart_installer import SmartInstaller, PlatformDetector
from core.utils.logger import get_logger

logger = get_logger("agent-interface")


class AgentCommand(Enum):
    """Commands that can be executed by external agents"""
    LIST_TOOLS = "list-tools"
    GET_TOOL_INFO = "get-tool-info"
    RECOMMEND_TOOLS = "recommend-tools"
    INSTALL_TOOL = "install-tool"
    INSTALL_MULTIPLE = "install-multiple"
    LIST_TEMPLATES = "list-templates"
    APPLY_TEMPLATE = "apply-template"
    GET_STATUS = "get-status"
    VERIFY_INSTALL = "verify-install"
    GET_ENVIRONMENT = "get-environment"


class ExecutionStatus(Enum):
    """Status of a command execution"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class AgentResponse:
    """Response structure for agent API"""
    status: ExecutionStatus
    data: Any
    message: str
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    execution_time_ms: Optional[float] = None


class DevSetupAgent:
    """
    Agent interface for external AI integration.

    Provides a clean API for AI agents to:
    - Query available tools and templates
    - Get intelligent recommendations
    - Execute installations
    - Check system status
    """

    def __init__(self):
        self.config = ConfigManager()
        self.recommender = SmartRecommender(self.config)
        self.installer = SmartInstaller(self.config)
        self.command_history: List[Dict[str, Any]] = []

        logger.info("DevSetupAgent initialized and ready for commands")

    def execute_command(self, command: AgentCommand, params: Dict[str, Any]) -> AgentResponse:
        """
        Execute an agent command with parameters.

        This is the main entry point for external AI agents.
        """
        import time
        start_time = time.time()

        logger.info(f"Executing command: {command.value} with params: {params}")

        try:
            # Dispatch to handler
            if command == AgentCommand.LIST_TOOLS:
                response = self._list_tools(params)
            elif command == AgentCommand.GET_TOOL_INFO:
                response = self._get_tool_info(params)
            elif command == AgentCommand.RECOMMEND_TOOLS:
                response = self._recommend_tools(params)
            elif command == AgentCommand.INSTALL_TOOL:
                response = self._install_tool(params)
            elif command == AgentCommand.INSTALL_MULTIPLE:
                response = self._install_multiple(params)
            elif command == AgentCommand.LIST_TEMPLATES:
                response = self._list_templates(params)
            elif command == AgentCommand.APPLY_TEMPLATE:
                response = self._apply_template(params)
            elif command == AgentCommand.GET_STATUS:
                response = self._get_status(params)
            elif command == AgentCommand.VERIFY_INSTALL:
                response = self._verify_install(params)
            elif command == AgentCommand.GET_ENVIRONMENT:
                response = self._get_environment(params)
            else:
                response = AgentResponse(
                    status=ExecutionStatus.FAILED,
                    data=None,
                    message=f"Unknown command: {command}",
                    errors=[f"Command {command} is not supported"]
                )

        except Exception as e:
            logger.error(f"Command failed: {e}")
            response = AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message=f"Command execution failed: {str(e)}",
                errors=[str(e)]
            )

        # Record history
        execution_time = (time.time() - start_time) * 1000
        response.execution_time_ms = execution_time
        self._record_command(command, params, response)

        return response

    def _list_tools(self, params: Dict[str, Any]) -> AgentResponse:
        """List all available tools, optionally filtered by category"""
        category = params.get("category", "all")

        tools = self._load_all_tools()

        if category != "all":
            tools = [t for t in tools if t.get("category") == category]

        return AgentResponse(
            status=ExecutionStatus.SUCCESS,
            data=tools,
            message=f"Found {len(tools)} tools"
        )

    def _get_tool_info(self, params: Dict[str, Any]) -> AgentResponse:
        """Get detailed info about a specific tool"""
        tool_name = params.get("tool_name")
        if not tool_name:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message="Tool name required",
                errors=["tool_name parameter is required"]
            )

        tool_info = self._load_tool_definition(tool_name)

        if tool_info:
            return AgentResponse(
                status=ExecutionStatus.SUCCESS,
                data=tool_info,
                message=f"Information for {tool_name}"
            )
        else:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message=f"Tool not found: {tool_name}",
                errors=[f"No definition found for {tool_name}"]
            )

    def _recommend_tools(self, params: Dict[str, Any]) -> AgentResponse:
        """Get intelligent tool recommendations based on context"""
        try:
            # Build user context from params
            context = UserContext(
                development_style=DevelopmentStyle(params.get("style", "full-stack")),
                project_size=ProjectSize(params.get("size", "medium")),
                cloud_provider=CloudProvider(params.get("cloud", "none")),
                os=params.get("os", PlatformDetector.get_os()),
                existing_tools=params.get("existing", [])
            )

            # Get recommendations and install plan
            install_plan = self.recommender.generate_install_plan(context)

            return AgentResponse(
                status=ExecutionStatus.SUCCESS,
                data=install_plan,
                message=f"Generated installation plan for {context.development_style.value} development"
            )
        except Exception as e:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message="Failed to generate recommendations",
                errors=[str(e)]
            )

    def _install_tool(self, params: Dict[str, Any]) -> AgentResponse:
        """Install a single tool"""
        tool_name = params.get("tool_name")
        if not tool_name:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message="Tool name required",
                errors=["tool_name parameter is required"]
            )

        try:
            tool_def = self._load_tool_definition(tool_name)
            if tool_def:
                tool = Tool(
                    name=tool_def["name"],
                    category=tool_def["category"],
                    description=tool_def["description"]
                )
                success = self.installer.install_tool(tool)

                if success:
                    return AgentResponse(
                        status=ExecutionStatus.SUCCESS,
                        data={"tool": tool_name, "installed": True},
                        message=f"Successfully installed {tool_name}"
                    )
                else:
                    return AgentResponse(
                        status=ExecutionStatus.FAILED,
                        data={"tool": tool_name, "installed": False},
                        message=f"Failed to install {tool_name}",
                        errors=["Installation did not succeed"]
                    )
            else:
                return AgentResponse(
                    status=ExecutionStatus.FAILED,
                    data=None,
                    message=f"Tool {tool_name} not found",
                    errors=[f"Tool definition not found for {tool_name}"]
                )
        except Exception as e:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data={"tool": tool_name},
                message=f"Installation error: {e}",
                errors=[str(e)]
            )

    def _install_multiple(self, params: Dict[str, Any]) -> AgentResponse:
        """Install multiple tools in sequence"""
        tools = params.get("tools", [])
        parallel = params.get("parallel", False)

        if not tools:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message="No tools specified",
                errors=["tools array parameter is required"]
            )

        results = []
        for tool_name in tools:
            try:
                result = self._install_tool({"tool_name": tool_name})
                results.append({
                    "tool": tool_name,
                    "success": result.status == ExecutionStatus.SUCCESS,
                    "message": result.message
                })
            except Exception as e:
                results.append({
                    "tool": tool_name,
                    "success": False,
                    "message": str(e)
                })

        success_count = sum(1 for r in results if r["success"])
        total_count = len(results)

        if success_count == total_count:
            status = ExecutionStatus.SUCCESS
            message = f"All {total_count} tools installed successfully"
        elif success_count > 0:
            status = ExecutionStatus.PARTIAL
            message = f"Installed {success_count}/{total_count} tools"
        else:
            status = ExecutionStatus.FAILED
            message = "No tools were installed successfully"

        return AgentResponse(
            status=status,
            data={"results": results},
            message=message
        )

    def _list_templates(self, params: Dict[str, Any]) -> AgentResponse:
        """List available environment templates"""
        templates_dir = Path(__file__).parent.parent.parent / "environment-templates"
        templates = []

        if templates_dir.exists():
            for template_file in templates_dir.glob("*.yaml"):
                import yaml
                with open(template_file) as f:
                    template_data = yaml.safe_load(f)
                    templates.append({
                        "name": template_data.get("name"),
                        "description": template_data.get("description"),
                        "category": template_data.get("category"),
                        "tags": template_data.get("tags", []),
                        "setup_time": template_data.get("estimated_setup_time", "unknown")
                    })

        return AgentResponse(
            status=ExecutionStatus.SUCCESS,
            data=templates,
            message=f"Found {len(templates)} environment templates"
        )

    def _apply_template(self, params: Dict[str, Any]) -> AgentResponse:
        """Apply an environment template"""
        template_name = params.get("template_name")
        if not template_name:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message="Template name required",
                errors=["template_name parameter is required"]
            )

        # Load template
        template = self._load_template(template_name)
        if not template:
            return AgentResponse(
                status=ExecutionStatus.FAILED,
                data=None,
                message=f"Template {template_name} not found",
                errors=[f"Template {template_name} not found"]
            )

        # Get tools from template
        core_tools = [t.get("name") for t in template.get("core_tools", []) if t.get("required")]
        database_tools = [t.get("name") for t in template.get("database_tools", []) if t.get("default")]
        all_tools = core_tools + database_tools

        return self._install_multiple({"tools": all_tools})

    def _get_status(self, params: Dict[str, Any]) -> AgentResponse:
        """Get current system status"""
        system_info = {
            "os": PlatformDetector.get_os(),
            "arch": PlatformDetector.get_architecture(),
            "package_manager": PlatformDetector.detect_package_manager(),
            "config_dir": str(self.config.config_dir),
        }

        # Get installed tools
        installed = self.config.load_installed_tools()

        return AgentResponse(
            status=ExecutionStatus.SUCCESS,
            data={
                "system": system_info,
                "installed_tools": installed.get("tools", [])
            },
            message="System status retrieved successfully"
        )

    def _verify_install(self, params: Dict[str, Any]) -> AgentResponse:
        """Verify if tools are correctly installed"""
        tools_to_check = params.get("tools", [])
        results = {}

        for tool_name in tools_to_check:
            results[tool_name] = self.installer.verify_installation(tool_name)

        all_good = all(results.values())

        return AgentResponse(
            status=ExecutionStatus.SUCCESS if all_good else ExecutionStatus.PARTIAL,
            data=results,
            message=f"Verified {len(tools_to_check)} tools"
        )

    def _get_environment(self, params: Dict[str, Any]) -> AgentResponse:
        """Get environment information"""
        env_vars = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
            "NODE_PATH": os.environ.get("NODE_PATH", ""),
        }

        # Check for common tools
        tool_versions = {}
        common_tools = ["python3", "node", "npm", "git", "docker", "code"]

        for tool in common_tools:
            try:
                import subprocess
                result = subprocess.run(
                    [tool, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    tool_versions[tool] = result.stdout.strip()
            except Exception:
                tool_versions[tool] = None

        return AgentResponse(
            status=ExecutionStatus.SUCCESS,
            data={
                "environment_variables": env_vars,
                "tool_versions": tool_versions,
                "platform": {
                    "os": PlatformDetector.get_os(),
                    "arch": PlatformDetector.get_architecture(),
                    "package_manager": PlatformDetector.detect_package_manager()
                }
            },
            message="Environment information retrieved"
        )

    def _load_all_tools(self) -> List[Dict]:
        """Load all tool definitions"""
        tools = []
        tools_dir = Path(__file__).parent.parent.parent / "tools"

        if tools_dir.exists():
            for category_dir in tools_dir.iterdir():
                if category_dir.is_dir():
                    for tool_dir in category_dir.iterdir():
                        if tool_dir.is_dir():
                            tool_file = tool_dir / "tool.yaml"
                            if tool_file.exists():
                                import yaml
                                with open(tool_file) as f:
                                    tool_data = yaml.safe_load(f)
                                    tools.append(tool_data)
        return tools

    def _load_tool_definition(self, tool_name: str) -> Optional[Dict]:
        """Load a specific tool definition"""
        tools_dir = Path(__file__).parent.parent.parent / "tools"

        if tools_dir.exists():
            for category_dir in tools_dir.iterdir():
                if category_dir.is_dir():
                    tool_dir = category_dir / tool_name
                    tool_file = tool_dir / "tool.yaml"
                    if tool_file.exists():
                        import yaml
                        with open(tool_file) as f:
                            return yaml.safe_load(f)
        return None

    def _load_template(self, template_name: str) -> Optional[Dict]:
        """Load an environment template"""
        templates_dir = Path(__file__).parent.parent.parent / "environment-templates"
        template_file = templates_dir / f"{template_name}.yaml"

        if template_file.exists():
            import yaml
            with open(template_file) as f:
                return yaml.safe_load(f)
        return None

    def _record_command(self, command: AgentCommand, params: Dict, response: AgentResponse):
        """Record command in history"""
        self.command_history.append({
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "command": command.value,
            "params": params,
            "status": response.status.value,
            "execution_time_ms": response.execution_time_ms
        })

        # Keep history trimmed
        if len(self.command_history) > 1000:
            self.command_history = self.command_history[-1000:]

    def quick_bootstrap(self, style: str = "full-stack") -> AgentResponse:
        """
        Quick bootstrap: recommend and install tools for a specific development style.

        This is a convenience method that combines recommendation and installation.
        """
        logger.info(f"Quick bootstrap for {style} development")

        # First get recommendations
        rec_params = {"style": style}
        rec_response = self._recommend_tools(rec_params)

        if rec_response.status != ExecutionStatus.SUCCESS:
            return rec_response

        # Extract tools to install (phase 1 first)
        tools_to_install = []
        for phase in rec_response.data.get("phases", []):
            if phase["phase"] == 1:  # Essential tools
                tools_to_install.extend([r["tool_name"] for r in phase["tools"]])

        if not tools_to_install:
            return AgentResponse(
                status=ExecutionStatus.SUCCESS,
                data={"recommendations": rec_response.data},
                message="No tools to install"
            )

        # Install the tools
        return self._install_multiple({"tools": tools_to_install})
