from flask import Flask, request, render_template, redirect
from flask import send_from_directory

from mongoengine import Document, StringField, DateTimeField, connect

import os
import datetime
import tasks

app = Flask(__name__)
app.debug = True


class Entry(Document):
    name = StringField()
    zip = StringField()
    timestamp = DateTimeField()


@app.route("/", methods=["GET", ])
def index():
    """List all the entries."""
    all_entries = Entry.objects
    return render_template("index.html", entries=all_entries)


@app.route("/new", methods=["GET", "POST", ])
def sign():
    """Allow users to create new entries."""
    if request.method == "GET":
        return render_template("new.html")
    else:
        the_zip = request.form["the_zip"]
        current_time = datetime.datetime.now()

        entry = Entry(
            zip=the_zip,
            timestamp=current_time
        )
        entry.save()
        tasks.lookup.delay(entry.id)
        return redirect("/")  # Redirect after POST is Good Behavor!


@app.route("/styles/<path:filename>")
def styles(filename):
    """Allow Flask to server our CSS files."""
    return send_from_directory("styles", filename)


if __name__ == "__main__":
    host = "localhost"
    port = int(os.getenv("PORT", 5000))
    if port != 5000:
        host = "0.0.0.0"
    else:
        connect("mempyflaskcelery")  # A MongoDB connection
    app.run(port=port, host=host)
