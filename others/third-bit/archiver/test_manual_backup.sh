BACKUPS=/tmp/backups
rm -rf $BACKUPS
python backup.py data $BACKUPS
tree --charset ascii $BACKUPS

