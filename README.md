# Recipe Recommendation API

Welcome to the Recipe Recommendation API! This API allows users to get personalized recipe recommendations based on their past recipe history. It utilizes content-based filtering and implicit feedback to suggest recipes that users might enjoy.

## Live API Endpoint

You can access the API at the following endpoint:

[Recipe Recommendation API](https://recipe-recommender-api.onrender.com/recommended)


## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
  - [POST /recommended](#post-recommended)
- [Input Format](#input-format)
- [Sample Request](#sample-request)
- [Sample Response](#sample-response)
- [Usage Example](#usage-example)
- [How to Run Locally](#how-to-run-locally)
- [Contributing](#contributing)


## Features

- Personalized recipe recommendations based on user history
- Content-based filtering using TF-IDF vectorization
- Implicit feedback integration for better suggestions



## Technologies Used

- Python
- Flask
- Pandas
- Scikit-learn
- NumPy
- JSON


## How It Works

1. The API accepts user history as input in JSON format, containing a list of previously interacted recipe numbers.
2. The API calculates content similarity using TF-IDF and combines it with implicit feedback scores to generate a list of recommended recipes.
3. The recommendations are returned in JSON format.

---

## API Endpoints

### POST /recommended

This endpoint returns a list of recommended recipes based on the user's recipe history.

#### Input Format

The API expects a JSON object with a key `recipe_nos`, which contains a list of recipe numbers that the user has interacted with.

#### Sample Request

```bash
curl -X POST https://recipe-recommender-api.onrender.com/recommended \
-H "Content-Type: application/json" \
-d '{"recipe_nos": [1, 2, 3]}'
```
#### Sample response:
```bash
[
    {
        "RecipeNo": 4,
        "TranslatedRecipeName": "Recipe 4 Name",
        "TranslatedIngredients": "Ingredient 1, Ingredient 2",
        "TotalTimeInMins": 30,
        "Cuisine": "Cuisine Type",
        "TranslatedInstructions": "Instructions for the recipe.",
        "URL": "http://example.com/recipe4",
        "image-url": "http://example.com/image4.jpg",
        "Ingredient-count": 5
    },
    ...
]
```


## Usage Example
- Send a POST request to the /recommended endpoint with your user history.
- Parse the JSON response to get the recommended recipes.



## How to Run Locally
To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Piyusharora04/trial_recipe_api.git
   ```
2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
3. **Run the Flask application**:
   ```bash
   python app.py
4. The API will be accessible at http://127.0.0.1:3000.



## Contributing
- Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.


