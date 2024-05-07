from app import app
from flask_login.utils import login_required
from flask import render_template, redirect, flash, url_for
from app.classes.data import User, Film
from app.classes.forms import ProfileForm
from flask_login import current_user

# These routes and functions are for accessing and editing user profiles.

# The first line is what listens for the user to type 'myprofile'
@app.route('/myprofile')
# This line tells the user that they cannot access this without being loggedin
@login_required
# This is the function that is run when the route is triggered
def myProfile():
    # This sends the user to their profile page which renders the 'profilemy.html' template
    films = Film.objects(author=current_user.id)

    return render_template('profilemy.html', films=films, filmCount=len(films))

# This is the route for editing a profile
# the methods part is required if you are using a form 
@app.route('/myprofile/edit', methods=['GET','POST'])
# This requires the user to be loggedin
@login_required
# This is the function that goes with the route
def profileEdit():
    # This gets an object that is an instance of the form class from the forms.pyin classes
    form = ProfileForm()
    # This asks if the form was valid when it was submitted
    if form.validate_on_submit():
        # if the form was valid then this gets an object that represents the currUser's data
        currUser = User.objects.get(id=current_user.id)
        # This updates the data on the user record that was collected from the form
        currUser.update(
            lname = form.lname.data,
            fname = form.fname.data,
            pronouns = form.pronouns.data,
            bio = form.bio.data

        )
        # This updates the profile image
        if form.image.data:
            if currUser.image:
                currUser.image.delete()
            currUser.image.put(form.image.data, content_type = 'image/jpeg')
            # This saves all the updates
            currUser.save()
        # Then sends the user to their profle page
        return redirect(url_for('myProfile'))

    # If the form was not submitted this prepopulates a few fields
    # then sends the user to the page with the edit profile form
    form.fname.data = current_user.fname
    form.lname.data = current_user.lname
    form.pronouns.data = current_user.pronouns
    form.bio.data = current_user.bio
    
    return render_template('profileform.html', form=form)

@app.route('/addToWatchlist/<filmID>', methods=['POST'])
@login_required
def add_to_watchlist(filmID):
    film = Film.objects.get(id=filmID)
    if film not in current_user.watchlist:
            # Add the film to the user's watchlist
            current_user.watchlist.append(film)
            current_user.save()
            flash("Film added to watchlist successfully.")
    else:
            flash("Film is already in your watchlist.")

    return redirect(url_for('watchlist'))

@app.route('/watchlist')
@login_required
def watchlist():
    # Fetch the films in the current user's watchlist
    watchlist_films = current_user.watchlist
    return render_template('watchlist.html', watchlist_films=watchlist_films)

@app.route('/removeFromWatchlist/<film_id>', methods=['POST'])
@login_required
def remove_from_watchlist(film_id):
    film = Film.objects.get(id=film_id)

    current_user.watchlist.remove(film)
    current_user.save()

    return redirect(url_for('watchlist'))

