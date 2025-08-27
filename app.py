from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
BOOKS_FILE = 'books.json'

def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_books(books):
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    books = load_books()

    # Ako je POST, dodaj novu knjigu
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        genre = request.form['genre']
        rating = int(request.form['rating'])
        books.append({'author': author, 'title': title, 'genre': genre, 'rating': rating})
        save_books(books)
        return redirect('/')

    # Filter i sortiranje
    sort_by = request.args.get('sort', 'rating')
    genre_filter = request.args.get('genre', None)
    filtered_books = books
    if genre_filter:
        filtered_books = [b for b in books if b['genre'].lower() == genre_filter.lower()]
    if sort_by == 'rating':
        filtered_books.sort(key=lambda x: x['rating'], reverse=True)

    genres = sorted(list(set([b['genre'] for b in books])))

    return render_template('index.html', books=filtered_books, genres=genres)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
