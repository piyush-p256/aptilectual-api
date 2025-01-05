from django.contrib import admin
from .models import CustomUser, Problem, UserAnswer, LeaderDaily

admin.site.register(CustomUser)
admin.site.register(Problem)
admin.site.register(UserAnswer)
admin.site.register(LeaderDaily)
