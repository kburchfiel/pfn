# The Case for Using Python at Nonprofits

*By Kenneth Burchfiel*

Python is a great option for managing, analyzing, and visualizing nonprofit data for four reasons: it's *flexible*, *fast*, *free*, and *famous*. And you might even find it to be *fun* as well.

This programming language won't be the right fit for every nonprofit, and it does require more study and practice than many commercial solutions. However, I would suggest that nonprofits at least consider incorporating Python into their data workflows. 

## Python is *flexible*
Python's versatility is one of its key strengths. You can use it to read in data from numerous different sources; reformat and analyze that data; create visualizations; and even share your analyses online via an interactive dashboard. Other tools, like spreadsheet programs or business intelligence software, may specialize in one or more of these components, but Python is a fantastic choice for all of them.

Python not only supports many different use cases but also allows you to create scripts that are tailored to your nonprofit's specific needs. If you want a closed-source commercial software program to perform an additional task, you'd probably need to submit a feature request and then wait for the developers to incorporate it into the next version of their program--if they choose to do so at all. Meanwhile, if you want a Python script to perform a certain task, you can add in code for that task yourself (provided, of course, that you have the time and capabilities to do so). 

This flexibility is greatly enhanced by the wide variety of libraries offered for Python. For instance, *Pandas* is a powerful tool for reading, reformatting, and analyzing data. *Plotly* allows you to easily create interactive charts and maps. And *Dash*, together with Plotly, can power interactive online dashboards in order to make your analyses and visualizations easier to share with others. (Each of these libraries, among others, will get featured in Python for Nonprofits.) These packages aren't part of the core Python programming language, but they are easy to install, and detailed documentation on each of them is accessible online.

One drawback of this flexibility, however, is that users of a Python script that another user wrote will need to take additional time to understand how it works--especially if it was not documented well. As long as someone has learned how to use a proprietary program, he or she should have little trouble making updates to a file that someone else created within that program, given that such software offers less room for variation. However, a Python expert will probably still need to take time to understand a script that another expert created, especially if it incorporates libraries or methods with which the expert isn't yet familiar.

## Python is *fast*
Once you've created a Python script that completes a certain task, you should then be able to finish that task much more quickly the next time around than you could have within a spreadsheet editor or other tool. Therefore, the more you incorporate Python into your workflow, the more productive you and your team can be.

For example, let's say that your nonprofit sends out a survey to its service recipients each month, then compiles that data into a report for its board. It's true that pivoting and charting this data within a spreadsheet editor would likely be quicker than writing a set of Python code to perform these same steps. *However*, once you've created that Python code, you could then have it create your tables and charts in a matter of minutes or even seconds. (Or, if you configure your script to read in the latest survey data automatically and then instruct your computer to run it on a regular basis, you could produce your analyses without any keypresses at all.)

Similarly, suppose your supervisor requests that you use a new color scheme for 20 different charts that you created as part of a report. If you created these charts in Python and defined the color scheme at the beginning of your script, you could easily update all 20 charts by changing that scheme's definition and rerunning the script. 

This speed advantage does have a few caveats. For instance, if a new set of data that you receive uses a different layout, different value types (e.g. '5%' instead of '0.05'), or different column names, you'll likely need to adjust your code to accommodate that new setup. However, Python also helps speed up data cleaning tasks, so if your nonprofit's data is imperfect (which I imagine to be the case just about anywhere), Python might become an even more useful tool as a result.

I also recognize that individuals with experience in Visual Basic for Applications (https://en.wikipedia.org/wiki/Visual_Basic_for_Applications) could likely create Excel macros that would provide similar speed advantages. However, I would suggest that the time spent learning VBA might be better spent on Python given the latter's versatility and popularity (more on this soon). 

## Python is *free*
The more companies rely on a SAAS (Software As A Service) model, in which you must provide ongoing payments to continue using a program, the more appealing Python and other free and open-source tools will appear as a result. This is the case for all organizations, but Python's cost advantage may be particularly compelling to nonprofits.

Suppose that you use a proprietary data visualization program that costs 200 dollars per user per year. If you have 300 staff members who use this software, your annual payments for it will amount to 60,000 dollars.

However, because Python is free to use and open source, you could dramatically reduce these costs by building a web dashboard using Python instead. You would probably need to pay for server and hosting costs, but you'd be able to avoid per-user fees and thus save significant amounts of money as a result.

Again, there are some caveats here. First, unless you build the web dashboard yourself (which would present opportunity costs), you'd need to pay someone to recreate it in Python; if your dashboard is particularly complex, these upfront costs may be too large for your nonprofit to bear. However, if you're already paying someone to manage your proprietary visualization program, having them rebuild your dashboard in Python instead *might* be a financially sound decision.

Second, not all versions of Python are free. For instance, if you use Anaconda for an organization with 200 or more employees, you may need to pay 50 dollars a month. (See Anaconda's Terms of Service (https://legal.anaconda.com/policies/en?name=terms-of-service#terms-of-service) for more details; the exact monthly cost is subject to change, if it hasn't changed already.) My understanding is that using Miniforge (https://github.com/conda-forge/miniforge) *should* allow you to legally avoid this monthly payment, but I can't guarantee that this is the case. (I do use Miniforge for my own personal and professional use and would recommend that you consider doing so as well.)

## Python is *famous*
Python, according to the TIOBE Index (https://www.tiobe.com/tiobe-index/), is the world's most popular language. The rating of 23.85% that it received in March 2025 was over 9 times the rating of VBA, the language behind Excel macros that I mentioned earlier, and 25 times that of R (another commonly-used language for data science applications). As just one example of its broad adoption, over 3.2 million users have enrolled in The University of Michigan's 'Programming for Everybody' Python course (https://www.coursera.org/learn/python). Due to the language's popularity, I would expect that nonprofits can find a broad pool of prospective talent for Python-related work.

Python's wide usage has another important benefit: if you're facing an error message or a bug, it's likely that you'll find someone on Stack Overflow or GitHub who encountered a similar issue--and someone else who was able to resolve it for them.

## Python is *fun* (to me, at least!)
Although your experience may vary, I have found great enjoyment in learning and applying Python. The mix of creativity, problem-solving, and real-world application that Python (like other programming languages) offers means that writing code often feels more like play than work. Granted, there have been plenty of frustrating moments along the way, but that frustration dissolves into gratification once a solution to the problem is found.

Although the first four of the 5 'Fs' that I've presented here might be more relevant to a nonprofit's management team or board, I'd argue that the 'fun' factor is one of the best reasons to study and apply Python. If you find working in Python to be entertaining and enjoyable, that's a great reason to continue building up your skills! Alternatively, if you come to loathe the programming experience, consider using another method to analyze data (or find someone else to take care of the Python work).

## Don't take my word for it--give it a try yourself!
I recognize that this essay glosses over the complexity of choosing what tools to use to meet a given nonprofit's data needs. There are undoubtedly many cases when proprietary software would be a better fit than Python for a given organization. However, I'm also confident that Python is an underutilized tool within the nonprofit sector. I hope that Python for Nonprofits can demonstrate the utility of this language for your organization *and* give you the confidence you need to begin applying it.




