from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional


app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="Id not required", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description : str=Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,le=5)

    model_config={
        "examples":{
            "title":"Computer Science Pro",
            "author":"codingwithroby",
            "description":"A very  nice book",
            "rating":5
        }
        }
BOOKS=[
    BookRequest(id=1, title="Computer Science Pro",author="codingwithroby",description="A very  nice book",rating=5),
    BookRequest(id=2, title="Be Fast with Fast API",author="codingwithroby",description="This is a great book",rating=5),
    BookRequest(id=3, title="Master Endpoints",author="codingwithroby",description="An awesome book",rating=5),
    BookRequest(id=4, title="HP1",author="Author 1",description="Book description",rating=2),
    BookRequest(id=5, title="HP2",author="Author 2",description="Book description",rating=3),
    BookRequest(id=6, title="HP3",author="Author 3",description="Book description",rating=1)
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

