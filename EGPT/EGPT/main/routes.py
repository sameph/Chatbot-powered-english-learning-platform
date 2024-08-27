# Import necessary modules and packages from Flask and other libraries
from flask import render_template, request, jsonify, Blueprint, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from EGPT.models import Dictionary, TranslationHistory, User, Messages
from EGPT.main.forms import DeleteForm, ContactForm
from EGPT import db
import secrets
import os
import json
# from EGPT.main.preprocess import preprocess_sentence
import re
from sqlalchemy.sql import or_

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
# @login_required
def contact_us():
    form = ContactForm()
    # if form.validate_on_submit():
    #     # If the form is submitted and valid, save the message to the database
    #     contact = Messages(user_id=current_user.id, subject=form.subject.data, message=form.message.data)
    #     db.session.add(contact)
    #     db.session.commit()
    #     flash('Your message has been sent!', 'success')
    #     return redirect(url_for('main.home'))
    # elif request.method == 'GET':
    #     # Pre-fill the form with the current user's information if the request method is GET
    #     form.first_name.data = current_user.first_name
    #     form.last_name.data = current_user.last_name
    #     form.email.data = current_user.email
    return render_template('contact.html', title='Contact Us', form=form)

# Route for displaying a specific dictionary entry
@main.route("/dictionary/<int:word_id>")
def sign(word_id):
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    total_emails = Messages.query.count()
    words = Dictionary.query.get_or_404(word_id)
    video_file = url_for('static', filename='dict/' + words.sign_video)
    return render_template('sign.html', title=words.word, video_file=video_file, 
                           image_file=image_file, total_emails=total_emails, words=words)

# Route for displaying the dictionary with pagination
@main.route('/dictionary')
def dictionary():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        total_emails = Messages.query.count()
    else:
        image_file = None
        total_emails = None
    page = request.args.get('page', 1, type=int)
    words = Dictionary.query.paginate(page=page, per_page=5)
    form = DeleteForm()
    return render_template('dictionary.html', words=words, form=form, 
                           image_file=image_file, total_emails=total_emails)

# Route for deleting a specific dictionary entry
@main.route('/delete/<int:word_id>', methods=['GET', 'POST'])
def delete_word(word_id):
    word = Dictionary.query.get_or_404(word_id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(word)
        db.session.commit()
        flash('Word deleted successfully', 'success')
        return redirect(url_for('main.dictionary'))
    return render_template('delete.html', word=word, form=form)

# Route for the translator page
@main.route('/translator')
def translator():
    return render_template('translator.html', title='Translator')

# Route for translating text to sign language
@main.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    try:
        # Translate the text to sign language and get the video URLs and unfound words
        video_urls, unfound_words = text_to_sign_language(text)

        # Save the translation history if the user is authenticated
        if current_user.is_authenticated:
            save_translation_history(current_user.id, text, video_urls)

        return jsonify({'video_urls': video_urls, 'unfound_words': unfound_words})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Function to translate text to sign language
def text_to_sign_language(text):
    words = text.split()
    word_entries = Dictionary.query.filter(or_(*[Dictionary.word == word for word in words])).all()
    word_to_video = {entry.word: url_for('static', filename='dict/' + entry.sign_video) for entry in word_entries}

    video_urls = []
    unfound_words = []
    for word in words:
        video_url = word_to_video.get(word)
        if video_url:
            video_urls.append(video_url)
        else:
            unfound_words.append(word)

    if not video_urls:
        raise ValueError("No valid videos found. Please check your dictionary and input text.")

    return video_urls, unfound_words

# Function to save translation history to the database
def save_translation_history(user_id, text, video_urls):
    history_entry = TranslationHistory(user_id=user_id, translated_text=text, video_urls=json.dumps(video_urls))
    db.session.add(history_entry)
    db.session.commit()

# Route for displaying the user's translation history, which requires the user to be logged in
@main.route('/history')
@login_required
def history():
    user_history = TranslationHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('translation_history.html', title='Translation History', history=user_history)
