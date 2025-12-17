import csv
import hashlib
import os
import uuid

from config.db import STAF_FILE


def hash_password(password):
    """Hash password menggunakan SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_id(prefix=""):
    """Generate unique ID"""
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def read_csv(file_path):
    """Membaca data dari CSV"""
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def write_csv(file_path, data, fieldnames):
    """Menulis data ke CSV"""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file_path, row_data):
    """Menambahkan satu baris ke CSV"""
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row_data.keys())
        writer.writerow(row_data)

def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_default_admin():
    """Membuat akun admin default"""
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
            "spesialisasi": "",
            "kontak": "000000000000",
            "jadwal": "",
            "shift": ""
        }
        append_csv(STAF_FILE, admin_data)
        print(">>> Admin default dibuat (username: admin, password: admin123)")