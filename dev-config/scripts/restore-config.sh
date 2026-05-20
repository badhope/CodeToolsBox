#!/bin/bash
# Dev-Config Restore Script

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$HOME/.global-dev-setup/backups"

print_help() {
    echo -e "${GREEN}Global-Dev-Setup - Configuration Restore${NC}"
    echo "Usage: $0 [options] [backup_file]"
    echo
    echo "Options:"
    echo "  -h, --help         Show this help message"
    echo "  -l, --list         List available backups"
    echo "  -f, --force        Force restore without confirmation"
}

list_backups() {
    echo -e "${GREEN}Available backups:${NC}"
    echo
    
    if [ -d "$BACKUP_DIR" ]; then
        local backups=($(ls -1 "${BACKUP_DIR}"/*.tar.gz 2>/dev/null | sort -r))
        if [ ${#backups[@]} -gt 0 ]; then
            for i in "${!backups[@]}"; do
                local backup="${backups[$i]}"
                local date=$(stat --format '%z' "$backup" 2>/dev/null || ls -lh "$backup" | awk '{print $6, $7, $8}')
                local size=$(du -h "$backup" | cut -f1)
                echo -e "${GREEN}$((i+1)).${NC} $(basename "$backup")"
                echo "   Size: $size | Date: $date"
                echo
            done
        else
            echo -e "${YELLOW}No backups found${NC}"
        fi
    else
        echo -e "${YELLOW}No backups directory found${NC}"
    fi
}

restore_config() {
    local backup_file=$1
    local force=$2
    
    if [ ! -f "$backup_file" ]; then
        echo -e "${RED}Error: Backup file not found: $backup_file${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Restoring from backup: $backup_file${NC}"
    
    # Confirm unless forced
    if [ "$force" != "true" ]; then
        read -p "Are you sure you want to restore? This will overwrite existing configs! (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Restore cancelled${NC}"
            exit 0
        fi
    fi
    
    # Backup existing files before restoring
    echo -e "${YELLOW}Creating pre-restore backup...${NC}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local pre_restore_backup="${BACKUP_DIR}/pre-restore-${timestamp}.tar.gz"
    
    # Build list of files that would be overwritten
    local restore_files=$(tar tzf "$backup_file" 2>/dev/null)
    local backup_cmd="tar czf \"$pre_restore_backup\""
    
    for file in $restore_files; do
        if [ -f "$HOME/$file" ]; then
            backup_cmd="$backup_cmd -C \"$HOME\" \"$file\""
        fi
    done
    
    eval "$backup_cmd" 2>/dev/null || true
    echo -e "${GREEN}Pre-restore backup saved to: $pre_restore_backup${NC}"
    
    # Now restore
    echo -e "${GREEN}Restoring configuration...${NC}"
    tar xzf "$backup_file" -C "$HOME"
    
    echo -e "${GREEN}Restore complete!${NC}"
    echo
    echo "Pre-restore backup is available at:"
    echo "  $pre_restore_backup"
}

main() {
    local list=false
    local force=false
    local backup_file=""
    
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            -h|--help)
                print_help
                exit 0
                ;;
            -l|--list)
                list_backups
                exit 0
                ;;
            -f|--force)
                force=true
                shift
                ;;
            *)
                if [ -z "$backup_file" ]; then
                    backup_file="$1"
                fi
                shift
                ;;
        esac
    done
    
    # List mode
    if [ "$list" = true ]; then
        list_backups
        exit 0
    fi
    
    # If no backup file specified, list backups and prompt
    if [ -z "$backup_file" ]; then
        list_backups
        echo -e "${YELLOW}Please select a backup or specify one as an argument${NC}"
        exit 1
    fi
    
    # If backup file doesn't exist, check if it's in the backup dir
    if [ ! -f "$backup_file" ]; then
        if [ -f "$BACKUP_DIR/$backup_file" ]; then
            backup_file="$BACKUP_DIR/$backup_file"
        elif [[ "$backup_file" != /* ]]; then
            echo -e "${RED}Error: Backup file not found${NC}"
            exit 1
        fi
    fi
    
    # Perform restore
    restore_config "$backup_file" "$force"
}

main "$@"
