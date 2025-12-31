import utils.crud as db
import datetime
from config.db import STAF_FILE, ANTRIAN_FILE, PASIEN_FILE, RIWAYAT_MEDIS_FILE, DETAIL_RESEP_FILE
from utils.crud import read_csv, write_csv, append_csv, generate_id
from .auth import log_aktivitas
from datetime import date

# ==================== MENU DOKTER ====================
def menu_dokter(user):
    """Menu utama untuk dokter"""
    while True:
        print("\n" + "="*50)
        print(f"     MENU DOKTER - {user['nama']}")
        print("="*50)
        print("[1] Lihat Daftar Antrian")
        print("[2] Periksa Pasien")
        print("[3] Lihat Riwayat Medis Pasien")
        print("[0] Logout")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            lihat_daftar_antrian_dokter(user)
        elif pilihan == "2":
            periksa_pasien(user)
        elif pilihan == "3":
            lihat_riwayat_medis_dokter()
        elif pilihan == "0":
            log_aktivitas(user['id_user'], "Logout dokter")
            print("\n>>> Logout berhasil!")
            break

def lihat_daftar_antrian_dokter(user):
    """Dokter melihat daftar antrian pasien"""
    print("\n--- Daftar Antrian Pasien ---")

    antrian_list = read_csv(ANTRIAN_FILE)
    pasien_list = read_csv(PASIEN_FILE)

    today = date.today().strftime("%Y-%m-%d")
    antrian_dokter = [a for a in antrian_list if a['id_dokter'] == user['id_user'] and a['tanggal'] == today]

    if not antrian_dokter:
        print(">>> Tidak ada antrian untuk hari ini.")
        return

    print(f"\nTanggal: {today}")
    print("-" * 60)
    print(f"{'No':<5} {'No.Antrian':<12} {'Nama Pasien':<20} {'Keluhan':<15} {'Status':<10}")
    print("-" * 60)

    for i, antrian in enumerate(antrian_dokter, 1):
        pasien = next((p for p in pasien_list if p['id_pasien'] == antrian['id_pasien']), None)
        nama_pasien = pasien['nama'] if pasien else "N/A"
        print(f"{i:<5} {antrian['no_antrian']:<12} {nama_pasien:<20} {antrian['keluhan'][:15]:<15} {antrian['status_antrian']:<10}")

def periksa_pasien(user):
    """Dokter melakukan pemeriksaan pasien"""
    print("\n--- Periksa Pasien ---")

    antrian_list = read_csv(ANTRIAN_FILE)
    pasien_list = db.read_csv(PASIEN_FILE)

    today = datetime.date.today().strftime("%Y-%m-%d")
    antrian_menunggu = [a for a in antrian_list if a['id_dokter'] == user['id_user'] 
                        and a['tanggal'] == today and a['status_antrian'] == "Menunggu"]

    if not antrian_menunggu:
        print(">>> Tidak ada pasien yang menunggu.")
        return

    # Ambil pasien pertama yang menunggu
    antrian = antrian_menunggu[0]
    pasien = next((p for p in pasien_list if p['id_pasien'] == antrian['id_pasien']), None)

    if not pasien:
        print(">>> Data pasien tidak ditemukan!")
        return

    print(f"\nPasien: {pasien['nama']}")
    print(f"NIK: {pasien['NIK']}")
    print(f"Jenis Kelamin: {pasien['jenis_kelamin']}")
    print(f"Tanggal Lahir: {pasien['tanggal_lahir']}")
    print(f"Keluhan Awal: {antrian['keluhan']}")
    print("-" * 40)

    # Input pemeriksaan
    keluhan_detail = input("Keluhan (detail): ")
    diagnosa = input("Diagnosa: ")
    catatan = input("Catatan/Saran: ")

    # Simpan riwayat medis
    id_riwayat = db.generate_id("RIW")
    riwayat_data = {
        "id_riwayat": id_riwayat,
        "id_pasien": pasien['id_pasien'],
        "id_dokter": user['id_user'],
        "keluhan": keluhan_detail,
        "diagnosa": diagnosa,
        "tanggal": today,
        "catatan": catatan
    }
    append_csv(RIWAYAT_MEDIS_FILE, riwayat_data)

    # Input resep obat
    print("\n--- Input Resep Obat ---")
    while True:
        obat = input("Nama Obat (kosongkan untuk selesai): ")
        if not obat:
            break
        dosis = input("Dosis: ")
        aturan_pakai = input("Aturan Pakai: ")

        resep_data = {
            "id_detail_resep": generate_id("RES"),
            "riwayat_id": id_riwayat,
            "obat": obat,
            "dosis": dosis,
            "aturan_pakai": aturan_pakai
        }
        append_csv(DETAIL_RESEP_FILE, resep_data)

    # Update status antrian
    for a in antrian_list:
        if a['id_antrian'] == antrian['id_antrian']:
            a['status_antrian'] = "Selesai"
            break

    fieldnames = ["id_antrian", "id_pasien", "id_dokter", "no_antrian", "keluhan", "tanggal", "jam", "status_antrian", "catatan"]
    write_csv(ANTRIAN_FILE, antrian_list, fieldnames)

    log_aktivitas(user['id_user'], f"Pemeriksaan pasien {pasien['nama']}")
    print("\n>>> Pemeriksaan selesai dan data tersimpan!")

def lihat_riwayat_medis_dokter():
    """Dokter melihat riwayat medis berdasarkan pasien"""
    print("\n--- Cari Riwayat Medis Pasien ---")

    keyword = input("Masukkan nama/NIK pasien: ")

    pasien_list = read_csv(PASIEN_FILE)
    riwayat_list = read_csv(RIWAYAT_MEDIS_FILE)
    resep_list = read_csv(DETAIL_RESEP_FILE)
    staf_list = read_csv(STAF_FILE)

    # Cari pasien
    pasien_ditemukan = [p for p in pasien_list if keyword.lower() in p['nama'].lower() or keyword in p['NIK']]

    if not pasien_ditemukan:
        print(">>> Pasien tidak ditemukan.")
        return

    for pasien in pasien_ditemukan:
        print(f"\n{'='*50}")
        print(f"Pasien: {pasien['nama']} (NIK: {pasien['NIK']})")
        print(f"{'='*50}")

        riwayat_pasien = [r for r in riwayat_list if r['id_pasien'] == pasien['id_pasien']]

        if not riwayat_pasien:
            print(">>> Belum ada riwayat medis.")
            continue

        for riwayat in riwayat_pasien:
            dokter = next((s for s in staf_list if s['id_user'] == riwayat['id_dokter']), None)
            dokter_nama = dokter['nama'] if dokter else "N/A"

            print(f"\n  Tanggal: {riwayat['tanggal']}")
            print(f"  Dokter: {dokter_nama}")
            print(f"  Keluhan: {riwayat['keluhan']}")
            print(f"  Diagnosa: {riwayat['diagnosa']}")
            print(f"  Catatan: {riwayat['catatan'] if riwayat['catatan'] else '-'}")

            resep_riwayat = [res for res in resep_list if res['riwayat_id'] == riwayat['id_riwayat']]
            if resep_riwayat:
                print("  Resep Obat:")
                for res in resep_riwayat:
                    print(f"    - {res['obat']} ({res['dosis']}) - {res['aturan_pakai']}")
            print("-" * 40)
