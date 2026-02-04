from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True, key=lambda x: x[1])

    names = []
    for i in distances[1:6]:
        names.append(movies.iloc[i[0]].title)
    return names

@app.route("/", methods=["GET", "POST"])
def home():
    movie_list = movies["title"].values
    recommendations = []
    selected_movie = None

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        recommendations = recommend(selected_movie)

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )

if __name__ == "__main__":
    app.run(debug=True)
