from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class UserType(models.TextChoices):
    SUPER_ADMIN = 'super_admin', 'SUPER ADMIN'
    DOSEN = 'dosen', 'USER DOSEN'
    MAHASISWA = 'mahasiswa', 'USER MAHASISWA'

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nama Lengkap")
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.MAHASISWA)
    profile_picture = models.ImageField(upload_to='profile_pictures/%Y/%m/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    program_studi = models.CharField(max_length=50, choices=[
        ('Program Studi Bisnis Digital', 'Program Studi Bisnis Digital')
    ], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tempat_lahir = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ], blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_full_name(self):
        return self.full_name or self.username
        
    def get_short_name(self):
        return self.full_name or self.username

    class Meta:
        verbose_name_plural = "All User"
        verbose_name = "All User"
        ordering = ['-created_at']


# Model untuk Dosen
class UserDosen(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='dosen_profile',
    )
    nip = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="NIP")
    jabatan_akademik = models.CharField(max_length=50,
        choices=[
            ('Asisten Ahli', 'Asisten Ahli'),
            ('Lektor', 'Lektor'),
            ('Lektor Kepala', 'Lektor Kepala'),
            ('Profesor', 'Profesor'),
        ],
        blank=True
    )
    pendidikan_terakhir = models.CharField(
        max_length=10,
        choices=[
            ('S1', 'S1'),
            ('S2', 'S2'),
            ('S3', 'S3'),
        ],
        default='S2'
    )
    bidang_keahlian = models.CharField(max_length=100, blank=True)
    status_kepegawaian = models.CharField(
        max_length=20,
        choices=[
            ('PNS', 'PNS'),
            ('Non-PNS', 'Non-PNS'),
            ('Kontrak', 'Kontrak'),
        ],
        default='PNS'
    )
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.nip}"

    class Meta:
        verbose_name_plural = "User Dosen"
        verbose_name = "User Dosen"

# Model untuk Mahasiswa
class UserMahasiswa(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='mahasiswa_profile',
        limit_choices_to={'user_type': UserType.MAHASISWA}
    )
    nim = models.CharField(max_length=20, unique=True, verbose_name="NIM", null=True, blank=True)
    angkatan = models.CharField(max_length=4)
    semester = models.PositiveIntegerField(default=1)
    kelas = models.CharField(
        max_length=10,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('E', 'E'),
            ('F', 'F'),
            ('G', 'G'),
        ],
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Aktif', 'Aktif'),
            ('Cuti', 'Cuti'),
            ('Non-Aktif', 'Non-Aktif'),
            ('Lulus', 'Lulus'),
            ('DO', 'Drop Out'),
        ],
        default='Aktif'
    )
    ipk = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    dosen_wali = models.ForeignKey(
        UserDosen, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mahasiswa_bimbingan'
    )
    tanggal_masuk = models.DateField()
    
    def __str__(self):
        kelas_info = f" - Kelas {self.kelas}" if self.kelas else ""
        return f"{self.user.get_full_name()} - {self.nim}{kelas_info}"
    
    def clean(self):
        if self.user.user_type != UserType.MAHASISWA:
            raise ValidationError('User harus bertipe Mahasiswa')

    class Meta:
        verbose_name_plural = "User Mahasiswa"
        verbose_name = "User Mahasiswa"
        ordering = ['angkatan', 'kelas', 'nim']
