import json

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI()

class Character(BaseModel):
    name : str
    show  : str
    height : float
    weight : float



def load_data():
    with open("chars.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("chars.json",'w') as f:
        json.dump(data, f,indent=4)

@app.get("/")
def home():
    return "Anime Characters"

@app.get("/chars")
def characters():
    d = load_data()
    return d

@app.get("/chars/{name}")
def view_char(name:str=Path(description="the name of anime character")):
    data = load_data()
    for character in data:
        if character["name"].lower() == name.lower():
            return character
    raise HTTPException(status_code=404,detail=f"{name} not found")
    
@app.get("/sort")
def sort_chars(sort_by:str = Query(...), order:str = Query(...)):
    valid_fields = ["height","weight"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400)

    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400)
    
    sort_order =  order=="desc" 
    data = load_data()
    sorted_data = sorted(data,key=lambda x: x.get(sort_by,0),reverse=sort_order)
    return sorted_data

@app.post("/create")
def post_character_data(char:Character):
    data = load_data()
    char_name = char.name
    exisiting = [char.get('name') for char in data]
    if char_name  in exisiting:
        raise HTTPException(status_code=400,detail="character already exists")
    new_char_dict = char.model_dump()
    data.append(new_char_dict)
    save_data(data)


@app.put("/update/{name}")
def update_char(char:Character):
    data = load_data()
    existing_names = [char.get('name') for char in data]
    name = char.name
    if name not in existing_names:
        raise HTTPException(status_code=400,detail="character doesnt exist")
    for id,char_info in enumerate(data):
        if char_info.get('name') == name:
            updated_dict = char.model_dump()
            data[id] = updated_dict
            break
    save_data(data)

@app.delete("/Delete")
def delete_Char(char:Character):
    data = load_data()
    exisiting_names = [char.get("name") for char in data]
    name = char.name
    if name not in exisiting_names:
        raise HTTPException(status_code=400,detail="character doesnt exist")
    for id,charInfo in enumerate(data):
        if charInfo.get('name') == name:
            del data[id]
            break
    save_data(data)

        
