
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.backends import BaseBackend


class MyBackend(BaseBackend):

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            # At the request of the user, we will update the date and time of the last visit
            user.last_online = timezone.now()
            user.save(update_fields=["last_online"])
            return user
        except get_user_model().DoesNotExist:
            return None
