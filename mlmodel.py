import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os


# Function to collect input during the game
def collect_input():
    x_position = float(input("Enter the x position of the basketball: "))
    y_position = float(input("Enter the y position of the basketball: "))
    power = float(input("Enter the power of the shot: "))
    direction = float(input("Enter the direction of the shot: "))
    return [x_position, y_position, power, direction]

# # Function to save input and predicted score to a CSV file
# def save_to_csv(input_data, predicted_score):
#     with open('game_data.csv', 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(input_data + [predicted_score])

def train_model(data_file):
    # Load the data
    data = pd.read_csv(data_file)

    # Separate independent variables (X) and dependent variable (y)
    X = data[['x', 'y']] 
    y = data[['power', 'direction']]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the Random Forest Regression model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train.to_numpy(), y_train.to_numpy())

    return rf_model


def predict(model, X_test):
    # Make predictions on the test set
    y_pred = model.predict([X_test])
    return y_pred

def save_to_csv(data_list, output_file):
    # Save predicted and actual values to a CSV file
    mode = "w"
    if "data.csv" in os.listdir(): mode = "a"
    with open(output_file, mode, newline='') as file:
        writer = csv.writer(file)
        if mode == "w": writer.writerow(["x", "y", "power", "direction"])
        writer.writerow(data_list)
