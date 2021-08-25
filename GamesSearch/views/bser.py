from flask import Blueprint, render_template, request
from urllib import parse
import requests
import json
import math
import time
import datetime
import os

from werkzeug.utils import redirect
from ..config import *
from GamesSearch.module import dbModule

bser_BluePrint = Blueprint("bser", __name__, url_prefix="/bser")

@bser_BluePrint.route("/")
def function_bser_main():
    return render_template("bser/index.html")

@bser_BluePrint.route("/Recall")
def function_bser_recall():
    enter_Player_Name = request.args.get("nickname")
    encode_Player_Name = parse.quote(enter_Player_Name)

    userNum_Url = f"https://open-api.bser.io/v1/user/nickname?query={encode_Player_Name}"
    userNum_Get = requests.get(userNum_Url, headers={"x-api-key": BSER["API_KEY"]})
    userNum_Json = json.loads(userNum_Get.content)

    #get api-site
    #print("API 받아옴")
    normalStats_Url = f'https://open-api.bser.io/v1/user/stats/{userNum_Json["user"]["userNum"]}/0'
    normalStats_Get = requests.get(normalStats_Url, headers={"x-api-key": BSER["API_KEY"]})
    normalStats_Json = json.loads(normalStats_Get.content)

    print(normalStats_Json)

    #Solo, Duo, Squad
    Solo = 1
    Duo = 2
    Squad = 3

    normal_soloJson = {}
    normal_duoJson = {}
    normal_squadJson = {}

    for i in range(len(normalStats_Json["userStats"])):
        temp_mmr = normalStats_Json["userStats"][i]["mmr"]
        temp_rankRate = round(normalStats_Json["userStats"][i]["rank"] / normalStats_Json["userStats"][i]["rankSize"] * 100, 2)
        temp_totalGames = normalStats_Json["userStats"][i]["totalGames"]
        temp_totalWins = normalStats_Json["userStats"][i]["totalWins"]
        temp_avgRank = normalStats_Json["userStats"][i]["averageRank"]
        temp_avgKills = normalStats_Json["userStats"][i]["averageKills"]
        temp_avgAssistants = normalStats_Json["userStats"][i]["averageAssistants"]
        temp_avgHunts = normalStats_Json["userStats"][i]["averageHunts"]
        temp_top1 = normalStats_Json["userStats"][i]["top1"]
        temp_top2 = normalStats_Json["userStats"][i]["top2"]
        temp_top3 = normalStats_Json["userStats"][i]["top3"]

        temp_characterCode = []
        temp_characterTotalGames = []
        temp_characterMaxKillings = []
        temp_characterTop3 = []
        temp_characterWins = []
        temp_characterAvgRank = []

        for j in range(len(normalStats_Json["userStats"][i]["characterStats"])):
            temp_characterCode.append(normalStats_Json["userStats"][i]["characterStats"][j]["characterCode"])
            temp_characterTotalGames.append(normalStats_Json["userStats"][i]["characterStats"][j]["totalGames"])
            temp_characterMaxKillings.append(normalStats_Json["userStats"][i]["characterStats"][j]["maxKillings"])
            temp_characterTop3.append(normalStats_Json["userStats"][i]["characterStats"][j]["top3"])
            temp_characterWins.append(normalStats_Json["userStats"][i]["characterStats"][j]["wins"])
            temp_characterAvgRank.append(normalStats_Json["userStats"][i]["characterStats"][j]["averageRank"])

        if temp_mmr >= 0 and temp_mmr < 1:
            temp_tier = "img/BSER/Rank/Unrank.png"
        elif temp_mmr >= 1 and temp_mmr < 400:
            temp_tier = "img/BSER/Rank/Iron.png"
        elif temp_mmr >= 400 and temp_mmr < 700:
            temp_tier = "img/BSER/Rank/Bronze.png"
        elif temp_mmr >= 700 and temp_mmr < 1100:
            temp_tier = "img/BSER/Rank/Silver.png"
        elif temp_mmr >= 1100 and temp_mmr < 1600:
            temp_tier = "img/BSER/Rank/Gold.png"
        elif temp_mmr >= 1600 and temp_mmr < 2000:
            temp_tier = "img/BSER/Rank/Platinum.png"
        elif temp_mmr >= 2000 and temp_mmr < 2400:
            temp_tier = "img/BSER/Rank/Diamond.png"
        elif temp_mmr >= 2400:
            temp_tier = "img/BSER/Rank/Titan.png"

        temp_Json = {
            "mmr": temp_mmr,
            "tier": temp_tier,
            "rankRate": temp_rankRate,
            "totalGames": temp_totalGames,
            "totalWins": temp_totalWins,
            "avgRank": temp_avgRank,
            "avgKills": temp_avgKills,
            "avgAssistants": temp_avgAssistants,
            "avgHunts": temp_avgHunts,
            "top1": temp_top1,
            "top2": temp_top2,
            "top3": temp_top3,
            "characterCode": temp_characterCode,
            "characterTotalGames": temp_characterTotalGames,
            "characterMaxKillings": temp_characterMaxKillings,
            "characterTop3": temp_characterTop3,
            "characterWins": temp_characterWins,
            "characterAvgRank": temp_characterAvgRank
        }

        #Solo, Duo, Squad
        if normalStats_Json["userStats"][i]["matchingTeamMode"] == Solo:
            normal_soloJson = temp_Json
        elif normalStats_Json["userStats"][i]["matchingTeamMode"] == Duo:
            normal_duoJson = temp_Json
        elif normalStats_Json["userStats"][i]["matchingTeamMode"] == Squad:
            normal_squadJson = temp_Json

    empty_Json = {
            "mmr": 0,
            "tier": "img/BSER/Rank/Unrank.png",
            "rankRate": 0,
            "totalGames": 0,
            "totalWins": 0,
            "avgRank": 0,
            "avgKills": 0,
            "avgAssistants": 0,
            "avgHunts": 0,
            "top1": 0,
            "top2": 0,
            "top3": 0,
            "characterCode": [],
            "characterTotalGames": [],
            "characterMaxKillings": [],
            "characterTop3": [],
            "characterWins": [],
            "characterAvgRank": []
        }

    if normal_soloJson == {}:
        normal_soloJson = empty_Json
    
    if normal_duoJson == {}:
        normal_duoJson = empty_Json

    if normal_squadJson == {}:
        normal_squadJson = empty_Json

    DB_Class = dbModule.Database()
    SQL = f'UPDATE EternalReturn2 SET userNum={userNum_Json["user"]["userNum"]}, userName=\'{userNum_Json["user"]["nickname"]}\', updateTime=\'{time.strftime("%Y-%m-%d %H:%M:%S")}\', normalSoloJson=\'{json.dumps(normal_soloJson)}\', normalDuoJson=\'{json.dumps(normal_duoJson)}\', normalSquadJson=\'{json.dumps(normal_squadJson)}\' WHERE userNum = {userNum_Json["user"]["userNum"]};'
    #print(SQL)
    DB_Class.execute(SQL)
    DB_Class.commit()

    return redirect(f"/bser/Player?nickname={enter_Player_Name}")

