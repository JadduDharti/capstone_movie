from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from movie.forms import MovieForm
from movie.models import db, Movie
import requests

site = Blueprint('site',__name__,template_folder='site_templates')



@site.route('/')
def home():
    #print("ooga booga in the terminal")
    return render_template('index.html')


@site.route('/search', methods=['GET', 'POST'])
@login_required
def search_movies():
    if request.method == 'POST':
        # Get the search query from the form
        query = request.form.get('search_query')
        
        # Make a request to the movie API
        url = "https://ott-details.p.rapidapi.com/search"

        querystring = {"title":query,"page":"1"}

        headers = {
            "X-RapidAPI-Key": "780cf98630mshc62147f8861e21dp1c4da7jsnce244a655e2a",
            "X-RapidAPI-Host": "ott-details.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
                
        data = response.json()
        print("Data= ", data)

        # Extract the relevant details from the API response
        movies = []
        if 'results' in data:
            for movie_data in data['results']:
                title = movie_data['title']
                imdb_id = movie_data['imdbid']
                release_year = movie_data['released']
                genre = movie_data['genre']
                m_type = movie_data['type']
                image_url = movie_data.get('imageurl')
                movies.append((title, imdb_id, release_year, genre, m_type, image_url))

        print("Movie: ", movies)
        return render_template('profile.html', movies_watch=movies)
    
    return render_template('profile.html')

@site.route('/addtowatchlist', methods=['GET', 'POST'])
@login_required
def add_to_watchlist():
    if request.method == 'POST':
        try:
            title = request.form.get('movie_title')
            imdb_id = request.form.get('movie_imdb_id')
            year = request.form.get('movie_release_year')
            genre = request.form.get('movie_genre')
            m_type = request.form.get('movie_type')
            image_url = request.form.get('movie_image_url')
            user_token = current_user.token


            new_movie = Movie(
                title=title, 
                imdb_id=imdb_id, 
                release_year=year,
                genre=genre,
                m_type=m_type,
                image_url=image_url,
                user_token=user_token
            )

            print(f"Movie data= {new_movie}")

            db.session.add(new_movie)
            db.session.commit()

            mov = Movie.query.all()
            
            return render_template('watchlist.html', movies=mov)

        except:
            raise Exception("Movie not added, please check your form and try again!")

@site.route('/watchlist')
@login_required
def watchlist():
    movies = Movie.query.all()
    return render_template('watchlist.html', movies=movies)


@site.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_movie():
    movie_id = request.form.get('movie_id')
    movie = Movie.query.get(movie_id)

    if movie:
        db.session.delete(movie)
        db.session.commit()

        return redirect('/watchlist')
    
    else:
        return "Movie not found"

