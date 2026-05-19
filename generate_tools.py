#!/usr/bin/env python3
# 批量生成工具定义文件

import os

# 定义所有工具及其配置
TOOLS_CONFIG = {
    # 编程语言
    "perl": {
        "category": "programming-language",
        "description": "Perl - 强大的文本处理语言",
        "homepage": "https://www.perl.org/",
        "tags": ["perl", "text-processing", "scripting", "cgi"]
    },
    "lua": {
        "category": "programming-language",
        "description": "Lua - 轻量级脚本语言",
        "homepage": "https://www.lua.org/",
        "tags": ["lua", "scripting", "embedded", "game"]
    },
    "haskell": {
        "category": "programming-language",
        "description": "Haskell - 纯函数式编程语言",
        "homepage": "https://www.haskell.org/",
        "tags": ["haskell", "functional", "lazy", "types"]
    },
    "elixir": {
        "category": "programming-language",
        "description": "Elixir - 函数式、并发编程语言",
        "homepage": "https://elixir-lang.org/",
        "tags": ["elixir", "erlang", "functional", "concurrency", "phoenix"]
    },
    "erlang": {
        "category": "programming-language",
        "description": "Erlang - 并发编程语言和运行时",
        "homepage": "https://www.erlang.org/",
        "tags": ["erlang", "concurrency", "distributed", "telecom"]
    },
    "clojure": {
        "category": "programming-language",
        "description": "Clojure - JVM上的Lisp方言",
        "homepage": "https://clojure.org/",
        "tags": ["clojure", "lisp", "jvm", "functional", "concurrent"]
    },
    "fsharp": {
        "category": "programming-language",
        "description": "F# - .NET平台函数式编程语言",
        "homepage": "https://fsharp.org/",
        "tags": ["fsharp", "dotnet", "functional", "ocaml"]
    },
    "ocaml": {
        "category": "programming-language",
        "description": "OCaml - 实用的函数式语言",
        "homepage": "https://ocaml.org/",
        "tags": ["ocaml", "functional", "compilers", "static-typing"]
    },
    "groovy": {
        "category": "programming-language",
        "description": "Groovy - JVM脚本语言",
        "homepage": "https://groovy-lang.org/",
        "tags": ["groovy", "jvm", "scripting", "gradle"]
    },
    "zig": {
        "category": "programming-language",
        "description": "Zig - 低级编程语言",
        "homepage": "https://ziglang.org/",
        "tags": ["zig", "systems", "low-level", "performance"]
    },
    "nim": {
        "category": "programming-language",
        "description": "Nim - 高效简洁的编译型语言",
        "homepage": "https://nim-lang.org/",
        "tags": ["nim", "metaprogramming", "high-performance", " compiles-to-c"]
    },
    # Web框架
    "svelte": {
        "category": "web-framework",
        "description": "Svelte - 编译型UI框架",
        "homepage": "https://svelte.dev/",
        "tags": ["svelte", "frontend", "compile-time", "reactive"]
    },
    "nuxt": {
        "category": "web-framework",
        "description": "Nuxt - Vue全栈框架",
        "homepage": "https://nuxt.com/",
        "tags": ["nuxt", "vue", "ssr", "fullstack", "static"]
    },
    "astro": {
        "category": "web-framework",
        "description": "Astro - 内容驱动静态网站框架",
        "homepage": "https://astro.build/",
        "tags": ["astro", "static", "islands", "performance"]
    },
    "solidjs": {
        "category": "web-framework",
        "description": "SolidJS - 声明式响应式UI库",
        "homepage": "https://www.solidjs.com/",
        "tags": ["solidjs", "reactive", "frontend", "performance"]
    },
    "express": {
        "category": "web-framework",
        "description": "Express - Node.js Web框架",
        "homepage": "https://expressjs.com/",
        "tags": ["express", "nodejs", "backend", "api", "rest"]
    },
    "fastify": {
        "category": "web-framework",
        "description": "Fastify - 高性能Node.js框架",
        "homepage": "https://www.fastify.io/",
        "tags": ["fastify", "nodejs", "high-performance", "backend"]
    },
    "nestjs": {
        "category": "web-framework",
        "description": "NestJS - Node.js渐进式框架",
        "homepage": "https://nestjs.com/",
        "tags": ["nestjs", "nodejs", "typescript", "backend", "angular-like"]
    },
    "koa": {
        "category": "web-framework",
        "description": "Koa - Node.js下一代Web框架",
        "homepage": "https://koajs.com/",
        "tags": ["koa", "nodejs", "middleware", "backend"]
    },
    "graphql": {
        "category": "web-framework",
        "description": "GraphQL - API查询语言",
        "homepage": "https://graphql.org/",
        "tags": ["graphql", "api", "query", "types", "schema"]
    },
    "strapi": {
        "category": "web-framework",
        "description": "Strapi - 开源Headless CMS",
        "homepage": "https://strapi.io/",
        "tags": ["strapi", "cms", "headless", "api", "backend"]
    },
    "remix": {
        "category": "web-framework",
        "description": "Remix - 全栈Web框架",
        "homepage": "https://remix.run/",
        "tags": ["remix", "react", "fullstack", "ssr"]
    },
    # 数据库
    "mariadb": {
        "category": "database",
        "description": "MariaDB - MySQL兼容数据库",
        "homepage": "https://mariadb.org/",
        "tags": ["mariadb", "mysql", "database", "sql", "galera"]
    },
    "cassandra": {
        "category": "database",
        "description": "Apache Cassandra - NoSQL分布式数据库",
        "homepage": "https://cassandra.apache.org/",
        "tags": ["cassandra", "nosql", "distributed", "scalable", "wide-column"]
    },
    "neo4j": {
        "category": "database",
        "description": "Neo4j - 图数据库",
        "homepage": "https://neo4j.com/",
        "tags": ["neo4j", "graph", "nosql", "cypher", "relationships"]
    },
    "influxdb": {
        "category": "database",
        "description": "InfluxDB - 时序数据库",
        "homepage": "https://www.influxdata.com/",
        "tags": ["influxdb", "time-series", "iot", "metrics", "monitoring"]
    },
    "clickhouse": {
        "category": "database",
        "description": "ClickHouse - 列式数据库",
        "homepage": "https://clickhouse.com/",
        "tags": ["clickhouse", "olap", "columnar", "analytics", "big-data"]
    },
    "tidb": {
        "category": "database",
        "description": "TiDB - 分布式SQL数据库",
        "homepage": "https://pingcap.com/",
        "tags": ["tidb", "distributed", "mysql-compatible", "htap", "scalable"]
    },
    "oceanbase": {
        "category": "database",
        "description": "OceanBase - 分布式关系数据库",
        "homepage": "https://www.oceanbase.com/",
        "tags": ["oceanbase", "distributed", "sql", "high-availability", "alibaba"]
    },
    "supabase": {
        "category": "database",
        "description": "Supabase - 开源Firebase替代",
        "homepage": "https://supabase.com/",
        "tags": ["supabase", "firebase", "postgres", "realtime", "auth"]
    },
    "duckdb": {
        "category": "database",
        "description": "DuckDB - 嵌入式分析数据库",
        "homepage": "https://duckdb.org/",
        "tags": ["duckdb", "embedded", "olap", "analytics", "sqlite-like"]
    },
    # DevOps工具
    "jenkins": {
        "category": "devops",
        "description": "Jenkins - 自动化服务器",
        "homepage": "https://www.jenkins.io/",
        "tags": ["jenkins", "ci-cd", "automation", "pipeline", "java"]
    },
    "gitlab": {
        "category": "devops",
        "description": "GitLab - DevOps平台",
        "homepage": "https://about.gitlab.com/",
        "tags": ["gitlab", "ci-cd", "devops", "git", "repository"]
    },
    "argocd": {
        "category": "devops",
        "description": "ArgoCD - GitOps持续交付",
        "homepage": "https://argoproj.github.io/cd/",
        "tags": ["argocd", "gitops", "kubernetes", "cd", "declarative"]
    },
    "prometheus": {
        "category": "devops",
        "description": "Prometheus - 监控系统",
        "homepage": "https://prometheus.io/",
        "tags": ["prometheus", "monitoring", "metrics", "alerting", "time-series"]
    },
    "grafana": {
        "category": "devops",
        "description": "Grafana - 可视化监控平台",
        "homepage": "https://grafana.com/",
        "tags": ["grafana", "dashboard", "monitoring", "visualization", "metrics"]
    },
    "loki": {
        "category": "devops",
        "description": "Loki - 日志聚合系统",
        "homepage": "https://grafana.com/oss/loki/",
        "tags": ["loki", "logging", "grafana", "prometheus-like", "kubernetes"]
    },
    "elk": {
        "category": "devops",
        "description": "ELK Stack - 日志分析套件",
        "homepage": "https://www.elastic.co/what-is/elk-stack",
        "tags": ["elk", "elasticsearch", "logstash", "kibana", "logging"]
    },
    # 安全工具
    "sonarqube": {
        "category": "security",
        "description": "SonarQube - 代码质量管理",
        "homepage": "https://www.sonarqube.org/",
        "tags": ["sonarqube", "code-quality", "static-analysis", "security", "clean-code"]
    },
    "trivy": {
        "category": "security",
        "description": "Trivy - 容器安全扫描",
        "homepage": "https://trivy.dev/",
        "tags": ["trivy", "security", "vulnerability", "container", "scanning"]
    },
    "vault": {
        "category": "security",
        "description": "HashiCorp Vault - 密钥管理",
        "homepage": "https://www.vaultproject.io/",
        "tags": ["vault", "secrets", "encryption", "iam", "security"]
    },
    "keycloak": {
        "category": "security",
        "description": "Keycloak - 身份和访问管理",
        "homepage": "https://www.keycloak.org/",
        "tags": ["keycloak", "iam", "sso", "oauth", "openid"]
    },
    "owasp-zap": {
        "category": "security",
        "description": "OWASP ZAP - Web应用安全扫描",
        "homepage": "https://www.zaproxy.org/",
        "tags": ["owasp", "zap", "security", "pentest", "vulnerability"]
    },
    # 监控工具
    "sentry": {
        "category": "monitoring",
        "description": "Sentry - 应用错误追踪",
        "homepage": "https://sentry.io/",
        "tags": ["sentry", "error-tracking", "monitoring", "debugging", "crash-reporting"]
    },
    "jaeger": {
        "category": "monitoring",
        "description": "Jaeger - 分布式追踪",
        "homepage": "https://www.jaegertracing.io/",
        "tags": ["jaeger", "tracing", "distributed", "observability", "opentracing"]
    },
    "opentelemetry": {
        "category": "monitoring",
        "description": "OpenTelemetry - 可观测性框架",
        "homepage": "https://opentelemetry.io/",
        "tags": ["opentelemetry", "telemetry", "metrics", "traces", "logs"]
    },
    # 网络工具
    "nginx": {
        "category": "networking",
        "description": "Nginx - Web服务器和反向代理",
        "homepage": "https://nginx.org/",
        "tags": ["nginx", "web-server", "reverse-proxy", "load-balancer", "http"]
    },
    "traefik": {
        "category": "networking",
        "description": "Traefik - 云原生反向代理",
        "homepage": "https://traefik.io/",
        "tags": ["traefik", "reverse-proxy", "kubernetes", "docker", "cloud-native"]
    },
    "kong": {
        "category": "networking",
        "description": "Kong - API网关",
        "homepage": "https://konghq.com/",
        "tags": ["kong", "api-gateway", "microservices", "plugins", "lua"]
    },
    "v2ray": {
        "category": "networking",
        "description": "V2Ray - 代理工具",
        "homepage": "https://www.v2fly.org/",
        "tags": ["v2ray", "proxy", "vpn", "shadowsocks", "trojan"]
    },
    "clash": {
        "category": "networking",
        "description": "Clash - 网络代理工具",
        "homepage": "https://github.com/Dreamacro/clash",
        "tags": ["clash", "proxy", "vpn", "rules", "tunnel"]
    },
    # 测试工具
    "cypress": {
        "category": "testing",
        "description": "Cypress - 前端E2E测试",
        "homepage": "https://www.cypress.io/",
        "tags": ["cypress", "e2e", "testing", "frontend", "javascript"]
    },
    "playwright": {
        "category": "testing",
        "description": "Playwright - 跨浏览器测试",
        "homepage": "https://playwright.dev/",
        "tags": ["playwright", "testing", "browser", "automation", "microsoft"]
    },
    "selenium": {
        "category": "testing",
        "description": "Selenium - Web自动化测试",
        "homepage": "https://www.selenium.dev/",
        "tags": ["selenium", "automation", "testing", "webdriver", "browser"]
    },
    "k6": {
        "category": "testing",
        "description": "k6 - 负载测试工具",
        "homepage": "https://k6.io/",
        "tags": ["k6", "load-testing", "performance", "grafana", "synthetic"]
    },
    "locust": {
        "category": "testing",
        "description": "Locust - Python负载测试",
        "homepage": "https://locust.io/",
        "tags": ["locust", "load-testing", "python", "distributed", "performance"]
    },
    # API工具
    "postman": {
        "category": "api",
        "description": "Postman - API开发协作平台",
        "homepage": "https://www.postman.com/",
        "tags": ["postman", "api", "rest", "graphql", "testing"]
    },
    "insomnia": {
        "category": "api",
        "description": "Insomnia - API客户端",
        "homepage": "https://insomnia.rest/",
        "tags": ["insomnia", "api", "rest", "graphql", "grpc"]
    },
    "swagger": {
        "category": "api",
        "description": "Swagger/OpenAPI - API文档工具",
        "homepage": "https://swagger.io/",
        "tags": ["swagger", "openapi", "api", "documentation", "rest"]
    },
    # 版本控制
    "github-cli": {
        "category": "version-control",
        "description": "GitHub CLI",
        "homepage": "https://cli.github.com/",
        "tags": ["github", "cli", "git", "automation", "pull-request"]
    },
    # 包管理器
    "conda": {
        "category": "package-manager",
        "description": "Conda - 环境管理器和包管理器",
        "homepage": "https://docs.conda.io/",
        "tags": ["conda", "python", "environment", "package-manager", "data-science"]
    },
    "poetry": {
        "category": "package-manager",
        "description": "Poetry - Python依赖管理",
        "homepage": "https://python-poetry.org/",
        "tags": ["poetry", "python", "dependencies", "packaging", "pyproject"]
    },
    "pnpm": {
        "category": "package-manager",
        "description": "pnpm - 高效Node包管理器",
        "homepage": "https://pnpm.io/",
        "tags": ["pnpm", "npm", "nodejs", "package-manager", "fast"]
    },
    "cargo": {
        "category": "package-manager",
        "description": "Cargo - Rust包管理器和构建工具",
        "homepage": "https://doc.rust-lang.org/cargo/",
        "tags": ["cargo", "rust", "package-manager", "build", "dependencies"]
    },
    # IDE
    "intellij": {
        "category": "ide",
        "description": "IntelliJ IDEA - Java/Kotlin IDE",
        "homepage": "https://www.jetbrains.com/idea/",
        "tags": ["intellij", "jetbrains", "java", "kotlin", "ide"]
    },
    "pycharm": {
        "category": "ide",
        "description": "PyCharm - Python IDE",
        "homepage": "https://www.jetbrains.com/pycharm/",
        "tags": ["pycharm", "jetbrains", "python", "ide", "data-science"]
    },
    "goland": {
        "category": "ide",
        "description": "GoLand - Go IDE",
        "homepage": "https://www.jetbrains.com/go/",
        "tags": ["goland", "jetbrains", "go", "ide"]
    },
    "datagrip": {
        "category": "ide",
        "description": "DataGrip - 数据库IDE",
        "homepage": "https://www.jetbrains.com/datagrip/",
        "tags": ["datagrip", "jetbrains", "database", "sql", "ide"]
    },
    # 云服务
    "vercel": {
        "category": "cloud-service",
        "description": "Vercel - 前端云平台",
        "homepage": "https://vercel.com/",
        "tags": ["vercel", "hosting", "serverless", "frontend", "nextjs"]
    },
    "netlify": {
        "category": "cloud-service",
        "description": "Netlify - 现代Web发布平台",
        "homepage": "https://www.netlify.com/",
        "tags": ["netlify", "hosting", "jamstack", "static", "cdn"]
    },
    "digitalocean": {
        "category": "cloud-service",
        "description": "DigitalOcean - 云服务器",
        "homepage": "https://www.digitalocean.com/",
        "tags": ["digitalocean", "vps", "cloud", "droplets", "hosting"]
    },
}

