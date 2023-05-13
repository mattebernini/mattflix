from flask import Blueprint, render_template, request
from website.utility import get_comune, get_seguiti, get_ti_seguono, get_tutti_utenti, get_tutti_film, save_cookie, get_film_search, get_preferiti, get_consigliati
from flask_login import login_required, current_user
from .models import Utente, Seguaci
from . import db

frontend = Blueprint('frontend', __name__)


@frontend.route('/', methods=['GET', 'POST'])
def index():
    # save_cookie("index")
    cercato = False
    tutti = consigliati = ricerca = preferiti = []
    if current_user.is_authenticated:
        preferiti = get_preferiti(current_user.id)   
        consigliati = get_consigliati(current_user.id)
        tutti = get_tutti_film(current_user.id)
    if request.method == "POST":
        filmname = request.form.get("film")
        ricerca = get_film_search(filmname)
        cercato = True
    return render_template("home.html",
                           cercato=cercato,
                            preferiti = preferiti,
                            consigliati = consigliati,
                            tutti = tutti,
                            ricerca = ricerca,
                            user=current_user)

@login_required
@frontend.route('/amici')
def amici():
    # save_cookie("amici")
    return render_template("amici.html",
                           seguiti = get_seguiti(current_user.id),
                           ti_seguono = get_ti_seguono(current_user.id),
                           tutti = get_tutti_utenti(current_user.id),
                            user=current_user)

@login_required
@frontend.route('/profilo/<username_amico>')
def profilo(username_amico):
    save_cookie("profilo/"+username_amico)
    id_amico =  db.session.query(Utente).filter(Utente.username == username_amico).first().id
    segue_gia =  Seguaci.query.filter_by(id_utente=current_user.id, segue=id_amico).first()
    gia_seguito = False if not segue_gia else True
    return render_template("profilo.html",
                            preferiti = get_preferiti(id_amico),
                            comune = get_comune(current_user.id, id_amico),
                            gia_seguito = gia_seguito,
                            consigliati = get_consigliati(id_amico),
                            username_amico = username_amico,
                            id_amico = id_amico,
                            user=current_user)
