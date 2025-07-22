from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import pickle
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; later, replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # must include OPTIONS
    allow_headers=["*"],
)
# Load model and encoders
model = tf.keras.models.load_model('diet_model.h5')
with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

# Food lookup per diet
food_lookup = {
    "Low Carb Diet": ["Eggs", "Chicken", "Broccoli", "Nuts", "Avocado"],
    "Mediterranean Diet": ["Olive oil", "Fish", "Whole grains", "Tomatoes", "Feta cheese"],
    "Diabetic Diet": ["Oats", "Beans", "Brown rice", "Leafy greens", "Berries"],
    "DASH Diet": ["Low-fat dairy", "Fruits", "Vegetables", "Whole grains", "Lean meat"],
    "Balanced Diet": ["Rice", "Vegetables", "Fruits", "Chicken", "Fish"],
    "High Protein Diet": ["Chicken breast", "Greek yogurt", "Eggs", "Tofu", "Almonds"]
}

class UserInput(BaseModel):
    age: int
    gender: str
    weight: float
    height: float
    diabetes: int
    cholesterol: int
    hypertension: int
    goal: str

@app.post('/recommend')
def recommend(input: UserInput):
    try:
        gender_enc = encoders['gender'].transform([input.gender])[0]
        goal_enc = encoders['goal'].transform([input.goal])[0]
        data = np.array([[input.age, gender_enc, input.weight, input.height,
                          input.diabetes, input.cholesterol, input.hypertension, goal_enc]])
        pred = model.predict(data)
        diet_idx = np.argmax(pred)
        diet = encoders['diet'].inverse_transform([diet_idx])[0]
        foods = food_lookup.get(diet, [])
        return {'recommended_diet': diet, 'foods': foods}
    except Exception as e:
        print("🔥 ERROR:", e)
        return {"error": str(e)}

