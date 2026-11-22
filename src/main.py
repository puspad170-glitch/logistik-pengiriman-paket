"""Program utama: skenario berhasil dan gagal dengan try/except/else/finally."""

from exceptions import (
    BeratTidakValidError,
    CatatanPenangananTidakValidError,
    DataKurirTidakValidError,
    KapasitasTerlampauiError,
    LogistikError,
    TransisiStatusError,
)
from kurir import KurirMotor
from paket import Paket, PaketRapuh
from pengiriman import Pengiriman


def ambil_berat_dari_teks(teks):
    """Gaya EAFP: langsung coba ubah ke angka, tangani jika gagal."""
    try:
        return float(teks)
    except ValueError as e:
        raise BeratTidakValidError(teks) from e      # exception chaining


def tambah_paket_dengan_log(pengiriman, alamat, paket):
    """Mencatat log lalu melempar ulang (re-raise) ke pemanggil."""
    try:
        pengiriman.tambah_paket(alamat, paket)
    except KapasitasTerlampauiError as e:
        print(f"[LOG] Paket {paket.no_resi} gagal ditambahkan ke {alamat} (lebih {e.kelebihan} kg)")
        raise                                        # re-raise: exception sama diteruskan


def jalankan_uji_kasus(judul, aksi):
    print(f"\n--- {judul} ---")
    try:
        hasil = aksi()
    except KapasitasTerlampauiError as e:
        print(f"[Gagal - Kapasitas] {e} Kurangi {e.kelebihan} kg.")
    except TransisiStatusError as e:
        print(f"[Gagal - Status] {e}")
        if e.__cause__ is not None:
            print(f"    (penyebab asli: {type(e.__cause__).__name__})")
    except BeratTidakValidError as e:
        print(f"[Gagal - Berat] {e}")
        if e.__cause__ is not None:
            print(f"    (penyebab asli: {type(e.__cause__).__name__})")
    except CatatanPenangananTidakValidError as e:
        print(f"[Gagal - Catatan Rapuh] {e}")
    except DataKurirTidakValidError as e:
        print(f"[Gagal - Data Kurir] {e} (bidang: {e.bidang})")
    except LogistikError as e:
        print(f"[Gagal - Umum Logistik] {e}")
    else:
        print(f"[Berhasil] {hasil}")
    finally:
        print("-> Selesai memproses percobaan ini.")


if __name__ == "__main__":
    motor = KurirMotor("K01", "Andi")
    p1 = Paket("Sari", 5)
    p2 = PaketRapuh("Dewa", 8, "Jangan dibanting")
    p_berat = Paket.dari_gram("Made", 150000)

    def skenario_sukses():
        s = Pengiriman(motor)
        s.tambah_paket("Jl. Sudirman 1", p1)
        s.tambah_paket("Jl. Gatsu 7", p2)
        s.berangkat()
        s.antar_semua()
        return f"{s} | Status p1: {p1.status} | Biaya p2: {p2.biaya_kirim()}"

    jalankan_uji_kasus("1. Skenario Pengiriman Normal", skenario_sukses)
    jalankan_uji_kasus("2. Berat Paket Negatif", lambda: Paket("Rudi", -2))
    jalankan_uji_kasus(
        "3. Berat dari Teks Bukan Angka",
        lambda: Paket("Rudi", ambil_berat_dari_teks("lima")),
    )
    jalankan_uji_kasus(
        "4. Kapasitas Kurir Terlampaui",
        lambda: tambah_paket_dengan_log(Pengiriman(motor), "Jl. Kuta 3", p_berat),
    )
    jalankan_uji_kasus("5. Loncat Status Paket", lambda: p_berat.perbarui_status("Terkirim"))
    jalankan_uji_kasus("6. Status Tidak Dikenal", lambda: p_berat.perbarui_status("Hilang"))
    jalankan_uji_kasus(
        "7. Catatan Paket Rapuh Kosong",
        lambda: PaketRapuh("Citra", 2, "   "),
    )
    jalankan_uji_kasus("8. Nama Kurir Kosong", lambda: KurirMotor("K09", "   "))