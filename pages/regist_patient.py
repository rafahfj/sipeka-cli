import pwinput
from config.db import PASIEN_FILE
from utils.crud import hash_password, append_csv, read_csv, generate_id

def input_wajib(prompt):
    nilai = input(prompt).strip()
    if nilai == "":
        print("\n---Input tidak boleh kosong!---")
        return None
    return nilai

def registrasi_pasien():
    print("\n" + "=" * 50)
    print("            REGISTRASI PASIEN BARU")
    print("=" * 50)

    nama = input_wajib("Nama Lengkap: ")
    if nama is None:
        return

    nik = input_wajib("NIK (16 digit): ")
    if nik is None:
        return

    email = input_wajib("Email: ")
    if email is None:
        return

    pasien_list = read_csv(PASIEN_FILE)

    for p in pasien_list:
        if p['email'] == email:
            print("\n---Email sudah terdaftar!---")
            return
        if p['NIK'] == nik:
            print("\n---NIK sudah terdaftar!---")
            return

    if len(nik) != 16 or not nik.isdigit():
        print("\n---NIK harus 16 digit angka!---")
        return

    password = pwinput.pwinput(prompt="Password: ", mask="*")
    
    if password == "":
        print("\n---Password tidak boleh kosong!---")
        return

    confirm_password = pwinput.pwinput(prompt="Konfirmasi Password: ", mask="*")
    if confirm_password == "":
        print("\n---Konfirmasi password tidak boleh kosong!---")
        return

    if password != confirm_password:
        print("\n---Password tidak cocok!---")
        return

    alamat = input_wajib("Alamat: ")
    if alamat is None:
        return

    no_telp = input_wajib("No. Telepon: ")
    if no_telp is None:
        return

    jenis_kelamin = input_wajib("Jenis Kelamin (L/P): ")
    if jenis_kelamin is None:
        return
    jenis_kelamin = jenis_kelamin.upper()

    tanggal_lahir = input_wajib("Tanggal Lahir (YYYY-MM-DD): ")
    if tanggal_lahir is None:
        return

    if jenis_kelamin != "L" and jenis_kelamin != "P":
        print("\n---Jenis kelamin harus L atau P!---")
        return

    pasien_data = {
        "id_pasien": generate_id("PAS"),
        "nama": nama,
        "NIK": nik,
        "password": hash_password(password),
        "alamat": alamat,
        "no_telp": no_telp,
        "jenis_kelamin": jenis_kelamin,
        "email": email,
        "tanggal_lahir": tanggal_lahir
    }

    append_csv(PASIEN_FILE, pasien_data)
    print(f"\n---Registrasi berhasil! ID Pasien Anda: {pasien_data['id_pasien']}---")