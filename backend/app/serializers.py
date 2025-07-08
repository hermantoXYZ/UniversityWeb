from rest_framework import serializers
from .models import CustomUser, UserDosen, UserMahasiswa

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'full_name', 'email', 'user_type', 
            'phone_number', 'profile_picture', 'tempat_lahir', 
            'birth_date', 'gender', 'program_studi', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class UserDosenSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(user_type='dosen'),
        source='user',
        write_only=True
    )

    class Meta:
        model = UserDosen
        fields = [
            'id', 'user', 'user_id', 'nip', 'jabatan_akademik',
            'pendidikan_terakhir', 'bidang_keahlian', 'status_kepegawaian'
        ]
        read_only_fields = ['id']

class UserMahasiswaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(user_type='mahasiswa'),
        source='user',
        write_only=True
    )
    dosen_wali_name = serializers.CharField(source='dosen_wali.user.full_name', read_only=True)

    class Meta:
        model = UserMahasiswa
        fields = [
            'id', 'user', 'user_id', 'nim', 'angkatan', 'semester',
            'kelas', 'status', 'ipk', 'dosen_wali', 'dosen_wali_name',
            'tanggal_masuk'
        ]
        read_only_fields = ['id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'full_name', 'email', 'password', 'password_confirm',
            'user_type', 'phone_number', 'tempat_lahir', 'birth_date', 'gender'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user 