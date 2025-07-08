from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserDosen, UserMahasiswa

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Fields to display in the list view
    list_display = ('username', 'full_name', 'email', 'user_type', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active', 'gender', 'created_at')
    search_fields = ('username', 'full_name', 'email', 'phone_number')
    ordering = ('-created_at',)
    
    # Fieldsets for the add/edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'full_name', 'email', 'phone_number', 'profile_picture',
                'tempat_lahir', 'birth_date', 'gender', 'program_studi'
            )
        }),
        ('Permissions', {
            'fields': (
                'user_type', 'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'full_name', 'email', 'password1', 'password2',
                'user_type', 'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

@admin.register(UserDosen)
class UserDosenAdmin(admin.ModelAdmin):
    list_display = ('user', 'nip', 'jabatan_akademik', 'pendidikan_terakhir', 'status_kepegawaian')
    list_filter = ('jabatan_akademik', 'pendidikan_terakhir', 'status_kepegawaian')
    search_fields = ('user__full_name', 'user__username', 'nip', 'bidang_keahlian')
    ordering = ('user__full_name',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Dosen Information', {
            'fields': ('nip', 'jabatan_akademik', 'pendidikan_terakhir', 'bidang_keahlian', 'status_kepegawaian')
        }),
    )

@admin.register(UserMahasiswa)
class UserMahasiswaAdmin(admin.ModelAdmin):
    list_display = ('user', 'nim', 'angkatan', 'semester', 'kelas', 'status', 'ipk', 'dosen_wali')
    list_filter = ('angkatan', 'semester', 'kelas', 'status', 'dosen_wali')
    search_fields = ('user__full_name', 'user__username', 'nim')
    ordering = ('angkatan', 'kelas', 'nim')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Mahasiswa Information', {
            'fields': ('nim', 'angkatan', 'semester', 'kelas', 'status', 'ipk', 'dosen_wali', 'tanggal_masuk')
        }),
    )