@bser_BluePrint.route("/Player")
def function_bser_player():
    enter_Player_Name = request.args.get("nickname")
    encode_Player_Name = parse.quote(enter_Player_Name)
    return render_template("bser/player2.html", playerName=enter_Player_Name)
#     enter_Player_Name = request.args.get("nickname")
#     encode_Player_Name = parse.quote(enter_Player_Name)

#     userNum_Url = f"https://open-api.bser.io/v1/user/nickname?query={encode_Player_Name}"
#     userNum_Get = requests.get(userNum_Url, headers={"x-api-key": BSER["API_KEY"]})
#     userNum_Json = json.loads(userNum_Get.content)

#     #check Result - Can`t find User
#     if userNum_Json["code"] == 404:
#         return render_template("bser/error.html", playerName=enter_Player_Name)

#     #connect db
#     DB_Class = dbModule.Database()
#     SQL = "SELECT * FROM EternalReturn2"
#     ROW = DB_Class.executeAll(SQL)

#     check_DB = False

#     #for db
#     for i in range(len(ROW)):
#         if ROW[i]["userNum"] == userNum_Json["user"]["userNum"]:
#             #get db
#             check_DB = True

#             normal_soloJson = json.loads(ROW[i]["normalSoloJson"])
#             normal_duoJson = json.loads(ROW[i]["normalDuoJson"])
#             normal_squadJson = json.loads(ROW[i]["normalSquadJson"])
            
