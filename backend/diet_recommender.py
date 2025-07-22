import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import pickle

# Load data
df = pd.read_csv('diet_dataset.csv')
df = df.dropna()  # remove missing values
df = df.reset_index(drop=True)

# Encode categorical columns
le_gender = LabelEncoder()
df['gender'] = le_gender.fit_transform(df['gender'])
le_goal = LabelEncoder()
df['goal'] = le_goal.fit_transform(df['goal'])
le_diet = LabelEncoder()
df['diet'] = le_diet.fit_transform(df['diet'])

# Ensure numeric dtypes
df = df.astype({
    'age': 'int64',
    'gender': 'int64',
    'weight': 'float64',
    'height': 'float64',
    'diabetes': 'int64',
    'cholesterol': 'int64',
    'hypertension': 'int64',
    'goal': 'int64',
    'diet': 'int64'
})

print(df.dtypes)
print(df.head())

X = df.drop(['diet'], axis=1)
y = df['diet']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Build model
model = Sequential([
    Dense(16, input_dim=X.shape[1], activation='relu'),
    Dense(8, activation='relu'),
    Dense(len(df['diet'].unique()), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, batch_size=4, verbose=1)

# Save
model.save('diet_model.h5')
with open('encoders.pkl', 'wb') as f:
    pickle.dump({'gender': le_gender, 'goal': le_goal, 'diet': le_diet}, f)
