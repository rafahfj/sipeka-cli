import pwinput
from datetime import datetime
from utils.crud import read_csv, append_csv
from utils.crud import hash_password
from utils.crud import generate_id

# ==================== AUTENTIKASI ====================

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
    password = pwinput.pwinput("Password: ", mask="*")

    if not email.strip() or not password.strip():
        print("\n>>> Email dan Password tidak boleh kosong!")
        return None, None

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