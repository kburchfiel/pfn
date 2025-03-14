# An Introduction to Python for Nonprofits

## Overview of PFN's contents

Python for Nonprofits covers a wide range of nonprofit data analysis tasks. First, the **Importing and Prepping Data** section of Python for Nonprofits will teach you how to read data into your Python scripts, then clean and reformat them. You'll also learn how to import American Community Survey data using the US Census Bureau's API.

Next, the **Analyzing Data** section will demonstrate how to calculate various descriptive statistics. Once you've calculated such statistics, you'll often want to visualize them; therefore, this component is followed by the **Visualizing Data** section, which shows how to display your findings in both graph and map form.

PFN then provides a brief introduction to inferential statistics via its **Regressions** section. (I had initially planned to place this component within the Analyzing Data section, but because it relies so heavily on visualizations, I realized that I should have it follow my data visualization code.) Finally, in the **Publishing Analyses Online** section, you'll learn how to use Python to export data to Google Sheets and display it within online dashboards. 

Later sections of Python for Nonprofits often reference content covered in earlier sections. For instance, data cleaning and reformatting will come up in many areas of PFN, not just the data prep chapter. In addition, the Regressions and Publishing Analyses Online sections will make extensive use of the graphing tools that the Visualizing Data section introduces. Therefore, I would recommend reading through PFN's sections in the order shown above.

## My reasons for writing PFN

To explain why I wrote this text, it might help to provide some background about my own education and career path. I should first clarify that I do *not* have a formal background in mathematics or computer science. Therefore, if you (like many nonprofit staff) have focused more on qualitative than quantitative skills in your schooling and career, don't worry--I'm very confident that you can still learn and apply Python in your work!

I focused mostly on writing in high school, then majored in psychology at Middlebury College. After working as an AmeriCorps VISTA member in Houston, I obtained a Master of Science in Social Work at UT Austin and worked as a mental health counselor with Catholic Charities of Evansville for two years. 

I first began studying Python seriously as a first-year MBA student, when I enrolled in Professor Mattan Griffel's Introduction to Programming in Python course. I was amazed with how easily Python facilitated various data analysis and visualization tasks, and I also loved how programming engaged both the creative and problem-solving portions of my brain. I then had the chance to take several other programming-related classes at CBS with Hardeep Johar, Daniel Guetta, and Jared Lander; these courses further opened my eyes to the capabilities of Python and other open-source tools.

I was fortunate to be able to apply Python during a summer internship at Seton Education Partners in The Bronx. My supervisor, David Morales, gave me lots of freedom to use Python for many analysis-related tasks. I greatly enjoyed my time at Seton, so I returned there full time after completing my MBA. At Seton, I not only applied the Python knowledge that I had picked up during my MBA but also learned many new libraries and applications.

My wife, son, and I then moved to Virginia in 2024 to be closer to our families. As a Research Fellow with the Institute for Family Studies, I have been applying Python (along with R, a powerful open-source statistical programming language) to analyze survey data and create visualizations. 

My professional experiences have taught me that Python is a very powerful tool for nonprofit work. It is a huge time saver, and it also allows for the creation of analyses and visualizations that would be difficult or impossible to perform in spreadsheet-based tools like Excel. (For a more detailed list of reasons to apply Python at your nonprofit, read 'The Case for Python at Nonprofits' within this same section.) 

Therefore, I wanted to create a guide that would allow others to learn how to apply Python at their present (or future) nonprofit jobs. Much of the text focuses on applications and methods that I have used in my own work, so I'm confident that you'll find this work to be relevant to many of your own nonprofit data analysis tasks as well. (I should also clarify, though, that I did not reference or copy any code from my work in the process of writing this text.)

I also hope to teach Python on a part-time basis one day; if that opportunity arises, I would plan to incorporate this guide into my curriculum. 

Those are some of my 'practical' reasons for writing Python for Nonprofits. However, I also found this project to be intrinsically rewarding--and truly *fun* as well. I greatly enjoy learning new things, than teaching others about them; therefore, it has been immensely enjoyable to develop the code and documentation for this project. There were many evenings in which I had trouble shutting down my computer and going to bed because I was having such a good time with PFN!

I recognize that writing educational Python materials is a strange hobby, but it's one that I hope to continue for years to come. I hope that you will have as much fun reading this text--and putting its examples into practice in your own personal and professional life--as I have had writing it.

## Development notes

It took me quite a while to write PFN. I was working full time during most of the writing period, and the birth of our first child also kept me and my wife (but especially my wife!) quite busy. Therefore, I generally worked on the project later in the day--and often right before going to bed. The benefit of this arrangement, though, was that the time I spent on PFN felt more like a fun break from other responsibilities than a chore in itself. I found that, as long as I had 4 or 6 hours a week to spend on this project, I could write a decent amount over the course of a year.

