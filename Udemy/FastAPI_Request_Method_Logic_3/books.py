from fastapi import FastAPI

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

@app.get("/books/{dynamic_params}")
async def read_book(dynamic_param:str):
    for book in BOOKS:
        if book.get('title').casefold()==dynamic_param.casefold():
            return {"message":dynamic_param}
    return {"message":"Book not found"}