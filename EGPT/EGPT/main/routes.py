from flask import render_template, request, jsonify, Blueprint, flash, redirect, url_for, abort, session
from flask_login import login_required, current_user
from EGPT.models import Dictionary, User, Messages, Tutorial, UserProgress, Service
from EGPT.main.forms import DeleteForm, ContactForm
from EGPT import db
import datetime
from EGPT.main.utils import DictionaryClass
from new.chat import get_response

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/contact_us", methods=['GET', 'POST'])
@login_required
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Messages(user_id=current_user.id, subject=form.subject.data, message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html', title='Contact Us', form=form)

@main.route("/dictionary/<int:word_id>")
def meaning(word_id):
    word_entry = Dictionary.query.get_or_404(word_id)
    meaning = DictionaryClass().get_definition(word_entry.word)
    return render_template('meaning.html', title=word_entry.word, meaning=meaning)

@main.route('/dictionary')
def dictionary():
    words = Dictionary.query.all()
    form = DeleteForm()
    return render_template('dictionary.html', words=words, form=form)


@main.route('/learning', methods=['GET'])
def learning():
    services = Service.query.all()
    service_list = []
    for service in services:
        # Calculate user progress for each service
        total_tutorials = len(service.tutorials)
        if current_user.is_authenticated:
            viewed_tutorials = UserProgress.query.filter_by(user_id=current_user.id, is_viewed=True).filter(UserProgress.tutorial_id.in_([t.id for t in service.tutorials])).count()
            progress = (viewed_tutorials / total_tutorials) * 100 if total_tutorials > 0 else 0
        else:
            progress = 0
        
        service_list.append({
            'name': service.name,
            'description': service.description,
            'progress': progress
        })
    return render_template('learning.html', services=service_list)

@main.route('/service/<service_name>')
def service_detail(service_name):
    service = Service.query.filter_by(name=service_name.replace('_', ' ')).first_or_404()

    tutorials = Tutorial.query.filter_by(service_id=service.id).all()
    tutorial_list = []
    for tutorial in tutorials:
        viewed = UserProgress.query.filter_by(user_id=current_user.id, tutorial_id=tutorial.id, is_viewed=True).first()
        tutorial_list.append({
            'id': tutorial.id,
            'title': tutorial.title,
            'video_url': tutorial.video_url,
            'viewed': bool(viewed)
        })

    return render_template('service_detail.html', service={'name': service.name}, tutorials=tutorial_list)

# Route to mark a tutorial as viewed
@main.route('/mark_tutorial_viewed/<int:tutorial_id>', methods=['POST'])
@login_required
def mark_tutorial_viewed(tutorial_id):
    tutorial = Tutorial.query.get_or_404(tutorial_id)
    progress = UserProgress.query.filter_by(user_id=current_user.id, tutorial_id=tutorial.id).first()
    
    if not progress:
        # If no record exists, create one
        progress = UserProgress(user_id=current_user.id, tutorial_id=tutorial.id, is_viewed=True, completion_date=datetime.datetime.utcnow())
        db.session.add(progress)
    else:
        progress.is_viewed = True
        progress.completion_date = datetime.datetime.utcnow()
    
    db.session.commit()
    
    # Optionally return the updated progress percentage
    return jsonify({'message': 'Tutorial marked as viewed successfully'}), 200

@main.post("/chat") 
def chat():
    try:
        text = request.json['message']
        response = get_response(text)
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"answer": "Something went wrong"}), 500
    

@main.route("/admin/messages")
@login_required
def admin_messages():
    messages = Messages.query.all()
    if current_user.is_admin:
        return render_template('admin.html', messages = messages)
    else:
        abort(403)

@main.route("/delete_message/<int:message_id>", methods=['POST'])
@login_required
def delete_message(message_id):
    message = Messages.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message has been deleted!', 'success')
    return redirect(url_for('main.admin_messages'))
