import pytz
from accounts.models import User, UserProfile
from django.db import models
from accounts.utils import send_notification
from datetime import time, date, datetime


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def is_open(self):
        today = date.today().isoweekday()
        current_time = datetime.now(pytz.timezone('America/Toronto'))
        now = current_time.strftime("%H:%M:%S")
        current_opening_hours = OpeningHours.objects.filter(vendor=self, day=today)
        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, '%I:%M %p').time())
                end = str(datetime.strptime(i.to_hour, '%I:%M %p').time())
                if start < now < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:

            vendor_user = Vendor.objects.get(pk=self.pk)
            if vendor_user.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    'user': self.user,
                    'vendor_user': vendor_user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved:
                    # send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    mail_template = "accounts/emails/admin_approval_email.html"
                    context = {
                        'user': self.user,
                        'vendor_user': vendor_user,
                        'is_approved': self.is_approved,
                        'to_email': self.user.email,
                    }
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = "Sorry! Your restaurant is not approved to share menu on our marketplace."

                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)


DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday"))
]

HOURS = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]


class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOURS, max_length=12, blank=True)
    to_hour = models.CharField(choices=HOURS, max_length=12, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()
