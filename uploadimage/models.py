from django.db import models

class File(models.Model):
    # all images from front will be saved in directory static/images
    file = models.FileField(upload_to='static/images', blank=False, null=False)

    def __str__(self):
        return self.file.name

