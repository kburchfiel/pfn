# Sharing Automatically-Updated Notebooks

(Note: to view the final product of the steps shown in part 1, enable Colaboratory within your Google Drive account (if it's not already active), then visit https://colab.research.google.com/drive/1AmcSXI5ykszbQryyQmGkDhTg_PTG3m4A . This page shows an online copy of recent_weather_data.ipynb that used to get updated on an hourly basis. The following steps explain how I got this notebook to refresh automatically.)

Let's say that you have a Jupyter Notebook that you wish to update automatically on a regular basis as new data becomes available. Let's also say that you want to automate the process of sharing these notebooks online so that others can view them also. This notebook demonstrates a few options for doing so.

**Note:** In many cases, an online Dash app (covered within the Online Visualizations section of Python for Nonprofits) will be a better alternative to this workflow. This is because these options, though they do technically work, have some important limitations.


## Instructions

### Part 1: Sharing updated notebooks via Google Drive

You can use Google Drive, a Python library called Papermill, and (if necessary) a tool called RClone to automatically run notebooks, then share that notebook online. This method has a number of advantages:

1. The updated notebooks can be viewed soon after they finish executing on your computer.

2. You don't need to make the automated notebook public (though you can still share it with the whole world if you so choose).

However, there is a significant disadvantage as well: HTML-based Plotly charts, and presumably other HTML items as well, won't show up within these notebooks by default. Therefore, if you would like to display Plotly charts within these notebooks, you'll need to export them as image files and then load those images back into your notebook. (You can also display them by running the notebook on Colab, but this approach may not work for you if your script loads data from your computer.)

Here are the steps for sharing notebooks via Google Drive:

1. Create a local version of your Google Drive on your computer. Google Drive is one of many online storage options, but I prefer it for this task because it easily allows notebooks to be opened within Colaboratory, thus allowing their output to be viewed online.)

This is relatively easy to do on Windows and Mac, as you can install and use Google Drive for Desktop (https://support.google.com/drive/answer/10838124?hl=en). For Linux, which doesn't have an official Google Drive desktop application, I recommend using rclone (https://rclone.org/); this utility allows you to mount your Google Drive to your computer.

Note: in order to speed up rclone's performance, I recommend adding `--vfs-cache-mode full` to your rclone mount command. (See https://rclone.org/commands/rclone_mount/#vfs-cache-mode-full for more information.) The following terminal entry provides an example; you'll of course need to change the rclone drive name (kjb3server) and local folder name (kjb3server_drive) to match your own drive and folder names, respectively.

`rclone mount kjb3server: ~/kjb3server_drive --vfs-cache-mode full`

2. Install papermill (https://papermill.readthedocs.io/en/latest/) within your Python environment.

3. Create a shell or batch script that can call papermill in order to run recent_weather_data.ipynb, then copy the executed version of this notebook into a Google Drive folder of your choice. autorun_shell_script.sh provides an example of this workflow within Linux, but you'll need to update it to match your own local and Drive-based file directories. (If you're on Windows, you'll need to create a batch script instead.)

4. Have your computer run your shell/batch script on an hourly basis, as the NWS data source that recent_weather_data.ipynb accesses gets updated on an hourly basis. This can be accomplished in Linux by creating a new crontab entry and in Windows via Task Scheduler.

5. Navigate to the online copy of your exported notebook within your Google Drive folder, then open it with the Colaboratory extension. (You'll need to install this extension if you haven't already done so.)

6. If you'd like to share the link to this Colab-hosted notebook with others, simply update the sharing permissions and then copy the link.

# Part 2: Viewing HTML versions of notebooks via NBViewer (and automatically updating your GitHub repository in the process)

HTML-based Plotly charts (and possibly other HTML data as well) *can* be viewed via NBViewer (https://nbviewer.org/). For example, you can view my recent_weather_data.ipynb notebook (along with its interactive Plotly charts) at nbviewer.org here: https://nbviewer.org/github/kburchfiel/recent_weather/blob/main/recent_weather.ipynb

However, a major limitation to this approach is that updates to notebooks may take a while to appear within NBViewer. Although the FAQ suggests that adding ?flush_cache=True to a URL can resolve this problem, this functionality (as of October 2024) [appears to be broken](https://github.com/jupyter/nbviewer/issues/914).

Due to this limitation, I'd say that it's not currently worth your effort to attempt to share automatically-updated notebooks via NBViewer, as your viewers may continue to see an older cached version. Nevertheless, if you'd like to give this approach a try, you can do so via the following steps:

[Note: I found kowsalya's StackOverflow answer at https://stackoverflow.com/a/54597670/13097194 to be helpful when implementing these steps.]


1. Install Git within your computer.

2. Create a new GitHub repository that can store new Papermill-rendered copies of your notebook.

3. Create a local folder that can store these Papermill-rendered notebooks also, then initialize a Git repository within it.

4. Use the same steps shown in the Google Drive section to update your notebook on a regular basis. (Make sure that your shell/Batch script copies your notebook into your new local folder and not just Google Drive.)

5. Update your existing shell/Batch script so that, after copying each new version of your notebook into a local folder, it then (1) navigates to this folder; (2) deletes the existing Git folder; (3) creates a new one; and (4) commits this new one to GitHub while overwriting anything already on the online repository. (See the linked Stackoverflow post by kowsalya for help with these steps; note that, since GitHub now uses 'main' rather than 'master' as its default branch name, you'll most likely want to replace 'master' in kowsalya's suggested commands with 'main'.)

A few notes on this step:

a. To overwrite the existing online repository with the newly created local repository, you can use `git push origin main --force`. (This code assumes that your repository is named 'main' rather than 'master.') See user456814's detailed overview of this and related code at https://stackoverflow.com/a/24768381/13097194 for more information.

b. The purpose of performing this step *and* deleting the existing local Git folder **is to prevent your local and remote repositories from becoming unmanageably large.** If you're making frequent automated updates to a GitHub folder with a Jupyter Notebook that contains large HTML files (and possibly large image files as well), you could end up with a very large repository in a short period of time. Therefore, my suggested approach is to keep only the most recent version of your automated notebook in both repositories, which these steps can help accomplish.

c. Even if you take these precautionary steps, I recommend periodically checking your local and remote GitHub folders in order to ensure that you're not filling your repository with obsolete copies of your automated notebook (and thus increasing its size).

d. In order to successfully push your notebook, you'll need to provide GitHub with your credentials if you haven't already done so. I initially used Git Credential Manager (https://github.com/git-ecosystem/git-credential-manager/blob/main/README.md) with the secretservice credential option (https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/credstores.md) to authenticate my computer with GitHub. However, I found that this setup did not work correctly within a crontab entry. Therefore, I instead decided to use the credential cache approach (also described within https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/credstores.md ).

6. Navigate to nbviewer.org, then paste the link to your Github-hosted notebook into the URL bar. (In my case, this link was https://github.com/kburchfiel/recent_weather/blob/main/recent_weather.ipynb ) You'll then be able to view the output of this notebook within nbviewer (e.g. https://nbviewer.org/github/kburchfiel/recent_weather/blob/main/recent_weather.ipynb ). **However**, as noted earlier, it may take a while for new updates to appear.

