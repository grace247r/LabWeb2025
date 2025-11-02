from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import loginForm
from .models import Nilai

def login_view(request):
    """
    Menangani proses login pengguna. Jika dosen, akan langsung diarahkan
    ke halaman rekap nilai setelah login.
    """
    if request.user.is_authenticated:
        # Jika pengguna sudah login, arahkan sesuai peran
        role = getattr(getattr(request.user, "profile", None), "role", "MAHASISWA")
        if role == "DOSEN":
            return redirect("accounts:dosen-only")
        return redirect("accounts:dashboard")

    form = loginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            messages.success(request, "Berhasil masuk.")
            
            # Cek peran (role) setelah login berhasil
            role = getattr(getattr(user, "profile", None), "role", "MAHASISWA")
            if role == "DOSEN":
                # Jika dosen, langsung arahkan ke halaman rekap nilai
                return redirect("accounts:dosen-only")
            else:
                # Jika bukan dosen (mahasiswa), arahkan ke dashboard biasa
                return redirect("accounts:dashboard")
                
        messages.error(request, "Username atau password salah.")
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    Menangani proses logout pengguna.
    """
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect("accounts:login")

@login_required
def dashboard(request):
    """
    Menampilkan halaman dashboard. Jika pengguna adalah dosen,
    maka akan diarahkan ke halaman khusus dosen.
    """
    role = getattr(getattr(request.user, "profile", None), "role", "MAHASISWA")
    
    # Jika peran adalah DOSEN, langsung redirect ke halaman khusus dosen
    if role == "DOSEN":
        return redirect("accounts:dosen-only")
        
    # Jika bukan, tampilkan dashboard biasa (untuk MAHASISWA)
    return render(request, "accounts/dashboard.html", {"role": role})

# ---- Halaman Khusus Dosen ----

def is_dosen(user):
    """
    Fungsi helper untuk memeriksa apakah pengguna memiliki peran 'DOSEN'.
    """
    return hasattr(user, "profile") and user.profile.role == "DOSEN"

@login_required
@user_passes_test(is_dosen, login_url="accounts:dashboard")
def dosen_only_view(request):
    """
    Menampilkan rekap nilai untuk dosen yang sedang login.
    """
    rekap_nilai = []
    try:
        dosen_obj = request.user.dosen
        rekap_nilai = Nilai.objects.filter(
            mata_kuliah__dosen_pengampu=dosen_obj
        ).select_related('mahasiswa', 'mata_kuliah').order_by('mata_kuliah__nama', 'mahasiswa__nama_lengkap')
    except AttributeError:
        messages.error(request, "Profil dosen Anda tidak ditemukan.")
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan saat memuat data: {e}")

    context = {
        'rekap_nilai': rekap_nilai
    }
    return render(request, "accounts/dosen_only.html", context)

