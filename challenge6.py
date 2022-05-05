# Challenge Problem 6
# A step-up from Challenge Problem 5
# Once again, I worked alongside Jake and Josiah!

# Imports for Python
# Pandas will read and write CSV
import pandas as pd
import os
import numpy as np


def import_csv(filename):
    file = pd.read_csv(filename)
    file = sweep(file)
    avgTeamNum, sum_teams, outie, merica = sort(file)
    institution, team = split(file)
    if not os.path.exists(os.path.abspath("./build/")):
        os.mkdir(os.path.abspath("./build/"))
    institution.to_csv("build/Institutions.csv", index=False)
    team.to_csv("build/Team.csv", index=False)

    # writing to csv files
    newFile = open("build/Average Teams for Institutions.txt", 'w')
    newFile.write(f"Average Number of Teams Per Institution: {avgTeamNum}")
    newFile.close()

    sum_teams.to_csv("build/Number_Teams_Entered.csv", index=False)
    outie.to_csv("build/Institution_Outstanding_Ranking.csv", index=False)
    merica.to_csv("build/Meritorious_US.csv", index=False)



def split(file):
    institution = file[["Institution ID", "Institution", "City", "State/Province", "Country"]]
    institution = institution.drop_duplicates(subset=["Institution ID"])
    team = file[["Team Number", "Institution ID", "Advisor", "Problem", "Ranking"]]
    institution = institution.sort_values(["Institution ID"])
    team = team.sort_values(["Team Number"])
    return institution, team

def sweep(file):
    file["Institution"] = file["ï»¿Institution"]
    file = file.drop(["ï»¿Institution"], axis=1)
    for col in file:
        if file.dtypes[col] == object:
            file[f"l_{col}"] = file[col].str.lower().str.strip()
    file["Institution ID"] = file.groupby(["l_Institution", "l_City"]).ngroup()
    return file

def sort(file):
    # Average teams per institution
    avgTeamNum = file[["Institution", "Institution ID", "Team Number"]]
    avgTeamNum = avgTeamNum.groupby(["Institution ID"]).size().reset_index(name="Sum_of_Teams")
    # finding the average number of teams at each institution
    avgTeamNum = np.mean(avgTeamNum['Sum_of_Teams'])
    print(avgTeamNum)

    # List of institutions that entered the most teams
    sum_teams = file[["Institution", "Institution ID", "Team Number"]]
    sum_teams = file.groupby(["Institution", "Institution ID", "Team Number"]).size()\
        .reset_index(name="Most_Teams")\
        .sort_values("Most_Teams", ascending=False)\
        .drop(["Institution ID"], axis=1)
    # list of all institutions
    print(sum_teams)

    # List of "Outstanding" Ranks
    # Looking at the file and seeing if the ranking is true in the sense that it is labeled "outstanding winner"
    outie = file[file["l_Ranking"] == "outstanding winner"]
    # Returns a list of all 19 outstanding winners. Wow!
    print(outie)

    # Looking for Meritorious or ranking higher for schools in the USA
    info = file["l_Ranking"].isin(['meritorious', 'finalist', 'outstanding winner']) & \
           file['l_Country'].isin(["us", "usa"])
    merica = file[info]
    print(merica)

    return avgTeamNum, sum_teams, outie, merica

#main
if __name__ == '__main__':
    import_csv("data/2015.csv")