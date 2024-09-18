import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import face_recognition
import cv2
import os
import numpy as np
from model import create_database, add_person, query_person_by_name_surname, get_all_people
from PIL import Image, ImageTk
import unicodedata

# Fotoğrafların kaydedileceği klasör yolu
PHOTO_DIR = "fotograflar"

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yüz Tanıma Sistemi")
        self.root.geometry("1000x700")
        self.root.style = ttk.Style()
        self.root.style.theme_use('clam')  # Modern bir tema kullanıyoruz
        self.root.configure(bg='#f0f0f0')  # Arka planı daha modern bir gri yapıyoruz

        # Menü oluştur
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Sekmeli yapı
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Kayıt sayfası
        self.kayıt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.kayıt_frame, text="Kayıt")
        self.create_kayıt_page(self.kayıt_frame)

        # Sorgu sayfası
        self.sorgu_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sorgu_frame, text="Sorgu")
        self.create_sorgu_page(self.sorgu_frame)

        # Tespit sayfası
        self.tespit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tespit_frame, text="Tespit")
        self.create_tespit_page(self.tespit_frame)

        # Kamera ile tespit sayfası
        self.kamera_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.kamera_frame, text="Kamera ile Tespit")
        self.create_kamera_page(self.kamera_frame)

        # Diğer değişkenler
        self.photo_path = None  # Fotoğraf yolunu kaydetmek için

    # Kayıt sayfası
    def create_kayıt_page(self, frame):
        ttk.Label(frame, text="Ad", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ad_entry = ttk.Entry(frame, font=("Arial", 12))
        self.ad_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(frame, text="Soyad", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.soyad_entry = ttk.Entry(frame, font=("Arial", 12))
        self.soyad_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(frame, text="Telefon", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.telefon_entry = ttk.Entry(frame, font=("Arial", 12))
        self.telefon_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(frame, text="Adres", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.adres_entry = ttk.Entry(frame, font=("Arial", 12))
        self.adres_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Fotoğraf seç butonu
        ttk.Button(frame, text="Fotoğraf Seç", command=self.fotoğraf_seç, style="TButton").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Kaydet butonu
        ttk.Button(frame, text="Kaydet", command=self.fotoğraf_kaydet, style="TButton").grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def fotoğraf_seç(self):
        self.photo_path = filedialog.askopenfilename(
            title="Fotoğraf Seç",
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        )
        if self.photo_path:
            messagebox.showinfo("Başarılı", "Fotoğraf başarıyla seçildi.")

    def fotoğraf_kaydet(self):
        if not self.photo_path:
            messagebox.showerror("Hata", "Lütfen önce fotoğraf seçin.")
            return

        ad = self.ad_entry.get()
        soyad = self.soyad_entry.get()
        telefon = self.telefon_entry.get()
        adres = self.adres_entry.get()

        frame = cv2.imread(self.photo_path)

        if frame is None:
            messagebox.showerror("Hata", "Fotoğraf yüklenemedi.")
            return

        photo_save_path = os.path.join(PHOTO_DIR, f"{ad}_{soyad}.jpg")
        cv2.imwrite(photo_save_path, frame)

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if face_encodings:
            add_person(ad, soyad, telefon, adres, face_encodings[0])
            messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi.")
        else:
            messagebox.showerror("Hata", "Yüz tespit edilemedi.")

    # Sorgulama sayfası
    def create_sorgu_page(self, frame):
        ttk.Label(frame, text="Ad", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.sorgu_ad_entry = ttk.Entry(frame, font=("Arial", 12))
        self.sorgu_ad_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.result_frame = ttk.Frame(frame)
        self.result_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        ttk.Button(frame, text="Sorgula", command=self.sorgula, style="TButton").grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def sorgula(self):
        ad = self.sorgu_ad_entry.get()

        # Türkçe karakter duyarsız hale getirme
        normalized_ad = self.normalize(ad)

        # Veritabanında sorgu
        people = get_all_people()
        filtered_people = [person for person in people if normalized_ad.lower() in self.normalize(person[1]).lower()]

        self.show_results(filtered_people)

    def normalize(self, text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    def show_results(self, people):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        for person in people:
            photo_label = ttk.Label(self.result_frame)
            photo_path = os.path.join(PHOTO_DIR, f"{person[1]}_{person[2]}.jpg")
            if os.path.exists(photo_path):
                img = Image.open(photo_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                photo_label.config(image=img_tk)
                photo_label.image = img_tk
            photo_label.grid(row=0, column=people.index(person), padx=5)

            info_label = ttk.Label(self.result_frame, text=f"Ad: {person[1]}\nSoyad: {person[2]}\nAdres: {person[4]}")
            info_label.grid(row=1, column=people.index(person), padx=5)

    # Tespit sayfası
    # Tespit sayfası
    def create_tespit_page(self, frame):
        self.tespit_label = ttk.Label(frame, text="Fotoğraf Yükleyin", font=("Arial", 12))
        self.tespit_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.photo_label = ttk.Label(frame)
        self.photo_label.grid(row=1, column=0, padx=10, pady=5)

        # Fotoğrafın sağında bilgiler için bir frame oluşturuyoruz
        self.info_frame = ttk.Frame(frame)
        self.info_frame.grid(row=1, column=1, padx=20, pady=5, sticky="w")

        self.result_label = ttk.Label(self.info_frame, text="", font=("Arial", 14, "bold"))
        self.result_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.info_label = ttk.Label(self.info_frame, text="", font=("Arial", 12))
        self.info_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        ttk.Button(frame, text="Fotoğraf Yükle ve Tespit Et", command=self.yüz_tespit, style="TButton").grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def yüz_tespit(self):
        file_path = filedialog.askopenfilename(
            title="Fotoğraf Seç",
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        )

        if not file_path:
            messagebox.showerror("Hata", "Fotoğraf seçilmedi.")
            return

        frame = cv2.imread(file_path)

        if frame is None:
            messagebox.showerror("Hata", "Fotoğraf yüklenemedi.")
            return

        # Fotoğrafı arayüzde göster
        self.display_photo(file_path)

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if face_encodings:
            self.veritabanından_yüz_bul(face_encodings[0])
        else:
            self.result_label.config(text="Yüz tespit edilemedi.", foreground="red")
            self.info_label.config(text="")

    def display_photo(self, file_path):
        img = Image.open(file_path)
        img = img.resize((200, 200), Image.Resampling.LANCZOS)  # Fotoğrafı yeniden boyutlandır
        img_tk = ImageTk.PhotoImage(img)
        self.photo_label.config(image=img_tk)
        self.photo_label.image = img_tk

    def veritabanından_yüz_bul(self, face_encoding):
        people = get_all_people()

        for person in people:
            stored_encoding = np.frombuffer(person[5], dtype=np.float64)
            results = face_recognition.compare_faces([stored_encoding], face_encoding)

            if results[0]:
                self.result_label.config(text="Kişi Tespit Edildi", foreground="green")
                self.info_label.config(text=f"Ad: {person[1]}\nSoyad: {person[2]}\nTelefon: {person[3]}\nAdres: {person[4]}")
                return

        self.result_label.config(text="Kişi bulunamadı.", foreground="red")
        self.info_label.config(text="")

    # Kamera ile tespit sayfası
    def create_kamera_page(self, frame):
        ttk.Label(frame, text="Kamera ile Tespit", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)

        ttk.Button(frame, text="Kamerayı Başlat", command=self.kameradan_yüz_tespit, style="TButton").grid(row=1, column=0, padx=10, pady=10)

        self.kamera_photo_label = ttk.Label(frame)
        self.kamera_photo_label.grid(row=2, column=0, padx=10, pady=5)

        self.kamera_info_label = ttk.Label(frame, text="", font=("Arial", 12))
        self.kamera_info_label.grid(row=2, column=1, padx=10, pady=5)

    def kameradan_yüz_tespit(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            cv2.imshow('Kamera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basıldığında kamerayı durdur
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # Fotoğrafı arayüzde göster
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        self.kamera_photo_label.config(image=img_tk)
        self.kamera_photo_label.image = img_tk

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if face_encodings:
            self.kamera_veritabanından_yüz_bul(face_encodings[0])
        else:
            self.kamera_info_label.config(text="Yüz tespit edilemedi.", foreground="red")

    def kamera_veritabanından_yüz_bul(self, face_encoding):
        people = get_all_people()

        for person in people:
            stored_encoding = np.frombuffer(person[5], dtype=np.float64)
            results = face_recognition.compare_faces([stored_encoding], face_encoding)

            if results[0]:
                self.kamera_info_label.config(text=f"Kişi Tespit Edildi\nAd: {person[1]}\nSoyad: {person[2]}\nTelefon: {person[3]}\nAdres: {person[4]}", foreground="green")
                return

        self.kamera_info_label.config(text="Kişi bulunamadı.", foreground="red")


# Uygulamayı başlatma
if __name__ == "__main__":
    create_database()  # Veritabanı oluştur
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
