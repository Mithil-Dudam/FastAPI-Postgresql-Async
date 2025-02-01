from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List,Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import Session,declarative_base


app=FastAPI()

class User(BaseModel):
    name:str
    email:str
    password:str

class User_login(BaseModel):
    email:str
    password:str

URL_db = 'postgresql://postgres:password@localhost:5432/APIdb' 

engine = create_engine(URL_db)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

class Users(Base):
    __tablename__='Users'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,index=True) 
    email = Column(String,index=True) 
    password = Column(String,index=True) 

class Posts(Base):
    __tablename__='Posts'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True) 
    content = Column(String,index=True) 
    user_id = Column(Integer,ForeignKey("Users.id"),index=True) 

Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

#users={}
#count=1

@app.post("/register",status_code=status.HTTP_201_CREATED)
async def create_user_in_db(user:User,db:db_dependency):
    user_exists = db.query(Users).filter(Users.email==user.email).first()
    if user_exists:
            raise HTTPException(status_code=400, detail="Email already exists")
    db_user=Users(name=user.name,email=user.email,password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"User registerd successfully"}

###def create_user(user:User):
    global count
    for i in users.values():
        if(user.email == i["email"]):
            raise HTTPException(status_code=400, detail="Email already exists")
    users[count] = {"name":user.name,"email":user.email,"password":user.password}
    count+=1
    return {"message":"User registerd successfully"}###



@app.post("/login",status_code=status.HTTP_200_OK)
async def login_in_db(user:User_login,db:db_dependency):
    login_accepted = db.query(Users).filter(Users.email==user.email, Users.password==user.password).first()
    if login_accepted:
        return {"id": login_accepted.id, "name":login_accepted.name,"email":login_accepted.email,"auth_token":"jwt-token"}
    raise HTTPException(status_code=400, detail="Invalid email or password")

###def login(user:User_login):
    global count
    for k,val in users.items():
        if(user.email == val["email"] and user.password==val["password"]):
            return {"id": k, "name":val["name"],"email":val["email"],"auth_token":"jwt-token"}
    raise HTTPException(status_code=400, detail="Invalid email or password")###

@app.get("/users",status_code=status.HTTP_200_OK)
async def get_users_in_db(db:db_dependency):
    allusers = db.query(Users).all()
    return [{"id": user.id, "name": user.name, "email": user.email} for user in allusers]

###def get_users():
    print_users_list=[]
    for i in users:
        print_users_dict={}
        print_users_dict["id"]=i
        print_users_dict["name"] = users[i]["name"]
        print_users_dict["email"] = users[i]["email"]
        print_users_list.append(print_users_dict)
    return print_users_list###

@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def get_user_in_db(user_id:int,db:db_dependency):
    user_exits = db.query(Users).filter(Users.id==user_id).first()
    if user_exits:
        return{"id":user_id,"name":user_exits.name,"email":user_exits.email}
    raise HTTPException(status_code=404, detail="User not found")

###def get_user(user_id:int):
    if(user_id not in users):
        raise HTTPException(status_code=404, detail="User not found")
    return{"id":user_id,"name":users[user_id]["name"],"email":users[user_id]["email"]}###

class Post(BaseModel):
    title:str
    content:str
    user_id:int

#posts={}
#postcount=1

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post_in_db(post:Post,db:db_dependency):
    created_at = datetime.now(timezone.utc).isoformat()
    post_exists = db.query(Users).filter(Users.id==post.user_id).first()
    if post_exists:
        db_post=Posts(title=post.title,content=post.content,user_id=post.user_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return {"id":db_post.id,"title":post.title,"content":post.content,"user_id":post.user_id,"created_at":created_at}
    raise HTTPException(status_code=404, detail="User not found")

###def create_post(post:Post):
    if(post.user_id not in users):
        raise HTTPException(status_code=404, detail="User not found")
    global postcount
    created_at = datetime.now(timezone.utc).isoformat()
    posts[postcount]={"id":postcount,"title":post.title,"content":post.content,"user_id":post.user_id,"created_at":created_at}
    postcount+=1
    return posts[postcount-1]###

@app.get("/posts",status_code=status.HTTP_200_OK)
async def get_posts_in_db(db:db_dependency):
    allposts = db.query(Posts).all()
    return [{"id": post.id, "title": post.title, "content": post.content,"user_id":post.user_id} for post in allposts]

###def get_posts():
    print_posts_list=[]
    for i in posts:
        print_posts_dict={}
        print_posts_dict["id"]=i
        print_posts_dict["title"] = posts[i]["title"]
        print_posts_dict["content"] = posts[i]["content"]
        print_posts_dict["user_id"] = posts[i]["user_id"]
        print_posts_list.append(print_posts_dict)
    return print_posts_list###

@app.get("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def get_post_in_db(post_id:int,db:db_dependency):
    post_exits = db.query(Posts).filter(Posts.id==post_id).first()
    if post_exits:
        return{"id":post_id,"title":post_exits.title,"content":post_exits.content,"user_id":post_exits.user_id}
    raise HTTPException(status_code=404, detail="Post not found")

###def get_post(post_id:int):
    if(post_id not in posts):
        raise HTTPException(status_code=404, detail="Post not found")
    return{"id":post_id,"title":posts[post_id]["title"],"content":posts[post_id]["content"],"user_id":posts[post_id]["user_id"]}###
