from collections import Counter
from django.contrib.auth.models import User

def count_inactive_users(request):
    total_users = User.objects.all()
    inactive_users = 0
    for user in total_users:
        if not user.is_active:
            inactive_users = inactive_users + 1
    return {'count_inactive_users': inactive_users}