#             now = datetime.datetime.now()
#             updateTime = ROW[i]["updateTime"]

#             updatedTime = now - ROW[i]["updateTime"]

#             updatedTime_Days = updatedTime.days
#             updatedTime_Minutes = math.trunc(updatedTime.seconds / 60)
#             updatedTime_Secondes = updatedTime.seconds % 60

#             if updatedTime_Minutes >= 60:
#                 updatedTime_Hours = math.trunc(updatedTime_Minutes / 60)
#                 updatedTime_Minutes = updatedTime_Minutes % 60

#             #days up to 0
#             if updatedTime_Days > 0:
#                 if updatedTime_Days >= 30:
#                     updatedTime_Months = math.trunc(updatedTime_Days / 30)

#                     if updatedTime_Months >= 12:
#                         updatedTime_Years = math.trunc(updatedTime_Months / 12)
#                         return_Time = f"{updatedTime_Years}년"

#                     else:
#                         return_Time = f"{updatedTime_Months}개월"
#                 else:
#                     return_Time = f"{updatedTime_Days}일"

#             else:
#                 #print(updatedTime.seconds)
#                 #print(math.trunc(updatedTime.seconds / 60 / 60))
#                 if math.trunc(updatedTime.seconds / 60 / 60) >= 1:
#                     updatedTime_Hours = math.trunc(updatedTime.seconds / 60 / 60)
#                     return_Time = f"{updatedTime_Hours}시간"

#                 elif updatedTime_Minutes >= 1:
#                     return_Time = f"{updatedTime_Minutes}분"
#                 else:
#                     return_Time = f"{updatedTime_Secondes}초"

#     #check db
#     if check_DB == False:
#         #get api-site
#         #print("API 받아옴")
#         normalStats_Url = f'https://open-api.bser.io/v1/user/stats/{userNum_Json["user"]["userNum"]}/0'
#         normalStats_Get = requests.get(normalStats_Url, headers={"x-api-key": BSER["API_KEY"]})
#         normalStats_Json = json.loads(normalStats_Get.content)

#         #print(normalStats_Json)

#         #Solo, Duo, Squad
#         Solo = 1
#         Duo = 2
#         Squad = 3

#         normal_soloJson = {}
#         normal_duoJson = {}
#         normal_squadJson = {}

#         for i in range(len(normalStats_Json["userStats"])):
#             temp_mmr = normalStats_Json["userStats"][i]["mmr"]
#             temp_rankRate = round(normalStats_Json["userStats"][i]["rank"] / normalStats_Json["userStats"][i]["rankSize"] * 100, 2)
#             temp_totalGames = normalStats_Json["userStats"][i]["totalGames"]
#             temp_totalWins = normalStats_Json["userStats"][i]["totalWins"]
#             temp_avgRank = normalStats_Json["userStats"][i]["averageRank"]
#             temp_avgKills = normalStats_Json["userStats"][i]["averageKills"]
#             temp_avgAssistants = normalStats_Json["userStats"][i]["averageAssistants"]
#             temp_avgHunts = normalStats_Json["userStats"][i]["averageHunts"]
#             temp_top1 = round(normalStats_Json["userStats"][i]["top1"] * 100, 2)
#             temp_top2 = round(normalStats_Json["userStats"][i]["top2"] * 100, 2)
#             temp_top3 = round(normalStats_Json["userStats"][i]["top3"] * 100, 2)

