from flask import Flask, send_file, request, jsonify
from movie_recommender import MovieRec
import os
app=Flask(__name__)
recommender=None
def init():
    global recommender
    print("Starting initialization...")
    try:
        recommender=MovieRec()
        print("MovieRec object created")
        success=recommender.setup()
        if success:
            print("MovieRec setup completed successfully!")
            print("Ready!")
        else:
            print("MovieRec setup failed!")
            recommender = None
        return success
    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        print(f"Initialization traceback: {traceback.format_exc()}")
        recommender = None
        return False
@app.route('/')
def home():
    return send_file('index.html')
@app.route('/api/search')
def search():
    query=request.args.get('q', '')
    if not query:
        return jsonify({'movies': []})
    try:
        results=recommender.search(query)
        return jsonify({'movies': results})
    except Exception as error:
        return jsonify({'movies': []})
@app.route('/api/recommend')
def recommend():
    global recommender
    movie=request.args.get('movie', '')
    print(f"Recommendation request for: {movie}")
    if not movie:
        return jsonify({'error': 'Need movie name'})
    try:
        if recommender is None:
            print("Recommender not initialized, trying lazy initialization...")
            if not init():
                print("Lazy initialization also failed!")
                return jsonify({'error': 'System not ready'})
        
        print(f"Calling recommend function for: {movie}")
        recommendations=recommender.recommend(movie)
        print(f"Got {len(recommendations) if recommendations else 0} recommendations")
        
        if not recommendations:
            print(f"No recommendations found for: {movie}")
            return jsonify({'error': f'Movie "{movie}" not found'})
        return jsonify({'recommendations': recommendations})
    except Exception as error:
        print(f"Detailed error in recommend: {str(error)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Error occurred'})
if __name__=='__main__':
    print("Starting app...")
    if init():
        port = int(os.environ.get('PORT', 5000))
        print(f"Server starting on port {port}...")
        app.run(debug=False, port=port, host='0.0.0.0')
    else:
        print("Could not start")