# Global-Dev-Setup - Tool Compatibility Matrix

## Compatibility Matrix

This matrix shows which tools work well together and known conflicts.

### Core Tools

| Tool | Linux | macOS | Windows | Notes |
|------|-------|-------|---------|-------|
| git | ✓ | ✓ | ✓ | Universal |
| curl | ✓ | ✓ | ✓ | Universal |
| python3 | ✓ | ✓ | ✓ | Universal |
| nodejs | ✓ | ✓ | ✓ | Universal |

### Databases

| Database | Linux | macOS | Windows | Docker |
|----------|-------|-------|---------|--------|
| postgresql | ✓ | ✓ | ✓ | ✓ |
| mysql | ✓ | ✓ | ✓ | ✓ |
| mongodb | ✓ | ✓ | ✓ | ✓ |
| redis | ✓ | ✓ | ✓ | ✓ |

### DevOps Tools

| Tool | Linux | macOS | Windows |
|------|-------|-------|---------|
| docker | ✓ | ✓ | ✓ |
| kubectl | ✓ | ✓ | ✓ |
| helm | ✓ | ✓ | ✓ |
| terraform | ✓ | ✓ | ✓ |

### Editors & IDEs

| Editor | Linux | macOS | Windows |
|--------|-------|-------|---------|
| vscode | ✓ | ✓ | ✓ |
| vim | ✓ | ✓ | ✓ |
| jetbrains | ✓ | ✓ | ✓ |

## Known Good Combinations

### Web Development Stack
```
✓ git + nodejs + python3 + docker + postgresql + redis + vscode
Works perfectly for full-stack development
```

### AI/ML Stack
```
✓ git + python3 + docker + vscode + jupyter + pytorch
Excellent for machine learning development
```

### DevOps Stack
```
✓ git + docker + kubectl + helm + terraform + vscode
Great for cloud native and DevOps work
```

### Mobile Stack
```
✓ git + nodejs + java + android-sdk + react-native + vscode
Good for cross-platform mobile development
```

## Known Conflicts

### Package Managers
| Tool 1 | Tool 2 | Issue | Resolution |
|--------|--------|-------|------------|
| conda | pipenv | Env var conflicts | Use one or the other |
| nvm | system node | PATH order | NVM is usually better |
| brew | apt | On Linux - duplicate packages | Prefer system packages first |

### Databases
| Database 1 | Database 2 | Issue | Resolution |
|------------|------------|-------|------------|
| postgresql | mysql | Port conflicts (both 3306/5432) | Use Docker with different ports |
| mongodb | couchdb | Port 5984 conflict | Use Docker or change ports |

### Memory Considerations

Some tools require significant memory:

| Tool | Min RAM | Recommended |
|------|---------|-------------|
| Docker + Kubernetes | 8GB | 16GB |
| PostgreSQL + Redis | 4GB | 8GB |
| AI/ML tools (PyTorch etc) | 16GB | 32GB |
| Android Studio + Emulator | 16GB | 32GB |

## Version Compatibility

### Node.js
- Node 18, 20 (LTS recommended)
- Compatible with npm 9+, yarn 1.22+, pnpm 8+

### Python
- Python 3.9 - 3.12 (3.11 recommended)
- pip 22+, setuptools 65+

### Docker
- Docker Engine 20.10+
- Docker Compose 2.0+
- Kubernetes 1.25+ for k8s integration

## Quick Reference

### Can I run X and Y together?
Check the tables above, but as a general rule:
- All core tools are compatible with each other
- Different databases need different ports
- Multiple package managers can conflict

### What if something doesn't work?
1. Check the tool's specific documentation
2. Look in the `docs/` directory
3. Check GitHub issues
4. Use Docker for isolation
