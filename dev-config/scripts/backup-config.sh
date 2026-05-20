#!/bin/bash
# Dev-Config Backup Script

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$HOME/.global-dev-setup/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/global-dev-setup-backup-${TIMESTAMP}.tar.gz"

print_help() {
    echo -e "${GREEN}Global-Dev-Setup - Configuration Backup${NC}"
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -h, --help         Show this help message"
    echo "  -o, --output <file>  Specify output file"
    echo "  -c, --clean        Clean old backups (keep last 5)"
}

backup_config() {
    local output_file=$1
    
    echo -e "${GREEN}Creating backup...${NC}"
    mkdir -p "$BACKUP_DIR"
    
    # Common config files to backup
    local backup_list=(
        "$HOME/.bashrc"
        "$HOME/.zshrc"
        "$HOME/.gitconfig"
        "$HOME/.gitignore_global"
        "$HOME/.npmrc"
        "$HOME/.yarnrc"
        "$HOME/.pip/pip.conf"
        "$HOME/.cargo/config"
        "$HOME/.config/Code/User/settings.json"
        "$HOME/.config/Code/User/keybindings.json"
    )
    
    # Build the tar command
    local tar_cmd="tar czf \"$output_file\""
    
    for file in "${backup_list[@]}"; do
        if [ -f "$file" ]; then
            tar_cmd="$tar_cmd -C \"$(dirname "$file")\" \"$(basename "$file")\""
        fi
    done
    
    # Execute backup
    eval "$tar_cmd" 2>/dev/null || true
    
    if [ -f "$output_file" ]; then
        echo -e "${GREEN}Backup created successfully: $output_file${NC}"
        local size=$(du -h "$output_file" | cut -f1)
        echo "Size: $size"
    else
        echo -e "${YELLOW}Warning: No files to backup${NC}"
    fi
}

clean_old_backups() {
    echo -e "${YELLOW}Cleaning old backups...${NC}"
    
    # Keep last 5 backups
    local num_keep=5
    local num_backups=$(ls -1 "${BACKUP_DIR}"/*.tar.gz 2>/dev/null | wc -l)
    
    if [ "$num_backups" -gt "$num_keep" ]; then
        local num_remove=$((num_backups - num_keep))
        echo "Keeping last $num_keep, removing $num_remove old backups"
        
        ls -1 "${BACKUP_DIR}"/*.tar.gz | sort | head -$num_remove | xargs -I {} rm -f {}
        
        echo -e "${GREEN}Old backups cleaned${NC}"
    else
        echo "No old backups to clean (only $num_backups)"
    fi
}

main() {
    local output_file="$BACKUP_FILE"
    local clean=false
    
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            -h|--help)
                print_help
                exit 0
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            -c|--clean)
                clean=true
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    # Ensure directory is there
    mkdir -p "$BACKUP_DIR"
    
    # Perform backup
    backup_config "$output_file"
    
    # Clean old backups if requested
    if [ "$clean" = true ]; then
        clean_old_backups
    fi
}

main "$@"
