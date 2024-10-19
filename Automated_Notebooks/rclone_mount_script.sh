# Sample script for using rclone to mount Google Drive file to local computer
# (You'll need to update this code to match your own local and Drive-based
# file directory names.)
# Including --vfs-cache-mode full should improve rclone's performance.

rclone mount kjb3server: ~/kjb3server_drive --vfs-cache-mode full