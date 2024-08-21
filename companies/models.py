from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    path = models.CharField(max_length=200, unique=True)
    website = models.URLField(unique=True)

    class Meta:
        verbose_name_plural = _("Companies")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
    def generate_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        num = 1
        while Company.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

