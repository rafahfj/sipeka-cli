from pages.auth import log_aktivitas
from utils.crud import read_csv, write_csv, append_csv, generate_id, hash_password
from config.db import STAF_FILE, PASIEN_FILE, ANTRIAN_FILE, RIWAYAT_MEDIS_FILE, LAPORAN_HARIAN_FILE


def menu_admin(user):
    """Menu utama untuk admin"""
    while True:
        print("\n" + "="*50)
        print(f"     MENU ADMIN - {user['nama']}")
        print("="*50)
        print("[1] Kelola Akun Staf")
        print("[2] Lihat Semua Pasien")
        print("[3] Lihat Semua Staf")
        print("[4] Lihat Log Aktivitas")
        print("[5] Laporan Statistik")
        print("[0] Logout")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            kelola_akun_staf()
        elif pilihan == "2":
            lihat_semua_pasien()
        elif pilihan == "3":
            lihat_semua_staf()
        elif pilihan == "4":
            lihat_log_aktivitas()
        elif pilihan == "5":
            laporan_statistik()
        elif pilihan == "0":
            log_aktivitas(user['id_user'], "Logout admin")
            print("\n>>> Logout berhasil!")
            break

def kelola_akun_staf():
    """Admin mengelola akun staf"""
    print("\n--- Kelola Akun Staf ---")
    print("[1] Tambah Dokter")
    print("[2] Tambah Resepsionis")
    print("[3] Hapus Staf")
    print("[0] Kembali")

    pilihan = input("\nPilih opsi: ")

    if pilihan == "1":
        tambah_staf("Dokter")
    elif pilihan == "2":
        tambah_staf("Resepsionis")
    elif pilihan == "3":
        hapus_staf()

def tambah_staf(jabatan):
    """Tambah staf baru"""
    print(f"\n--- Tambah {jabatan} Baru ---")

    nama = input("Nama Lengkap: ")
    username = input("Username: ")

    # Validasi username unik
    staf_list = read_csv(STAF_FILE)
    if any(s['username'] == username for s in staf_list):
        print("\n>>> Username sudah digunakan!")
        return

    password = input("Password: ")
    email = input("Email: ")
    nip = input("NIP: ")
    kontak = input("No. Telepon: ")

    staf_data = {
        "id_user": generate_id("STF"),
        "nama": nama,
        "username": username,
        "password": hash_password(password),
        "email": email,
        "jabatan": jabatan,
        "NIP": nip,
        "spesialisasi": "",
        "kontak": kontak,
        "jadwal": "",
        "shift": ""
    }

    if jabatan == "Dokter":
        staf_data['spesialisasi'] = input("Spesialisasi: ")
        staf_data['jadwal'] = input("Jadwal Praktik: ")
    else:
        staf_data['shift'] = input("Shift: ")

    append_csv(STAF_FILE, staf_data)
    print(f"\n>>> {jabatan} berhasil ditambahkan!")

def hapus_staf():
    """Hapus staf"""
    print("\n--- Hapus Staf ---")

    staf_list = read_csv(STAF_FILE)
    staf_non_admin = [s for s in staf_list if s['jabatan'] != 'Admin']

    if not staf_non_admin:
        print(">>> Tidak ada staf untuk dihapus.")
        return

    for i, staf in enumerate(staf_non_admin, 1):
        print(f"[{i}] {staf['nama']} - {staf['jabatan']}")

    try:
        pilihan = int(input("\nPilih nomor staf yang akan dihapus: ")) - 1
        if pilihan < 0 or pilihan >= len(staf_non_admin):
            print(">>> Pilihan tidak valid!")
            return
    except ValueError:
        print(">>> Input tidak valid!")
        return

    staf_hapus = staf_non_admin[pilihan]
    konfirmasi = input(f"Yakin ingin menghapus {staf_hapus['nama']}? (y/n): ")

    if konfirmasi.lower() == 'y':
        staf_list = [s for s in staf_list if s['id_user'] != staf_hapus['id_user']]
        fieldnames = ["id_user", "nama", "username", "password", "email", "jabatan", "NIP", "spesialisasi", "kontak", "jadwal", "shift"]
        write_csv(STAF_FILE, staf_list, fieldnames)
        print("\n>>> Staf berhasil dihapus!")

def lihat_semua_pasien():
    """Lihat semua pasien terdaftar"""
    print("\n--- Daftar Pasien Terdaftar ---")

    pasien_list = read_csv(PASIEN_FILE)

    if not pasien_list:
        print(">>> Belum ada pasien terdaftar.")
        return

    print("-" * 90)
    print(f"{'No':<5} {'ID':<12} {'Nama':<20} {'NIK':<18} {'Email':<25} {'No.Telp':<15}")
    print("-" * 90)

    for i, pasien in enumerate(pasien_list, 1):
        print(f"{i:<5} {pasien['id_pasien']:<12} {pasien['nama'][:20]:<20} {pasien['NIK']:<18} {pasien['email'][:25]:<25} {pasien['no_telp']:<15}")

def lihat_semua_staf():
    """Lihat semua staf"""
    print("\n--- Daftar Staf ---")

    staf_list = read_csv(STAF_FILE)

    if not staf_list:
        print(">>> Belum ada staf terdaftar.")
        return

    print("-" * 80)
    print(f"{'No':<5} {'Nama':<20} {'Jabatan':<15} {'Username':<15} {'Email':<25}")
    print("-" * 80)

    for i, staf in enumerate(staf_list, 1):
        print(f"{i:<5} {staf['nama'][:20]:<20} {staf['jabatan']:<15} {staf['username']:<15} {staf['email'][:25]:<25}")

def lihat_log_aktivitas():
    """Lihat log aktivitas sistem"""
    print("\n--- Log Aktivitas ---")

    log_list = read_csv(LAPORAN_HARIAN_FILE)

    if not log_list:
        print(">>> Belum ada log aktivitas.")
        return

    # Tampilkan 20 log terakhir
    log_terbaru = log_list[-20:]

    print("-" * 70)
    print(f"{'Waktu':<22} {'ID User':<15} {'Aktivitas':<30}")
    print("-" * 70)

    for log in reversed(log_terbaru):
        print(f"{log['waktu_aktivitas']:<22} {log['id_user']:<15} {log['aktivitas_terakhir'][:30]:<30}")

def laporan_statistik():
    """Menampilkan laporan statistik"""
    print("\n--- Laporan Statistik ---")

    pasien_list = read_csv(PASIEN_FILE)
    staf_list = read_csv(STAF_FILE)
    antrian_list = read_csv(ANTRIAN_FILE)
    riwayat_list = read_csv(RIWAYAT_MEDIS_FILE)

    dokter_count = sum(1 for s in staf_list if s['jabatan'] == 'Dokter')
    resepsionis_count = sum(1 for s in staf_list if s['jabatan'] == 'Resepsionis')

    print("\n" + "=" * 40)
    print("         STATISTIK SISTEM SIPEKA")
    print("=" * 40)
    print(f"\nTotal Pasien Terdaftar  : {len(pasien_list)}")
    print(f"Total Dokter            : {dokter_count}")
    print(f"Total Resepsionis       : {resepsionis_count}")
    print(f"Total Antrian (All Time): {len(antrian_list)}")
    print(f"Total Pemeriksaan       : {len(riwayat_list)}")
    print("=" * 40)