Most PFN files were written in Jupyter Notebook (.ipynb) format, though quite a few--such as this chapter--were produced in Markdown format (.md). I also moved some Python code into standalone .py files to make them easier to incorporate into various projects. I used JupyterLab Desktop (https://github.com/jupyterlab/jupyterlab-desktop) for almost all of the writing process, though the code should also be viewable and executable within other code editors that support .ipynb files.

I switched over to Linux Mint in 2024 for most of my professional and personal work; however, the code should also run fine on Windows and Mac. (Please let me know if you have any trouble with certain parts of PFN on one of those operating systems.)

### The book version of PFN

Although I imagine that most people would prefer to access Python for Nonprofits online, it was also important to me that I make it available in print form. Although web-based resources offer incredible convenience and accessibility, to truly learn a subject, I find that it helps to read through a book from cover to cover. 

Therefore, I made use of the fantastic Jupyter Book (https://jupyterbook.org/en/stable/intro.html) tool to convert the .ipynb and .md files that comprise Python for Nonprofits into a single PDF. Jupyter Book took care of much of the formatting for me, allowing me to focus more on the actual content. (I plan to make this PDF available to order in printed form in the near future--though you are of course welcome to print it out yourself in the meantime.) It appeared that Jupyter Book couldn't process .py files on its own, though, so I copied those scripts into standalone Jupyter Notebooks, thus allowing them to get incorporated into the book.

If you're interested in using Jupyter Book for your own articles and books, check out the documentation at https://jupyterbook.org/ . Note that the `_config.yml`, `_toc.yml`, `create_html_book.sh`, and `create_pdflatex_book.sh` files in PFN's root folder are part of my workflow for turning PFN into a Jupyter Book project. (These files were also based on Jupyter Book's documentation.)

Jupyter Book *also* allowed me to convert these files into an HTML-based online book that you may find useful. See the Getting Started section, found in the main PFN readme on GitHub or the 'Getting Started' chapter of the Print/PDF book, for more details.

### My reasons for eschewing Generative AI

I chose not to use generative AI tools in the process of writing Python for Nonprofits. When I needed to learn how to perform a particular task, I preferred to consult the documentation for the library that I was using; StackOverflow answers; or similar human-created resources.

I had a few reasons for this approach. First, I believed that it was important for me to understand how my code was working and what it was doing. If I relied on generative AI to solve challenges for me, my own understanding of Python--and the libraries that PFN utilizes--would suffer. If Kristen Nygaard is correct that 'Programming is understanding' (https://www.stroustrup.com/3rd_pref.html), then copying and pasting Generative AI-produced code could lead to a *lack* of understanding on my part. And in the world of data analysis, this deficit in understanding could lead to all sorts of insidious errors.

I also have substantial concerns about potential copyright infringement caused by generative AI. If a Generative API tool provided me with code that was actually protected by a 'copyleft' license like the GPL, I might then need to release my entire project under the GPL rather than the more 'permissive' MIT license that I selected. If it instead gave me a block of code that was actually covered under a proprietary license, I might then get sued for using someone else's work without his or her permission.

In addition, I wanted my own style--both in writing and programming terms--to manifest itself within Python for Nonprofits. It would have been harder to maintain that voice if I interspersed Generative AI-generated content within my own text.

Finally, as noted earlier, I find the process of writing my own code to be a great deal of fun--which is a relevant consideration for a hobby project like this. If I outsourced that process to an AI-based tool, I doubt that I would have enjoyed working on PFN as much.

None of this is meant to imply that individuals who use generative AI, whether for programming, writing, or other forms of content creation, are mistaken in their approach. I simply believe that avoiding the use of generative AI so far has been the best choice *for me*.

## Gratitude and Acknowledgments

First, I am grateful to God for giving me the opportunity to write this text and share what I've learned with others. God's infinite love is a gift that cannot be put into words, and I hope that PFN can serve as a very small offering of love back to Him. 

I am also grateful to Kenneth, my son, who has brought me and my wife joy, laughter, and a deeper sense of meaning and purpose for our lives. Although watching Python for Nonprofits grow has been fun, *your* growth has been far more exciting--and, of course, far more important! This text and code will pass away, but you are eternal. I know you're a bit young to use a computer at the moment, but I hope you will find this project useful one day.

I'm grateful to my parents, Linda and Ken, as well. You provided me with immense love growing up, and I hope I can share that same love with Kenneth (and any other children with whom God might bless us). Dad, you showed me (with *Biotechnology and the Federal Circuit*) that it's possible to write a book while raising a young family and holding down a job. I'm honored to be able to follow in your footsteps 30 years later--and I hope that we will be able to reunite in Heaven one day.

I also want to thank my professors at Columbia Business School--especially Mattan Griffel, Daniel Guetta, Hardeep Johar, and Jared Lander--for introducing me to the valuable role that Python and R can play within organizations. In addition, I'm grateful to my supervisors at Seton Education Partners and the Institute for Family Studies: David Morales, Michael Carbone, Michael Toscano, and Wendy Wang. You gave me the opportunity to apply Python to real-world challenges, which has allowed me to extend my study of programming far beyond the classroom.

This book would not have been possible without the developers of Python and the many, many libraries that it makes use of (particularly Pandas, Plotly, Folium, and Dash). Thank you for making your work accessible to the world!

I also wish to thank the developers of the open-source software and tools (including, but not limited to, JupyterLab Desktop, LibreOffice, Jupyter Book, Linux, and Linux Mint) that I used to develop Python for Nonprofits.

Finally, I want to thank you for reading (or at least flipping through) this book. I hope that, regardless of where you are in your Python and nonprofit career journey, it will be a helpful tool for you.

## Dedication

This work is dedicated to my wife, Allie Burchfiel. Allie generously allowed me to take the time I needed to put this project together, even though that meant that I was less available to help her with chores, childcare, and the many other tasks (big and small) that go into running a household. She also believed in my vision for this work--and in my dreams of sharing my (still growing) understanding of Python with others. Allie is an amazing wife and mother, and I am incredibly fortunate to spend my life with her.

Blessed (and soon to be Saint) Carlo Acutis, pray for us!