#             #print(temp_top1)

#             temp_characterCode = []
#             temp_characterTotalGames = []
#             temp_characterMaxKillings = []
#             temp_characterTop3 = []
#             temp_characterWins = []
#             temp_characterAvgRank = []

#             for j in range(len(normalStats_Json["userStats"][i]["characterStats"])):
#                 temp_characterCode.append(normalStats_Json["userStats"][i]["characterStats"][j]["characterCode"])
#                 temp_characterTotalGames.append(normalStats_Json["userStats"][i]["characterStats"][j]["totalGames"])
#                 temp_characterMaxKillings.append(normalStats_Json["userStats"][i]["characterStats"][j]["maxKillings"])
#                 temp_characterTop3.append(normalStats_Json["userStats"][i]["characterStats"][j]["top3"])
#                 temp_characterWins.append(normalStats_Json["userStats"][i]["characterStats"][j]["wins"])
#                 temp_characterAvgRank.append(normalStats_Json["userStats"][i]["characterStats"][j]["averageRank"])

#             if temp_mmr >= 0 and temp_mmr < 1:
#                 temp_tier = "img/BSER/Rank/Unrank.png"
#             elif temp_mmr >= 1 and temp_mmr < 400:
#                 temp_tier = "img/BSER/Rank/Iron.png"
#             elif temp_mmr >= 400 and temp_mmr < 700:
#                 temp_tier = "img/BSER/Rank/Bronze.png"
#             elif temp_mmr >= 700 and temp_mmr < 1100:
#                 temp_tier = "img/BSER/Rank/Silver.png"
#             elif temp_mmr >= 1100 and temp_mmr < 1600:
#                 temp_tier = "img/BSER/Rank/Gold.png"
#             elif temp_mmr >= 1600 and temp_mmr < 2000:
#                 temp_tier = "img/BSER/Rank/Platinum.png"
#             elif temp_mmr >= 2000 and temp_mmr < 2400:
#                 temp_tier = "img/BSER/Rank/Diamond.png"
#             elif temp_mmr >= 2400:
#                 temp_tier = "img/BSER/Rank/Titan.png"

#             temp_Json = {
#                 "mmr": temp_mmr,
#                 "tier": temp_tier,
#                 "rankRate": temp_rankRate,
#                 "totalGames": temp_totalGames,
#                 "totalWins": temp_totalWins,
#                 "avgRank": temp_avgRank,
#                 "avgKills": temp_avgKills,
#                 "avgAssistants": temp_avgAssistants,
#                 "avgHunts": temp_avgHunts,
#                 "top1": temp_top1,
#                 "top2": temp_top2,
#                 "top3": temp_top3,
#                 "characterCode": temp_characterCode,
#                 "characterTotalGames": temp_characterTotalGames,
#                 "characterMaxKillings": temp_characterMaxKillings,
#                 "characterTop3": temp_characterTop3,
#                 "characterWins": temp_characterWins,
#                 "characterAvgRank": temp_characterAvgRank
#             }

#             #Solo, Duo, Squad
#             if normalStats_Json["userStats"][i]["matchingTeamMode"] == Solo:
#                 normal_soloJson = temp_Json
#             elif normalStats_Json["userStats"][i]["matchingTeamMode"] == Duo:
#                 normal_duoJson = temp_Json
#             elif normalStats_Json["userStats"][i]["matchingTeamMode"] == Squad:
#                 normal_squadJson = temp_Json

