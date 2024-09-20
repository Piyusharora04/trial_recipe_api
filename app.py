import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import flask
import json
from flask import Flask, jsonify, request
import logging

df = pd.read_csv('Cleaned_Indian_Food_Dataset.csv')
df['RecipeNo'] = df.index + 1

# Hyperparameters to tune
alpha = 0.7  # Weight for content-based similarity 
beta = 0.3  # Weight for implicit feedback
view_weight = 2  # Weight for multiple views

# TF-IDF for content-based similarity
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['TranslatedIngredients'])

def calculate_content_similarity(history_recipe_nos):
    history_tfidf = tfidf_matrix[history_recipe_nos].mean(axis=0)
    history_tfidf_array = np.asarray(history_tfidf) # Convert to NumPy array
    similarity_scores = cosine_similarity(history_tfidf_array, tfidf_matrix)[0] 
    return similarity_scores

def calculate_implicit_feedback_scores(history_recipe_nos):
    # Normalize Ingredient Count
    max_ingredients = df['Ingredient-count'].max()
    df['norm_ingredients'] = df['Ingredient-count'] / max_ingredients

    # Normalize Preparation Time
    max_prep_time = df['TotalTimeInMins'].max()
    df['norm_prep_time'] = df['TotalTimeInMins'] / max_prep_time

    # Cuisine Boost
    cuisine_counts = df.loc[history_recipe_nos, 'Cuisine'].value_counts()
    df['cuisine_boost'] = df['Cuisine'].apply(lambda x: cuisine_counts[x] if x in cuisine_counts else 0)

    # Weighted Combination
    weight_ingredients = 0.2
    weight_prep_time = 0.1
    weight_cuisine = 0.7 

    implicit_scores = (
        weight_ingredients * df.loc[history_recipe_nos, 'norm_ingredients'] +
        weight_prep_time * df.loc[history_recipe_nos, 'norm_prep_time'] +
        weight_cuisine * df.loc[history_recipe_nos, 'cuisine_boost']
    )
    
    # Create an array to store scores for ALL recipes (initialized with zeros)
    all_implicit_scores = np.zeros(df.shape[0]) 

    # Assign calculated scores to the corresponding indices
    all_implicit_scores[history_recipe_nos] = implicit_scores 

    return all_implicit_scores

# def recommend_recipes(user_history_recipe_nos):
#     content_scores = calculate_content_similarity(user_history_recipe_nos)
#     implicit_scores = calculate_implicit_feedback_scores(user_history_recipe_nos)

#     combined_scores = (alpha * content_scores) + (beta * implicit_scores)

#     top_100_indices = combined_scores.argsort()[-10:][::-1]

#     results = df.iloc[top_100_indices][[
#         'RecipeNo', 'TranslatedRecipeName', 'TranslatedIngredients', 
#         'TotalTimeInMins', 'Cuisine', 'TranslatedInstructions', 
#         'URL', 'image-url', 'Ingredient-count'
#     ]].to_json(orient='records')

#     return results

def recommend_recipes(user_history_json_file):
# def recommend_recipes(user_history_recipe_nos):
    
    with open(user_history_json_file, 'r') as f:
        user_history = json.load(f)
        user_history_recipe_nos = user_history['recipe_nos']  # Assuming your JSON has 'recipe_nos' key
        
        
    # ... (Your content_similarity, implicit_feedback_scores calculations) ...
    content_scores = calculate_content_similarity(user_history_recipe_nos)
    implicit_scores = calculate_implicit_feedback_scores(user_history_recipe_nos)

    combined_scores = (alpha * content_scores) + (beta * implicit_scores)

# Get only the indices for the top 20 recipes
    top_20_indices = combined_scores.argsort()[-20:][::-1]  

#     # Create a DataFrame for the results
#     results_df = df.iloc[top_100_indices][[
#         'RecipeNo', 'TranslatedRecipeName', 'TranslatedIngredients', 
#         'TotalTimeInMins', 'Cuisine', 'TranslatedInstructions', 
#         'URL', 'image-url', 'Ingredient-count'
#     ]]

#     return results_df

# Create a DataFrame for the results
    results_df = df.iloc[top_20_indices][[
        'RecipeNo', 'TranslatedRecipeName', 'TranslatedIngredients', 
        'TotalTimeInMins', 'Cuisine', 'TranslatedInstructions', 
        'URL', 'image-url', 'Ingredient-count'
    ]].to_json(orient='records')

    return results_df 


app = Flask(__name__) 

@app.route('/recommended', methods=['POST'])
def recommend():
    user_history = request.get_json()

    with open('result.json', 'w') as fp:
        json.dump(user_history, fp)

    recommendations_df = recommend_recipes('result.json')

    return recommendations_df , 210

@app.route('/')
def welcome():
    text = """<h1>Recipe Recommnendation API</h1><br>
    Welcome to the Recipe Recommendation Project.<br>
    You are recommended to use postman or other any api testing platform to check its performance<br>
    You need to add 'recommended' after the link and give a json file ass the input and method should be set to 'POST'<br>
    The JSON file input should be a dictionary with key as 'recipe_no' (that in my project is a refrence to the the repcipes in the dataset) followed by a list of some random integrs between 1 to 2000."""
    list = ["Hello", "World"]
    return text

if __name__ == '__main__':
    app.run(debug = True, port = 3000, use_reloader = False)