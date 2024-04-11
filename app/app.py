
from flask import Flask, request, render_template, Blueprint
import xml.etree.ElementTree as ET

app = Flask(__name__)

class Album:
    def __init__(self, title, release_year, songs):
        self.title = title
        self.release_year = release_year
        self.songs = songs

class Songer:
    def __init__(self, name, city, website, biography, albums):
        self.name = name
        self.city = city
        self.website = website
        self.biography = biography
        self.albums = albums

def load_data():
    songers = []

    tree = ET.parse("artists.xml")
    root = tree.getroot()

    for songer_elem in root.findall("songer"):
        name = songer_elem.find("name").text
        city = songer_elem.find("city").text
        website = songer_elem.find("website").text
        biography = songer_elem.find("biography").text

        albums = []
        for album_elem in songer_elem.find("albums").findall("album"):
            album_title = album_elem.find("title").text
            release_year = int(album_elem.find("release_year").text)

            songs = [song.text for song in album_elem.find("songs").findall("song")]
            album = Album(album_title, release_year, songs)
            albums.append(album)

        songer = Songer(name, city, website, biography, albums)
        songers.append(songer)

    return songers


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html",
                           title = "Homepage",
                           page_head="Artits Search"
                           )


@app.route("/search", methods=['GET', 'POST'])
def search():
    q = request.args.get("q")
    print(q)

    song_data = load_data()

    if q:
        results = [songer for songer in song_data if q.lower() in songer.name.lower()]
    else:
        results = []

    return render_template("search_results.html",
                            results=results,
                           custom_css="search_results")
