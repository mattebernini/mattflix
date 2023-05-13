from flask import Blueprint, render_template, request
from website.utility import save_cookie, get_film_search
from flask_login import login_required, current_user
from .models import Film, Recensione, Utente, Seguaci
from website.utility import get_film_data
from . import db

ajax = Blueprint('ajax', __name__)

@login_required
@ajax.route('/submit_rating', methods=['POST'])
def submit_rating():
    rating = request.form['rating']
    film_id = request.form['film_id']
    print(f"{current_user.username}, {film_id}, {rating}")

    # se il film non è in locale lo salvo
    film = Film.query.filter_by(imdb_id_film=film_id).first()
    if not film:
        film_data = get_film_data(film_id)  
        if film_data:
            film = Film(imdb_id_film=film_id, title=film_data['title'], rating=film_data['rating'], tipo=film_data['kind'], year=film_data['year'], img_url=film_data['cover url'])
            db.session.add(film)
            db.session.commit()
    # controllo se la recensione esiste già
    vecchia_recensione = Recensione.query.filter_by(imdb_id_film=film_id, id_utente=current_user.id).first()
    if not vecchia_recensione:
        nuova_recensione = Recensione(id_utente=current_user.id, imdb_id_film=film_id, voto_utente=rating, consigliato=0)
        db.session.add(nuova_recensione)
    else:
        vecchia_recensione.voto_utente = rating
    db.session.commit()
    return {'success': True}

@login_required
@ajax.route('/submit_consiglia', methods=['POST'])
def submit_consiglia():
    consiglia = request.form['consiglia']
    film_id = request.form['film_id']
    print(f"{current_user.username}, {film_id}, {consiglia}")

    # controllo se la recensione esiste già
    vecchia_recensione = Recensione.query.filter_by(imdb_id_film=film_id, id_utente=current_user.id).first()
    if not vecchia_recensione:
        return {'success': False}
    # se e solo se esiste aggiorno consiglia
    vecchia_recensione.consigliato = 1 if consiglia=="true" else 0
    db.session.commit()
    return {'success': True}

@login_required
@ajax.route('/segui', methods=['POST'])
def segui():
    id_amico = request.form['id_amico']
    print(f"{current_user.username}, {id_amico}")
    # se lo segue già smette
    segue_gia =  Seguaci.query.filter_by(id_utente=current_user.id, segue=id_amico).first()
    if not segue_gia:
        seguaci = Seguaci(id_utente=current_user.id, segue=id_amico)
        db.session.add(seguaci)
    else:
        db.session.delete(segue_gia)
    db.session.commit()
    return {'success': True}