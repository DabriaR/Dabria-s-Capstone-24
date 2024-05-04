from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from bson import ObjectId  
from app.classes.data import Film, Comment, Reply
from app.classes.forms import FilmForm, CommentForm, ProfileForm, ReplyForm
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
            genre = form.genre.data,
            release = form.release.data,
            review=form.review.data,
            rating=form.rating.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        
        if form.poster.data:
           newFilm.poster.put(form.poster.data, content_type = 'image/jpeg')
           newFilm.save()
        
        return redirect(url_for('film',filmID=newFilm.id))

 
    return render_template('filmform.html',form=form)



@app.route('/film/<filmID>')

@login_required
def film(filmID):
    try:
        film_object_id = ObjectId(filmID)
        thisFilm = Film.objects.get(id=film_object_id)
    
        theseReplies = Reply.objects(film=thisFilm)

        return render_template('film.html',film=thisFilm,replies=theseReplies)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', message="Invalid film ID")

@app.route('/film/list')
@app.route('/films')

@login_required
def filmList():
  
    films = Film.objects()
    if films is None:
        return render_template('no_films.html')
    else:
        return render_template('films.html',films=films)

@app.route('/film/list/<userID>')
@app.route('/films/<userID>')

@login_required
def filmlogged(userID):
  
    films = Film.objects(author=userID)

    return render_template('films.html',films=films)\

@app.route('/myfilms')

@login_required
def myFilms(userID):
  
    films = Film.objects(author=current_user.id)
  
    return render_template('films.html',films=films)\

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
            genre = form.genre.data,
            release = form.release.data,
            review=form.review.data,
            rating=form.rating.data,
            modify_date = dt.datetime.utcnow
        )

            # This saves all the updates
        editFilm.save()
        if form.poster.data:
           if editFilm.poster:
               editFilm.poster.delete()
           editFilm.poster.put(form.poster.data, content_type = 'image/jpeg')
           # This saves all the updates
           editFilm.save()

        return redirect(url_for('film',filmID=filmID))


    form.filmname.data = editFilm.filmname
    form.director.data = editFilm.director
    form.genre.data = editFilm.genre
    form.release.data = editFilm.release
    form.review.data=editFilm.review
    form.rating.data=editFilm.rating

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

@app.route('/reply/new/<filmID>', methods=['GET', 'POST'])
@login_required
def replyNew(filmID):
    film = Film.objects.get(id=filmID)
    form = ReplyForm()
    if form.validate_on_submit():
        newReply = Reply(
            author = current_user.id,
            film = filmID,
            content = form.content.data
        )
        newReply.save()
        return redirect(url_for('film',filmID=filmID))
    return render_template('replyform.html',form=form,film=film)

@app.route('/reply/edit/<replyID>', methods=['GET', 'POST'])
@login_required
def replyEdit(replyID):
    editReply = Reply.objects.get(id=replyID)
    if current_user != editReply.author:
        flash("You can't edit a reply you didn't write.")
        return redirect(url_for('film',filmID=editReply.film.id))
    film = Film.objects.get(id=editReply.film.id)
    form = ReplyForm()
    if form.validate_on_submit():
        editReply.update(
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('film',filmID=editReply.film.id))

    form.content.data = editReply.content

    return render_template('replyform.html',form=form,film=film)  

@app.route('/reply/delete/<replyID>')
@login_required
def replyDelete(replyID): 
    deleteReply = Reply.objects.get(id=replyID)
    deleteReply.delete()
    flash('The reply was deleted.')
    return redirect(url_for('film',filmID=deleteReply.film.id)) 
