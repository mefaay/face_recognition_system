import sqlite3

# Veritabanı dosyasının yolu
DATABASE_PATH = "veritabani/face_database.db"

# Veritabanı bağlantısını açan ve tabloyu oluşturan fonksiyon


def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    # Tablo oluşturma
    c.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        face_encoding BLOB NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Kişiyi veritabanına ekleyen fonksiyon


def add_person(name, surname, phone, address, face_encoding):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute('INSERT INTO people (name, surname, phone, address, face_encoding) VALUES (?, ?, ?, ?, ?)',
              (name, surname, phone, address, face_encoding.tobytes()))

    conn.commit()
    conn.close()

# Kişi sorgulama fonksiyonu


def query_person_by_name_surname(name, surname):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM people WHERE name=? AND surname=?", (name, surname))
    person = c.fetchone()

    conn.close()
    return person

# Veritabanındaki tüm kişileri getirir


def get_all_people():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM people")
    people = c.fetchall()

    conn.close()
    return people
