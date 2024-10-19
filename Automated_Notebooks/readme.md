# Automating Notebooks

This section will demonstrate how to automatically run a Jupyter Notebook, then share that notebook online (via Google Drive) so that others can easily access a recently-updated version of it.

## Prerequisites for replicating this process on your own computer:

1. Create a local copy of a Google Drive folder on your computer. This folder should automatically sync with its cloud-based equivalent.

(Google Drive is one of many online storage options, but I prefer it for this task because it easily allows notebooks to be opened within Colaboratory, thus allowing their output to be viewed online.)

This is relatively easy to do on Windows and Mac, as you can install and use Google Drive for desktop (https://support.google.com/drive/answer/10838124?hl=en). For Linux, which doesn't have an official Google Drive desktop application, I recommend using rclone (https://rclone.org/); this utility allows you to mount your Google Drive to your computer.

Note: in order to speed up rclone's performance, I recommend adding `--vfs-cache-mode full` to your rclone mount command. (See https://rclone.org/commands/rclone_mount/#vfs-cache-mode-full for more information.) The following terminal entry provides an example; you'll of course need to change the rclone drive name (kjb3server) and local folder name (kjb3server_drive) to match your own drive and folder names, respectively.

`rclone mount kjb3server: ~/kjb3server_drive --vfs-cache-mode full`

2. Install papermill (https://papermill.readthedocs.io/en/latest/) within your Python environment.

3. Create a shell or batch script that can call papermill in order to run recent_weather_data.ipynb, then copy the executed version of this notebook into a Google Drive folder of your choice. autorun_shell_script.sh provides an example of this workflow within Linux, but you'll need to update it to match your own local and Drive-based file directories. (If you're on Windows, you'll need to create a batch script instead.)

4. Have your computer run your shell/batch script on an hourly basis, as the NWS data source that recent_weather_data.ipynb accesses gets updated on an hourly basis. This can be accomplished in Linux by creating a new crontab entry and in Windows via Task Scheduler.

