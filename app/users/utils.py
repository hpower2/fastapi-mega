import random
from .models import User, User_detail
from sqlalchemy.future import select
from .schemas import UsersInCreate, UsersInLogIn
from .service import hash_password, verify_password, ResponseOut, create_access_token
from datetime import datetime, timedelta

#* SET TIME FOR TOKEN
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#* Authentikasi
#* Untuk mengecek apakah username teah terdaftar atau belum
async def auth(username, db):
    async with db as session:
        user = await session.execute(select(User).filter(User.username == username))
        user_ = user.scalars().first()
        return user_ is None

#* REGISTER
async def register(user: UsersInCreate, db):
    async with db as session:
        
        username = user.username
        nama = user.nama
        no_telpon = user.nomor_telpon
        password = user.password
        
        #* Generate nomor rekening
        no_rek = ''.join([str(random.randint(0, 9)) for i in range(10)])
        
        #* Enskripsi password menggunakan bcrypt
        hash_pass = await hash_password(password)
        
        try:
            if await auth(username, db):
                #* Menambahkan data kedalam tabel user
                user = User(username = username, password = hash_pass.decode('utf8'))
                session.add(user)
                await session.commit()
                
                #* Mengambil user_id data yang baru di input
                data_user = await session.execute(select(User).filter(User.username == username))
                user_ = data_user.scalars().first()
                
                #* Menambahkan data kedalam tabel user_detail
                user_detail = User_detail(
                    user_id = user_.user_id,
                    nama = nama,
                    no_telpon = no_telpon,
                    no_rekening = no_rek,
                    no_pin = "",
                    saldo = 0)
                
                session.add(user_detail)
                await session.commit()
                return ResponseOut("00", "Pendaftaran akun berhasil", [{"username": username,"Nomer_rekening" : no_rek}]), 200
            else:
                return ResponseOut("01", f"Pendaftaran akun gagal, username : {username} telah terdaftar", []), 409
        except Exception as e:
            return ResponseOut("03", f"Terjadi kesalahan saat proses regitrasi akun: {str(e)}", []), 500
        
#* LOGIN
async def login(data: UsersInLogIn, db):
    async with db as session:
        try:
            #* mengecek apakah username ada didalam tabel user
            db_user = await session.execute(select(User).filter(User.username == data.username))
            user = db_user.scalars().first()
            
            if not user or user.deleted_at:
                return ResponseOut("02", f"Login Gagal, silahkan sek kembali email atau password yang dimasukan", []), 404
            
            #* jika username ada didalam tabel user, lalu cocokan password pada tabel dan input user
            if user and await verify_password(data.password, user.password):
                dt = {
                    "user_id": user.user_id,
                    "access_date": str(datetime.now())
                }
                _token = create_access_token(data=dt, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
                return ResponseOut("00", "Login Berhasil", data= [{"token_bearer": _token}]), 200
            else:
                return ResponseOut("02", f"Login Gagal, silahkan sek kembali email atau password yang dimasukan", []), 404
        except Exception as e:
            return ResponseOut("03",f"Terjadi kesalahan pada proses login akun: {str(e)}", []), 500
        
import random
from .models import User_detail, User
from sqlalchemy.future import select
from .schemas import UsersInUpdate, ValidateRekening
from .service import hash_password, ResponseOut
from datetime import datetime

#* GET DETAIL USER BY ID
async def get_detail_user(db, token):
    try:
        async with db as session:
            #* mengecek data user berdasarkan user_id yang terdapat pada token
            db_users = await session.execute(select(User_detail).filter(User_detail.user_id == token['user_id']))
            users = db_users.scalars().first()
            if users is None or users.deleted_at is not None:
                return ResponseOut("02", f"Data pengguna dengan id: {token['user_id']} tidak ditemukan", []), 404
            return ResponseOut("00", f"Berhasil menampilkan data pengguna dengan id: {token['user_id']}", [users.serialize()]), 200
    except Exception as e:
        return ResponseOut("03",f"Terjadi error saat menampilkan data pengguna: {str(e)}", []), 500
    
#* UPDATE DETAIL USER BY ID
async def edit_user(user_id, data: UsersInUpdate, db):
    async with db as session:
        try:
            db_user = await session.execute(select(User_detail).filter(User_detail.user_id == user_id))
            users = db_user.scalars().first()
            
            if not users or users.deleted_at:
                return ResponseOut("02", "Update profile gagal, user tidak ditemukan", []), 404
            
            if data.nama:
                users.nama = data.nama
            
            if data.nomor_telpon:
                users.no_telpon = data.nomor_telpon
            
            await session.commit()
            return ResponseOut("00", "Update profile berhasil", [users.serialize()]), 200
        except Exception as e:
            return ResponseOut("03", f"Terjadi kesalahan saat update profile: {str(e)}", []), 500

#* VALIDATION REKENING
async def validate_rekening(data: ValidateRekening, db, token):
    async with db as session:
        try:
            db_user = await session.execute(select(User_detail).filter(User_detail.user_id == token['user_id']))
            users = db_user.scalars().first()
            
            if not users or users.deleted_at:
                return ResponseOut("02", "Validasi rekening gagal, user tidak ditemukan", []), 404
            
            if users.no_rekening != data.nomor_rekening:
                return ResponseOut("02", "Validasi rekening gagal, nomor rekening tidak ditemukan", []), 404
            
            if users.no_pin != '':
                return ResponseOut("02", "Validasi rekening gagal, rekening telah tervalidasi sebelumnya", []), 409
            
            #* generate pin
            no_pin = ''.join([str(random.randint(0, 9)) for i in range(6)])
            
            users.no_pin = no_pin
            await session.commit()
            return ResponseOut("00", "Validasi rekening berhasil", [{"nomor_pin":no_pin}]), 200
        except Exception as e:
            return ResponseOut("03", f"Terjadi kesalahan saat validasi rekening: {str(e)}", []), 500

#* DELETE USER BY ID
async def delete_user(user_id, db):
    async with db as session:
        try:
            account = await session.get(User, user_id)
            query = await session.execute(select(User_detail).filter(User_detail.user_id == user_id))
            detail_account = query.scalars().first()
            
            if not account or account.deleted_at:
                return ResponseOut("02", f"Hapus akun gagal, akun tidak ditemukan", []), 404
            
            account.deleted_at = datetime.now()
            detail_account.deleted_at = datetime.now()
            await session.commit()
            return ResponseOut("00", "Berhasil menghapus akun", [{"username": account.username}]), 200
        except Exception as e:
            return ResponseOut("03",f"{str(e)}", []), 500