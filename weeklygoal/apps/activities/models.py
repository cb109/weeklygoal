from django.db import models
from django.utils import timezone
from filer.fields.image import FilerImageField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)


class Activity(BaseModel):
    name = models.CharField(max_length=128)
    image = FilerImageField(
        null=True, blank=True, related_name="image_activity", on_delete=models.CASCADE
    )
