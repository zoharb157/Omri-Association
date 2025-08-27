#!/bin/bash

# Omri Dashboard Backup Script

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup in $BACKUP_DIR"

# Backup configuration files
cp -r *.py "$BACKUP_DIR/"
cp -r ui/ "$BACKUP_DIR/"
cp -r modules/ "$BACKUP_DIR/"
cp -r reports/ "$BACK_DIR/"
cp *.md "$BACKUP_DIR/"
cp *.sh "$BACKUP_DIR/"
cp *.yml "$BACKUP_DIR/"
cp *.service "$BACKUP_DIR/"
cp requirements*.txt "$BACKUP_DIR/"

# Backup data (if exists)
if [ -d "data" ]; then
    cp -r data/ "$BACKUP_DIR/"
fi

# Create backup info
cat > "$BACKUP_DIR/backup_info.txt" << BACKUP_INFO
Backup created: $(date)
Dashboard version: $(git describe --tags 2>/dev/null || echo "Unknown")
Python version: $(python3 --version)
System: $(uname -a)
BACKUP_INFO

echo "✅ Backup completed: $BACKUP_DIR"
echo "📁 Backup size: $(du -sh "$BACKUP_DIR" | cut -f1)"
