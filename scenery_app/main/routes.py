from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from scenery_app.models import Location, List, Entry, User
from scenery_app.main.forms import LocationForm, ListForm, EntryForm
from scenery_app.extensions import app, db, bcrypt

main = Blueprint('main', __name__)

# Create your routes here.

@main.route('/')
def homepage():
    all_locations = Location.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_locations=all_locations, all_users=all_users)

@main.route('/create_location', methods=['GET', 'POST'])
@login_required
def create_location():
    form = LocationForm()

    if form.validate_on_submit(): 
        new_location = Location(
            title=form.title.data,
            visited_date=form.visited_date.data,
            list=form.list.data,
            landscape=form.landscape.data,
            entries=form.entries.data
        )
        db.session.add(new_location)
        db.session.commit()

        flash('New location was created successfully.')
        return redirect(url_for('main.location_detail', location_id=new_location.id))
    return render_template('create_location.html', form=form)

@main.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    form = ListForm()
    if form.validate_on_submit():
        new_list = List(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_list)
        db.session.commit()

        flash('New list created successfully.')
        return redirect(url_for('main.homepage'))
    
    return render_template('create_list.html', form=form)

@main.route('/create_entry', methods=['GET', 'POST'])
@login_required
def create_entry():
    form = EntryForm()
    if form.validate_on_submit():
        new_entry = Entry(
            name=form.name.data
        )
        db.session.add(new_entry)
        db.session.commit()

        flash('New entry created successfully.')
        return redirect(url_for('main.homepage'))
    
    return render_template('create_entry.html', form=form)

@main.route('/location/<location_id>', methods=['GET', 'POST'])
def location_detail(location_id):
    location = Location.query.get(location_id)
    form = LocationForm(obj=location)
    
    if form.validate_on_submit():
        location.title = form.title.data
        location.visited_date = form.visited_date.data
        location.list = form.list.data
        location.landscape = form.landscape.data
        location.entries = form.entries.data

        db.session.commit()

        flash('Location was updated successfully.')
        return redirect(url_for('main.location_detail', location_id=location_id))

    return render_template('location_detail.html', location=location, form=form)

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

@main.route('/favorite/<location_id>', methods=['POST'])
@login_required
def favorite_location(location_id):
    location = Location.query.get(location_id)
    if location in current_user.favorite_locations:
        flash('Location already in favorites.')
    else:
        current_user.favorite_locations.append(location)
        db.session.add(current_user)
        db.session.commit()
        flash('Location added to favorites.')
    return redirect(url_for('main.location_detail', location_id=location_id))

@main.route('/unfavorite/<location_id>', methods=['POST'])
@login_required
def unfavorite_location(location_id):
    location = Location.query.get(location_id)
    if location not in current_user.favorite_locations:
        flash('Location not in favorites.')
    else:
        current_user.favorite_locations.remove(location)
        db.session.add(current_user)
        db.session.commit()
        flash('Location removed from favorites.')
    return redirect(url_for('main.location_detail', location_id=location_id))

@main.route('/visitlist/<location_id>', methods=['POST'])
@login_required
def visit_location(location_id):
    location = Location.query.get(location_id)
    if location in current_user.visitlist_locations:
        flash('Location already in visitlist.')
    else:
        current_user.visitlist_locations.append(location)
        db.session.add(current_user)
        db.session.commit()
        flash('Location added to visitlist.')
    return redirect(url_for('main.location_detail', location_id=location_id))

@main.route('/unvisitlist/<location_id>', methods=['POST'])
@login_required
def unvisitlist_location(location_id):
    location = Location.query.get(location_id)
    if location not in current_user.visitlist_locations:
        flash('Location not in visitlist')
    else:
        current_user.visitlist_locations.remove(location)
        db.session.add(current_user)
        db.session.commit()
        flash('Location removed from visitlist.')
    return redirect(url_for('main.location_detail', location_id=location_id))