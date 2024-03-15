
from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Film, Comment
from app.classes.forms import FilmForm, CommentForm
from flask_login import login_required
import datetime as dt


@app.route('/film/new', methods=['GET', 'POST'])

@login_required

def filmNew():
   
    form = FilmForm()

   
    if form.validate_on_submit():

       
        newFilm = Film(
          
            filmname = form.filmname.data,
            director = form.director.data,
            director_race = form.director_race.data,
            genre = form.genre.data,
            release = form.release.data,
            author = current_user.id,
            
            modify_date = dt.datetime.utcnow
        )
        
        newFilm.save()

   
        return redirect(url_for('film',filmID=newFilm.id))

 
    return render_template('filmform.html',form=form)



@app.route('/film/<filmID>')

@login_required
def film(filmID):
    
    thisFilm = Film.objects.get(id=filmID)
    
    return render_template('film.html',Film=thisFilm)


@app.route('/film/list')
@app.route('/films')

@login_required
def filmList():
  
    films = Film.objects()
  
    return render_template('films.html',films=films)


@app.route('/film/edit/<filmID>', methods=['GET', 'POST'])
@login_required
def filmEdit(filmID):
    editFilm = Film.objects.get(id=filmID)
   
    if current_user != editFilm.author:
        flash("You can't edit a film you don't own.")
        return redirect(url_for('film',filmID=filmID))
   
    form = FilmForm()
    
    if form.validate_on_submit():
       
        editFilm.update(
            filmname = form.filmname.data,
            director = form.director.data,
            director_race = form.director_race.data,
            genre = form.genre.data,
            release = form.release.data,
            modify_date = dt.datetime.utcnow
        )
        
        return redirect(url_for('film',filmID=filmID))


    form.filmname.data = editFilm.filmname
    form.director.data = editFilm.director
    form.director_race.data = editFilm.director_race
    form.genre.data = editFilm.genre
    form.release.data = editFilm.release

    return render_template('filmform.html',form=form)


@app.route('/film/delete/<filmID>')

@login_required
def filmDelete(filmID):
  
    deleteFilm = Film.objects.get(id=filmID)
   
    if current_user == deleteFilm.author:
       
        deleteFilm.delete()
       
        flash('The Film was deleted.')
    else:
        
        flash("You can't delete a film you don't own.")
   
    films = Film.objects()  
    
    return render_template('films.html',films=films)