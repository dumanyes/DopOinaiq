from django.contrib import admin
from .models import Turf, TimeSlot, Booking, TurfImage, Facilities, Sports, TurfReview


# Register your models here.
admin.site.register(Turf)
admin.site.register(TimeSlot)
admin.site.register(Booking)
admin.site.register(TurfImage)
admin.site.register(Facilities)
admin.site.register(Sports)
admin.site.register(TurfReview)