from flask import Blueprint, render_template

pubg_BluePrint = Blueprint("pubg", __name__, url_prefix="/pubg")

@pubg_BluePrint.route("/")
def function_pubg_main():
    return render_template("pubg/index.html")