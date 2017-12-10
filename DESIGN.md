# DESIGN.md

Welcome to Fascinate.  Here are some details underneath the hood:

I wanted to build a web app that would not only display fascinating content, but also enable user to interact
with the content and store the interaction resutls.  Beyond the html/css backbone of the website and some javascript
for additional click functionality, I decided to use python and a SQL db.  I tried to keep the various languages' code
in separate files.

I wanted to compartmentalize the various pages, so that you recommend on one page, validate on anther page, same for
login and register.  I utilized render_template and redirect along with GET/POST within my python to accomplish
the switching pages.

Functionally, I wanted Fascinate to display a teaser of content on the initial index page and then supplement it with
full content and added filtering ability on index page 2.  This will draw the reader in but provide a benefit
to them registering (along with recommending content and weighing in on the validity of content).

A primary design decision was to make the facts display iteratively and dynamically, without hardcoding them
in the html or elsewhere.  Therefore, I stored all the fact content in the entries table of my db
and then passed through the data using SQL select statements in application.py to index.html and index_p2.html.
I used {% for item in items %} type loop to display the entries I had pulled dynamically.  This did, however, pose some
challenges, and required being creating.  It broke many times when trying to display by rating stars within the
loop, leaving me to wrestle with how to get the interaction to work for not just the first entry displayed but
for all subsequent as well.  I also leveraged {% ifs %} to help bring the back end content to life but not if
a given field (like source #2) wasn't populated for that entry.

Another design decision was to use blocks in my html to extend index to index2 in order to not replicate code.  Along
the same code-line writing efficiency standpoint, I placed the star_rating() function in helpers.py so I did not
have to copy it over to multiple places in application.py and instead called the function.

Another area that required a clever workaround was trying to return attributes of a html tag other than name/value pair;
if the absence of being able to do that, I instead concatented and then split out the elements I needed to pass through.

In constructing the star ratings, I wanted to be able to submit the data to the backend without reloading the page to the top
which was a decision made to facilitate good user experience.

Also, aesthetically, I wanted the design to be simple, with lots of white background, with color accent pops of green buttons,
for instance.  I also liked the simple light gray rounded boarders to contain each entry.



