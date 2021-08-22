from flask import Blueprint, render_template

lol_BluePrint = Blueprint("lol", __name__, url_prefix="/lol")

@lol_BluePrint.route("/")
def function_lol_main():
    return render_template("lol/index.html")