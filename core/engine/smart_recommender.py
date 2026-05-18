"""
Global-Dev-Setup - Smart Recommendation Engine
Analyzes user's context and recommends the best tools for their needs.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import yaml

from core.models.models import Tool, ToolCategory
from core.utils.logger import get_logger

logger = get_logger("smart-recommender")


class DevelopmentStyle(Enum):
    """Developer style classification"""
    FULL_STACK = "full-stack"
    FRONTEND = "frontend"
    BACKEND = "backend"
    AI_ML = "ai-ml"
    DEVOPS = "devops"
    MOBILE = "mobile"
    DATA_SCIENCE = "data-science"
    GAME_DEVELOPMENT = "game-dev"


class ProjectSize(Enum):
    """Project size classification"""
    SMALL = "small"  # 1-3 devs
    MEDIUM = "medium"  # 4-10 devs
    LARGE = "large"  # 11+ devs


class CloudProvider(Enum):
    """Cloud provider preference"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    NONE = "none"
    ALL = "all"


@dataclass
class UserContext:
    """Context about the user's situation"""
    development_style: DevelopmentStyle
    project_size: ProjectSize
    cloud_provider: CloudProvider
    os: str  # linux, macos, windows
    existing_tools: List[str]
    project_type: Optional[str] = None
    team_size: int = 1
    experience_level: str = "intermediate"


@dataclass
class Recommendation:
    """Tool recommendation"""
    tool_name: str
    confidence_score: float  # 0.0 - 1.0
    reason: str
    priority: int  # 1 = highest
    alternatives: List[str]
    category: str


