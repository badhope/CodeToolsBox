#!/bin/bash
# Global-Dev-Setup - One-Click Installer (Linux/macOS)
# Quick and easy setup for development environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logo and welcome
print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║        Global-Dev-Setup - One-Click Installer              ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
    echo -e "Detected: ${GREEN}$OS${NC}"
}

# Ask user which profile they want
select_profile() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "              Select your development profile"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "=== Web Development ==="
    echo "  1) Full-Stack Web Developer"
    echo "  2) Frontend Developer"
    echo "  3) Backend Developer"
    echo ""
    echo "=== AI & Machine Learning ==="
    echo "  4) AI/ML Developer"
    echo "  5) AI Agent Developer"
    echo "  6) ML Engineer"
    echo "  7) Data Scientist"
    echo ""
    echo "=== Big Data & Data Engineering ==="
    echo "  8) Big Data Engineer"
    echo "  9) Data Engineer"
    echo ""
    echo "=== DevOps & Cloud ==="
    echo " 10) DevOps Engineer"
    echo " 11) Cloud Native Developer"
    echo " 12) System Administrator"
    echo ""
    echo "=== Mobile & Game ==="
    echo " 13) Mobile App Developer"
    echo " 14) Game Developer"
    echo ""
    echo "=== Specialized ==="
    echo " 15) Blockchain Developer"
    echo " 16) IoT Developer"
    echo " 17) Embedded Developer"
    echo " 18) Security Engineer"
    echo " 19) QA/Testing Engineer"
    echo ""
    echo "=== Language-Specific ==="
    echo " 20) Python Developer"
    echo " 21) Java Developer"
    echo " 22) Go Developer"
    echo " 23) Rust Developer"
    echo ""
    read -p "Enter your choice (1-23): " choice

    case $choice in
        1) PROFILE="full-stack" ;;
        2) PROFILE="frontend" ;;
        3) PROFILE="backend" ;;
        4) PROFILE="ai-ml" ;;
        5) PROFILE="ai-agent" ;;
        6) PROFILE="ml-engineer" ;;
        7) PROFILE="data-science" ;;
        8) PROFILE="big-data" ;;
        9) PROFILE="data-engineering" ;;
        10) PROFILE="devops" ;;
        11) PROFILE="cloud-native" ;;
        12) PROFILE="sysadmin" ;;
        13) PROFILE="mobile" ;;
        14) PROFILE="game-dev" ;;
        15) PROFILE="blockchain" ;;
        16) PROFILE="iot" ;;
        17) PROFILE="embedded" ;;
        18) PROFILE="security" ;;
        19) PROFILE="qa" ;;
        20) PROFILE="python" ;;
        21) PROFILE="java" ;;
        22) PROFILE="go" ;;
        23) PROFILE="rust" ;;
        *) PROFILE="full-stack" ;;
    esac

    echo -e "${GREEN}Selected profile: $PROFILE${NC}"
}

# Install dependencies
install_base_deps() {
    echo ""
    echo -e "${BLUE}Installing base dependencies...${NC}"

    if [ "$OS" == "linux" ]; then
        if [ "$DISTRO" == "ubuntu" ] || [ "$DISTRO" == "debian" ]; then
            sudo apt-get update
            sudo apt-get install -y git curl wget build-essential
        elif [ "$DISTRO" == "fedora" ]; then
            sudo dnf install -y git curl wget gcc-c++ make
        elif [ "$DISTRO" == "arch" ]; then
            sudo pacman -Syu --noconfirm git curl wget base-devel
        fi
    elif [ "$OS" == "macos" ]; then
        if ! command -v brew &>/dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install git curl wget
    fi
}

# Run the Python bootstrapper
run_bootstrap() {
    echo ""
    echo -e "${BLUE}Starting intelligent setup...${NC}"

    # Check if Python is available
    if command -v python3 &>/dev/null; then
        python3 bootstrap.py "$PROFILE"
    else
        echo "Python3 not found, trying to install..."
        install_base_deps
        python3 bootstrap.py "$PROFILE"
    fi
}

# Main
main() {
    print_banner
    detect_os
    select_profile
    install_base_deps
    run_bootstrap

    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Setup complete!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Restart your terminal or source your shell config"
    echo "  2. Check installed tools with: python3 global-dev-setup.py status"
    echo "  3. For help: python3 global-dev-setup.py --help"
    echo ""
}

# Run main
main "$@"
