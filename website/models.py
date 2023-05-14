from . import db
from flask_login import UserMixin

class Visite(db.Model):
    __tablename__ = "Visite"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    giorno = db.Column(db.Date)
    user_agent = db.Column(db.String, unique=False)    
    content = db.Column(db.String, unique=False)
    ip_addr = db.Column(db.String, unique=False)    

class Feedback(db.Model):
    __tablename__ = "Feedback"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utente = db.Column(db.Integer)
    text = db.Column(db.String(500))

# auth
class Utente(db.Model, UserMixin):
    __tablename__ = "utente"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))

class Seguaci(db.Model):
    __tablename__ = "seguaci"
    id_utente = db.Column(db.Integer, primary_key=True)
    segue = db.Column(db.Integer, primary_key=True)

# film
class Film(db.Model):
    __tablename__ = "film"
    imdb_id_film = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    rating = db.Column(db.String(150))
    tipo = db.Column(db.String(150))
    year = db.Column(db.String(150))
    img_url = db.Column(db.String(1000))

class Recensione(db.Model):
    __tablename__ = "recensione"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utente = db.Column(db.Integer)
    imdb_id_film = db.Column(db.Integer)
    voto_utente = db.Column(db.Integer)
    consigliato = db.Column(db.Integer)
    da_vedere = db.Column(db.Integer)
    