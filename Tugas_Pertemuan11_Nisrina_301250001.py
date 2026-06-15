# Nama Program : Mini Sistem CLI Mahasiswa (Tugas 9, 10, 11)
# Nama Pembuat : Nisrina Dwi Hasna
# NIM          : 301250001
# Tanggal      : 15 Juni 2026
# Nama File    : 301250001_Nisrina_Tugas9_10_11.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📦 MINI SISTEM CLI MAHASISWA
Mencakup:
  - Tugas 9  : Refactor ke Dictionary (NIM sebagai key)
  - Tugas 10 : Integrasi File JSON (simpan & baca otomatis)
  - Tugas 11 : Parsing Log File (set untuk user unik)
Plus fitur dari Tugas 7: Sorting & Searching data nilai mahasiswa
"""

import json
import os
from datetime import datetime


# =========================================================
# 📁 KONFIGURASI FILE
# =========================================================
DATA_FILE = "mahasiswa_data.json"
LOG_FILE  = "aktivitas_log.txt"


# =========================================================
# 📐 MODUL SORTING
# =========================================================
def bubble_sort(arr: list) -> tuple:
    """Bubble Sort. Mengembalikan (array_terurut, jumlah_perbandingan)"""
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j][1] > arr[j + 1][1]:   # bandingkan berdasarkan nilai
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr, comparisons


def insertion_sort(arr: list) -> tuple:
    """Insertion Sort. Mengembalikan (array_terurut, jumlah_perbandingan)"""
    arr = arr.copy()
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if key[1] < arr[j][1]:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comparisons


# =========================================================
# 🔍 MODUL SEARCHING
# =========================================================
def linear_search(arr: list, target: str) -> tuple:
    """Linear search berdasarkan NIM. Mengembalikan (indeks, langkah)"""
    steps = 0
    for i, (nim, _) in enumerate(arr):
        steps += 1
        if nim == target:
            return i, steps
    return -1, steps


def binary_search(arr: list, target: str) -> tuple:
    """Binary search berdasarkan NIM (data harus terurut NIM). Mengembalikan (indeks, langkah)"""
    steps = 0
    low, high = 0, len(arr) - 1
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if arr[mid][0] == target:
            return mid, steps
        elif arr[mid][0] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps


# =========================================================
# 📝 MODUL LOG
# =========================================================
def tulis_log(aksi: str, detail: str = ""):
    """Menulis satu baris log ke file LOG_FILE."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nim_aktif = "SYSTEM"   # bisa diganti dengan session user jika ada
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}|{nim_aktif}|{aksi}|{detail}\n")


def baca_log() -> dict:
    """
    Membaca LOG_FILE dan mengembalikan dict berisi:
      - total_aktivitas : int
      - user_unik       : set  (NIM yang pernah melakukan aksi)
      - ringkasan_aksi  : dict {aksi: jumlah}
    """
    if not os.path.exists(LOG_FILE):
        return {"total_aktivitas": 0, "user_unik": set(), "ringkasan_aksi": {}}

    total = 0
    user_unik: set = set()
    ringkasan: dict = {}

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for baris in f:
            baris = baris.strip()
            if not baris:
                continue
            bagian = baris.split("|")
            if len(bagian) < 3:
                continue
            _, nim, aksi, *_ = bagian
            total += 1
            user_unik.add(nim)
            ringkasan[aksi] = ringkasan.get(aksi, 0) + 1

    return {
        "total_aktivitas": total,
        "user_unik": user_unik,
        "ringkasan_aksi": ringkasan,
    }


