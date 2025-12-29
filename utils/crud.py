import csv
import hashlib
import os
import uuid
from config.db import STAF_FILE, PASIEN_FILE, ANTRIAN_FILE, RIWAYAT_MEDIS_FILE

def hash_password(password):
    """Hash password menggunakan SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_id(prefix=""):
    """Generate unique ID"""
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_csv(file_path):
    """Membaca data dari CSV dan mengembalikan list of dictionary"""
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def write_csv(file_path, data, fieldnames):
    """Menulis ulang seluruh data ke CSV"""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file_path, row_data):
    """Menambahkan satu baris data baru ke akhir CSV"""
    # Cek apakah file ada untuk menentukan apakah perlu tulis header
    file_exists = os.path.exists(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)

def create_default_admin():
    """Membuat akun admin default jika belum ada"""
    staf = read_csv(STAF_FILE)
    admin_exists = any(s['jabatan'] == 'Admin' for s in staf)

    if not admin_exists:
        admin_data = {
            "id_user": generate_id("ADM"),
            "nama": "Administrator",
            "username": "admin",
            "password": hash_password("admin123"),
            "email": "admin@sipeka.com",
            "jabatan": "Admin",
            "NIP": "000000000",
            "spesialisasi": "-",
            "kontak": "080000000000",
            "jadwal": "-",
            "shift": "-"
        }
        append_csv(STAF_FILE, admin_data)
        print(">>> Admin default dibuat (username: admin, password: admin123)")

def ambil_antrian_dokter():
    """
    Mengambil antrian status 'menunggu' dan menggabungkan (JOIN) 
    dengan nama pasien dari file pasien.csv secara efisien.
    """
    list_pasien = read_csv(PASIEN_FILE)
    map_pasien = {p['id_pasien']: p['nama'] for p in list_pasien}

    antrian_raw = read_csv(ANTRIAN_FILE)
    antrian_bersih = []

    for row in antrian_raw:
        status = row.get('status_antrian', '').lower()
        if status == 'menunggu': 
            id_pasien = row['id_pasien']
            
            nama_pasien = map_pasien.get(id_pasien, "Nama Tidak Ditemukan")
            
            data_gabungan = {
                'id_antrian': row['id_antrian'],
                'id_pasien': row['id_pasien'],
                'nama': nama_pasien,
                'keluhan': row['keluhan'],
                'no_antrian': row['no_antrian']
            }
            antrian_bersih.append(data_gabungan)
            
    return antrian_bersih

def simpan_diagnosa(data_diagnosa):
    """Menyimpan hasil pemeriksaan ke riwayat_medis.csv"""
    append_csv(RIWAYAT_MEDIS_FILE, data_diagnosa)

def update_status_antrian(id_antrian_target, status_baru='selesai'):
    """Mengupdate status di antrian.csv menjadi 'selesai'"""
    semua_antrian = read_csv(ANTRIAN_FILE)
    updated_data = []
    is_updated = False
    
    for row in semua_antrian:
        if row['id_antrian'] == id_antrian_target:
            row['status_antrian'] = status_baru
            is_updated = True
        updated_data.append(row)
    
    if is_updated and updated_data:
        fieldnames = list(updated_data[0].keys())
        write_csv(ANTRIAN_FILE, updated_data, fieldnames)
        return True
    return False