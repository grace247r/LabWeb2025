from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ("MAHASISWA", "Mahasiswa"),
        ("DOSEN", "Dosen"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="MAHASISWA")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
class Dosen(models.Model):
    """
    Model untuk menyimpan data Dosen.
    Terhubung dengan User yang memiliki peran 'DOSEN'.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'DOSEN'})
    nama_lengkap = models.CharField(max_length=100)
    nidn = models.CharField(max_length=20, unique=True, verbose_name="Nomor Induk Dosen Nasional")

    def __str__(self):
        return self.nama_lengkap

class Mahasiswa(models.Model):
    """
    Model untuk menyimpan data Mahasiswa.
    Terhubung dengan User yang memiliki peran 'MAHASISWA'.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'MAHASISWA'})
    nama_lengkap = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True, verbose_name="Nomor Induk Mahasiswa")

    def __str__(self):
        return f'{self.nama_lengkap} ({self.nim})'

class MataKuliah(models.Model):
    """
    Model untuk menyimpan data Mata Kuliah.
    Setiap mata kuliah diajar oleh satu dosen.
    """
    nama = models.CharField(max_length=100)
    kode_mk = models.CharField(max_length=10, unique=True, verbose_name="Kode Mata Kuliah")
    dosen_pengampu = models.ForeignKey(Dosen, on_delete=models.SET_NULL, null=True, related_name="mata_kuliah_diampu")

    def __str__(self):
        return f'{self.nama} ({self.kode_mk})'

class Nilai(models.Model):
    """
    Model untuk merekam nilai seorang Mahasiswa pada suatu Mata Kuliah.
    Pastikan model ini ada dan namanya sudah benar.
    """
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name="nilai_mahasiswa")
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, related_name="nilai_matakuliah")
    nilai_huruf = models.CharField(max_length=2, help_text="Contoh: A, B+, C, D, E")
    nilai_angka = models.FloatField(default=0.0)

    class Meta:
        # Menjadikan setiap mahasiswa hanya bisa punya satu nilai per mata kuliah
        unique_together = ('mahasiswa', 'mata_kuliah')
        verbose_name_plural = "Daftar Nilai"

    def __str__(self):
        return f'Nilai {self.mahasiswa} untuk {self.mata_kuliah}: {self.nilai_huruf}'
