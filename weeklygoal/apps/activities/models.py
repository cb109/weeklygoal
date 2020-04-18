from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _
from filer.fields.image import FilerImageField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.modified_at = datetime.now()
        super().save(*args, **kwargs)


class Activity(BaseModel):
    name = models.CharField(max_length=128)
    image = FilerImageField(
        null=True, blank=True, related_name="image_activity", on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Event(BaseModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        day_str = _(self.created_at.date().strftime("%A"))
        date_str = self.created_at.date().strftime(f"%d.%m.%Y")
        return f"{self.activity.name} @ {day_str}, {date_str}"
