# Sistem Logistik Pengiriman Paket (Exception Handling)

Pengembangan proyek Ujian Tengah Semester (UTS) Pemrograman Berorientasi Objek (**Kasus No. 9: Logistik Pengiriman Paket**) dengan penambahan *custom exception handling*, validasi aturan bisnis menggunakan `raise`, serta penanganan pengecualian (`try`, `except`, `else`, `finally`) di program utama.

## Anggota Kelompok

| No | Nama | NIM | Bagian yang Dikerjakan |
| :--- | :--- | :--- | :--- |
| 1 | [Tiara Kartini] | [2501020070] | Identifikasi aturan bisnis & hierarki custom exception (`exceptions.py`) |
| 2 | [Gusti Ayu Komang Tari Kusuma Wardani] | [2501020061] | Validasi `raise` pada setter & method kelas domain (`kurir.py`, `paket.py`, `pengiriman.py`) |
| 3 | [Ni Kadek Puspa Tirani Dewi] | [2501020081] | Program utama `try-except-else-finally` (`main.py`) & revisi class diagram (`README.md`) |

---

## Struktur Repository

```text
logistik-exception/
├── README.md
├── docs/
│   └── class-diagram (1).png     #revisi class diagram
└── src/
    ├── exceptions.py        # Hierarki custom exception aplikasi
    ├── kurir.py             # Class Kurir (abstrak), KurirMotor, KurirMobil
    ├── paket.py             # Class CatatanStatus, Paket, MixinAsuransi, PaketRapuh
    ├── pengiriman.py        # Class TitikAntar, Rute, Pengiriman
    └── main.py              # Program utama dengan blok try/except/else/finally
```

---

## Cara Menjalankan Program

1. Buka terminal dan arahkan ke folder `src/`:
   ```bash
   cd src
   ```
2. Jalankan program utama:
   ```bash
   python main.py
   ```

---

## Aturan Bisnis & Custom Exception

Berikut aturan bisnis pada sistem logistik pengiriman paket beserta *custom exception* yang dilempar (`raise`) saat aturan dilanggar:

| No | Aturan Bisnis | Method / Setter Pemicu | Custom Exception |
| :--- | :--- | :--- | :--- |
| 1 | **Berat paket harus** berupa angka (`int`/`float`, bukan `bool`) dan lebih dari `0` kg. | `Paket.berat_kg` (setter), `Paket.dari_gram()`, `ambil_berat_dari_teks()` | `BeratTidakValidError` |
| 2 | **Total berat paket tidak boleh melebihi kapasitas maksimal** kurir (`20` kg untuk Motor, `200` kg untuk Mobil). | `Pengiriman.tambah_paket()` | `KapasitasTerlampauiError` |
| 3 | **Perubahan status paket harus berurutan** satu langkah sesuai alur (`Diterima` -> `Dalam Perjalanan` -> `Terkirim`), **tidak boleh** loncat, mundur, atau tidak dikenal. | `Paket.perbarui_status()` | `TransisiStatusError` |
| 4 | **Catatan penanganan paket rapuh tidak boleh** kosong atau bukan teks (`str`). | `PaketRapuh.catatan_penanganan` (setter) | `CatatanPenangananTidakValidError` |
| 5 | **Nama dan kapasitas kurir harus valid** (nama tidak boleh kosong, kapasitas harus angka `> 0` kg). | `Kurir.nama` (setter), `Kurir.kapasitas_maks` (setter) | `DataKurirTidakValidError` |

---

## Revisi Class Diagram (Hierarki Custom Exception & Relasi Domain)

Diagram berikut menambahkan hierarki `LogistikError` beserta *subclass*-nya (`«exception»`) dan menunjukkan kelas/method domain yang memunculkan exception tersebut:

![Class Diagram](docs/class-diagram.png)