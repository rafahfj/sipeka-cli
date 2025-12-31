from datetime import date
from utils.crud import read_csv, write_csv

from config.db import ANTRIAN_FILE, PASIEN_FILE, RIWAYAT_MEDIS_FILE, STAF_FILE
from .auth import log_aktivitas
from .regist_patient import registrasi_pasien


def menu_receptionist(user):
    """Menu utama untuk resepsionis"""
    while True:
        print("\n" + "="*50)
        print(f"     MENU RESEPSIONIS - {user['nama']}")
        print("="*50)
        print("[1] Lihat Daftar Antrian")
        print("[2] Verifikasi Antrian Pasien")
        print("[3] Daftarkan Pasien Baru")
        print("[4] Lihat Laporan Harian")
        print("[0] Logout")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            lihat_daftar_antrian_resepsionis()
        elif pilihan == "2":
            verifikasi_antrian()
        elif pilihan == "3":
            daftarkan_pasien_baru()
        elif pilihan == "4":
            lihat_laporan_harian()
        elif pilihan == "0":
            log_aktivitas(user['id_user'], "Logout resepsionis")
            print("\n>>> Logout berhasil!")
            break

def lihat_daftar_antrian_resepsionis():
    """Resepsionis melihat semua antrian hari ini"""
    print("\n--- Daftar Antrian Hari Ini ---")

    antrian_list = read_csv(ANTRIAN_FILE)
    pasien_list = read_csv(PASIEN_FILE)
    staf_list = read_csv(STAF_FILE)

    today = date.today().strftime("%Y-%m-%d")
    antrian_hari_ini = [a for a in antrian_list if a['tanggal'] == today]

    if not antrian_hari_ini:
        print(">>> Tidak ada antrian untuk hari ini.")
        return

    print(f"\nTanggal: {today}")
    print(f"Total Antrian: {len(antrian_hari_ini)}")
    print("-" * 80)
    print(f"{'No':<5} {'No.Antrian':<12} {'Nama Pasien':<18} {'Dokter':<18} {'Status':<12} {'Jam':<10}")
    print("-" * 80)

    for i, antrian in enumerate(antrian_hari_ini, 1):
        pasien = next((p for p in pasien_list if p['id_pasien'] == antrian['id_pasien']), None)
        dokter = next((s for s in staf_list if s['id_user'] == antrian['id_dokter']), None)
        nama_pasien = pasien['nama'] if pasien else "N/A"
        nama_dokter = dokter['nama'] if dokter else "N/A"
        print(f"{i:<5} {antrian['no_antrian']:<12} {nama_pasien[:18]:<18} {nama_dokter[:18]:<18} {antrian['status_antrian']:<12} {antrian['jam']:<10}")

def verifikasi_antrian():
    """Resepsionis memverifikasi kedatangan pasien"""
    print("\n--- Verifikasi Antrian ---")

    no_antrian = input("Masukkan No. Antrian: ")

    antrian_list = read_csv(ANTRIAN_FILE)
    pasien_list = read_csv(PASIEN_FILE)
    today = date.today().strftime("%Y-%m-%d")

    antrian = next((a for a in antrian_list if a['no_antrian'] == no_antrian and a['tanggal'] == today), None)

    if not antrian:
        print(">>> Antrian tidak ditemukan!")
        return

    pasien = next((p for p in pasien_list if p['id_pasien'] == antrian['id_pasien']), None)

    print(f"\nPasien: {pasien['nama'] if pasien else 'N/A'}")
    print(f"Status saat ini: {antrian['status_antrian']}")

    catatan = input("Catatan (opsional): ")

    for a in antrian_list:
        if a['no_antrian'] == no_antrian:
            a['status_antrian'] = "Diverifikasi"
            a['catatan'] = catatan
            break

    fieldnames = ["id_antrian", "id_pasien", "id_dokter", "no_antrian", "keluhan", "tanggal", "jam", "status_antrian", "catatan"]
    write_csv(ANTRIAN_FILE, antrian_list, fieldnames)

    print("\n>>> Antrian berhasil diverifikasi!")

def daftarkan_pasien_baru():
    """Resepsionis mendaftarkan pasien baru"""
    print("\n--- Daftarkan Pasien Baru ---")
    registrasi_pasien()

def lihat_laporan_harian():
    """Lihat laporan harian klinik"""
    print("\n--- Laporan Harian ---")

    antrian_list = read_csv(ANTRIAN_FILE)
    riwayat_list = read_csv(RIWAYAT_MEDIS_FILE)

    today = date.today().strftime("%Y-%m-%d")

    antrian_hari_ini = [a for a in antrian_list if a['tanggal'] == today]
    riwayat_hari_ini = [r for r in riwayat_list if r['tanggal'] == today]

    menunggu = sum(1 for a in antrian_hari_ini if a['status_antrian'] == "Menunggu")
    diverifikasi = sum(1 for a in antrian_hari_ini if a['status_antrian'] == "Diverifikasi")
    selesai = sum(1 for a in antrian_hari_ini if a['status_antrian'] == "Selesai")

    print(f"\nTanggal: {today}")
    print("=" * 40)
    print(f"Total Antrian     : {len(antrian_hari_ini)}")
    print(f"  - Menunggu      : {menunggu}")
    print(f"  - Diverifikasi  : {diverifikasi}")
    print(f"  - Selesai       : {selesai}")
    print(f"Total Pemeriksaan : {len(riwayat_hari_ini)}")
    print("=" * 40)