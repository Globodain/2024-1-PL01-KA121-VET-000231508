from fastapi import FastAPI, HTTPException, Header
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
conn = MongoClient('mongodb://localhost:27017/')
db = conn['users']
coll = db['users']

class User(BaseModel):
    username: str
    password: str
    email: str

@app.get('/user/{name}')
async def get_user(name: str):
    user = coll.find_one({"username": name})
    if user is None:
        raise HTTPException(status_code=404, detail={"Failed to find user"})
    else:
        user["_id"] = str(user["_id"]) 
        return JSONResponse(content=user)
 
@app.delete('/user/{name}')
async def delete_user(name: str):
    result = coll.delete_one({"username": name})
    if result.deleted_count >= 1:
        return {"Successfully deleted user"}
    else:
        raise HTTPException(status_code=500, detail={"Failed to delete user"})
    
@app.post('/user')
async def create_user(user: User):
    user_d = user.model_dump()
    d_list= list(coll.find({"username": user_d.get("username")}))
    if len(d_list) >= 1:
        raise HTTPException(status_code=500, detail="User with this name currently exists")
    d_list= list(coll.find({"email": user_d.get("email")}))
    if len(d_list) >= 1:
        raise HTTPException(status_code=500, detail="User with this email currently exists")
    result = coll.insert_one(user_d) 
    return JSONResponse(content={"message": "User created succesfully"})

@app.put('/user/{name}')
async def edit_user(name: str, user: User):
    d_list= list(coll.find({"username": name}))
    if len(d_list) < 1:
        raise HTTPException(status_code=500, detail="User not found")
    else:
        user_d = user.model_dump()
        result = coll.update_one({"username": name}, {"$set": user_d})
        if result.acknowledged:
            return JSONResponse(content={"message": "User edited successfully", "modifications_made": result.modified_count})
        else:
            raise HTTPException(status_code=500, detail="User was not edited successfully")