#         empty_Json = {
#             "mmr": 0,
#             "tier": "img/BSER/Rank/Unrank.png",
#             "rankRate": 0,
#             "totalGames": 0,
#             "totalWins": 0,
#             "avgRank": 0,
#             "avgKills": 0,
#             "avgAssistants": 0,
#             "avgHunts": 0,
#             "top1": 0,
#             "top2": 0,
#             "top3": 0,
#             "characterCode": [],
#             "characterTotalGames": [],
#             "characterMaxKillings": [],
#             "characterTop3": [],
#             "characterWins": [],
#             "characterAvgRank": []
#         }

#         if normal_soloJson == {}:
#             normal_soloJson = empty_Json
        
#         if normal_duoJson == {}:
#             normal_duoJson = empty_Json

#         if normal_squadJson == {}:
#             normal_squadJson = empty_Json

#         while True:
#             games_Url = f'https://open-api.bser.io/v1/user/games/{userNum_Json["user"]["userNum"]}'
#             games_Get = requests.get(games_Url, headers={"x-api-key": BSER["API_KEY"]})
#             games_Json = json.loads(games_Get.content)

#             if games_Json["message"] == "Success":
#                 break

#         gameData = []
        
#         for i in range(len(games_Json["userGames"])):
#             gameData.append(parse_Game(games_Json["userGames"][i]["gameId"], userNum_Json["user"]["userNum"]))
        
#         #for j in range(len(gameData)):
#         #    print(gameData[j])
#         #    print("======================")

#         #print(gameData)

#         DB_Class = dbModule.Database()
#         SQL = f'INSERT INTO EternalReturn2 VALUES ({userNum_Json["user"]["userNum"]}, \'{userNum_Json["user"]["nickname"]}\', \'{time.strftime("%Y-%m-%d %H:%M:%S")}\', \'{json.dumps(normal_soloJson)}\', \'{json.dumps(normal_duoJson)}\', \'{json.dumps(normal_squadJson)}\');'
#         #print(SQL)
#         #DB_Class.execute(SQL)
#         #DB_Class.commit()
#         return_Time = "방금"

#     teamType = ["solo", "duo", "squad"]
#     teamType_Kor = ["솔로", "듀오", "스쿼드"]
#     color = [0.8, 0.5, 0.8]

#     return render_template("bser/player.html", playerName=enter_Player_Name, updatedTime=return_Time, teamType=teamType, teamType_Kor=teamType_Kor, color=color, normal={"solo": normal_soloJson, "duo": normal_duoJson, "squad": normal_squadJson}, games=gameData)

# def parse_Game(gameId, userId):
#     while True:
#         game_Url = f'https://open-api.bser.io/v1/games/{gameId}'
#         game_Get = requests.get(game_Url, headers={"x-api-key": BSER["API_KEY"]})
#         game_Json = json.loads(game_Get.content)

#         if game_Json["message"] == "Success":
#             break
#         #else:
#             #print(game_Json["message"])
        
#     userName_List = []
#     character_Eng_List = []
#     character_Kor_List = []
#     equipment_List = []
#     teamNum_List = []
#     Rank_List = []
#     Kill_List = []
#     Assistant_List = []
#     Hunt_List = []

#     character_Code = []
#     character_Eng_Name = []
#     character_Kor_Name = []

#     with open(f"./GamesSearch/static/json/BSER_Character.json", "r", encoding="utf-8") as f:
#         character_Data = json.load(f)

#     for i in range(len(character_Data["data"])):
#         character_Code.append(character_Data["data"][i]["code"])
#         character_Eng_Name.append(character_Data["data"][i]["name"])
#         character_Kor_Name.append(character_Data["data"][i]["name_Kor"])

#     #print(character_Code)
#     #print(character_Eng_Name)
#     #print(character_Kor_Name)

#     for i in range(len(game_Json["userGames"])):
#         character_Eng = character_Eng_Name[character_Code.index(game_Json["userGames"][i]["characterNum"])]
#         character_Kor = character_Kor_Name[character_Code.index(game_Json["userGames"][i]["characterNum"])]

