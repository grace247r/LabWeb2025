from django.db import models

Grade = [
    ('excellent', 1),
    ('average', 0),
    ('bad', -1),
]

class DRFPost(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    uploaded = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=10, choices=Grade, default='average')
    image = models.ImageField(upload_to='image/', blank=True, null=True, default=None)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.name
    

class dosen(models.Model):
    nama = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
    
class mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=100)
    mentor = models.ForeignKey(dosen, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama