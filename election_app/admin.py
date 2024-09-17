from django.contrib import admin
from .models import Candidate, Election, Vote

admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(Vote)
