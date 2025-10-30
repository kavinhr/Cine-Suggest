# Movie Recommendation System

A Flask-based web application that provides movie recommendations using machine learning algorithms. The system uses TMDB dataset to suggest similar movies based on user input.

## Live Demo

**Try the Demo:** https://codenex.onrender.com/

## Demo Video

Watch the application in action:

https://github.com/NITHISHKUMAR0283/CodeNex/raw/main/code_nex-VEED.mp4

## Features

- Search for movies in the database
- Get personalized movie recommendations
- Clean and intuitive web interface
- RESTful API endpoints

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NITHISHKUMAR0283/CodeNex.git
cd CodeNex
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Dataset Files

Make sure the following CSV files are in the project directory:
- `tmdb_5000_credits.csv`
- `tmdb_5000_movies.csv`

These files contain the movie data used for recommendations.

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Use the search feature to find movies
3. Click on a movie to get recommendations for similar movies

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /api/search?q=<query>` - Search for movies
- `GET /api/recommend?movie=<movie_name>` - Get recommendations for a specific movie

## Project Structure

```
├── app.py                    # Flask application and routes
├── movie_recommender.py      # Movie recommendation logic
├── index.html               # Frontend interface
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway deployment configuration
├── README.md                # Project documentation
├── code_nex-VEED.mp4        # Demo video
├── tmdb_5000_credits.csv    # Movie credits data
└── tmdb_5000_movies.csv     # Movie metadata
```

## Dependencies

- Flask - Web framework
- Pandas - Data manipulation
- NumPy - Numerical computing
- Scikit-learn - Machine learning algorithms
- Gunicorn - WSGI HTTP server

## Troubleshooting

- Make sure all CSV files are present in the project directory
- Verify Python version compatibility (3.7+)
- Check if all dependencies are installed correctly
- Ensure port 5000 is not being used by another application

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.
