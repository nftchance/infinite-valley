from django.db import models

from .sdxl import get_image


class Day(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.IntegerField(null=True, blank=True)
    image_data = models.TextField(null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_image(self, text_pipe, image_pipe):
        if self.image_data is not None:
            return

        last_image = Day.objects.all().order_by('-id').first()
        last_image_data = last_image.image_data if last_image else None

        (self.prompt, self.image_data) = get_image(
            text_pipe,
            image_pipe,
            self.day,
            last_image_data
        )

        self.save()

    def __str__(self):
        if self.day is None:
            return "Failure"

        return f"Day {self.day}"
