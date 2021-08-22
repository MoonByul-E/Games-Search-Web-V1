from flask import Blueprint, render_template, request
from urllib import parse
import requests
import json
import pymysql
from ..config import *
from GamesSearch.module import dbModule

bser_BluePrint = Blueprint("bser", __name__, url_prefix="/bser")

@bser_BluePrint.route("/")
def function_bser_main():
    return render_template("bser/index.html")

@bser_BluePrint.route("/Player")
def function_bser_player():
    enter_Player_Name = request.args.get("nickname")
    encode_Player_Name = parse.quote(enter_Player_Name)

    userNum_Url = f"https://open-api.bser.io/v1/user/nickname?query={encode_Player_Name}"
    userNum_Get = requests.get(userNum_Url, headers={"x-api-key": BSER["API_KEY"]})
    userNum_Json = json.loads(userNum_Get.content)

    #check Result - Can`t find User
    if userNum_Json["code"] == 404:
        return render_template("bser/error.html", playerName=enter_Player_Name)

    #connect db
    DB_Class = dbModule.Database()
    SQL = "SELECT * FROM EternalReturn"
    ROW = DB_Class.executeAll(SQL)

    #for db
    for i in range(len(ROW)):
        if ROW[i]["userNum"] == userNum_Json["user"]["userNum"]:
            #get db
            print("DB에서 긁어옴")
        else:
            #get api-site
            normalStats_Url = f'https://open-api.bser.io/v1/user/stats/{userNum_Json["user"]["userNum"]}/0'
            normalStats_Get = requests.get(normalStats_Url, headers={"x-api-key": BSER["API_KEY"]})
            normalStats_Json = json.loads(normalStats_Get.content)

            print(normalStats_Json)

    print(userNum_Json)
    return render_template("bser/player.html", playerName=enter_Player_Name)