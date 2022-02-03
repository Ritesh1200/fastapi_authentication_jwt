from fastapi import FastAPI , status , Depends
from models import Base, engine , User
from schema import UserSchema , UserLoginSchema
from auth.jwt_handler import signJWT
from sqlalchemy.orm import Session
from fastapi import HTTPException
from auth.jwt_bearer import jwtBearer

app = FastAPI()


# Create the database
Base.metadata.create_all(engine)


@app.post("/user/signup" , status_code=status.HTTP_201_CREATED)
def signup(user : UserSchema):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    # create an instance of the book database model
    userobj = User(name = user.name , email = user.email ,password = user.password , age = user.age )

    # add it to the session and commit it
    session.add(userobj)
    session.commit()

    # close the session
    session.close() 


    return signJWT(user.email)

def check_user(userdata : UserLoginSchema):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    # it check that user with this detail present or not
    userobj = session.query(User).filter(User.email==userdata.email, User.password==userdata.password)

    # close the session
    session.close() 

    if not userobj:
        return False
    else:
        return True

@app.post("/user/login")
def login(user : UserLoginSchema):

    if check_user(user):
        return signJWT(user.email)
    else: 
        raise HTTPException(status_code=404, detail=f"User not found")
        
@app.put("/user/update")
def update_todo(userdata : UserSchema , Tokenpayload = Depends(jwtBearer())):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    userobj = session.query(User).filter(User.email == Tokenpayload["userID"]).first()

    # update todo item with the given task (if an item with the given id was found)
    if userobj:
        userobj.name = userdata.name
        userobj.email = userdata.email
        userobj.password = userdata.password
        userobj.age = userdata.age
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not userobj:
        raise HTTPException(status_code=404, detail=f"User not found")

    return userobj


@app.get("/user/profile")
def profile(Tokenpayload = Depends(jwtBearer())):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 


    # it check that user with this detail present or not
    userobj = session.query(User).filter(User.email == Tokenpayload["userID"]).first()

    # close the session
    session.close() 

    return userobj
    
        


