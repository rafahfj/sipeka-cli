# ==================== AUTENTIKASI ====================
from datetime import datetime
from utils.crud import read_csv, append_csv
from utils.crud import hash_password
from utils.crud import generate_id

from config.db import PASIEN_FILE, STAF_FILE, LAPORAN_HARIAN_FILE

def login():
    """Proses login pengguna"""
    print("\n" + "="*50)
    print("           LOGIN SIPEKA")
    print("="*50)
    print("\n[1] Login sebagai Pasien")
    print("[2] Login sebagai Staf (Dokter/Resepsionis/Admin)")
    print("[0] Kembali")

    pilihan = input("\nPilih opsi: ")

    if pilihan == "1":
        return login_pasien()
    elif pilihan == "2":
        return login_staf()
    else:
        return None, None

def login_pasien():
    """Login untuk pasien"""
    print("\n--- Login Pasien ---")
    email = input("Email: ")
    password = input("Password: ")

    pasien_list = read_csv(PASIEN_FILE)
    for pasien in pasien_list:
        if pasien['email'] == email and pasien['password'] == hash_password(password):
            log_aktivitas(pasien['id_pasien'], "Login pasien berhasil")
            print(f"\n>>> Login berhasil! Selamat datang, {pasien['nama']}")
            return pasien, "Pasien"

    print("\n>>> Email atau password salah!")
    return None, None

def login_staf():
    """Login untuk staf (Dokter/Resepsionis/Admin)"""
    print("\n--- Login Staf ---")
    username = input("Username: ")
    password = input("Password: ")

    staf_list = read_csv(STAF_FILE)
    for staf in staf_list:
        if staf['username'] == username and staf['password'] == hash_password(password):
            log_aktivitas(staf['id_user'], f"Login {staf['jabatan']} berhasil")
            print(f"\n>>> Login berhasil! Selamat datang, {staf['nama']} ({staf['jabatan']})")
            return staf, staf['jabatan']

    print("\n>>> Username atau password salah!")
    return None, None

def log_aktivitas(id_user, aktivitas):
    """Mencatat log aktivitas pengguna"""
    log_data = {
        "id_log": generate_id("LOG"),
        "id_user": id_user,
        "waktu_aktivitas": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aktivitas_terakhir": aktivitas
    }
    append_csv(LAPORAN_HARIAN_FILE, log_data)

# ==================== REGISTRASI PASIEN ====================
def registrasi_pasien():
    """Registrasi pasien baru"""
    print("\n" + "="*50)
    print("       REGISTRASI PASIEN BARU")
    print("="*50)

    nama = input("Nama Lengkap: ")
    nik = input("NIK (16 digit): ")
    email = input("Email: ")

    # Validasi email unik
    pasien_list = read_csv(PASIEN_FILE)
    if any(p['email'] == email for p in pasien_list):
        print("\n>>> Email sudah terdaftar!")
        return

    if any(p['NIK'] == nik for p in pasien_list):
        print("\n>>> NIK sudah terdaftar!")
        return

    password = input("Password: ")
    confirm_password = input("Konfirmasi Password: ")

    if password != confirm_password:
        print("\n>>> Password tidak cocok!")
        return

    alamat = input("Alamat: ")
    no_telp = input("No. Telepon: ")
    jenis_kelamin = input("Jenis Kelamin (L/P): ").upper()
    tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")

    pasien_data = {
        "id_pasien": generate_id("PAS"),
        "nama": nama,
        "NIK": nik,
        "password": hash_password(password),
        "alamat": alamat,
        "no_telp": no_telp,
        "jenis_kelamin": jenis_kelamin,
        "email": email,
        "tanggal_lahir": tanggal_lahir
    }

    append_csv(PASIEN_FILE, pasien_data)
    print(f"\n>>> Registrasi berhasil! ID Pasien Anda: {pasien_data['id_pasien']}")
