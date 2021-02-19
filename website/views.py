from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html")


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/design', methods=['GET'])
def design():
    return render_template("design.html")

@views.route('/guide', methods=['GET'])
def guide():
    return render_template("guide.html")             


@views.route('/submitted', methods=['POST','GET'])
def submit_info():
    if request.method == 'POST':
        print(request)
        message = request.form.get('options')
        print("selected unit is:")
        print(message)
    
    return render_template("guide.html", namme=message)    