#         if game_Json["userGames"][i]["userNum"] != userId:
#             userName_List.append(game_Json["userGames"][i]["nickname"])
#             character_Eng_List.append(character_Eng)
#             character_Kor_List.append(character_Kor)
#             equipment_List.append(game_Json["userGames"][i]["equipment"])
#             teamNum_List.append(game_Json["userGames"][i]["teamNumber"])
#             Rank_List.append(game_Json["userGames"][i]["gameRank"])
#             Kill_List.append(game_Json["userGames"][i]["playerKill"])
#             Assistant_List.append(game_Json["userGames"][i]["playerAssistant"])
#             Hunt_List.append(game_Json["userGames"][i]["monsterKill"])

#         elif game_Json["userGames"][i]["userNum"] == userId:
#             playerName = game_Json["userGames"][i]["nickname"]
#             playerCharacterEng = character_Eng
#             playerCharacterKor = character_Kor
#             playerMMRGain = game_Json["userGames"][i]["mmrGain"]
#             playerDamageToPlayer = game_Json["userGames"][i]["damageToPlayer"]
#             playerDamageFromPlayer = game_Json["userGames"][i]["damageFromPlayer"]
#             playerRank = game_Json["userGames"][i]["gameRank"]
#             playerKill = game_Json["userGames"][i]["playerKill"]
#             playerAssistant = game_Json["userGames"][i]["playerAssistant"]
#             playerMonsterKill = game_Json["userGames"][i]["monsterKill"]
#             playerWeapon = game_Json["userGames"][i]["bestWeapon"]
#             playerWeaponLv = game_Json["userGames"][i]["bestWeaponLevel"]


#     seasonId = game_Json["userGames"][0]["seasonId"]
#     teamMode = game_Json["userGames"][0]["matchingTeamMode"]
    
#     if teamMode == 1:
#         teamMode_Name = "솔로"
#     elif teamMode == 2:
#         teamMode_Name = "듀오"
#     else:
#         teamMode_Name = "스쿼드"

#     if seasonId == 0:
#         season_Name = "일반"
#     elif seasonId == 1:
#         season_Name = "경쟁전 시즌 1"
#     elif seasonId == 2:
#         season_Name = "경쟁전 프리 시즌 1"
#     elif seasonId == 3:
#         season_Name = "경쟁전 시즌 2"
#     elif seasonId == 4:
#         season_Name = "경쟁전 프리 시즌 2"
#     elif seasonId == 5:
#         season_Name = "경쟁전 시즌 3"

#     temp_gameData = {
#         "seasonName": season_Name,
#         "teamMode": teamMode_Name,
#         "another_player": {
#             "userName_List": userName_List,
#             "character_Eng_List": character_Eng_List,
#             "character_Kor_List": character_Kor_List,
#             "equipment_List": equipment_List,
#             "teamNum_List": teamNum_List,
#             "Rank_List": Rank_List,
#             "Kill_List": Kill_List,
#             "Assistant_List": Assistant_List,
#             "Hunt_List": Hunt_List
#         },
#         "player": {
#             "playerName": playerName,
#             "playerCharacterEng": playerCharacterEng,
#             "playerCharacterKor": playerCharacterKor,
#             "playerMMRGain": playerMMRGain,
#             "playerDamageToPlayer": playerDamageToPlayer,
#             "playerDamageFromPlayer": playerDamageFromPlayer,
#             "playerRank": playerRank,
#             "playerKill": playerKill,
#             "playerAssistant": playerAssistant,
#             "playerMonsterKill": playerMonsterKill,
#             "playerWeapon": playerWeapon,
#             "playerWeaponLv": playerWeaponLv,
#             "playerCharactionImgHalf": f"img/BSER/Character/{playerCharacterEng}_Half.png",
#             "playerCharactionImgMini": f"img/BSER/Character/{playerCharacterEng}_Mini.png",
#         }
#     }

#     return temp_gameData

