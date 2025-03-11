# An introduction to Python for Nonprofits

## Overview of PFN's contents

Python for Nonprofits covers a wide range of nonprofit data analysis tasks. First, the **Importing and Prepping Data** section of Python for Nonprofits will teach you how to read data into your Python scripts, then clean and reformat them. You'll also learn how to import American Community Survey data using the US Census Bureau's API.

Next, the **Analyzing Data** section will demonstrate how to calculate various descriptive statistics. Once you've calculated such statistics, you'll often want to visualize them; therefore, this component is followed by the **Visualizing Data** section, which shows how to display your findings in both graph and map form.

PFN then provides a brief introduction to inferential statistics via its **Regressions** section. (I had initially planned to place this component within the Analyzing Data section, but because it relies so heavily on visualizations, I realized that I should have it follow my data visualization code.) Finally, in the **Publishing Analyses Online** section, you'll learn how to use Python to export data to Google Sheets and display it within online dashboards. 

Later sections of Python for Nonprofits often reference content covered in earlier sections. For instance, data cleaning and reformatting will come up in many sections, not just the data prep chapter. In addition, the Regressions and Publishing Analyses Online sections will make extensive use of the graphing tools that the Visualizing Data section introduces. Therefore, I would recommend reading through PFN's sections in the order shown above.

## My reasons for writing PFN

To explain why I wrote this text, it will help to provide some background about my own educational and career path. 

I should start by saying that I do *not* have a background in mathematics or computer science. I focused mostly on writing in high school, then majored in psychology at Middlebury College. I later obtained a Master of Science in Social Work at UT Austin and worked as a mental health counselor with Catholic Charities for a few years. These experiences did not teach me about Python or computer programming, but they *did* help me build my writing and communication skills--which certainly came in handy for this project. Therefore, if you (like many nonprofit staff) do not have much in the way of a quantitative background, don't worry--I'm very confident that you can learn and apply Python in your own work!

I first began studying Python seriously as a first-year MBA student, when I enrolled in Professor Mattan Griffel's Introduction to Programming in Python course. I was amazed with how easy Python facilitated various data analysis and visualization tasks, and I also loved how programming engaged both the creative and problem-solving portions of my brain. I then had the chance to take several other programming-related classes at CBS with Hardeep Johar, Daniel Guetta, and Jared Lander; these courses further opened my eyes to the capabilities of Python and other open-source tools.

I then had the opportunity to apply Python during a summer internship at Seton Education Partners. My supervisor, David Morales, gave me lots of freedom to use Python for many analysis-related tasks. I greatly enjoyed my time at Seton, so I returned there full time after completing my MBA. At Seton, I not only applied the Python knowledge that I had picked up during my MBA, but also learned many new libraries and applications for the language.

My wife, son, and I then moved to Virginia in 2024 to be closer to our families. As a Research Fellow with the Institute for Family Studies, I have been applying Python (along with R, a powerful open-source statistical programming language) to analyze survey data and create visualizations. 

