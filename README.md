# Amateur Hockey Analysis

Amateur Hockey Analysis is an application for amateur hockey player and team comparison.

With this application, you can:

  - View team statistics
  - View individual player statistics
  - Compare similar players
  - View our draft rankings for draft eligible players
  - Build and compare your own team

For every team and player statistic, we provide the raw statistic value along with a visualization for where the stat is located in its standard deviation.

## Algorithms

For ranking, we go for a more statistical and consistant approach than the publicized NHL rankings. Our algorithm takes in to account multiple stats scraped and calculated from game data rather than instance scouting. Because of this, we are able to rank players based on their consistancy and individual performance rather than instanced scoutings where limited stats are collected and certain visual features are overemphasized. We are able to normalized these stats based on league differences and playestyles giving as accurate prediction accross all leagues.

For computing similar players, we cluster players using k-means. Since not every league collects the same statistics, we have found the common stats accross all players, and created a vector representation of each player using those stats. We then compute 21 different cluters through 20 iterations of our k-means clustering algorithm.

## Data

All of our data was collected from [here] and were originally scraped from previous game data.  We also collected stats for the [AHL] but decided against using them. Our data was parsed from the CSV files given on the website and turned into a JSON object we could load in to our application and treat as a dictionary. Unfortunately, the data is static and is always the same when loaded in to the application.

## Team and Player Statistics

For each team and player, we have provided a view that gives the raw value for each stat and a visual to show where the team/player is within the standard deviation for that stat. For each player, we give you the ability to add them to your custom team and compare them to other players in the cluster that the player is present in.  At anytime, you can navigate to My Team to view the custom team you have built.  It compares every player stat on your team with that of the average for every other amateur team and shows you how it compares.

## Heroku

We have launched our application and it can be found on our [heroku].

[here]: <http://www.prospect-stats.com/>
[AHL]: <http://theahl.com/>
[heroku]: <http://enigmatic-brook-97634.herokuapp.com/stats/>
