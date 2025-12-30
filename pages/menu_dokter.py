import utils.crud as db
import datetime

# ==================== MENU DOKTER ====================

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

def periksa_pasien():
    list_antrian = tampilkan_antrian()
    
    if not list_antrian:
        input("\nTekan Enter untuk kembali...")
        return

    print("\n" + "-"*60)
    pilihan = input("Pilih Nomor Urut Pasien yang akan diperiksa (contoh: 1): ")
    
    if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(list_antrian):
        print("Pilihan tidak valid.")
        input("Tekan Enter...")
        return

    pasien_terpilih = list_antrian[int(pilihan) - 1]
    
    print(f"\n[SEDANG MEMERIKSA] : {pasien_terpilih['nama']}")
    print(f"Keluhan            : {pasien_terpilih['keluhan']}")
    print("-" * 30)
    
    diagnosa = input("Masukkan Diagnosa : ")
    resep = input("Masukkan Resep    : ")
    
    konfirmasi = input("\nSimpan hasil pemeriksaan? (y/n): ")
    if konfirmasi.lower() == 'y':
        data_simpan = {
            'id_antrian': pasien_terpilih['id_antrian'],
            'id_pasien': pasien_terpilih['id_pasien'],
            'diagnosa': diagnosa,
            'resep_obat': resep,
            'tanggal_periksa': datetime.datetime.now().strftime("%Y-%m-%d")
        }
        db.simpan_diagnosa(data_simpan)
        db.update_status_antrian(pasien_terpilih['id_antrian'], 'selesai')
        
        print("\n[SUKSES] Data berhasil disimpan dan status antrian diperbarui.")
    else:
        print("\nPemeriksaan dibatalkan.")
        
    input("Tekan Enter untuk kembali...")

def menu_dokter(user):
    jabatan = user.get('jabatan', '').strip()
    if jabatan not in ['Admin', 'Dokter']:
        print("\n" + "!"*50)
        print(f"[AKSES DITOLAK] Maaf {user['nama']},")
        print("Menu ini hanya khusus untuk Dokter atau Admin.")
        print("!"*50)
        input("\nTekan Enter untuk kembali...")
        return
    
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
            periksa_pasien()
        elif opsi == '3':
            break
        else:
            print("Menu tidak tersedia.")