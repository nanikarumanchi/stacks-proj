from django.db import models

from accounts.models import GuestEmail


class BillingManager(models.Manager):
    def new_or_get(self, request):
        obj=None
        is_created = False
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        if user.is_authenticated:
            obj, is_created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, is_created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, is_created
