from abc import ABC, abstractmethod
from datetime import datetime


class CatatanStatus:
    """Satu catatan status paket (dibuat di dalam Paket -> KOMPOSISI)."""

    def __init__(self, status):
        self.status = status
        self.waktu = datetime.now()


class Paket:
    _hitung = 0                       # atribut class: jumlah paket dibuat
    ALUR_STATUS = ["Diterima", "Dalam Perjalanan", "Terkirim"]

    def __init__(self, penerima, berat_kg):
        self.berat_kg = berat_kg      # lewat setter (validasi dulu)
        Paket._hitung += 1
        self._no_resi = f"PKT{Paket._hitung:03d}"
        self._penerima = penerima
        self._riwayat = [CatatanStatus("Diterima")]   # komposisi

    @property
    def no_resi(self):
        return self._no_resi

    @property
    def berat_kg(self):
        return self._berat_kg

    @berat_kg.setter
    def berat_kg(self, nilai):
        if not Paket.berat_valid(nilai):
            raise ValueError("Berat paket harus lebih dari 0")
        self._berat_kg = nilai

    @property
    def status(self):
        return self._riwayat[-1].status

    @staticmethod
    def berat_valid(nilai):
        return isinstance(nilai, (int, float)) and nilai > 0

    @classmethod
    def dari_gram(cls, penerima, gram):
        return cls(penerima, gram / 1000)

    @classmethod
    def total_dibuat(cls):
        return Paket._hitung

    def perbarui_status(self, status_baru):
        posisi = Paket.ALUR_STATUS.index(self.status)
        if status_baru not in Paket.ALUR_STATUS or \
                Paket.ALUR_STATUS.index(status_baru) != posisi + 1:
            raise ValueError(f"Status tidak boleh dari {self.status} ke {status_baru}")
        self._riwayat.append(CatatanStatus(status_baru))

    def biaya_kirim(self):
        return int(self._berat_kg * 2000)

    def __str__(self):
        return f"{self._no_resi} ({self._berat_kg} kg) -> {self._penerima} [{self.status}]"

    def __repr__(self):
        return f"Paket(no_resi={self._no_resi!r})"


class MixinAsuransi:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def nilai_asuransi(self):
        return self.berat_kg * 100000


class PaketRapuh(MixinAsuransi, Paket):
    def __init__(self, penerima, berat_kg, catatan_penanganan="Hati-hati"):
        super().__init__(penerima, berat_kg)
        self.catatan_penanganan = catatan_penanganan   # lewat setter

    @property
    def catatan_penanganan(self):
        return self._catatan_penanganan

    @catatan_penanganan.setter
    def catatan_penanganan(self, nilai):
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError("Catatan penanganan tidak boleh kosong")
        self._catatan_penanganan = nilai

    def biaya_kirim(self):            # override
        return super().biaya_kirim() + 5000


class Kurir(ABC):
    def __init__(self, id_kurir, nama, kapasitas_maks):
        self._id_kurir = id_kurir
        self.nama = nama                       # lewat setter
        self.kapasitas_maks = kapasitas_maks   # lewat setter

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError("Nama kurir tidak boleh kosong")
        self._nama = nilai

    @property
    def kapasitas_maks(self):
        return self._kapasitas_maks

    @kapasitas_maks.setter
    def kapasitas_maks(self, nilai):
        if not isinstance(nilai, (int, float)) or nilai <= 0:
            raise ValueError("Kapasitas kurir harus lebih dari 0")
        self._kapasitas_maks = nilai

    @abstractmethod
    def jenis_kendaraan(self):
        pass

    def __str__(self):
        return f"Kurir {self._nama} ({self.jenis_kendaraan()}, maks {self._kapasitas_maks} kg)"

    def __eq__(self, lain):
        return isinstance(lain, Kurir) and self._id_kurir == lain._id_kurir

    def __hash__(self):
        return hash(self._id_kurir)


