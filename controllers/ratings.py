from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required

from forms import CreateRatingForm
from models.profile import Profile
from models.rating import Rating

ratings = Blueprint('ratings', __name__, template_folder='templates')


@ratings.route('/ratings', methods=['GET'])
@login_required
def ratings_admin():
    form = CreateRatingForm()
    profile = Profile.get_profile(current_user.id)
    ratings = Rating.get_all_ratings_admin()
    return render_template('rating.html', page='Ratings', profile=profile, form=form, ratings=ratings)


@ratings.route('/createRating', methods=['POST'])
@login_required
def create_rating_admin():
    form = request.form
    Rating.add_rating_admin(form.get('id'), form.get('user_id'), form.get('ride_id'), form.get('passenger_id'),
                            form.get('rating'), form.get('created_at'), form.get('updated_at'))
    return redirect('/ratings')

@ratings.route('/editRating/<rating_id>', methods=['POST'])
@login_required
def update_rating(rating_id):
    form = request.form
    rating = Rating.get_rating_by_id(rating_id)
    Rating.edit_rating_admin(rating_obj=rating, id=form.get('id'), user_id=form.get('user_id'),
                             ride_id=form.get('ride_id'), passenger_id=form.get('passenger_id'), rating=form.get('rating'), created_at=form.get('created_at'), updated_at=form.get('updated_at'))
    return redirect('/ratings')


@ratings.route('/deleterating/<rating_id>', methods=['DELETE'])
@login_required
def delete_rating(rating_id):
    Rating.delete_rating_admin(rating_id)
    return redirect('/ratings')


@ratings.route('/getDeleteRatingModal/<rating_id>', methods=['GET'])
@login_required
def get_delete_rating_modal(rating_id):
    rating = Rating.get_rating_by_id(rating_id)
    return render_template('delete-rating-modal.html', rating=rating)


@ratings.route('/getEditRatingModal/<rating_id>', methods=['GET'])
@login_required
def get_edit_rating_modal(rating_id):
    rating = Rating.get_rating_by_id(rating_id)
    form = CreateRatingForm(id=rating.id, user_id=rating.user_id, ride_id=rating.ride_id,
                            passenger_id=rating.passenger_id, rating=rating.rating, created_at=rating.created_at,
                            updated_at=rating.updated_at)

    return render_template('edit-rating-modal.html', rating=rating, form=form)

