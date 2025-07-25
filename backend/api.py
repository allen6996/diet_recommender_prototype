from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd

app = FastAPI()

# Load dataset
df = pd.read_csv('diet_recommendations_dataset.csv')

# DB setup
engine = create_engine('sqlite:///users.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    disease_type = Column(String)
    blood_pressure = Column(String)

Base.metadata.create_all(bind=engine)

class SignUpInput(BaseModel):
    username: str
    password: str
    age: int
    weight: float
    disease_type: str
    blood_pressure: str

class LoginInput(BaseModel):
    username: str
    password: str

def get_recommendation(disease_type, blood_pressure):
    filtered = df[
        (df['disease_type'].str.lower() == disease_type.lower()) &
        (df['blood_pressure'].str.lower() == blood_pressure.lower())
    ]
    if not filtered.empty:
        row = filtered.iloc[0]
        return {
            "recommended_diet": row['recommended_diet'],
            "foods": row['foods'].split(",")
        }
    else:
        return {
            "recommended_diet": "General Healthy Diet",
            "foods": ["vegetables", "fruits", "whole grains"]
        }

@app.post("/signup")
def signup(user: SignUpInput):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(
        username=user.username,
        password=user.password,
        age=user.age,
        weight=user.weight,
        disease_type=user.disease_type,
        blood_pressure=user.blood_pressure
    )
    db.add(new_user)
    db.commit()
    recommendation = get_recommendation(user.disease_type, user.blood_pressure)
    return {"message": "User created", "recommendation": recommendation}

@app.post("/login")
def login(credentials: LoginInput):
    db = SessionLocal()
    user = db.query(User).filter(User.username == credentials.username, User.password == credentials.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    recommendation = get_recommendation(user.disease_type, user.blood_pressure)
    return {
        "username": user.username,
        "age": user.age,
        "weight": user.weight,
        "disease_type": user.disease_type,
        "blood_pressure": user.blood_pressure,
        "recommendation": recommendation
    }
