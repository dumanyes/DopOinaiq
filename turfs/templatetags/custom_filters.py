import availability as availability
from django import template
from datetime import datetime

from turfs.models import TimeSlot
from turfs.views import turf_details

register = template.Library()


@register.filter
def timeslot_available(args):
    args_list = args.split(':')
    day = args_list[0]
    timeslot = args_list[1]
    turf = args_list[2]

    time_slot_obj = TimeSlot.objects.filter(
        turf=turf, day_of_week=day, start_time=timeslot.split('-')[0], end_time=timeslot.split('-')[1], booked=False
    ).first()
    return time_slot_obj is not None

@register.simple_tag
def get_timeslot_availability(slot, day, timeslot_availability):
    # Your implementation here
    # Ensure it returns the correct availability status based on the input
    return availability
@register.simple_tag
def get_item(dictionary, key):
    return dictionary.get(key, None)


@register.filter
def split_timeslot(value, delimiter):
    return value.split(delimiter)
@register.filter
def check_availability(time_slot, day, start_time, end_time):
    return time_slot.filter(day_of_week=day, start_time__lte=start_time, end_time__gte=end_time).first().available


@register.filter
def available_time_slot(time_slots, turf, day):
    # Find a matching time slot for the specified turf and day
    for time_slot in time_slots:
        if (
            time_slot.turf == turf
            and time_slot.start_time.strftime('%a') == day
            and time_slot.available
        ):
            return time_slot

    return None
