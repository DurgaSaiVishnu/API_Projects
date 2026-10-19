import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id:str
    title:str
    author:str
    published_year:int
    genre:list[str]
    is_available:bool
    stock:int


def load_data():
    with open("books.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("books.json","w") as f:
        json.dump(data,f,indent=4)



@app.post("/create")
def add_book(book:Book):
    data = load_data()
    ids = [book.get("id") for book in data]
    if book.id  in ids:
        raise HTTPException(status_code=400,detail="book with the same id already exists")
    updated_dict = book.model_dump()
    data.append(updated_dict)
    save_data(data)



@app.get("/") 
def home():
    data = load_data()
    return data


@app.get("/books/{book_id}")
def read_book_info(book_id:str):
    data = load_data()
    book = [book for book in data if book.get("id")==book_id]
    if book is  None:
        raise HTTPException(status_code=404,detail="no book with this id found")
    return book


@app.put("/update")
def update_info(book:Book):
    data = load_data()
    for index,Existing_book in enumerate(data):
        if Existing_book.get("id") == book.id:
            data[index] = book.model_dump()
            break
    save_data(data)


@app.delete("/delete")
def delete(book:Book):
    target_index = None
    data = load_data()
    for index,exist_book in enumerate(data):
        if exist_book.get("id") == book.id:
            target_index = index
    if target_index is None:
        raise HTTPException(status_code=404,detail="book doesnt exist")
    else:
        del data[target_index]
    save_data(data)