class KurirMotor(Kurir):
    def __init__(self, id_kurir, nama):
        super().__init__(id_kurir, nama, 20)

    def jenis_kendaraan(self):
        return "Motor"


class KurirMobil(Kurir):
    def __init__(self, id_kurir, nama):
        super().__init__(id_kurir, nama, 200)

    def jenis_kendaraan(self):
        return "Mobil"


class TitikAntar:
    """Titik antar. Paket dari luar -> AGREGASI."""

    def __init__(self, alamat, paket):
        self._alamat = alamat
        self._paket = paket

    @property
    def alamat(self):
        return self._alamat

    @property
    def paket(self):
        return self._paket


class Rute:
    def __init__(self, asal):
        self._asal = asal
        self._titik = []

    def tambah_titik(self, alamat, paket):
        self._titik.append(TitikAntar(alamat, paket))   # komposisi

    def total_berat(self):
        return sum(t.paket.berat_kg for t in self._titik)

    @property
    def titik(self):
        return list(self._titik)


class Pengiriman:
    def __init__(self, kurir, asal="Gudang Utama"):
        self._kurir = kurir           # asosiasi ke Kurir
        self._rute = Rute(asal)       # komposisi

    def tambah_paket(self, alamat, paket):
        total = self._rute.total_berat() + paket.berat_kg
        if total > self._kurir.kapasitas_maks:
            raise ValueError(
                f"Melebihi kapasitas {self._kurir.kapasitas_maks} kg (jadi {total} kg)")
        self._rute.tambah_titik(alamat, paket)

    def berangkat(self):
        for titik in self._rute.titik:
            titik.paket.perbarui_status("Dalam Perjalanan")

    def antar_semua(self):
        for titik in self._rute.titik:
            titik.paket.perbarui_status("Terkirim")

    def total_berat(self):
        return self._rute.total_berat()

    def __str__(self):
        return f"Pengiriman oleh {self._kurir} dengan {len(self._rute.titik)} titik"


if __name__ == "__main__":
    motor = KurirMotor("K01", "Andi")
    mobil = KurirMobil("K02", "Budi")
    p1 = Paket("Sari", 5)
    p2 = PaketRapuh("Dewa", 8)
    p3 = Paket.dari_gram("Made", 150000)

    print("=== Skenario normal ===")
    print(motor)
    print(p1)
    s = Pengiriman(motor)
    s.tambah_paket("Jl. Sudirman 1", p1)
    s.tambah_paket("Jl. Gatsu 7", p2)
    print(s)
    print("Total berat:", s.total_berat(), "kg")
    s.berangkat()
    print(p1.status)
    s.antar_semua()
    print(p1.status)
    print("Biaya p1:", p1.biaya_kirim(), "| biaya p2:", p2.biaya_kirim())
    print("Nilai asuransi p2:", p2.nilai_asuransi())

    print("=== Data tidak valid ===")
    try:
        Paket("Rudi", -2)
    except ValueError as e:
        print("Ditolak:", e)
    try:
        p1.berat_kg = -5
    except ValueError as e:
        print("Ditolak:", e)
    print("Berat p1 tetap:", p1.berat_kg, "kg")
    try:
        Pengiriman(motor).tambah_paket("Jl. Kuta 3", p3)
    except ValueError as e:
        print("Ditolak:", e)
    try:
        p3.perbarui_status("Terkirim")
    except ValueError as e:
        print("Ditolak:", e)
    try:
        Kurir("K03", "Eko", 10)
    except TypeError:
        print("Ditolak: Kurir adalah class abstrak")

    print("=== Perbandingan == ===")
    print("motor == Kurir K01 lain :", motor == KurirMotor("K01", "Andi2"))
    print("motor == mobil          :", motor == mobil)

    print("Total paket dibuat:", Paket.total_dibuat())
    print("MRO PaketRapuh:", [k.__name__ for k in PaketRapuh.mro()])
