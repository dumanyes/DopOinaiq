from django.contrib import messages

from time import timezone

from django.shortcuts import render, redirect, get_object_or_404

from dopoinaiq12 import settings
from users.forms import RegisterForm
from .models import Turf
from django.contrib.auth.decorators import login_required
import pytz
from datetime import datetime, timedelta
from .models import Turf, TimeSlot, Booking, TurfReview
from .forms import BookingForm, ReviewForm
from django.core.mail import send_mail
from django.db.models import Avg



def turfs_view(request):
    turfs = Turf.objects.all()
    return render(request, 'turfs.html', {'turfs': turfs})


def search_turfs(request):
    query = request.GET.get('query')

    if query:
        # Perform a case-insensitive search on both name and location
        turfs = Turf.objects.filter(name__icontains=query) | Turf.objects.filter(location__icontains=query)
    else:
        turfs = Turf.objects.all()

    context = {
        'turfs': turfs
    }

    return render(request, 'search_turfs.html', context)


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def turf_details(request, turf_id):
    # Get the Turf object or return a 404 error if not found
    turf = get_object_or_404(Turf, pk=turf_id)
    sports = turf.sports_set.all()
    facilities = turf.facilities_set.all()

    specific_timeslots = [
        '7:00-8:00', '8:00-9:00', '9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00',
        '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', '18:00-19:00',
        '19:00-20:00', '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-00:00'
    ]

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    timeslot_data = []

    for timeslot in specific_timeslots:
        timeslot_entry = {
            'timeslot': timeslot,
            'availability': {},
        }

        for day in days:
            day_timeslot = turf.timeslot_set.filter(
                day_of_week=day,
                start_time=timeslot.split('-')[0],
                end_time=timeslot.split('-')[1]
            ).first()

            if day_timeslot:
                timeslot_entry['availability'][day] = 'available' if not day_timeslot.booked else 'unavailable'
            else:
                timeslot_entry['availability'][day] = 'inactive'

        timeslot_data.append(timeslot_entry)

    number_of_days = 7

    almaty_timezone = pytz.timezone('Asia/Almaty')
    today = datetime.now()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    days = [start_of_week + timedelta(days=i) for i in range(7)]

    # Retrieve reviews for the turf
    reviews = turf.reviews.all()

    # Create a Paginator instance with 5 reviews per page
    paginator = Paginator(reviews, 5)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        reviews_on_page = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        reviews_on_page = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page
        reviews_on_page = paginator.page(paginator.num_pages)

    context = {
        'turf': turf,
        'timeslot_data': timeslot_data,
        'days': days,
        'sports': sports,
        'facilities': facilities,
        'today': today,
        'reviews': reviews_on_page,
    }

    return render(request, 'turf_details.html', context)




@login_required
def book_turf(request, turf_id):
    turf = get_object_or_404(Turf, pk=turf_id)

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['user_email'] = request.user.email
        form = BookingForm(form_data)

        if form.is_valid():
            selected_timeslot_id = form.cleaned_data['timeslot'].id
            user_name = form.cleaned_data['user_name']

            timeslot = get_object_or_404(TimeSlot, pk=selected_timeslot_id)

            if timeslot.booked:
                return render(request, 'booking_error.html', {'error_message': 'Timeslot is already booked.'})

            booking = Booking(user_name=user_name, user_email=request.user.email, time_slot=timeslot)
            booking.save()

            timeslot.booked = True
            timeslot.save()

            subject = 'New Booking Request'
            message = f'Hi, {turf.owner_name},\n\nYou have a new booking request from {user_name} ({request.user.email}) for a timeslot at {turf.name} on {timeslot.day_of_week} from {timeslot.start_time} to {timeslot.end_time}.'
            from_email = 'dopoinaiyq@gmail.com'
            recipient_list = [turf.owner_email]

            # Send an email to the user as well
            subject_user = 'Booking Confirmation'
            message_user = f'Hi {user_name},\n\nYou have successfully booked a timeslot at {turf.name} on {timeslot.day_of_week} from {timeslot.start_time} to {timeslot.end_time}.'
            recipient_user = [request.user.email]

            send_mail(subject, message, from_email, recipient_list)
            send_mail(subject_user, message_user, from_email, recipient_user)

            return render(request, 'booking_success.html', {'user_name': user_name, 'timeslot': timeslot})

    else:
        form = BookingForm()

    return render(request, 'booking.html', {'turf': turf, 'form': form})

@login_required
def write_review(request, turf_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.turf_id = turf_id
            review.user = request.user  # Assuming user is logged in
            review.save()
            return redirect('turf_details', turf_id=turf_id)  # Redirect to the turf details page

    else:
        form = ReviewForm()

    return render(request, 'write_review.html', {'form': form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(TurfReview, pk=review_id)

    # Check if the user is the owner of the review
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Review updated successfully.')
                return redirect('turf_details', turf_id=review.turf_id)
        else:
            form = ReviewForm(instance=review)
        return render(request, 'edit_review.html', {'form': form, 'review': review})
    else:
        messages.error(request, 'You do not have permission to edit this review.')
        return redirect('turf_details', turf_id=review.turf_id)

@login_required
def confirm_delete_review(request, review_id):
    review = get_object_or_404(TurfReview, pk=review_id)

    # Check if the user is the owner of the review
    if request.user == review.user:
        if request.method == 'POST':
            # Redirect to the deletion view if the user confirms the delete action
            return redirect('delete_review', review_id=review_id)
        return render(request, 'confirm_delete_review.html', {'review': review})
    else:
        messages.error(request, 'You do not have permission to delete this review.')
        return redirect('turf_details', turf_id=review.turf_id)

@login_required
def delete_review(request, review_id):
    # Get the review object
    review = get_object_or_404(TurfReview, pk=review_id)

    # Check if the user has permission to delete the review
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Review deleted successfully')  # Set a success message
    else:
        messages.error(request, 'You do not have permission to delete this review')  # Set an error message

    return redirect('turf_details', turf_id=review.turf.id)