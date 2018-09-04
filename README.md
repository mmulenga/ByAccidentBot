# By-Accident-Bot
> A reddit bot built to correct and track the usage of the phrase "on accident" on reddit.

[![CircleCI](https://circleci.com/gh/mmulenga/ByAccidentBot.svg?style=svg)](https://circleci.com/gh/mmulenga/ByAccidentBot)

## How does it work?
Using PRAW the bot parses through reddit comments looking for the usage of "on accident". 
Once it finds an occurrence it responds to the offending comment with a GIF and a 
pre-made message. In addition to responding to the comment the bot copies the comment's
ID to a database which is later read from to create a statistical graph. Ultimately, I
would like to see if the bot has a noticeable effect on the frequency of the usage of
"on accident".  

Disclaimer: Please don't take the bot too seriously! Above all else, this is a project for me
to expand my programming skills.

## Occurrence Graph
![Occurrence Graph](https://i.imgur.com/uH3qWyo.png)

## Don't Forget!
![It's by accident!](https://thumbs.gfycat.com/JointHiddenHummingbird-size_restricted.gif)
