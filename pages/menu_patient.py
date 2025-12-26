from datetime import datetime
from datetime import date

from config.db import STAF_FILE, ANTRIAN_FILE, PASIEN_FILE, RIWAYAT_MEDIS_FILE, DETAIL_RESEP_FILE
from utils.crud import read_csv, append_csv, write_csv, generate_id
from pages.auth import log_aktivitas


# ==================== MENU PASIEN ====================
def menu_pasien(user):
    """Menu utama untuk pasien"""
    while True:
        print("\n" + "="*50)
        print(f"     MENU PASIEN - {user['nama']}")
        print("="*50)
        print("[1] Daftar Antrian")
        print("[2] Lihat Status Antrian")
        print("[3] Lihat Riwayat Medis")
        print("[4] Update Profil")
        print("[0] Logout")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            daftar_antrian(user)
        elif pilihan == "2":
            lihat_status_antrian(user)
        elif pilihan == "3":
            lihat_riwayat_medis_pasien(user)
        elif pilihan == "4":
            update_profil_pasien(user)
        elif pilihan == "0":
            log_aktivitas(user['id_pasien'], "Logout pasien")
            print("\n>>> Logout berhasil!")
            break

def daftar_antrian(user):
    """Pasien mendaftar antrian"""
    print("\n--- Daftar Antrian ---")

    # Tampilkan daftar dokter yang tersedia
    staf_list = read_csv(STAF_FILE)
    dokter_list = [s for s in staf_list if s['jabatan'] == 'Dokter']

    if not dokter_list:
        print(">>> Belum ada dokter yang tersedia.")
        return

    print("\nDaftar Dokter:")
    for i, dokter in enumerate(dokter_list, 1):
        print(f"  [{i}] {dokter['nama']} - {dokter['spesialisasi']}")

    try:
        pilihan_dokter = int(input("\nPilih dokter (nomor): ")) - 1
        if pilihan_dokter < 0 or pilihan_dokter >= len(dokter_list):
            print(">>> Pilihan tidak valid!")
            return
    except ValueError:
        print(">>> Input tidak valid!")
        return

    dokter_terpilih = dokter_list[pilihan_dokter]
    keluhan = input("Keluhan: ")

    # Generate nomor antrian
    antrian_list = read_csv(ANTRIAN_FILE)
    today = date.today().strftime("%Y-%m-%d")
    antrian_hari_ini = [a for a in antrian_list if a['tanggal'] == today]
    no_antrian = f"A-{len(antrian_hari_ini) + 1:03d}"

    antrian_data = {
        "id_antrian": generate_id("ANT"),
        "id_pasien": user['id_pasien'],
        "id_dokter": dokter_terpilih['id_user'],
        "no_antrian": no_antrian,
        "keluhan": keluhan,
        "tanggal": today,
        "jam": datetime.now().strftime("%H:%M:%S"),
        "status_antrian": "Menunggu",
        "catatan": ""
    }

    append_csv(ANTRIAN_FILE, antrian_data)
    log_aktivitas(user['id_pasien'], f"Daftar antrian {no_antrian}")
    print(f"\n>>> Pendaftaran berhasil!")
    print(f">>> Nomor Antrian Anda: {no_antrian}")
    print(f">>> Dokter: {dokter_terpilih['nama']}")

def lihat_status_antrian(user):
    """Lihat status antrian pasien"""
    print("\n--- Status Antrian Anda ---")

    antrian_list = read_csv(ANTRIAN_FILE)
    staf_list = read_csv(STAF_FILE)

    antrian_pasien = [a for a in antrian_list if a['id_pasien'] == user['id_pasien']]

    if not antrian_pasien:
        print(">>> Anda belum memiliki antrian.")
        return

    today = date.today().strftime("%Y-%m-%d")
    for antrian in antrian_pasien:
        dokter = next((s for s in staf_list if s['id_user'] == antrian['id_dokter']), None)
        dokter_nama = dokter['nama'] if dokter else "N/A"

        status_icon = "⏳" if antrian['status_antrian'] == "Menunggu" else "✅" if antrian['status_antrian'] == "Selesai" else "🔄"

        print(f"\n  No. Antrian: {antrian['no_antrian']}")
        print(f"  Tanggal: {antrian['tanggal']}")
        print(f"  Dokter: {dokter_nama}")
        print(f"  Keluhan: {antrian['keluhan']}")
        print(f"  Status: {status_icon} {antrian['status_antrian']}")
        print(f"  Catatan: {antrian['catatan'] if antrian['catatan'] else '-'}")
        print("-" * 40)

def lihat_riwayat_medis_pasien(user):
    """Lihat riwayat medis pasien"""
    print("\n--- Riwayat Medis Anda ---")

    riwayat_list = read_csv(RIWAYAT_MEDIS_FILE)
    resep_list = read_csv(DETAIL_RESEP_FILE)
    staf_list = read_csv(STAF_FILE)

    riwayat_pasien = [r for r in riwayat_list if r['id_pasien'] == user['id_pasien']]

    if not riwayat_pasien:
        print(">>> Belum ada riwayat medis.")
        return

    for riwayat in riwayat_pasien:
        dokter = next((s for s in staf_list if s['id_user'] == riwayat['id_dokter']), None)
        dokter_nama = dokter['nama'] if dokter else "N/A"

        print(f"\n  Tanggal: {riwayat['tanggal']}")
        print(f"  Dokter: {dokter_nama}")
        print(f"  Keluhan: {riwayat['keluhan']}")
        print(f"  Diagnosa: {riwayat['diagnosa']}")
        print(f"  Catatan: {riwayat['catatan'] if riwayat['catatan'] else '-'}")

        # Tampilkan resep obat
        resep_riwayat = [res for res in resep_list if res['riwayat_id'] == riwayat['id_riwayat']]
        if resep_riwayat:
            print("  Resep Obat:")
            for res in resep_riwayat:
                print(f"    - {res['obat']} ({res['dosis']}) - {res['aturan_pakai']}")
        print("-" * 40)

def update_profil_pasien(user):
    """Update profil pasien"""
    print("\n--- Update Profil ---")
    print(f"Nama: {user['nama']}")
    print(f"Email: {user['email']}")
    print(f"No. Telepon: {user['no_telp']}")
    print(f"Alamat: {user['alamat']}")

    print("\n(Kosongkan jika tidak ingin mengubah)")

    nama_baru = input(f"Nama baru [{user['nama']}]: ") or user['nama']
    no_telp_baru = input(f"No. Telepon baru [{user['no_telp']}]: ") or user['no_telp']
    alamat_baru = input(f"Alamat baru [{user['alamat']}]: ") or user['alamat']

    pasien_list = read_csv(PASIEN_FILE)
    for pasien in pasien_list:
        if pasien['id_pasien'] == user['id_pasien']:
            pasien['nama'] = nama_baru
            pasien['no_telp'] = no_telp_baru
            pasien['alamat'] = alamat_baru
            user.update(pasien)
            break

    fieldnames = ["id_pasien", "nama", "NIK", "password", "alamat", "no_telp", "jenis_kelamin", "email", "tanggal_lahir"]
    write_csv(PASIEN_FILE, pasien_list, fieldnames)

    log_aktivitas(user['id_pasien'], "Update profil pasien")
    print("\n>>> Profil berhasil diupdate!")