def generate_tool_yaml(tool_name, config):
    """生成工具定义YAML内容"""
    category = config["category"]
    
    # 确定路径
    if "/" in category:
        path = f"tools/{category}/{tool_name}/tool.yaml"
    else:
        path = f"tools/{category}/{tool_name}/tool.yaml"
    
    yaml_content = f"""# {tool_name.title()} - {config['description']}
name: {tool_name}
category: {category}
description: "{config['description']}"
homepage: "{config['homepage']}"

tags:
{chr(10).join([f'  - {tag}' for tag in config['tags']])}

supported_os:
  - linux
  - macos
  - windows

installation_sources:
  - type: official
    os: [all]
    description: "Official installation"
    priority: 1
    command: |
      # See {config['homepage']} for installation instructions

verify_commands:
  - "{tool_name} --version"

compatible_with: []
"""
    
    return path, yaml_content

def main():
    """主函数"""
    base_path = "/workspace/Global-Dev-Setup"
    count = 0
    
    for tool_name, config in TOOLS_CONFIG.items():
        try:
            path, content = generate_tool_yaml(tool_name, config)
            full_path = os.path.join(base_path, path)
            
            # 创建目录
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # 写入文件
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            count += 1
            print(f"Created: {path}")
            
        except Exception as e:
            print(f"Error creating {tool_name}: {e}")
    
    print(f"\nTotal tools created: {count}")

if __name__ == "__main__":
    main()
