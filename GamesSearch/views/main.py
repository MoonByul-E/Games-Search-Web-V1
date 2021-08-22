from flask import Blueprint, render_template

main_BluePrint = Blueprint("main", __name__, url_prefix="/")

@main_BluePrint.route("/")
def function_main():
    return render_template("main/index.html")