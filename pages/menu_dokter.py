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

def tampilkan_antrian():
    print("="*60)
    print("HALAMAN DOKTER - DAFTAR ANTRIAN PASIEN")
    print("="*60)
    
    antrian = db.ambil_antrian_dokter()
    
    if not antrian:
        print("\nTidak ada pasien dalam antrian saat ini.")
        return []
    
    print(f"{'No':<4} | {'ID Antrian':<12} | {'Nama Pasien':<20} | {'Keluhan':<15}")
    print("-" * 60)
    
    for i, pasien in enumerate(antrian):
        print(f"{i+1:<4} | {pasien['id_antrian']:<12} | {pasien['nama']:<20} | {pasien['keluhan']:<15}")
        
    return antrian

def periksa_pasien(dokter):
    list_antrian = tampilkan_antrian()

    if not list_antrian:
        print("Tidak ada pasien dalam antrian saat ini.")
        print("-" * 60)
        input("\nTekan Enter untuk kembali...")
        return

    pasien_terpilih = list_antrian[0]
    
    print(f"\n[SEDANG MEMERIKSA] : {pasien_terpilih['nama']}")
    print(f"Keluhan : {pasien_terpilih['keluhan']}")
    print("-" * 30)

    diagnosa = input("Masukkan Diagnosa : ")
    print("\n--- RESEP OBAT ---")
    nama_obat    = input("Nama Obat    : ")
    dosis        = input("Dosis (mg/gr): ")
    aturan_pakai = input("Aturan Pakai : ")
    catatan      = input("Catatan Tambahan (opsional): ")
    
    konfirmasi = input("\nSimpan data pemeriksaan & resep? (y/n): ")
    if konfirmasi.lower() == 'y':
        data_simpan = {
            'id_antrian': pasien_terpilih['id_antrian'],
            'id_pasien': pasien_terpilih['id_pasien'],
            'id_dokter': dokter['id_user'],
            'keluhan': pasien_terpilih['keluhan'],
            'diagnosa': diagnosa,
            'tanggal_periksa': datetime.datetime.now().strftime("%Y-%m-%d"),
            'catatan': catatan
        }
        data_resep = {
            'obat': nama_obat,
            'dosis': dosis,
            'aturan_pakai': aturan_pakai
        }
        db.simpan_diagnosa(data_simpan, data_resep)
        db.update_status_antrian(pasien_terpilih['id_antrian'], 'selesai')
        
        print("\n[SUKSES] Data berhasil disimpan dan status antrian diperbarui.")
    else:
        print("\nPemeriksaan dibatalkan.")
        
    input("Tekan Enter untuk kembali...")

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
        print("\n=== MENU DOKTER SIPEKA ===")
        print("1. Lihat Daftar Antrian")
        print("2. Mulai Pemeriksaan")
        print("3. Kembali ke Menu Utama")
        
        opsi = input("\nPilih menu: ")
        
        if opsi == '1':
            tampilkan_antrian()
            input("\nTekan Enter kembali...")
        elif opsi == '2':
            periksa_pasien(user)
        elif opsi == '3':
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
