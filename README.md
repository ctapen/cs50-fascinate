# README.md

Project Title: Fascinate
Project Creator: C.Tapen
Project Date: 2017-12-07

Project Description:

In this day and age, information is prevalent, but quality information is harder to find and to discern.  In this
climate of fake news, how is a reader to know what to believe?  Moreover, quality news outlets provide an amazing service, but
no provider extracts insightful nuggets across the news and think tank landscape.  Wouldn't it be great to have high quality
(and maybe even mind-blowing) facts at your fingertips.  That's what Fascinate aims to provide!  Interested to hear your thoughts!


Intended Display:

A blog or news-feed like display of fascinating facts, flowing from newest to oldest, or highest rated to lowest.


Additional Features/Functionality:

-Sources: importantly, in the name of high quality content, each entry has at least one source link.  The site aims to
leverage minimially-partisan and highly reputable sights.
-Pictures: when possible, graphics associated with facts help bring them to life.  This is an integral part of the Fascinate
proposition.
-Filtering & tags: maybe you are particularly interested in technology facts, or health facts.  Well through Fascinate
preliminary tagging and filtering, you can filter on some of these attributes.  You can also filter by newest/highest rated.
-Ratings: to engage users, the web app contains the ability to rate the content, from one to five stars.  This is then recorded
on the backend (via python to fascinate.db).  Additionally, average ratings are made visible upon the user rating the content
for a bit of gamification/enhanced engagement opportunity to compare his/her rating to the group's.
-Recommend: it also provides the opportunity to recommend content (e.g., provide a fascinating fact) for the site admin
to review before posting.
-Validate: to help ensure quality of the platform, users can submit a form questioning the quality of a fact, for an admin
to review.


Usability:

-Files: This project contains a mix of html, css, js, and python files, along with a database (SQL-based relational db).
-DB tables: The database, called fascinate.db, contains eight tables: entries, ratings, recommendations, tags, tags_horizontal,
tags _ref, users, validate. More on this in DESIGN.md.
-Folders: The html files are contained in the templates folder, and the js and css files in the static folder.
-HTML files: The project contains eight html files, first displaying index.html to show teaser of facts/ratings,
later displaying index_p2.html with extended fact content and ability to filter on newest/highest rated/some tags,
also using login.html and register.html to login and register, using apology.html for error check failures,
using validate.html to let user to submit any concerns on questionable content, using recommend.html to let user suggest content,
and leveraging layout.html across.
-The project leverages jinja as well.
-Run instructions: To run the content, navigate to project folder (e.g., cd project/) then type in terimnal flask run .
Then click on the link to the 8080 link to display the webapp!
-Pre vs. Post Login Content: some content is available pre-login (user can view & rate content of limited number of entries displayed on home screen)
but for more extensive interaction (viewing all content, filtering content on tags, submittiing recommendation or validate content)
user needs to register/log in.


Hope you enjoy & find it fascinating!