My professional experiences have taught me that Python is a very powerful tool for nonprofit work. It is a huge time saver, and it also allows for the creation of analyses and visualizations that would be difficult or impossible to perform in spreadsheet-based tools like Excel. (For a more detailed list of reasons to apply Python at your nonprofit, read 'The Case for Python at Nonprofits' within PFN's Introduction section.) 

Therefore, I wanted to create a guide that would allow others to learn how to apply Python at their present (or future) nonprofit jobs. Much of the text focuses on applications and methods that I have used in my own work; therefore, I am confident that you'll find each section to be useful for your own nonprofit data analysis tasks as well. (I should also clarify, though, that I did not reference or copy any code from my work in the process of writing this text.)

I also hope to teach Python on a part-time basis one day; if that opportunity arises, I would plan to incorporate this guide into my curriculum. 

Those are some of my 'practical' reasons for writing Python for Nonprofits. However, I also found this project to be intrinsically rewarding--and actually *fun*. I greatly enjoy learning new things, than teaching others about them; therefore, it has been immensely enjoyable to develop the code and documentation that comprises PFN. There were many evenings in which I had trouble shutting down my computer and going to bed because I was having such a good time with PFN!

I recognize that writing educational Python materials is a strange hobby, but it's one that I hope to continue for years to come. I hope that you will have as much fun reading this text--and putting its examples into practice in your own personal and professional life--as I have had writing it.

## Development notes

It took me quite a while to write Python for Nonprofits. I was working full time during most of the writing period, and the birth of our first child also kept my wife and I (but especially my wife!) quite busy. Therefore, I generally needed to work on the project in the evenings and later in night. The benefit of this arrangement, though, was that the time I spent on PFN felt more like a fun break from other responsibilities than a chore in itself. I found that, as long as I had 4 or 6 hours a week to spend on this project, I could write a decent amount over the course of a year.

Most PFN files were written in Jupyter Notebook format (https://jupyter.org/), though quite a few were produced in Markdown format (.md). I also moved some Python code into standalone .py files to make them easier to incorporate into various projects. I used JupyterLab Desktop (https://github.com/jupyterlab/jupyterlab-desktop) for almost all of the writing process, and would recommend that you install that program as well for viewing and running this code (though Visual Studio Code should also work).

I switched over to Linux Mint in 2024 for most of my professional and personal work; however, the code should also run fine on Windows and Mac. (Please let me know if you have any trouble with certain parts of PFN on one of those operating systems.)

### The book version of PFN

Although I knew that most people would likely access Python for Nonprofits online, it was also important to me that I make it available in print form. Although online resources offer incredible convenience and accessibility, to truly learn a subject, I find that it helps to read through a book from cover to cover. Therefore, I made use of the fantastic Jupyter Book (https://jupyterbook.org/en/stable/intro.html) tool to convert the .ipynb and .md files that comprise Python for Nonprofits into a single PDF. Jupyter Book took care of much of the formatting for me, allowing me to focus more on the actual content. (I plan to make this PDF available to order in printed form in the near future--though you are of course welcome to print it out yourself in the meantime.)

### My reasons for eschewing Generative AI

I chose not to use generative AI tools in the process of writing Python for Nonprofits. When I needed to learn how to perform a particular task, I preferred to consult the documentation for the library that I was using; StackOverflow; or similar human-created resources.

I had a few reasons for this approach. First, I believed that it was important for me to understand how my code was working and what it was doing. If I relied on generative AI to solve challenges for me, my own understanding of Python--and the libraries that PFN utilizes--would suffer. If Kristen Nygaard is correct that 'Programming is understanding' (https://www.stroustrup.com/3rd_pref.html), then copying and pasting Generative AI-produced code could lead to a *lack* of understanding on my part. And in the world of data analysis, this deficit in understanding could lead to all sorts of insidious errors.

I also have substantial concerns about potential copyright infringement caused by generative AI. If a Generative API tool provided me with code that was actually protected by a 'copyleft' license like the GPL, I might then need to release my entire project under the GPL, rather than the more 'permissive' MIT license that I selected. If it instead gave me tool that was actually covered under a proprietary license, I might then get sued for using someone else's work without his or her permission.

In addition, I wanted my own style--both in writing and programming terms--to manifest itself within Python for Nonprofits. It would have been harder to maintain that voice if I interspersed Generative AI-generated content within my own text.

Finally, I find the process of writing and debugging my own code to be *fun*. If I outsourced that process to an AI-based tool, I think I would not have enjoyed this project so much.

None of this is to imply that individuals who use generative AI, whether for programming, writing, or other forms of content creation, are somehow worse at what they do or mistaken in their approach. I simply believe that avoiding the use of generative AI is the best choice *for me*.

## Acknowledgments

[Many acknowledgments to come!]

## Dedication

This work is dedicated to my wife, Allie Burchfiel. Allie generously allowed me to take the time I needed to put this project together, even though that meant that I was less available to help her with chores, childcare, and the many other tasks (big and small) that go into running a household. She also believed in my vision for this work--and in my dreams of sharing my (still limited) understanding of Python with others. Allie is an amazing wife and mother, and I am incredibly fortunate to spend my life with her.