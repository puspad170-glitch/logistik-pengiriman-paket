"""Hierarki custom exception untuk sistem logistik pengiriman paket.

Struktur:
    Exception
     └── LogistikError                       (base exception aplikasi)
          ├── BeratTidakValidError
          ├── KapasitasTerlampauiError
          ├── TransisiStatusError
          ├── CatatanPenangananTidakValidError
          └── DataKurirTidakValidError
"""


class LogistikError(Exception):
    """Base exception untuk seluruh kesalahan pada sistem logistik."""


class BeratTidakValidError(LogistikError):
    """Berat paket bukan angka atau kurang dari/sama dengan 0."""

    def __init__(self, nilai):
        self.nilai = nilai
        super().__init__(
            f"Berat paket harus berupa angka lebih dari 0 kg (diberikan: {nilai!r})."
        )


class KapasitasTerlampauiError(LogistikError):
    """Total berat paket melebihi kapasitas maksimal kurir."""

    def __init__(self, kapasitas, total):
        self.kapasitas = kapasitas
        self.total = total
        self.kelebihan = total - kapasitas
        super().__init__(
            f"Melebihi kapasitas {kapasitas} kg "
            f"(total menjadi {total} kg, lebih {self.kelebihan} kg)."
        )


class TransisiStatusError(LogistikError):
    """Perubahan status paket melanggar urutan alur."""

    def __init__(self, status_sekarang, status_baru):
        self.status_sekarang = status_sekarang
        self.status_baru = status_baru
        super().__init__(
            f"Status tidak boleh berubah dari '{status_sekarang}' ke '{status_baru}'."
        )


class CatatanPenangananTidakValidError(LogistikError):
    """Catatan penanganan paket rapuh kosong atau bukan teks."""

    def __init__(self, nilai):
        self.nilai = nilai
        super().__init__(
            f"Catatan penanganan tidak boleh kosong (diberikan: {nilai!r})."
        )


class DataKurirTidakValidError(LogistikError):
    """Nama atau kapasitas kurir tidak valid."""

    def __init__(self, bidang, nilai):
        self.bidang = bidang
        self.nilai = nilai
        super().__init__(f"{bidang} kurir tidak valid (diberikan: {nilai!r}).")
