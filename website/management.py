from flask import Blueprint, render_template, request, redirect
from website.utility import get_feedback, query
from flask_login import login_required, current_user
from .models import Utente, Seguaci, Feedback
from . import db

management = Blueprint('management', __name__)

@login_required
@management.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        feedback = request.form.get("opinione")
        print(feedback)
        new_fb = Feedback(id_utente=current_user.id, text=feedback)
        db.session.add(new_fb)
        db.session.commit()
        return redirect("/")
    return render_template("management/feedback.html",
                            user=current_user)

@login_required
@management.route('leggi/feedback', methods=['GET', 'POST'])
def leggi_feedback():
    if current_user.id > 3:
        return redirect("/")
    return render_template("management/leggi_feedback.html",
                           feedback = get_feedback(),
                           info_users = query("utenti"),
                            user=current_user)