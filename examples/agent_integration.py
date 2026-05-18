#!/usr/bin/env python3
"""
Global-Dev-Setup - Smart Agent Usage Examples
Examples showing how external AI agents can integrate with Global-Dev-Setup.
"""

import sys
import os
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from core.agent_interface import DevSetupAgent, AgentCommand, ExecutionStatus


def example_1_getting_started():
    """Example 1: Basic initialization and status check"""
    print("\n" + "="*60)
    print("Example 1: Getting Started")
    print("="*60)

    agent = DevSetupAgent()

    # Check system status
    result = agent.execute_command(AgentCommand.GET_STATUS, {})
    print(f"Status: {result.status.value}")
    print(f"Message: {result.message}")
    if result.data:
        print("System info:", result.data.get("system"))


def example_2_list_tools():
    """Example 2: List available tools"""
    print("\n" + "="*60)
    print("Example 2: Listing Available Tools")
    print("="*60)

    agent = DevSetupAgent()

    # List all tools
    result = agent.execute_command(AgentCommand.LIST_TOOLS, {})
    print(f"Found {len(result.data)} tools")

    # List only devops tools
    result = agent.execute_command(AgentCommand.LIST_TOOLS, {"category": "devops"})
    print(f"Found {len(result.data)} devops tools")


def example_3_recommendations():
    """Example 3: Get smart recommendations"""
    print("\n" + "="*60)
    print("Example 3: Smart Recommendations")
    print("="*60)

    agent = DevSetupAgent()

    # Get recommendations for full-stack development
    result = agent.execute_command(
        AgentCommand.RECOMMEND_TOOLS,
        {
            "style": "full-stack",
            "size": "medium",
            "cloud": "none",
            "existing": ["git"]
        }
    )

    if result.status == ExecutionStatus.SUCCESS:
        plan = result.data
        print(f"Recommended template: {plan.get('recommended_template')}")
        print(f"Estimated time: {plan.get('estimated_time')}")
        print("\nPhases:")
        for phase in plan.get('phases', []):
            print(f"\nPhase {phase['phase']}: {phase['name']}")
            for tool in phase['tools'][:3]:  # Show first 3
                print(f"  - {tool['tool_name']} ({tool['confidence_score']:.0%})")


def example_4_templates():
    """Example 4: Browse and apply templates"""
    print("\n" + "="*60)
    print("Example 4: Environment Templates")
    print("="*60)

    agent = DevSetupAgent()

    # List templates
    result = agent.execute_command(AgentCommand.LIST_TEMPLATES, {})
    print(f"Available templates: {len(result.data)}")

    for template in result.data:
        print(f"\n  📦 {template['name']}")
        print(f"     {template['description']}")
        print(f"     Tags: {', '.join(template['tags'])}")
        print(f"     Setup time: {template['setup_time']}")


def example_5_environment_info():
    """Example 5: Get environment information"""
    print("\n" + "="*60)
    print("Example 5: Environment Information")
    print("="*60)

    agent = DevSetupAgent()
    result = agent.execute_command(AgentCommand.GET_ENVIRONMENT, {})

    if result.status == ExecutionStatus.SUCCESS:
        data = result.data
        print(f"Platform: {data['platform']}")
        print("\nTool versions:")
        for tool, version in data['tool_versions'].items():
            status = "✓" if version else "✗"
            ver_str = f" - {version}" if version else ""
            print(f"  {status} {tool}{ver_str}")


def example_6_quick_bootstrap():
    """Example 6: Quick bootstrap (similar to bootstrap.py)"""
    print("\n" + "="*60)
    print("Example 6: Quick Bootstrap")
    print("="*60)

    agent = DevSetupAgent()

    print("Running quick bootstrap for AI/ML development...")
    result = agent.quick_bootstrap("ai-ml")

    print(f"Result: {result.status.value}")
    print(f"Message: {result.message}")


# This is the main function external agents would use
def example_agent_integration_pattern():
    """
    Example of how an external AI agent would integrate.

    This is a pattern showing how another AI system can use the
    Global-Dev-Setup agent interface to set up development environments.
    """
    print("\n" + "="*60)
    print("Example 7: Agent Integration Pattern")
    print("="*60)

    agent = DevSetupAgent()

    # This is how another AI would use the API
    # 1. First understand the user's context
    user_context = {
        "project_type": "web_app",
        "user_role": "full_stack_developer",
        "team_size": 3,
        "tech_stack_preferences": ["javascript", "python"],
        "cloud_preference": "aws"
    }

    print("User context:", user_context)

    # 2. Map context to our API params
    api_params = {
        "style": "full-stack",
        "size": "small",
        "cloud": "aws",
        "existing": []
    }

    # 3. Get recommendations
    rec_result = agent.execute_command(AgentCommand.RECOMMEND_TOOLS, api_params)

    if rec_result.status == ExecutionStatus.SUCCESS:
        print("\nGenerated installation plan!")
        plan = rec_result.data
        print(f"Template: {plan['recommended_template']}")
        print(f"Phases: {[p['name'] for p in plan['phases']]}")

        # 4. Optionally, start installation (commented for safety)
        # install_result = agent.execute_command(
        #     AgentCommand.APPLY_TEMPLATE,
        #     {"template_name": plan['recommended_template']}
        # )


def main():
    """Run all examples"""
    print("Global-Dev-Setup - Agent Integration Examples")
    print("These examples show how external AI agents can use the API")

    try:
        example_1_getting_started()
        example_2_list_tools()
        example_3_recommendations()
        example_4_templates()
        example_5_environment_info()
        # example_6_quick_bootstrap()  # Commented out - actually tries installation
        example_agent_integration_pattern()

        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
