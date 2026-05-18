#!/usr/bin/env python3
"""
Global-Dev-Setup - Quick Bootstrapper
One-command setup for common development environments.
"""

import sys
import os
from pathlib import Path

# Add core directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from core.agent_interface import DevSetupAgent, AgentCommand


def print_welcome():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                     Global-Dev-Setup                              ║
║                Universal Developer Environment                    ║
╚══════════════════════════════════════════════════════════════════╝

This tool will automatically set up your development environment with
smart recommendations tailored to your needs.
    """
    print(banner)


def main():
    """Main bootstrapper function"""
    print_welcome()

    # Initialize agent
    agent = DevSetupAgent()

    # Parse arguments
    if len(sys.argv) > 1:
        style = sys.argv[1].lower()
    else:
        style = "full-stack"

    valid_styles = [
        "full-stack", "frontend", "backend", "ai-ml",
        "devops", "mobile", "data-science"
    ]

    if style not in valid_styles:
        print(f"Unknown style: {style}")
        print(f"Valid styles: {', '.join(valid_styles)}")
        return 1

    print(f"\n🚀 Bootstrapping for {style} development...\n")

    # Quick bootstrap
    result = agent.quick_bootstrap(style)

    print(f"\n{'═' * 60}")
    print(f"Status: {result.status.value.upper()}")
    print(f"Message: {result.message}")

    if result.warnings:
        print("\n⚠️ Warnings:")
        for warning in result.warnings:
            print(f"   - {warning}")

    if result.errors:
        print("\n❌ Errors:")
        for error in result.errors:
            print(f"   - {error}")
        return 1

    print(f"\n✅ Setup completed in {result.execution_time_ms:.0f}ms")
    print(f"\nNext steps:")
    print("  1. Check installed tools with: python3 global-dev-setup.py status")
    print("  2. Browse available templates: python3 global-dev-setup.py templates")
    print("  3. For help: python3 global-dev-setup.py help")

    return 0


if __name__ == "__main__":
    sys.exit(main())
