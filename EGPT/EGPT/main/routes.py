# Import necessary modules and packages from Flask and other libraries
from flask import render_template, request, jsonify, Blueprint, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from EGPT.models import Dictionary, TranslationHistory, User, Messages
from EGPT.main.forms import DeleteForm, ContactForm
from EGPT import db
import secrets
import os
import json
import re
from sqlalchemy.sql import or_
from EGPT.main.utils import DictionaryClass

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

# Route for the home page
@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

# Route for the about page
@main.route("/about")
def about():
    return render_template('about.html', title='About')

# Route for the contact us page, which requires the user to be logged in
@main.route("/contact_us", methods=['GET', 'POST'])
@login_required
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        # If the form is submitted and valid, save the message to the database
        contact = Messages(user_id=current_user.id, subject=form.subject.data, message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        # Pre-fill the form with the current user's information if the request method is GET
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('contact.html', title='Contact Us', form=form)

# Route for displaying a specific dictionary entry
@main.route("/dictionary/<int:word_id>")
def meaning(word_id):
    word_entry = Dictionary.query.get_or_404(word_id)
    meaning = DictionaryClass().get_definition(word_entry.word)
    return render_template('meaning.html', title=word_entry.word, meaning=meaning)

# Route for displaying the dictionary with pagination
@main.route('/dictionary')
def dictionary():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        total_emails = Messages.query.count()
    else:
        image_file = None
        total_emails = None
    words = Dictionary.query.all()
    form = DeleteForm()
    return render_template('dictionary.html', words=words, form=form, 
                           image_file=image_file, total_emails=total_emails)


# Route for deleting a specific dictionary entry
@main.route('/learning', methods=['GET', 'POST'])
def learning():
    return render_template('learning.html')



# Route for displaying the user's translation history, which requires the user to be logged in
@main.route('/history')
@login_required
def history():
    user_history = TranslationHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('translation_history.html', title='Translation History', history=user_history)
