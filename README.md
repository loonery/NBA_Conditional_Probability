# NBA_Conditional_Probability
I completed this project for my discrete math class. The goal was to ask and answer a question related to course topics. 
Below is the question that my teammates and I posed for the projects.

For this final project, we pose the question: “For any given NBA basketball game matchup, what is the
probability that a certain team wins, given certain metrics analyzed before and during the game?”
"Certain metrics" are meant to be questions that are commonly ordered by basketball fans and are also
interesting and approachable to people who do not follow the game closely.
The "certain metrics" portion of the question then begs a few sub questions:
1. Scoring first - what advantage does this give in terms of winning probability, if any?
2. What is the probability that either team wins if holding a lead after the 1st quarter? What about
after the 2nd quarter? And after the 3rd quarter?

The project involved the following steps:
1) Parsing NBA play-by-play data into discrete data about 6000+ unique games.
2) Using the processed data to calculate the conditional probability of specific game events based upon other game events. 
3) Analyzing and presenting findings

Repository structure:
 - The data processing code lives in the /src directory
 - The final project presentation materials (including conditional probability calculations) live in the /project_output directory
 - The play-by-play data files (retrieved from kaggle) are zipped and accessible for download as nba_pbp_data.zip
 
Please see the final presentation for more information about the project outcomes :).
