# ==================== MAIN PROGRAM ====================
from pages import menu_admin, menu_dokter
from pages.auth import login
from pages.menu_patient import menu_pasien
from sipeka import menu_resepsionis, registrasi_pasien
from utils.init_db import init_database


def main():
    """Program utama SIPEKA"""
    init_database()

    while True:
        print("\n" + "="*50)
        print("    ╔═══════════════════════════════════════╗")
        print("    ║         SELAMAT DATANG DI             ║")
        print("    ║              SIPEKA                   ║")
        print("    ║      Sistem Informasi Pelayanan       ║")
        print("    ║             Kesehatan                 ║")
        print("    ╚═══════════════════════════════════════╝")
        print("="*50)
        print("\n[1] Login")
        print("[2] Registrasi Pasien Baru")
        print("[0] Keluar")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            user, role = login()
            if user and role:
                if role == "Pasien":
                    menu_pasien(user)
                elif role == "Dokter":
                    menu_dokter(user)
                elif role == "Resepsionis":
                    menu_resepsionis(user)
                elif role == "Admin":
                    menu_admin(user)
        elif pilihan == "2":
            registrasi_pasien()
        elif pilihan == "0":
            print("\n>>> Terima kasih telah menggunakan SIPEKA!")
            print(">>> Sampai jumpa!")
            break
        else:
            print("\n>>> Pilihan tidak valid!")

if __name__ == "__main__":
    main()
