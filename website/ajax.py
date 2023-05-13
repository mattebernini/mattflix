from flask import Blueprint, render_template, request
from website.utility import save_cookie, get_film_search
from flask_login import login_required, current_user
from .models import Film, Recensione, Utente
from website.utility import get_film_data
from . import db

ajax = Blueprint('ajax', __name__)

@login_required
@ajax.route('/submit_rating', methods=['POST'])
def submit_rating():
    rating = request.form['rating']
    film_id = request.form['film_id']
    print(f"{current_user.username}, {film_id}, {rating}")

    # salvo nel database
    film = Film.query.filter_by(imdb_id_film=film_id).first()
    if not film:
        film_data = get_film_data(film_id)  
        if film_data:
            film = Film(imdb_id_film=film_id, title=film_data['title'], rating=film_data['rating'], tipo=film_data['kind'], year=film_data['year'], img_url=film_data['cover url'])
            db.session.add(film)
            db.session.commit()

    recensione = Recensione(id_utente=current_user.id, imdb_id_film=film_id, voto_utente=rating, consigliato=0)
    db.session.add(recensione)
    db.session.commit()

    # Return success response
    return {'success': True}

@login_required
@ajax.route('/submit_consiglia', methods=['POST'])
def submit_consiglia():
    consiglia = request.form['consiglia']
    film_id = request.form['film_id']
    print(f"{current_user.username}, {film_id}, {consiglia}")

    # Return success response
    return {'success': True}