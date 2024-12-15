from django.contrib.auth.decorators import user_passes_test

def is_not_authenticated(user):
    return not user.is_authenticated