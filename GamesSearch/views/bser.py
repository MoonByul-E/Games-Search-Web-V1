from flask import Blueprint, render_template, request
from urllib import parse
import requests
import json
from ..config import *

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

    print(userNum_Json)
    return render_template("bser/player.html", playerName=enter_Player_Name)