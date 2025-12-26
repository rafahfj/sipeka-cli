import csv
import os
import hashlib
import uuid
import msvcrt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PASIEN_FILE = os.path.join(DATA_DIR, "pasien.csv")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def input_wajib(prompt):
    nilai = input(prompt).strip()
    if nilai == "":
        print("\n---Input tidak boleh kosong!---")
        return None
    return nilai

def generate_id(prefix=""):
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def read_csv(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def append_csv(file_path, row_data):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    file_exists = os.path.exists(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)

def masked_input(prompt=""):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()

        if char in (b'\r', b'\n'): 
            print()
            return password

        if char == b'\x08':
            if password:
                password = password[:-1]
                print('\b \b', end="", flush=True)
        else:
            ch = char.decode('utf-8', errors='ignore')
            password += ch
            print('*', end="", flush=True)

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

    password = masked_input("Password: ")
    if password == "":
        print("\n---Password tidak boleh kosong!---")
        return

    confirm_password = masked_input("Konfirmasi Password: ")
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