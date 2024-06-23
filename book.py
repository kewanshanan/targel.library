import datetime

class Book:
    def __init__(self, title, author, publication_year, genre, last_updated=None):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.last_updated = last_updated or datetime.datetime.now().replace(microsecond=0)

    def update_last_updated(self):
        self.last_updated = datetime.datetime.now().replace(microsecond=0)

    def __str__(self):
        return f"{self.title} by {self.author}, {self.publication_year}, Genre: {self.genre}, Last Updated: {self.last_updated}"
