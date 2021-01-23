######################### Laden der nötigen Packete  ########################
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from funktionen import pickler, entpickler
import pathlib
################  Einlesen des Datensatzes (seperator = ;) #################
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()
races_g = pd.read_csv(DATA_PATH.joinpath("races.csv"), sep = ";")
##########################    Data Preperation   ###########################

## Neuer Datensatz mit allen "finished" races
races_mask = (races_g["status"] == "finished")
races = races_g[races_mask]
races.loc[races["challenger"] == races["winner"], "winner_id"] = "Challenger gewinnt"
races.loc[races["challenger"] != races["winner"], 'winner_id'] = "Challenger verliert"
races = races.drop(["winner", "money" ,"weather", "fuel_consumption", "forecast", "race_created", 'race_driven', "id", "status"], axis=1)

####### Matrix mit erklärenden und zu erklärende Variable #####
X = races.drop('winner_id', axis=1)
y = races['winner_id']

# train/test split für Accuracy gebraucht
# Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
filename = 'finalized_model.sav'
pickler("model.pck", model)