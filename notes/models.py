from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title
    