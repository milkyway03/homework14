import sqlite3
from collections import Counter

from flask import Flask, request, jsonify

app = Flask(__name__)


def db_connect(db, query):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result


def get_rating(rating):
    response = []
    if len(rating) > 1:
        str_rating = "','".join(rating)
    else:
        str_rating = "".join(rating)
    print(str_rating)
    query = f'''SELECT `title`, `country`, `release_year`, `listed_in`, `description`, `rating`
                    FROM netflix
                    WHERE rating in ('{str_rating}')
                    LIMIT 100'''
    result = db_connect('netflix.db', query)
    for line in result:
        line_dict = {
            "title": line[0],
            "rating": line[1],
            "description": line[2]
        }
        response.append(line_dict)
    return response


@app.route('/movie/title')
def search_title():
    if request.method == 'GET':
        response = {}
        title = request.args.get('title')
        if title:
            query = f'''
            select
                title,
                country,
                listed_in,
                release_year,
                description
            from netflix
            where title = '{title}'
            order by release_year DESC
            LIMIT 1
            '''
            result = db_connect('netflix.db', query)
            if len(result):
                response = {
                    "title": result[0][0],
                    "country": result[0][0],
                    "listed_in": result[0][0],
                    "release_year": result[0][0],
                    "description": result[0][0],
                }
        return jsonify(response)


@app.route("/movie/year/")
def search_year():
    if request.method == 'GET':
        response = []
        start_year = request.args.get('start_year')
        end_year = request.args.get('end_year')
        if start_year and end_year:
            query = f'''
            select title, release_year
            from netflix
            where release_year between {start_year} and {end_year}
            limit 100
            '''
            result = db_connect('netflix.db', query)
            for line in result:
                line_dict = {
                    "title": line[0],
                    "release_year": line[1]
                }
                response. append(line_dict)
        return jsonify(response)


@app.route("/rating/children/")
def rating_children():
    response = get_rating(['G'])
    return jsonify(response)


@app.route("/rating/family/")
def rating_family():
    response = get_rating(['PG', 'PG-13'])
    return jsonify(response)


@app.route("/rating/adult/")
def rating_adult():
    response = get_rating(['R', 'NC-17'])
    return jsonify(response)


@app.route("/genre/<genre>")
def search_genre(genre):
    query = f"""SELECT title, description FROM netflix
                WHERE listed_in like "%{genre}%"
                ORDER BY release_year DESC
                LIMIT 10"""
    result = db_connect('netflix.db', query)
    response = []
    for line in result:
        line_dict = {
            "title": line[0],
            "description": line[1]
        }
        response.append(line_dict)
    return jsonify(response)


def search_pair(actor1, actor2):
    query = f"SELECT \"cast\" FROM netflix " \
            f"WHERE \"cast\" LIKE '%{actor1}%' AND \"cast\" LIKE '%{actor2}%'"
    result = db_connect('netflix.db', query)
    result_list = []
    for line in result:
        line_list = line[0].split(',')
        result_list += line_list
    counter = Counter(result_list)
    print(counter)
    actors_list = []
    for key, value in counter.items():
        if value > 2 and key.strip() not in [actor1, actor2]:
            actors_list.append(key)
    return actors_list


print(search_pair('Rose McIver', 'Ben Lamb'))


app.run(debug=True)
