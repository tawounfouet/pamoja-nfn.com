#!/bin/bash

# Create backup directory with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="backups"
#BACKUP_DIR="backups_$TIMESTAMP"
BACKUP_DIR="$BASE_DIR/$TIMESTAMP"
mkdir -p $BACKUP_DIR

# List of apps to backup
APPS=(
    "authentication"
    "location"
    "messaging"
    "favorites"
    "listing"
    #"search"
    "theme"
    "pages"
    "users"
)

# Backup each app
for APP in "${APPS[@]}"
do
    echo "Backing up $APP..."
    python manage.py dumpdata $APP --indent 2 > "$BACKUP_DIR/${APP}_$TIMESTAMP.json"
done

# Backup third party apps
python manage.py dumpdata taggit --indent 2 > "$BACKUP_DIR/taggit_$TIMESTAMP.json"
python manage.py dumpdata phonenumber_field --indent 2 > "$BACKUP_DIR/phonenumber_field_$TIMESTAMP.json"
python manage.py dumpdata django_countries --indent 2 > "$BACKUP_DIR/django_countries_$TIMESTAMP.json"

# Compress the backup directory
tar -czf "${BACKUP_DIR}.tar.gz" $BACKUP_DIR

echo "Backup completed! Files are stored in ${BACKUP_DIR}.tar.gz"