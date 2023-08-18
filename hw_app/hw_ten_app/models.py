from django.db import models


# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True, null=False)
    born_date = models.DateTimeField()
    born_location = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.quote[:50]}"
