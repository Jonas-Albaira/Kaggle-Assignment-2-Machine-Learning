#Jonas Albaira - Assignment 2
from __future__ import print_function, division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
palette = sns.color_palette('deep', 5)
palette[1], palette[2] = palette[2], palette[1]

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.metrics import classification_report, accuracy_score

#######################################################################
#                             TRAINING DATA                           #
#######################################################################
nba_k = pd.read_csv('train.csv')

action_type_k = pd.get_dummies(nba_k["ACTION_TYPE"])
shot_type_k = pd.get_dummies(nba_k["SHOT_TYPE"])
shot_zone_area_k = pd.get_dummies(nba_k["SHOT_ZONE_AREA"])
shot_zone_basic_k = pd.get_dummies(nba_k["SHOT_ZONE_BASIC"])
shot_zone_range_k = pd.get_dummies(nba_k["SHOT_ZONE_RANGE"])

nba_k = nba_k.drop(["ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_AREA","SHOT_ZONE_BASIC","SHOT_ZONE_RANGE", "EVENTTIME",
                    "GAME_DATE","GAME_ID","HTM","LOC_X","LOC_Y","MINUTES_REMAINING","PERIOD","PLAYER_ID","PLAYER_NAME",
                    "SHOT_ATTEMPTED_FLAG","SHOT_TIME","TEAM_ID","TEAM_NAME","VTM"], axis=1)

nba_k = pd.concat([nba_k,action_type_k,shot_type_k,shot_zone_area_k,shot_zone_basic_k,shot_zone_range_k], axis=1)

X_train_k = nba_k.drop(["SHOT_MADE_FLAG","GAME_EVENT_ID"], axis=1)
y_train_k = nba_k["SHOT_MADE_FLAG"]

#
# fitting is equal to training.
# Then, after it is trained,
# the model can be used to make predictions,
# usually with a .predict() method call.
#
#In this case, training dataframe using LogiscticRegression()
#
#Train X_train(no SHOT_MADE_FLAG) dataframe based on y_train dataframe(without SHOT_MADE_FLAG)
#
logmodel = LogisticRegression()

logmodel.fit(X_train_k, y_train_k)

# generate training data predictions
predictions_k = logmodel.predict(X_train_k)

# display the classification report for training data
print(classification_report(y_train_k, predictions_k))
print("Accuracy: {}".format(accuracy_score(y_train_k, predictions_k)))


#######################################################################
#                             SOLUTION                                #
#######################################################################
nba = pd.read_csv('solution_no_answer.csv')

#Convert categorical variable into dummy/indicator variables
action_type = pd.get_dummies(nba["ACTION_TYPE"])
shot_type = pd.get_dummies(nba["SHOT_TYPE"])
shot_zone_area = pd.get_dummies(nba["SHOT_ZONE_AREA"])
shot_zone_basic = pd.get_dummies(nba["SHOT_ZONE_BASIC"])
shot_zone_range = pd.get_dummies(nba["SHOT_ZONE_RANGE"])

#Return new object with labels in requested axis removed.
nba = nba.drop(["ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_AREA","SHOT_ZONE_BASIC","SHOT_ZONE_RANGE",
                "EVENTTIME","GAME_DATE","HTM","LOC_X","LOC_Y","MINUTES_REMAINING","PERIOD","PLAYER_ID","PLAYER_NAME","SHOT_ATTEMPTED_FLAG",
                "SHOT_TIME","TEAM_ID","TEAM_NAME","VTM"], axis=1)

#combine all headers
nba = pd.concat([nba, action_type, shot_type, shot_zone_area, shot_zone_basic, shot_zone_range], axis=1)

# define feature data (test data)
X_test = nba.drop('GAME_EVENT_ID', axis=1)

# add missing headers to the dataframe (test data)
X_test['Running Alley Oop Layup Shot'] = pd.Series(0, X_test.index)
X_test['Driving Jump Shot'] = pd.Series(0, X_test.index)


# generate predictions for the test data
predictions = logmodel.predict(X_test)

competition_entry = pd.DataFrame({"GAME_EVENT_ID": nba["GAME_EVENT_ID"], "SHOT_MADE_FLAG": predictions})
competition_entry.to_csv("competition-entry.csv", index=False)
