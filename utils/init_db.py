# ==================== UTILITY FUNCTIONS ====================
import os
import csv
from config.db import DETAIL_RESEP_FILE, PASIEN_FILE, STAF_FILE, ANTRIAN_FILE, RIWAYAT_MEDIS_FILE, LAPORAN_HARIAN_FILE, DATA_DIR
from utils.crud import create_default_admin


def init_database():
    """Inisialisasi folder dan file CSV jika belum ada"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Struktur CSV sesuai SKPL
    files_headers = {
        PASIEN_FILE: ["id_pasien", "nama", "NIK", "password", "alamat", "no_telp", "jenis_kelamin", "email", "tanggal_lahir"],
        STAF_FILE: ["id_user", "nama", "username", "password", "email", "jabatan", "NIP", "spesialisasi", "kontak", "jadwal", "shift"],
        ANTRIAN_FILE: ["id_antrian", "id_pasien", "id_dokter", "no_antrian", "keluhan", "tanggal", "jam", "status_antrian", "catatan"],
        RIWAYAT_MEDIS_FILE: ["id_riwayat", "id_pasien", "id_dokter", "keluhan", "diagnosa", "tanggal", "catatan"],
        DETAIL_RESEP_FILE: ["id_detail_resep", "riwayat_id", "obat", "dosis", "aturan_pakai"],
        LAPORAN_HARIAN_FILE: ["id_log", "id_user", "waktu_aktivitas", "aktivitas_terakhir"]
    }

    for file_path, headers in files_headers.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    # Buat admin default jika belum ada
    create_default_admin()