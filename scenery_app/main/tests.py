# Create your tests here.

import os
import unittest
import app

from datetime import date
from scenery_app.extensions import app, db, bcrypt
from scenery_app.models import Location, Country, User, Landscape, Entry

"""
Run these tests with the command:
python -m unittest scenery_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_locations():
    a1 = Country(name='Chile')
    b1 = Location(
        title='Torres del Paine National Park',
        visited_date=date(2016, 5, 17),
        country=a1
    )
    db.session.add(b1)

    a2 = Country(name='Seychelles')
    b2 = Location(title='Anse Soucr d\'Argent', country=a2)
    db.session.add(b2)
    db.session.commit()

def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the locations show up on the homepage."""
        # Set up
        create_locations()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Torres del Paine National Park', response_text)
        self.assertIn('Anse Soucr d\'Argent', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Location', response_text)
        self.assertNotIn('Create Country', response_text)
        self.assertNotIn('Create Entry', response_text)
 
    def test_homepage_logged_in(self):
        """Test that the locations show up on the homepage."""
        # Set up
        create_locations()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Torres del Paine National Park', response_text)
        self.assertIn('Anse Soucr d\'Argent', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Create Location', response_text)
        self.assertIn('Create Country', response_text)
        self.assertIn('Create Entry', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_location_detail_logged_out(self):
        """Test that the location appears on its detail page."""
        # TODO: Use helper functions to create locations, Country, user
        create_locations()
        create_user()

        # TODO: Make a GET request to the URL /location/1, check to see that the
        # status code is 200
        response = self.app.get('/location/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


        # TODO: Check that the response contains the location's title, publish date,
        # and Country's name
        response_text = response.get_data(as_text=True)
        self.assertIn("<h1>Torres del Paine National Park</h1>", response_text)
        self.assertIn("Chile", response_text)

        # TODO: Check that the response does NOT contain the 'Favorite' button
        # (it should only be shown to logged in users)
        self.assertNotIn("Favorite This Location", response_text)

    def test_location_detail_logged_in(self):
        """Test that the location appears on its detail page."""
        # TODO: Use helper functions to create locations, Countrys, user, & to log in
        create_locations()
        create_user()
        login(self.app, 'me1', 'password')
        # TODO: Make a GET request to the URL /location/1, check to see that the
        # status code is 200
        response = self.app.get('/location/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # TODO: Check that the response contains the location's title, publish date,
        # and Country's name
        response_text = response.get_data(as_text=True)
        self.assertIn("<h1>Torres del Paine National Park</h1>", response_text)
        self.assertIn("Chile", response_text)
        # TODO: Check that the response contains the 'Favorite' button
        self.assertIn("Favorite This Location", response_text)

    def test_update_location(self):
        """Test updating a location."""
        # Set up
        create_locations()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'title': 'Victoria Falls',
            'visited_date': '2014-07-13',
            'Country': 1,
            'Landscape': 'Waterfall',
            'entries': []
        }
        self.app.post('/location/1', data=post_data)
        
        # Make sure the location was updated as we'd expect
        location = Location.query.get(1)
        self.assertEqual(location.title, 'Victoria Falls')
        self.assertEqual(location.visited_date, date(2018, 11, 7))
        self.assertEqual(location.landscape, Landscape.WATERFALL)

    def test_create_location(self):
        """Test creating a location."""
        # Set up
        create_locations()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'title': 'Niagara Falls',
            'visited_date': '2012-08-07',
            'Country': 'USA',
            'Landscape': 'WATERFALL',
            'Landscapes': []
        }
        self.app.post('/create_location', data=post_data)

        # Make sure location was updated as we'd expect
        created_location = Location.query.filter_by(title='Niagara Falls').one()
        self.assertIsNotNone(created_location)
        self.assertEqual(created_location.list.name, 'Chile')

    def test_create_location_logged_out(self):
        """
        User is redirected when trying to access the create location 
        route if not logged in.
        """

        # Set up
        create_locations()
        create_user()

        # GET request
        response = self.app.get('/create_location')

        # Make sure that the user was redirected to the login page.
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_location', response.location)

    def test_create_country(self):
        """Test creating an country."""
        # TODO: Create a user & login (so that the user can access the route)
        create_user()
        login(self.app, 'me1', 'password')
        # TODO: Make a POST request to the /create_country route
        post_data = {
            'name': 'Avenue of the Baobabs',
            'region': 'Madagascar.'
        }

        self.app.post('/create_Country', data=post_data)
        # TODO: Verify that the Country was updated in the database
        create_country = Country.query.filter_by(name='Avenue of the Baobabs').one()
        self.assertIsNotNone(create_country)
        self.assertEqual(create_country.region, 'Madagascar')

    def test_create_entry(self):
        # TODO: Create a user & login (so that the user can access the route)
        create_user()
        login(self.app, 'me1', 'password')
        # TODO: Make a POST request to the /create_Landscape route, 
        post_data = {
            'name': 'Test Entry',
        }
        self.app.post('/create_entry', data=post_data)
        # TODO: Verify that the Landscape was updated in the database
        create_entry = Entry.query.filter_by(name='Test Entry').one()
        self.assertIsNotNone(create_entry)
        self.assertEqual(create_entry.name, 'Test Entry')

    def test_profile_page(self):
        # TODO: Make a GET request to the /profile/me1 route
        create_user()
        login(self.app, 'me1', 'password')
        # TODO: Verify that the response shows the appropriate user info
        response = self.app.get('/profile/me1')
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('me1', response_text)

    def test_favorite_location(self):
        # TODO: Login as the user me1
        create_user()
        create_locations()
        login(self.app, 'me1', 'password')
        # TODO: Make a POST request to the /favorite/1 route
        post_data = {
            'location_id': 1
        }

        response = self.app.post('/favorite/1', data=post_data)
        # TODO: Verify that the location with id 1 was added to the user's favorites
        user = User.query.filter_by(username='me1').one()
        location = Location.query.get(1)
        self.assertIn(location, user.favorite_locations)

    def test_unfavorite_location(self):
        # TODO: Login as the user me1, and add location with id 1 to me1's favorites
        create_locations()
        create_user()
        login(self.app, 'me1', 'password')
        # TODO: Make a POST request to the /unfavorite/1 route
        post_data = {
            'location,_id': 1
        }

        response = self.app.post('/unfavorite/1', data=post_data)
        # TODO: Verify that the location with id 1 was removed from the user's 
        # favorites
        user = User.query.filter_by(username='me1').one()
        location = Location.query.get(1)
        self.assertNotIn(location, user.favorite_locations)