# =========================================================
# 🏗️ KELAS UTAMA — MINI SISTEM CLI
# =========================================================
class MiniSistemMahasiswa:
    """
    Penyimpanan utama menggunakan DICTIONARY:
        self.mahasiswa = {
            "301250001": {"nama": "Nisrina", "nilai": 90},
            ...
        }
    """

    def __init__(self):
        # ── Tugas 9: Dictionary sebagai penyimpanan utama ──
        self.mahasiswa: dict[str, dict] = {}
        self.is_sorted   = False
        self.last_sort   = None

        # ── Tugas 10: Baca file JSON saat program dijalankan ──
        self._muat_dari_file()

    # --------------------------------------------------
    # TUGAS 10: Integrasi File JSON
    # --------------------------------------------------
    def _muat_dari_file(self):
        """Membaca data dari DATA_FILE saat startup."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.mahasiswa = json.load(f)
                print(f"📂 Data dimuat dari '{DATA_FILE}' ({len(self.mahasiswa)} mahasiswa).")
            except (json.JSONDecodeError, IOError):
                print(f"⚠️  File '{DATA_FILE}' rusak atau tidak bisa dibaca. Memulai dengan data kosong.")
                self.mahasiswa = {}
        else:
            print(f"ℹ️  File '{DATA_FILE}' belum ada. Memulai dengan data kosong.")

    def _simpan_ke_file(self):
        """Menyimpan self.mahasiswa ke DATA_FILE."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.mahasiswa, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Gagal menyimpan file: {e}")

    # --------------------------------------------------
    # TUGAS 9: Operasi CRUD dengan Dictionary
    # --------------------------------------------------
    def tambah_mahasiswa(self):
        print("\n➕ TAMBAH MAHASISWA")
        nim = input("   NIM    : ").strip()
        if not nim:
            print("   ⚠️  NIM tidak boleh kosong.")
            return
        if nim in self.mahasiswa:
            print(f"   ⚠️  NIM '{nim}' sudah ada.")
            return

        nama = input("   Nama   : ").strip()
        if not nama:
            print("   ⚠️  Nama tidak boleh kosong.")
            return

        try:
            nilai = float(input("   Nilai  : ").strip())
            if not (0 <= nilai <= 100):
                raise ValueError
        except ValueError:
            print("   ❌ Nilai harus angka antara 0-100.")
            return

        # Simpan ke dictionary — O(1)
        self.mahasiswa[nim] = {"nama": nama, "nilai": nilai}
        self.is_sorted = False
        self._simpan_ke_file()
        tulis_log("TAMBAH", f"NIM={nim}, Nama={nama}, Nilai={nilai}")
        print(f"   ✅ Mahasiswa '{nama}' (NIM: {nim}) berhasil ditambahkan.")

    def lihat_semua(self):
        print("\n📋 DAFTAR SEMUA MAHASISWA")
        if not self.mahasiswa:
            print("   (Data masih kosong)")
            return
        print(f"   {'NIM':<15} {'Nama':<25} {'Nilai':>6}")
        print("   " + "-" * 50)
        for nim, info in self.mahasiswa.items():
            print(f"   {nim:<15} {info['nama']:<25} {info['nilai']:>6.1f}")
        print(f"\n   Total: {len(self.mahasiswa)} mahasiswa")
        tulis_log("LIHAT_SEMUA")

    def cari_mahasiswa(self):
        print("\n🔍 CARI MAHASISWA")
        nim_cari = input("   Masukkan NIM yang dicari: ").strip()

        # Pencarian langsung di dictionary — O(1)
        if nim_cari in self.mahasiswa:
            info = self.mahasiswa[nim_cari]
            print(f"\n   ✅ Ditemukan!")
            print(f"   NIM   : {nim_cari}")
            print(f"   Nama  : {info['nama']}")
            print(f"   Nilai : {info['nilai']}")
        else:
            print(f"   ❌ NIM '{nim_cari}' tidak ditemukan.")

        tulis_log("CARI", f"NIM={nim_cari}")

    def hapus_mahasiswa(self):
        print("\n🗑️  HAPUS MAHASISWA")
        nim = input("   Masukkan NIM yang akan dihapus: ").strip()
        if nim not in self.mahasiswa:
            print(f"   ❌ NIM '{nim}' tidak ditemukan.")
            return
        nama = self.mahasiswa[nim]["nama"]
        konfirmasi = input(f"   Yakin hapus '{nama}' (NIM: {nim})? (y/n): ").strip().lower()
        if konfirmasi == "y":
            del self.mahasiswa[nim]
            self._simpan_ke_file()
            tulis_log("HAPUS", f"NIM={nim}, Nama={nama}")
            print(f"   ✅ Data '{nama}' berhasil dihapus.")
        else:
            print("   ℹ️  Penghapusan dibatalkan.")

    def update_nilai(self):
        print("\n✏️  UPDATE NILAI")
        nim = input("   Masukkan NIM: ").strip()
        if nim not in self.mahasiswa:
            print(f"   ❌ NIM '{nim}' tidak ditemukan.")
            return
        try:
            nilai_baru = float(input(f"   Nilai baru untuk {self.mahasiswa[nim]['nama']}: ").strip())
            if not (0 <= nilai_baru <= 100):
                raise ValueError
        except ValueError:
            print("   ❌ Nilai harus angka antara 0-100.")
            return

        nilai_lama = self.mahasiswa[nim]["nilai"]
        self.mahasiswa[nim]["nilai"] = nilai_baru
        self.is_sorted = False
        self._simpan_ke_file()
        tulis_log("UPDATE", f"NIM={nim}, Nilai: {nilai_lama} -> {nilai_baru}")
        print(f"   ✅ Nilai berhasil diperbarui: {nilai_lama} → {nilai_baru}")

    # --------------------------------------------------
    # TUGAS 7 (tetap): Sorting & Searching
    # --------------------------------------------------
    def sorting_nilai(self):
        if not self.mahasiswa:
            print("⚠️  Data kosong.")
            return

        print("\n🔄 SORTING DATA NILAI")
        print("   1. Bubble Sort")
        print("   2. Insertion Sort")
        pilih = input("   Pilih algoritma (1/2): ").strip()

        # Ubah dictionary ke list [(nim, nilai)] untuk sorting
        arr = [(nim, info["nilai"]) for nim, info in self.mahasiswa.items()]

        if pilih == "1":
            arr_sorted, comps = bubble_sort(arr)
            self.last_sort = "Bubble Sort"
        elif pilih == "2":
            arr_sorted, comps = insertion_sort(arr)
            self.last_sort = "Insertion Sort"
        else:
            print("   ❌ Pilihan tidak valid.")
            return

        self.is_sorted = True
        print(f"\n   ✅ Sorting selesai ({self.last_sort})")
        print(f"   📊 Jumlah perbandingan: {comps}")
        print(f"\n   {'Rank':<6} {'NIM':<15} {'Nama':<25} {'Nilai':>6}")
        print("   " + "-" * 55)
        for rank, (nim, nilai) in enumerate(arr_sorted, 1):
            nama = self.mahasiswa[nim]["nama"]
            print(f"   {rank:<6} {nim:<15} {nama:<25} {nilai:>6.1f}")

        tulis_log("SORTING", self.last_sort)

    def searching_nim(self):
        if not self.mahasiswa:
            print("⚠️  Data kosong.")
            return

        print("\n🔍 SEARCHING DATA (berdasarkan NIM)")
        nim_cari = input("   Masukkan NIM: ").strip()

        arr = [(nim, info["nilai"]) for nim, info in self.mahasiswa.items()]

        print("   1. Linear Search")
        print("   2. Binary Search (NIM diurutkan dulu secara otomatis)")
        pilih = input("   Pilih algoritma (1/2): ").strip()

        if pilih == "1":
            idx, steps = linear_search(arr, nim_cari)
            metode = "Linear Search"
        elif pilih == "2":
            arr_nim_sorted = sorted(arr, key=lambda x: x[0])
            idx, steps = binary_search(arr_nim_sorted, nim_cari)
            if idx != -1:
                nim_cari = arr_nim_sorted[idx][0]   # pastikan hasil benar
            metode = "Binary Search"
        else:
            print("   ❌ Pilihan tidak valid.")
            return

        if idx != -1:
            nama  = self.mahasiswa[nim_cari]["nama"]
            nilai = self.mahasiswa[nim_cari]["nilai"]
            print(f"   ✅ {metode}: Ditemukan! | Nama: {nama} | Nilai: {nilai} | Langkah: {steps}")
        else:
            print(f"   ❌ {metode}: NIM '{nim_cari}' tidak ditemukan. | Langkah: {steps}")

        tulis_log("SEARCHING", f"NIM={nim_cari}, Metode={metode}")

    # --------------------------------------------------
    # TUGAS 11: Parsing Log File menggunakan Set
    # --------------------------------------------------
    def tampil_statistik_log(self):
        print("\n📊 STATISTIK LOG AKTIVITAS (Tugas 11)")
        hasil = baca_log()

        if hasil["total_aktivitas"] == 0:
            print("   ℹ️  Belum ada log aktivitas.")
            return

        print(f"   Total aktivitas tercatat : {hasil['total_aktivitas']}")
        print(f"   Jumlah user unik (set)   : {len(hasil['user_unik'])}")
        print(f"   Daftar user unik         : {', '.join(sorted(hasil['user_unik']))}")
        print(f"\n   Ringkasan per aksi:")
        for aksi, jml in sorted(hasil["ringkasan_aksi"].items()):
            print(f"     • {aksi:<20} : {jml} kali")

    # --------------------------------------------------
    # MENU UTAMA
    # --------------------------------------------------
    def run(self):
        print("\n🖥️  === MINI SISTEM CLI MAHASISWA ===")
        print("   Tugas 9 (Dictionary) + Tugas 10 (File) + Tugas 11 (Log)\n")

        while True:
            print("\n📋 MENU UTAMA:")
            print("   [1] Tambah Mahasiswa")
            print("   [2] Lihat Semua Mahasiswa")
            print("   [3] Cari Mahasiswa (Dictionary O(1))")
            print("   [4] Hapus Mahasiswa")
            print("   [5] Update Nilai")
            print("   ─────────────────────────────")
            print("   [6] Sorting Nilai (Bubble/Insertion)")
            print("   [7] Searching NIM (Linear/Binary)")
            print("   ─────────────────────────────")
            print("   [8] Lihat Statistik Log (Set)")
            print("   [9] Keluar")

            pilih = input("\n   Pilih menu [1-9]: ").strip()

            if   pilih == "1": self.tambah_mahasiswa()
            elif pilih == "2": self.lihat_semua()
            elif pilih == "3": self.cari_mahasiswa()
            elif pilih == "4": self.hapus_mahasiswa()
            elif pilih == "5": self.update_nilai()
            elif pilih == "6": self.sorting_nilai()
            elif pilih == "7": self.searching_nim()
            elif pilih == "8": self.tampil_statistik_log()
            elif pilih == "9":
                print("\n   👋 Program ditutup. Data tersimpan otomatis. Sampai jumpa!")
                tulis_log("KELUAR")
                break
            else:
                print("   ❌ Pilihan tidak valid.")


# =========================================================
# ▶️  ENTRY POINT
# =========================================================
if __name__ == "__main__":
    sistem = MiniSistemMahasiswa()
    sistem.run()