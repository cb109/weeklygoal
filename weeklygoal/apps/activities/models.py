from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from filer.fields.image import FilerImageField

from colorfield.fields import ColorField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.modified_at = datetime.now()
        super().save(*args, **kwargs)


class Activity(BaseModel):
    class Meta:
        verbose_name_plural = "Activities"

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=128)
    image = FilerImageField(
        null=True, blank=True, related_name="image_activity", on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class UserSettings(BaseModel):
    class Meta:
        verbose_name_plural = "User settings"

    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, related_name="settings"
    )

    goal = models.IntegerField(default=5)

    background_color = ColorField(default=settings.COLOR_BACKGROUND_DEFAULT)
    highlight_color = ColorField(default=settings.COLOR_HIGHLIGHT_DEFAULT)
    text_color = ColorField(default=settings.COLOR_TEXT_DEFAULT)
    checkmark_color = ColorField(default=settings.COLOR_CHECKMARK_DEFAULT)

    def __str__(self):
        return f"UserSettings for {self.user}"


class Event(BaseModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        day_str = _(self.created_at.date().strftime("%A"))
        date_str = self.created_at.date().strftime(f"%d.%m.%Y")
        return f"{self.activity.name} @ {day_str}, {date_str}"
