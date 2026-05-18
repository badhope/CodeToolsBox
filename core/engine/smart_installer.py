"""
Global-Dev-Setup - Tool Installer with Intelligent Selection
Automatically chooses the best installation method based on system context.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum
import platform

from core.utils.logger import get_logger
from core.models.models import Tool
from core.utils.exceptions import InstallationError, UnsupportedOSError

logger = get_logger("smart-installer")


class InstallationMethod(Enum):
    """Available installation methods"""
    APT = "apt"
    BREW = "brew"
    PIP = "pip"
    NPM = "npm"
    DOCKER = "docker"
    CURL = "curl"
    MANUAL = "manual"
    NVM = "nvm"


class PlatformDetector:
    """Detects the current platform and provides system info"""

    @staticmethod
    def get_os() -> str:
        """Get OS type (linux, macos, windows)"""
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name

    @staticmethod
    def get_architecture() -> str:
        """Get CPU architecture"""
        arch = platform.machine().lower()
        if arch in ["x86_64", "amd64"]:
            return "amd64"
        elif arch in ["arm64", "aarch64"]:
            return "arm64"
        return arch

    @staticmethod
    def is_command_available(command: str) -> bool:
        """Check if a command is available in PATH"""
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @staticmethod
    def detect_package_manager() -> Optional[str]:
        """Detect available package manager"""
        current_os = PlatformDetector.get_os()

        if current_os == "linux":
            if PlatformDetector.is_command_available("apt-get"):
                return "apt"
            elif PlatformDetector.is_command_available("dnf"):
                return "dnf"
            elif PlatformDetector.is_command_available("pacman"):
                return "pacman"
        elif current_os == "macos":
            if PlatformDetector.is_command_available("brew"):
                return "brew"
        elif current_os == "windows":
            if PlatformDetector.is_command_available("winget"):
                return "winget"
        return None


class SmartInstaller:
    """Intelligent tool installer that chooses the best installation method"""

    def __init__(self, config):
        self.config = config
        self.platform_info = {
            "os": PlatformDetector.get_os(),
            "arch": PlatformDetector.get_architecture(),
            "package_manager": PlatformDetector.detect_package_manager()
        }
        logger.info(f"Detected platform: {self.platform_info}")

    def install_tool(self, tool: Tool, use_docker_fallback: bool = True) -> bool:
        """
        Install a tool using the best available method.

        Args:
            tool: The tool to install
            use_docker_fallback: If system install fails, try Docker container

        Returns:
            bool: True if installation successful
        """
        logger.info(f"Installing {tool.name}...")

        # Find best installation source for current platform
        best_source = self._select_best_source(tool)

        if not best_source:
            raise InstallationError(f"No installation method available for {tool.name} on {self.platform_info['os']}")

        logger.info(f"Selected installation method: {best_source.type}")

        try:
            success = self._execute_installation(tool, best_source)

            if success:
                logger.info(f"✓ Successfully installed {tool.name}")
                return True
            else:
                logger.warning(f"Failed to install {tool.name} with {best_source.type}")

            # Try Docker as fallback if available
            if use_docker_fallback and best_source.type != "docker":
                docker_source = next((s for s in tool.installation_sources if s.type == "docker"), None)
                if docker_source:
                    logger.info("Trying Docker as fallback...")
                    return self._execute_installation(tool, docker_source)

            return False

        except Exception as e:
            logger.error(f"Installation failed for {tool.name}: {e}")
            raise InstallationError(f"Failed to install {tool.name}: {e}")

    def _select_best_source(self, tool: Tool) -> Any:
        """Select the best installation source based on current platform"""
        current_os = self.platform_info['os']
        package_manager = self.platform_info['package_manager']

        # Filter sources compatible with current OS
        compatible_sources = []
        for source in tool.installation_sources:
            if hasattr(source, 'os') and source.os:
                # Check if current OS is in source's OS list
                if 'all' in source.os or current_os in source.os:
                    compatible_sources.append(source)
            else:
                # If no OS specified, assume compatible with all
                compatible_sources.append(source)

        if not compatible_sources:
            return None

        # Score and sort sources by priority and suitability
        scored_sources = []
        for source in compatible_sources:
            score = source.priority if hasattr(source, 'priority') else 5

            # Prefer the detected package manager
            if source.type == package_manager:
                score += 10  # Major priority boost

            # For macOS, prefer Brew
            if current_os == "macos" and source.type == "brew":
                score += 5

            # For Linux, prefer apt/dnf/pacman
            if current_os == "linux" and source.type in ["apt", "dnf", "pacman"]:
                score += 5

            scored_sources.append((score, source))

        # Sort by score descending
        scored_sources.sort(key=lambda x: x[0], reverse=True)
        return scored_sources[0][1] if scored_sources else None

    def _execute_installation(self, tool: Tool, source: Any) -> bool:
        """Execute the installation using the specified source"""
        if source.type == "apt":
            return self._install_apt(tool, source)
        elif source.type == "brew":
            return self._install_brew(tool, source)
        elif source.type == "pip":
            return self._install_pip(tool, source)
        elif source.type == "curl":
            return self._install_curl(tool, source)
        elif source.type == "docker":
            return self._install_docker(tool, source)
        elif source.type == "nvm":
            return self._install_nvm(tool, source)
        elif source.type == "manual":
            logger.info(f"Manual installation required for {tool.name}")
            logger.info(f"See: {source.url}")
            return False
        return False

    def _install_apt(self, tool: Tool, source: Any) -> bool:
        """Install via apt-get"""
        try:
            logger.info("Updating package list...")
            subprocess.run(
                ["sudo", "apt-get", "update", "-qq"],
                check=True,
                capture_output=True
            )

            package = source.package_name if hasattr(source, 'package_name') else tool.name
            logger.info(f"Installing {package}...")
            result = subprocess.run(
                ["sudo", "apt-get", "install", "-y", package],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"apt install failed: {e.stderr}")
            return False

    def _install_brew(self, tool: Tool, source: Any) -> bool:
        """Install via Homebrew"""
        try:
            package = source.package_name if hasattr(source, 'package_name') else tool.name
            logger.info(f"Installing {package} via Homebrew...")
            result = subprocess.run(
                ["brew", "install", package],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"brew install failed: {e.stderr}")
            return False

    def _install_pip(self, tool: Tool, source: Any) -> bool:
        """Install via pip"""
        try:
            package = source.package_name if hasattr(source, 'package_name') else tool.name
            logger.info(f"Installing {package} via pip...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"pip install failed: {e.stderr}")
            return False

    def _install_curl(self, tool: Tool, source: Any) -> bool:
        """Install via curl"""
        if hasattr(source, 'command'):
            try:
                logger.info("Executing curl installation...")
                result = subprocess.run(
                    source.command,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"curl install failed: {e.stderr}")
                return False
        return False

    def _install_docker(self, tool: Tool, source: Any) -> bool:
        """Run via Docker container"""
        try:
            # Docker is used for running, not installing
            logger.info(f"Docker container available for {tool.name}")
            return True
        except Exception as e:
            logger.error(f"Docker setup failed: {e}")
            return False

    def _install_nvm(self, tool: Tool, source: Any) -> bool:
        """Install via NVM"""
        try:
            if hasattr(source, 'command'):
                subprocess.run(
                    source.command,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
            return True
        except Exception as e:
            logger.error(f"NVM install failed: {e}")
            return False

    def verify_installation(self, tool_name: str) -> bool:
        """Verify if a tool was installed successfully"""
        verify_commands = {
            "git": ["git", "--version"],
            "nodejs": ["node", "--version"],
            "python3": ["python3", "--version"],
            "docker": ["docker", "--version"],
            "vscode": ["code", "--version"],
            "postgresql": ["psql", "--version"],
            "redis": ["redis-server", "--version"],
        }

        cmd = verify_commands.get(tool_name)
        if not cmd:
            logger.warning(f"No verify command known for {tool_name}")
            return False

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"✓ {tool_name} verified: {result.stdout.strip()}")
                return True
            return False
        except Exception:
            return False
