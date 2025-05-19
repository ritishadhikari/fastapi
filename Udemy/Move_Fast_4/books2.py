from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional


app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date:int

    def __init__(self, id, title, author, description, rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="Id not required", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description : str=Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,le=5)
    published_date: int=Field(gt=1999, lt=2031)

    model_config={
        "examples":{
            "title":"Computer Science Pro",
            "author":"codingwithroby",
            "description":"A very  nice book",
            "rating":5,
            "published_date":2029
        }
        }
BOOKS=[
    BookRequest(id=1, title="Computer Science Pro",author="codingwithroby",description="A very  nice book",rating=5,published_date=2030),
    BookRequest(id=2, title="Be Fast with Fast API",author="codingwithroby",description="This is a great book",rating=5,published_date=2030),
    BookRequest(id=3, title="Master Endpoints",author="codingwithroby",description="An awesome book",rating=5,published_date=2029),
    BookRequest(id=4, title="HP1",author="Author 1",description="Book description",rating=2,published_date=2028),
    BookRequest(id=5, title="HP2",author="Author 2",description="Book description",rating=3,published_date=2027),
    BookRequest(id=6, title="HP3",author="Author 3",description="Book description",rating=1,published_date=2026)
]

@app.get(path="/books")
async def read_all_books():
    return BOOKS


async def find_book_id(book:Book):
    if len(BOOKS):
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book

@app.post(path="/create_book")
async def create_book(book_request:BookRequest):  # the incoming request is of type BookRequest
    try:
        # Ensuring that the elements in the BOOKS list are of type Book and not BookRequest
        # to maintain consistency
        new_book=Book(**book_request.model_dump())
        new_book=await find_book_id(new_book)
        BOOKS.append(new_book)
        return {"message":"Book created successfully"}
    except Exception as e:
        return {"message":"Book not created"}

@app.get(path="/books/{book_id}")
async def read_book(book_id: int=Path(gt=0)):  # book_id must be greater than 0
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get(path="/books/rating/")
async def read_book_by_rating(book_rating:int=Query(le=5,ge=1)):
    books_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

@app.put(path="/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book

@app.delete(path="/books/delete/{book_id}")
async def delete_books(book_id:int=Path(gt=0)):
    index_nos=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            index_nos.append(i)
    if index_nos:
        for i in index_nos:
            BOOKS.pop(i)
        return {"message":"Books removed successfully!"}
    else:
        return {"message":"Book ID did not match!"}


@app.get(path="/books/publish_date/")
async def read_books_by_publish_date(published_date:int=Query(lt=2031,gt=1999)):
    books_to_return=[]
    for book in BOOKS:
        if book.published_date==published_date:
            books_to_return.append(book)

    return books_to_return