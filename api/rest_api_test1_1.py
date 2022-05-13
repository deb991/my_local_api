import flask
from flask import request, jsonify
import sqlite3


'''App/API/Server defication'''

app = flask.Flask(__name__)
app.config['Debug'] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('C:\\Users\\002CSC744\\Documents\\my_api\\db\\books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * from books;').fetchall()
    return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 Page not found</h1><p>Resource not found</p>"


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    query = query[:-4] + ';'

    conn = sqlite3.connect('C:\\Users\\002CSC744\\Documents\\my_api\\db\\books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    print('Execution check for query:\t', cur)
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run(debug=True)