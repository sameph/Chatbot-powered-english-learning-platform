# Import necessary modules and packages from Flask and other libraries
from flask import render_template, request, jsonify, Blueprint, flash, redirect, url_for, current_app, abort, session
from flask_login import login_required, current_user
from EGPT.models import Dictionary, User, Messages, Tutorial, UserProgress
from EGPT.main.forms import DeleteForm, ContactForm
from EGPT import db
import secrets
import os
import json
import re
from sqlalchemy.sql import or_
from flask_wtf import CSRFProtect
import openai
from EGPT.main.utils import DictionaryClass
from flask_login import current_user

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

@main.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'response': 'No message sent'}), 400

    # Send the message to the OpenAI API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use your preferred model
            prompt=message,
            max_tokens=150
        )
        bot_reply = response.choices[0].text.strip()
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return jsonify({'response': bot_reply})


# Route for displaying the learning services and their progress
@main.route('/learning', methods=['GET', 'POST'])
def learning():
    services = [
        {'name': 'Vocabulary Mastery', 'description': 'Enhance your word knowledge.', 'progress': session.get('Vocabulary_Mastery', {}).get('progress', 0)},
        {'name': 'Grammar Essentials', 'description': 'Understand and apply grammar rules.', 'progress': session.get('Grammar_Essentials', {}).get('progress', 0)},
        {'name': 'Speaking Fluency', 'description': 'Improve your speaking skills.', 'progress': session.get('Speaking_Fluency', {}).get('progress', 0)},
        {'name': 'Listening Skills', 'description': 'Sharpen your listening abilities.', 'progress': session.get('Listening_Skills', {}).get('progress', 0)},
        {'name': 'Writing Proficiency', 'description': 'Develop your writing expertise.', 'progress': session.get('Writing_Proficiency', {}).get('progress', 0)},
        {'name': 'Reading Comprehension', 'description': 'Improve your reading skills.', 'progress': session.get('Reading_Comprehension', {}).get('progress', 0)},
    ]
    return render_template('learning.html', services=services)

# Route for displaying the user's translation history, which requires the user to be logged in
@main.route('/history')
@login_required
def history():
    user_history = TranslationHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('translation_history.html', title='Translation History', history=user_history)

# Route for displaying tutorials for a specific service
@main.route('/service/<service_name>')
def service_detail(service_name):
    tutorials = {
        'Vocabulary_Mastery': [
            {'title': 'Synonyms and Antonyms', 'content': 'Learn about synonyms and antonyms to enhance your vocabulary.', 'video_url': 'https://www.youtube.com/embed/ixosNNS2ncI?si=MygMBYsMn844On1u'},
            {'title': 'Commonly Confused Words', 'content': 'Understand the differences between commonly confused words.', 'video_url': 'https://www.youtube.com/embed/VIDEO_ID_2'},
            {'title': 'Phrasal Verbs', 'content': 'Master phrasal verbs to sound more fluent.', 'video_url': 'https://www.youtube.com/embed/VIDEO_ID_3'},
        ],
        'Grammar_Essentials': [
            {'title': 'Tenses', 'content': 'Understand different tenses and their usage.', 'video_url': 'https://www.youtube.com/embed/VIDEO_ID_4'},
            {'title': 'Prepositions', 'content': 'Learn about prepositions and how they are used.', 'video_url': 'https://www.youtube.com/embed/VIDEO_ID_5'},
        ],
        # Add more services and tutorials here...
    }

    service_name_key = service_name.replace(' ', '_')
    service_tutorials = tutorials.get(service_name_key)

    if not service_tutorials:
        flash(f"No tutorials found for {service_name.replace('_', ' ')}", 'warning')
        return redirect(url_for('main.learning'))

    return render_template('service_detail.html', service={'name': service_name.replace('_', ' ')}, tutorials=service_tutorials)


# Route for marking a tutorial as viewed and updating progress
@main.route('/mark_tutorial_viewed/<int:tutorial_id>', methods=['POST'])
@login_required
def mark_tutorial_viewed(tutorial_id):
    tutorial = Tutorial.query.get_or_404(tutorial_id)
    user_progress = UserProgress.query.filter_by(user_id=current_user.id, tutorial_id=tutorial_id).first()

    if user_progress:
        # If the user has already viewed the tutorial, don't mark it again
        if not user_progress.is_viewed:
            user_progress.is_viewed = True
            db.session.commit()
    else:
        # Create a new progress record for the user and mark the tutorial as viewed
        user_progress = UserProgress(user_id=current_user.id, tutorial_id=tutorial_id, is_viewed=True)
        db.session.add(user_progress)
        db.session.commit()

    # Calculate progress
    return update_user_progress()

# Helper function to update user's progress
def update_user_progress():
    services = Service.query.all()  # Assuming Service has tutorials related
    for service in services:
        tutorials = Tutorial.query.filter_by(service_id=service.id).all()
        total_tutorials = len(tutorials)
        viewed_tutorials = UserProgress.query.filter_by(user_id=current_user.id, is_viewed=True).count()
        if total_tutorials > 0:
            service_progress = (viewed_tutorials / total_tutorials) * 100
        else:
            service_progress = 0

        # You can save the progress for each service if needed
        current_user.service_progress = service_progress
        db.session.commit()

    return jsonify({'message': 'Progress updated'})
