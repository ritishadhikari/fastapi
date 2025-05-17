from fastapi import FastAPI
from fastapi import Body

app=FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    # return {"message":"Hello Eric"}
    return BOOKS

# Path Parameters
@app.get("/books/{dynamic_params}")
async def read_book(dynamic_param:str):
    for book in BOOKS:
        if book.get('title').casefold()==dynamic_param.casefold():
            return {"message":dynamic_param}
    return {"message":"Book not found"}

# Query Parameters with Path Parameters
# http://127.0.0.1:8000/books/Title%20Two?category=science
@app.get("/books/{author_name}")
async def read_book_by_author(author_name:str, category:str):
    categories=[]
    for book in BOOKS:
        if book.get('author').casefold()==author_name.casefold() and book.get('category').casefold()==category.casefold():
            categories.append(book)
    
    return categories

# Post Method
@app.post("/books/create_book")
async def create_book (book:dict=Body()):
    BOOKS.append(book)
    return BOOKS

@app.put("/books/update_book")
# {"title": "Title Three", "author": "Author Three", "category": "geography"}
async def update_book(updated_book:dict=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold()==updated_book.get('title').casefold():
            BOOKS[i]=updated_book
    return BOOKS

@app.delete(path="/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold()==book_title.casefold():
            BOOKS.pop(i)
            break
    return BOOKS


@app.get("/book_author/{author_name}")
async def get_books_by_writer(author_name:str):
    books_by_author=[]
    for book in BOOKS:
        print(book)
        if book.get("author").casefold()==author_name.casefold():
            books_by_author.append(book)
    return books_by_author