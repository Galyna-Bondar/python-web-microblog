import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    client = MongoClient(os.getenv("MONGODB_URI"))
    # client = MongoClient("mongodb+srv://halyna:030592ufp@microblog.vbbur57.mongodb.net/test")
    # connecting to our cluster (database) "microblog" in MongoClient
    app.db = client.Microblog

    # entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        # print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # entries.append((entry_content, formatted_date))
            # saving the content from the form to our database
            app.db.entries.insert_one(
                {"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            # for entry in entries
            for entry in app.db.entries.find({})
            # it's going to find all the entries in MongoDB and give it back to us as a list of dictionaries, but actially a Cursos Object, but behaves like a list
        ]

        return render_template("home.html", entries=entries_with_date)

    return app


# terminal bash $:
# pip freeze   -> shows everything that you have installed
