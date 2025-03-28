from fastapi import FastAPI
app=FastAPI()

@app.get(path="/users/me")  # Fixed path
async def read_user_me():
    return {"user_id":"the current user"} 

@app.get(path="/users/{user_id}")  # Path parameter
async def read_user(user_id:str): 
    return {"user_id":user_id} 


