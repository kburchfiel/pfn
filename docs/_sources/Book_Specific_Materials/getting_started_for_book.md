# Getting Started

If you already have experience with Python (which I *do* recommend as a prerequisite for reading Python for Nonprofits), you shouldn't need to perform too much additional setup in order to begin going through PFN's chapters. 

I am a big fan of print-based programming guides, so I do encourage you to read this book or PDF front to back if you prefer to learn that way. However, I also recommend that you download PFN's GitHub repository, available at https://github.com/kburchfiel/pfn . That way, you can run and modify the code contained within this book--and, of course, incorporate it into your own projects. (The repository also contains certain source data files that you'll need to correctly run certain scripts.) As you read through each section of PFN, you may also find it helpful to keep that section's corresponding Jupyter Notebook open on your computer.

*Note: When running these notebooks on your own computer, you may want to confirm that the `render_for_pdf` setting within the `Appendix/helper_funcs.py` file is set to False. That way, many visualizations will appear in interactive HTML rather than static PNG format. (If `render_for_pdf` was initially set to True, you'll need to rerun each section after changing it to False in order for that change to take effect.)*

An HTML-based version of this book is also available; you can access it by downloading the entire GitHub repository, then opening `docs/index.html` within the downloaded folder. I do plan to make this HTML-based book available online as well, but I'll first need to work out some bugs with [the online version](https://kburchfiel.github.io/pfn/README.html).

In reading through PFN, you can of course choose to skip over sections with which you are already familiar or don't (yet) have a need for; however, keep in mind that later sections assume that you have already read through earlier ones.

Finally, the best way to internalize this content is to use it as the starting point for your own projects. In the future, I may also add suggested 'homework' that will make this practice a bit more formal--but for now, you'll need to 'BYOA' (bring your own assignments). One option would be to find a dataset related to a subject that interests you, then apply the contents of each section to clean, analyze, and visualize it.

## Initial setup

I created much of PFN within Jupyter Desktop (https://github.com/jupyterlab/jupyterlab-desktop), an open-source tool for opening and viewing Jupyter Notebooks. I recommend that you use this program for viewing PFN notebooks, though PFN should run well within other Jupyter Notebook viewers as well. 

You'll of course also want to have Python set up on your computer. As noted within The Case for Python at Nonprofits, I recommend that you install and use Python (and the libraries that PFN applies) via Miniforge rather than Anaconda, as you may not be able to use the latter for free. 

Although most of the libraries that Python for Nonprofits uses are available within conda-forge (https://github.com/conda-forge), some may need to be installed via pip (https://pypi.org/). 

## Errata

When I become aware of errors within printed versions of the book, I will plan to make note of those errors within https://github.com/kburchfiel/pfn/tree/main/Book_Specific_Materials/book_errata.md .

## Let's begin!

Now that these introductory matters are out of the way, you can start learning how to use Python in a nonprofit setting. We'll begin, as many analysis tasks do, with data retrieval.