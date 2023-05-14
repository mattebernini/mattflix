from sqlalchemy import text, func, case, desc
from flask import request
from imdb import Cinemagoer, IMDbError
from . import db
from .models import Film, Recensione, Utente, Visite, Seguaci, Feedback
import os 

def save_cookie(content):
    ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   
    # if ip_addr == "127.0.0.1":
    #    return
    visita = Visite(giorno=func.now(), user_agent=request.user_agent.string, ip_addr=ip_addr, content=content)
    db.session.add(visita)
    db.session.commit()

def query(sql_filename):
    with open("sql/"+sql_filename+".sql", "r") as f:
        q = f.read()
        return db.session.execute(text(q))
    
# https://github.com/cinemagoer/cinemagoer/issues/146
def pulisci_img_url(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

# FIlms and Recensioni
# *****************************************************
def get_film_search(str):
    films = []
    ia = Cinemagoer()
    try:
        ia = Cinemagoer()
        search = ia.search_movie(str)
    except IMDbError as e:
        print(e)
        return films
    for i in range(len(search)):
        # togliere film già visti
        id = search[i].movieID
        url_img = search[i]['cover url'] if 'cover url'in search[i] else ""
        film = [id, search[i]['title'], pulisci_img_url(url_img)]
        films.append(film)
        if i > 15:
            break
    return films

def get_film_data(id):
    ia = Cinemagoer()
    try:
        ia = Cinemagoer()
        movie = ia.get_movie(id)
        movie['cover url'] = pulisci_img_url(movie['cover url'])
    except IMDbError as e:
        print(e)
    return movie

def get_preferiti(user_id):
    results = db.session.query(Recensione.imdb_id_film, Film.title, Film.img_url, Recensione.voto_utente, Film.year, Film.tipo, Recensione.consigliato, Recensione.da_vedere).\
            join(Film, Recensione.imdb_id_film == Film.imdb_id_film).\
            filter(Recensione.id_utente == user_id, Recensione.voto_utente == 5).\
            order_by(desc(Recensione.imdb_id_film)).all()
    return results

def get_consigliati(user_id):
    results = db.session.query(Recensione.imdb_id_film, Film.title, Film.img_url, Recensione.voto_utente, Film.year, Film.tipo, Recensione.consigliato, Recensione.da_vedere)\
            .join(Film, Recensione.imdb_id_film == Film.imdb_id_film)\
            .filter(Recensione.id_utente == user_id, Recensione.consigliato == 1)\
            .order_by(Recensione.voto_utente.desc())\
            .all()
    return results

def get_da_vedere(user_id):
    results = db.session.query(Recensione.imdb_id_film, Film.title, Film.img_url, Recensione.voto_utente, Film.year, Film.tipo, Recensione.consigliato, Recensione.da_vedere)\
            .join(Film, Recensione.imdb_id_film == Film.imdb_id_film)\
            .filter(Recensione.id_utente == user_id, Recensione.da_vedere == 1)\
            .all()
    print(len(results))
    return results

def get_tutti_film(user_id):
    results = db.session.query(Recensione.imdb_id_film, Film.title, Film.img_url, Recensione.voto_utente, Film.year, Film.tipo, Recensione.consigliato, Recensione.da_vedere)\
            .join(Film, Recensione.imdb_id_film == Film.imdb_id_film)\
            .filter(Recensione.id_utente == user_id, Recensione.voto_utente > 1)\
            .order_by(Recensione.imdb_id_film.desc())\
            .all()
    return results

def get_comune(user1, user2):
    results =  db.session.execute(text(f"""
    select recensione.imdb_id_film, title, img_url, voto_utente, year, tipo, consigliato, da_vedere
    from recensione inner join film
        on recensione.imdb_id_film = film.imdb_id_film
    where id_utente = {user1} and film.imdb_id_film in (
        select imdb_id_film
        from recensione
        where id_utente = {user2}
    )
    order by voto_utente desc
    """))
    return results

# Users
# *****************************************************
def get_seguiti(user_id):
    res = db.session.query(Seguaci, Utente).join(Utente, Utente.id == Seguaci.segue).\
            filter(Seguaci.id_utente == user_id)
    return [u.username for s, u in res.all()]

def get_ti_seguono(user_id):
    res = db.session.query(Seguaci, Utente).join(Utente, Utente.id == Seguaci.id_utente).\
            filter(Seguaci.segue == user_id)
    return [u.username for s, u in res.all()]

def get_tutti_utenti(user_id):
    return [u.username for u in db.session.query(Utente).filter(Utente.id != user_id).order_by(Utente.id.desc())]

def get_feedback():
    return db.session.query(Utente.username, Feedback.text)\
        .join(Utente, Utente.id == Feedback.id_utente).all()
