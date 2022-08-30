#################### IMPORTS ####################
import pandas as pd
import glob
import re

#################### FUNCTION DEFS ####################

def get_nba_play_by_play(seasons):
    '''this function transforms nba play by play data and returns a new dataframe with Boolean codified information about each game for each row'''

    #################### LOAD & PROCESS DATA ####################
    path = "[insert nba_pbp_data path]"
    filenames = glob.glob(path + "/*.csv")

    #Import each CSV file in the wd folder to a collection of pandas dataframes based on passed integer value 'seasons'
    season_frames = []
    for i in range(seasons):
        season_frames.append(pd.read_csv(filenames[i]))

    #initialize a dictionary. To be loaded into a Pandas data frame with each key representing a game that maps to a dictionary containing information about that game
    games_dict = {} 

    #For each data frame that is requested...(every seasons[i] refers to a Dataframe object)
    for i in range(len(season_frames)):

        #rename URL column in each dataframe to demonstrate that the URL is acting as a game ID.
        season_frames[i].rename(columns = {'URL':'GameID'}, inplace = True)

        #remove the first 11 and the last 5 characters of the URL in a given dataframe, to make the GameID not be a URL
        for row, data in season_frames[i].iterrows():
            if season_frames[i].at[row, 'GameID'] != 'GameID':
                url = season_frames[i].at[row, 'GameID']
                season_frames[i].at[row, 'GameID'] = url[11:-5]

        #Remove superfluous columns in each requested dataframe
        season_frames[i] = season_frames[i].drop(['Shooter', 'ShotType', 'ShotOutcome', 'ShotDist', 'Assister', 'Blocker', 'FoulType', 'Fouler', 'Fouled', 'Rebounder', 'ReboundType', 'ViolationPlayer', 'ViolationType', 'TimeoutTeam', 'FreeThrowShooter', 'FreeThrowOutcome', 'FreeThrowNum', 'EnterGame', 'LeaveGame', 'TurnoverPlayer', 'TurnoverType', 'TurnoverCause', 'TurnoverCauser', 'JumpballAwayPlayer', 'JumpballHomePlayer', 'JumpballPoss', 'Location'], axis = 1)

        #################### CREATE VARIABLES TO MARK INCIDENTS IN DATA ####################

        '''
        COLUMN NAME REFERENCE

        ['GameID', 'GameType', 'Date', 'Time', 'WinningTeam', 'Quarter',
        'SecLeft', 'AwayTeam', 'AwayPlay', 'AwayScore', 'HomeTeam', 'HomePlay', 
        'HomeScore']

        '''
        #For each row and the data it is holding in the loop...
        for row, data in season_frames[i].iterrows():
            
            game_type = str(season_frames[i].at[row, 'GameType'])
            if game_type == 'playoff':
                continue
            
            #If the game has not been processed into the games dict yet...
            game_id = str(season_frames[i].at[row, 'GameID'])
            if game_id not in games_dict:

                #Initialize variables and add them to the dictionary storing the game's static information
                home_team = str(season_frames[i].at[row, 'HomeTeam'])
                away_team = str(season_frames[i].at[row, 'AwayTeam'])
                winning_team = str(season_frames[i].at[row, 'WinningTeam'])
                date = str(season_frames[i].at[row, 'Date'])
                
                #If the winning team is the home team...
                if winning_team == home_team:
                    home_team_wins = True

                elif winning_team == away_team:
                    home_team_wins = False
                
                games_dict.update({game_id : {'date' : date, 'home_team' : home_team, 'away_team' : away_team, 'winning_team' : winning_team, 'home_team_wins' : home_team_wins, 'away_team_wins' : not home_team_wins}})

            #Create variables for each row that evaluate each happenning
            home_play = str(season_frames[i].at[row, 'HomePlay'])
            away_play = str(season_frames[i].at[row, 'AwayPlay'])
            away_score = int(season_frames[i].at[row, 'AwayScore'])
            home_score = int(season_frames[i].at[row, 'HomeScore'])
            seconds_left = int(season_frames[i].at[row, 'SecLeft'])
            quarter = season_frames[i].at[row, 'Quarter']


            #If the game being analyzed goes to overtime, remove that game from the dictionary of games
            if quarter >= 5:
                games_dict.pop(game_id)

            #################### ASSESS EACH ROW AGAINST INCIDENCE VARIABLES ####################

            ###which team scores first?
            home_team_scores_first = (quarter == 1) and (away_score == 0 and (home_score <= 3 and home_score > 0))
            away_team_scores_first = (quarter == 1) and (home_score == 0 and (away_score <= 3 and away_score > 0))

            if home_team_scores_first:
                games_dict[game_id].update({'home_team_scores_first' : True})
                games_dict[game_id].update({'away_team_scores_first' : False})
            if away_team_scores_first:
                games_dict[game_id].update({'home_team_scores_first' : False})
                games_dict[game_id].update({'away_team_scores_first' : True})
            

            ###Does the home team lead after first?
            is_end_of_first = (quarter == 1 and home_play == 'End of 1st quarter' or away_play == 'End of 1st quarter')

            if is_end_of_first and home_score > away_score:
                games_dict[game_id].update({'home_leads_after_first' : True})
                games_dict[game_id].update({'away_leads_after_first' : False})
            elif is_end_of_first and home_score < away_score:
                games_dict[game_id].update({'home_leads_after_first' : False})
                games_dict[game_id].update({'away_leads_after_first' : True})
            elif is_end_of_first and home_score == away_score:
                games_dict[game_id].update({'home_leads_after_first' : 'Tie'})
                games_dict[game_id].update({'away_leads_after_first' : 'Tie'})
            
            ###Does the home team lead after second?
            is_end_of_second = (quarter == 2 and home_play  == 'End of 2nd quarter' or away_play == 'End of 2nd quarter')

            if is_end_of_second and home_score > away_score:
                games_dict[game_id].update({'home_leads_after_second' : True})
                games_dict[game_id].update({'away_leads_after_second' : False}) 
            elif is_end_of_second and home_score < away_score:
                games_dict[game_id].update({'home_leads_after_second' : False})
                games_dict[game_id].update({'away_leads_after_second' : True})
            elif is_end_of_second and home_score == away_score:
                games_dict[game_id].update({'home_leads_after_second' : 'Tie'})
                games_dict[game_id].update({'away_leads_after_second' : 'Tie'})


            ###Does the home team lead after third?
            is_end_of_third = (quarter == 3 and home_play == 'End of 3rd quarter' or away_play == 'End of 3rd quarter')

            if is_end_of_third and home_score > away_score:
                games_dict[game_id].update({'home_leads_after_third' : True})
                games_dict[game_id].update({'away_leads_after_third' : False})
            elif is_end_of_third and home_score < away_score:
                games_dict[game_id].update({'home_leads_after_third' : False})
                games_dict[game_id].update({'away_leads_after_third' : False})
            elif is_end_of_third and home_score == away_score:
                games_dict[game_id].update({'home_leads_after_third' : 'Tie'})
                games_dict[game_id].update({'away_leads_after_third' : 'Tie'})


            ###Does the home team lead during the fourth?
            is_middle_of_fourth = (quarter == 4 and (seconds_left > 240 and seconds_left <= 480))
            if is_middle_of_fourth and home_score > away_score:
                games_dict[game_id].update({'home_leads_mid_fourth' : True})
                games_dict[game_id].update({'away_leads_mid_fourth' : False})
            elif is_middle_of_fourth and home_score < away_score:
                games_dict[game_id].update({'home_leads_mid_fourth' : False})
                games_dict[game_id].update({'away_leads_mid_fourth' : True})
            elif is_middle_of_fourth and home_score == away_score:
                games_dict[game_id].update({'home_leads_mid_fourth' : 'Tie'})
                games_dict[game_id].update({'away_leads_mid_fourth' : 'Tie'})

    #Create a new data frame from the dictionary created in the for loop
    games_frame = pd.DataFrame.from_dict(games_dict, orient='index')
    games_frame.to_excel("games_out.xlsx")
    return games_frame


