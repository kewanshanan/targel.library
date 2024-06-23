
from flask import Flask, render_template, request, redirect, url_for, flash
from library import Library
from book import Book

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey'
library = Library()

@app.route('/')
def index():
    books = library.list_books()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        genre = request.form['genre']
        book = Book(title, author, int(publication_year), genre)
        if not any(b.title == book.title and b.author == book.author for b in library.books):
            library.add_book(book)
            flash('Book added successfully!')
        else:
            flash('Book already exists in the library.')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:book_index>', methods=['GET', 'POST'])
def edit_book(book_index):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        genre = request.form['genre']
        library.edit_book(book_index, title, author, int(publication_year), genre)
        flash('Book updated successfully!')
        return redirect(url_for('index'))
    book = library.books[book_index]
    return render_template('edit_book.html', book=book, index=book_index)

@app.route('/delete/<int:book_index>', methods=['POST'])
def delete_book(book_index):
    library.delete_book(book_index)
    flash('Book deleted successfully!')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        query = request.form['query']
        filtered_books = library.filter_books(author=query)
        return render_template('search.html', books=filtered_books, query=query)
    return render_template('search.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/save_and_exit')
def save_and_exit():
    library.save_and_exit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

##End
