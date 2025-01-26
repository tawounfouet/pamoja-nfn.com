#!/bin/bash

# Setup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# List of apps to backup
APPS=(
    "authentication"
    "location"
    "messaging"
    "favorites"
    "listing"
    "theme"
    "pages"
    "users"
)

# Backup each app with error checking
for APP in "${APPS[@]}"
do
    echo "Backing up $APP..."
    OUTPUT_FILE="$BACKUP_DIR/${APP}.json"
    
    if python manage.py dumpdata $APP --indent 2 > "$OUTPUT_FILE"; then
        # Check if file is empty or contains only whitespace
        if [ -s "$OUTPUT_FILE" ] && grep -q '[^[:space:]]' "$OUTPUT_FILE"; then
            echo "✓ Successfully backed up $APP"
        else
            echo "⚠️  Warning: Backup file for $APP is empty"
            rm "$OUTPUT_FILE"
        fi
    else
        echo "❌ Failed to backup $APP"
        rm -f "$OUTPUT_FILE"
    fi
done

# Backup third party apps
for APP in "taggit" "phonenumber_field" "django_countries"; do
    echo "Backing up $APP..."
    python manage.py dumpdata $APP --indent 2 > "$BACKUP_DIR/${APP}.json" 2>/dev/null || echo "⚠️  Failed to backup $APP"
done

echo "Backup completed! Files are stored in $BACKUP_DIR/"

# To restore, run:
echo "To restore, run: python manage.py loaddata $BACKUP_DIR/[app_name].json"