class SmartRecommender:
    """Intelligent tool recommendation engine"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.load_tool_data()

    def load_tool_data(self):
        """Load tool definitions"""
        self.tools = {}
        self.tool_rules = {}

        # Load default tool recommendations
        self.recommendation_rules = {
            "full-stack": {
                "must_have": ["git", "nodejs", "python3", "docker", "vscode", "postgresql"],
                "recommended": ["redis", "nginx", "eslint", "prettier"],
                "optional": ["mongodb", "kubernetes"]
            },
            "frontend": {
                "must_have": ["git", "nodejs", "vscode"],
                "recommended": ["eslint", "prettier", "tailwindcss"],
                "optional": ["typescript"]
            },
            "backend": {
                "must_have": ["git", "python3", "docker", "postgresql"],
                "recommended": ["redis", "nginx"],
                "optional": ["kubernetes"]
            },
            "ai-ml": {
                "must_have": ["git", "python3", "vscode", "docker"],
                "recommended": ["pytorch", "jupyter", "pandas", "numpy"],
                "optional": ["tensorflow", "mlflow"]
            },
            "devops": {
                "must_have": ["git", "docker", "kubectl"],
                "recommended": ["terraform", "helm", "minikube"],
                "optional": ["ansible"]
            },
            "mobile": {
                "must_have": ["git", "nodejs", "vscode"],
                "recommended": ["java", "react-native", "android-sdk"],
                "optional": ["flutter"]
            }
        }

    def analyze_context(self, context: UserContext) -> List[Recommendation]:
        """Analyze user context and generate recommendations"""

        recommendations = []

        # Get base recommendations by style
        style = context.development_style.value
        style_rules = self.recommendation_rules.get(style, {})

        # Must-have tools (high priority)
        for tool_name in style_rules.get("must_have", []):
            if tool_name not in context.existing_tools:
                recommendations.append(
                    Recommendation(
                        tool_name=tool_name,
                        confidence_score=0.95,
                        reason=f"Essential for {style} development",
                        priority=1,
                        alternatives=self.get_alternatives(tool_name),
                        category=self.get_tool_category(tool_name)
                    )
                )

        # Recommended tools (medium priority)
        for tool_name in style_rules.get("recommended", []):
            if tool_name not in context.existing_tools:
                recommendations.append(
                    Recommendation(
                        tool_name=tool_name,
                        confidence_score=0.8,
                        reason=f"Recommended for productivity in {style} development",
                        priority=2,
                        alternatives=self.get_alternatives(tool_name),
                        category=self.get_tool_category(tool_name)
                    )
                )

        # Optional tools (low priority)
        for tool_name in style_rules.get("optional", []):
            if tool_name not in context.existing_tools:
                recommendations.append(
                    Recommendation(
                        tool_name=tool_name,
                        confidence_score=0.6,
                        reason=f"Optional enhancement for {style} development",
                        priority=3,
                        alternatives=self.get_alternatives(tool_name),
                        category=self.get_tool_category(tool_name)
                    )
                )

        # Cloud-specific recommendations
        if context.cloud_provider != CloudProvider.NONE:
            cloud_tools = self.get_cloud_recommendations(context.cloud_provider)
            recommendations.extend(cloud_tools)

        # Project size adjustments
        if context.project_size == ProjectSize.LARGE:
            recommendations.extend(self.get_large_team_recommendations())

        # Sort by priority and confidence
        recommendations.sort(key=lambda x: (x.priority, -x.confidence_score))

        return recommendations

    def get_alternatives(self, tool_name: str) -> List[str]:
        """Get alternative tools"""
        alternatives = {
            "nodejs": ["deno", "bun"],
            "postgresql": ["mysql", "mongodb"],
            "docker": ["podman"],
            "git": ["mercurial"],
            "vscode": ["vim", "jetbrains"],
            "pytorch": ["tensorflow"],
        }
        return alternatives.get(tool_name, [])

    def get_tool_category(self, tool_name: str) -> str:
        """Get tool category"""
        categories = {
            "git": "productivity",
            "nodejs": "programming-language",
            "python3": "programming-language",
            "docker": "devops",
            "vscode": "editor",
            "postgresql": "database",
            "redis": "database",
            "mysql": "database",
            "mongodb": "database",
            "kubectl": "devops",
            "terraform": "devops",
            "helm": "devops",
            "eslint": "developer-tools",
            "prettier": "developer-tools",
            "typescript": "programming-language",
            "java": "programming-language",
            "pytorch": "ai-ml",
            "tensorflow": "ai-ml",
            "jupyter": "ai-ml",
            "pandas": "ai-ml",
        }
        return categories.get(tool_name, "utility")

    def get_cloud_recommendations(self, provider: CloudProvider) -> List[Recommendation]:
        """Get cloud-specific tool recommendations"""
        recommendations = []

        cloud_tools = {
            CloudProvider.AWS: ["aws-cli"],
            CloudProvider.GCP: ["gcloud-cli"],
            CloudProvider.AZURE: ["azure-cli"],
        }

        tools = cloud_tools.get(provider, [])
        for tool in tools:
            recommendations.append(
                Recommendation(
                    tool_name=tool,
                    confidence_score=0.9,
                    reason=f"Official CLI for {provider.value}",
                    priority=2,
                    alternatives=[],
                    category="devops"
                )
            )

        return recommendations

    def get_large_team_recommendations(self) -> List[Recommendation]:
        """Get recommendations for large teams"""
        return [
            Recommendation(
                tool_name="kubernetes",
                confidence_score=0.85,
                reason="Recommended for large teams for container orchestration",
                priority=2,
                alternatives=["docker-compose"],
                category="devops"
            )
        ]

    def find_best_environment_template(self, context: UserContext) -> Optional[str]:
        """Find the best environment template for the context"""
        template_mapping = {
            DevelopmentStyle.FULL_STACK: "web-developer",
            DevelopmentStyle.FRONTEND: "web-developer",
            DevelopmentStyle.BACKEND: "web-developer",
            DevelopmentStyle.AI_ML: "ai-ml-developer",
            DevelopmentStyle.DEVOPS: "devops-engineer",
            DevelopmentStyle.MOBILE: "mobile-developer",
        }
        return template_mapping.get(context.development_style)

    def generate_install_plan(self, context: UserContext) -> Dict[str, Any]:
        """Generate a complete installation plan"""
        recommendations = self.analyze_context(context)
        template = self.find_best_environment_template(context)

        # Group by installation priority
        plan = {
            "recommended_template": template,
            "phases": [
                {
                    "phase": 1,
                    "name": "Essential Tools",
                    "tools": [r for r in recommendations if r.priority == 1]
                },
                {
                    "phase": 2,
                    "name": "Recommended Tools",
                    "tools": [r for r in recommendations if r.priority == 2]
                },
                {
                    "phase": 3,
                    "name": "Optional Tools",
                    "tools": [r for r in recommendations if r.priority == 3]
                }
            ],
            "estimated_time": self.estimate_installation_time(recommendations),
            "context_used": {
                "style": context.development_style.value,
                "os": context.os,
                "project_size": context.project_size.value
            }
        }

        return plan

    def estimate_installation_time(self, recommendations: List[Recommendation]) -> str:
        """Estimate installation time based on recommendations"""
        essential_count = len([r for r in recommendations if r.priority == 1])
        recommended_count = len([r for r in recommendations if r.priority == 2])

        base_time = 5  # Base time in minutes
        per_tool = 5

        total_minutes = base_time + (essential_count * per_tool) + (recommended_count * per_tool * 0.5)

        if total_minutes < 15:
            return "5-15 minutes"
        elif total_minutes < 45:
            return "15-45 minutes"
        else:
            return "45-90 minutes"
