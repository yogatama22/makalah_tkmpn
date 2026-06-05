#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator dokumen .docx untuk REVISI LANGKAH 1 makalah VOLMON.
Dibangun via raw XML + zipfile (tanpa dependency eksternal seperti python-docx).
"""
import zipfile
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


# ---------- Helper pembentuk XML ----------
def run(text, bold=False, italic=False, size=None, color=None):
    rpr = ""
    props = ""
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    if size:
        props += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
    if color:
        props += f'<w:color w:val="{color}"/>'
    if props:
        rpr = f'<w:rPr>{props}</w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(text="", style=None, bold=False, italic=False, size=None, align=None,
         color=None, spacing_after=120):
    ppr_items = ""
    if style:
        ppr_items += f'<w:pStyle w:val="{style}"/>'
    if align:
        ppr_items += f'<w:jc w:val="{align}"/>'
    ppr_items += f'<w:spacing w:after="{spacing_after}"/>'
    ppr = f'<w:pPr>{ppr_items}</w:pPr>'
    r = run(text, bold=bold, italic=italic, size=size, color=color) if text else ""
    return f'<w:p>{ppr}{r}</w:p>'


def heading(text, level=1):
    style = f"Heading{level}"
    return para(text, style=style, spacing_after=160)


def bullet(text, bold_prefix=None):
    ppr = ('<w:pPr><w:pStyle w:val="ListParagraph"/>'
           '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="60"/></w:pPr>')
    runs = ""
    if bold_prefix:
        runs += run(bold_prefix, bold=True)
    runs += run(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def numbered(text):
    ppr = ('<w:pPr><w:pStyle w:val="ListParagraph"/>'
           '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>'
           '<w:spacing w:after="60"/></w:pPr>')
    return f'<w:p>{ppr}{run(text)}</w:p>'


def cell(text, bold=False, width=None, shade=None, align=None):
    tcpr = '<w:tcPr>'
    if width:
        tcpr += f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if shade:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    tcpr += '<w:vAlign w:val="center"/></w:tcPr>'
    ppr_items = '<w:spacing w:after="40"/>'
    if align:
        ppr_items += f'<w:jc w:val="{align}"/>'
    # support multi-line within a cell using \n
    lines = str(text).split("\n")
    runs = ""
    for i, ln in enumerate(lines):
        if i > 0:
            runs += '<w:br/>'
        runs += run(ln, bold=bold)
    p = f'<w:p><w:pPr>{ppr_items}</w:pPr>{runs}</w:p>'
    return f'<w:tc>{tcpr}{p}</w:tc>'


def table(rows, widths=None, header_shade="D9E2F3"):
    """rows: list of list of (text) ; first row treated as header."""
    n = len(rows[0])
    if not widths:
        widths = [int(9300 / n)] * n
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
    tblpr = ('<w:tblPr>'
             '<w:tblStyle w:val="TableGrid"/>'
             '<w:tblW w:w="9300" w:type="dxa"/>'
             '<w:tblBorders>'
             '<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '</w:tblBorders>'
             '</w:tblPr>')
    out = f'<w:tbl>{tblpr}{grid}'
    for ri, r in enumerate(rows):
        is_header = (ri == 0)
        cells = ""
        for ci, c in enumerate(r):
            shade = header_shade if is_header else None
            align = "center" if is_header else None
            cells += cell(c, bold=is_header, width=widths[ci], shade=shade, align=align)
        trpr = '<w:trPr><w:tblHeader/></w:trPr>' if is_header else ''
        out += f'<w:tr>{trpr}{cells}</w:tr>'
    out += '</w:tbl>'
    # spacer paragraph after table
    return out + para("", spacing_after=120)


def figure_placeholder(text):
    ppr = ('<w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/>'
           '<w:pBdr>'
           '<w:top w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '<w:left w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '<w:bottom w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '<w:right w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '</w:pBdr></w:pPr>')
    return f'<w:p>{ppr}{run(text, italic=True, color="808080")}</w:p>'


# ---------- Susun isi dokumen ----------
body = []

# Judul
body.append(para("REVISI & PENGEMBANGAN LANGKAH 1", bold=True, size=16, align="center", spacing_after=40))
body.append(para("MENENTUKAN AKTIFITAS", bold=True, size=14, align="center", spacing_after=40))
body.append(para("Makalah VOLMON (Volume Monitoring) - Tim VAMOS, IT KAI Commuter",
                 italic=True, size=10, align="center", spacing_after=200))
body.append(para("Catatan: Dokumen ini adalah versi pengembangan Langkah 1 yang memuat tambahan "
                 "alur eksisting, kuantifikasi beban kerja penyisiran manual, konsistensi data tiket, "
                 "analisa Pareto, serta visual before-after dan dampak finansial. Bagian yang masih "
                 "memerlukan gambar/diagram diberi penanda [GAMBAR].",
                 italic=True, size=10, color="C00000", spacing_after=200))

# 1.1 Identifikasi Masalah
body.append(heading("1.1  Identifikasi Masalah", 1))
body.append(para(
    "PT Kereta Commuter Indonesia (KCI) mengoperasikan sistem gate elektronik pada stasiun KRL "
    "sebagai media transaksi perjalanan penumpang sekaligus pencatatan data volume penumpang yang "
    "berkaitan langsung dengan data operasional dan revenue perusahaan. Saat ini terdapat 1.024 gate "
    "aktif yang tersebar di 84 stasiun dan beroperasi setiap hari. Sistem gate masih menggunakan pola "
    "single operated, di mana masing-masing gate memiliki sistem operasi, aplikasi sinkronisasi, dan "
    "database PostgreSQL tersendiri yang berdiri sendiri (standalone) dan berjalan secara offline. "
    "Dengan pola ini, apabila satu gate bermasalah maka tidak berdampak ke gate lain, namun di sisi "
    "lain data transaksi pada gate tersebut berpotensi terlambat atau gagal tersinkron ke server pusat."))

body.append(para(
    "Karena setiap gate berdiri sendiri, tidak tersedia mekanisme yang dapat memantau status seluruh "
    "gate secara terpusat. Untuk memastikan data tersinkron, Tim IT melakukan penyisiran rutin dengan "
    "cara me-remote PC setiap gate satu per satu. Alur proses monitoring eksisting digambarkan sebagai berikut."))

body.append(para("Alur Proses Monitoring Eksisting (Saat Ini):", bold=True, spacing_after=60))
body.append(numbered("Petugas IT melakukan remote ke PC Gate."))
body.append(numbered("Petugas menganalisa status gate: ONLINE atau OFFLINE."))
body.append(numbered("Jika OFFLINE -> laporkan ke teknisi lapangan untuk pengecekan perangkat secara langsung; "
                     "setelah gate kembali ONLINE, lanjut ke pengecekan data."))
body.append(numbered("Jika ONLINE -> lakukan pengecekan data di dalam gate: apakah aplikasi sinkronisasi "
                     "hang/perlu restart, atau apakah database PostgreSQL perlu di-restart."))
body.append(numbered("Lakukan tindakan perbaikan (restart aplikasi sync / restart database) sesuai temuan."))
body.append(numbered("Pastikan data transaksi gate berhasil tersinkron ke server pusat."))
body.append(figure_placeholder("[GAMBAR: Flowchart Alur Monitoring Eksisting - dibuat dari 6 langkah di atas "
                               "dengan percabangan keputusan Online/Offline]"))

body.append(para(
    "Penyisiran dilakukan secara remote dan dibagi kepada 7 personel. Mengingat jumlah gate yang sangat "
    "banyak dan tersebar, beban kerja proses manual ini sangat besar sebagaimana dirinci pada tabel berikut."))

body.append(para("Tabel 1.1  Perhitungan Beban Kerja Penyisiran Manual", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Parameter", "Nilai"],
    ["Jumlah stasiun dipantau", "84 stasiun"],
    ["Jumlah gate per stasiun", "minimal 3 - maksimal 20 gate"],
    ["Total gate aktif", "1.024 gate"],
    ["Waktu pengecekan per gate", "minimal 15 menit"],
    ["Total waktu 1x penyisiran penuh", "1.024 gate x 15 menit = 15.360 menit (+- 256 jam)"],
    ["Frekuensi penyisiran", "2x / minggu (Senin & Jumat)"],
    ["Total waktu penyisiran per minggu", "+- 512 jam / minggu"],
    ["Jumlah personel", "7 orang"],
    ["Beban rata-rata per personel", "+- 73 jam / orang / minggu"],
], widths=[4200, 5100]))
body.append(para(
    "Berdasarkan Tabel 1.1, beban penyisiran manual mencapai +- 73 jam/orang/minggu, jauh melebihi jam "
    "kerja normal (40 jam/minggu). Kondisi ini menunjukkan bahwa metode monitoring manual tidak efisien "
    "dan tidak berkelanjutan, sehingga membuka peluang perbaikan melalui sistem monitoring terpusat.",
    spacing_after=160))

# Tabel Volume & Revenue
body.append(para("Tabel 1.2  Program Volume dan Pendapatan per Bulan", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Bulan", "Volume (penumpang)", "Revenue (Rp)"],
    ["Okt-2025", "29.092.956", "114.158.754.767"],
    ["Nov-2025", "27.607.760", "108.066.954.126"],
    ["Des-2025", "28.608.724", "113.091.793.952"],
], widths=[2300, 3500, 3500]))
body.append(para(
    "Berdasarkan Tabel 1.2, volume penumpang periode Oktober-Desember 2025 berada pada rentang 27-29 juta "
    "transaksi per bulan dengan revenue lebih dari Rp108 miliar per bulan. Besarnya volume transaksi ini "
    "menunjukkan bahwa keandalan data gate sangat penting dalam mendukung monitoring operasional dan "
    "pencapaian target pendapatan perusahaan.", spacing_after=160))

# Tabel Rekap Tiket (gunakan 533 valid)
body.append(para(
    "Keterlambatan sinkronisasi data gate juga tercermin dari tiket kendala E-Ticketing yang masuk pada "
    "Website it-helpdesk.kci.id. Pada periode Oktober-Desember 2025 tercatat 533 tiket yang valid dengan "
    "rincian sebagai berikut."))
body.append(para("Tabel 1.3  Rekapitulasi Tiket Kendala E-Ticketing Periode Oktober-Desember 2025",
                 bold=True, size=10, spacing_after=60))
body.append(table([
    ["No", "Jenis Kendala Tiket Helpdesk", "Okt", "Nov", "Des", "Total"],
    ["1", "Volume Gate In - Gate Out Tidak Update", "81", "72", "87", "240"],
    ["2", "Data Card History Tidak Update", "41", "38", "37", "116"],
    ["3", "Selisih Data Transaksi Mesin Struk POS dengan Website Pusat", "34", "33", "37", "104"],
    ["4", "Kendala Akun Staff Stasiun di Website Pusat E-Ticketing", "23", "22", "28", "73"],
    ["", "TOTAL", "179", "165", "189", "533"],
], widths=[600, 4500, 1050, 1050, 1050, 1050]))

# Tabel Identifikasi Masalah (Pareto)
body.append(para("Tabel 1.4  Identifikasi Masalah (Dasar Analisa Pareto)", bold=True, size=10, spacing_after=60))
body.append(table([
    ["No", "Item Masalah", "Jumlah", "Kumulatif", "%", "% Kumulatif"],
    ["1", "Volume Gate In - Gate Out Tidak Update", "240", "240", "45%", "45%"],
    ["2", "Data Card History Tidak Update", "116", "356", "22%", "67%"],
    ["3", "Selisih Data Transaksi Mesin Struk POS dengan Website Pusat", "104", "460", "20%", "86%"],
    ["4", "Kendala Akun Staff Stasiun di Website Pusat E-Ticketing", "73", "533", "14%", "100%"],
    ["", "TOTAL", "533", "", "100%", ""],
], widths=[500, 3900, 1100, 1200, 1100, 1500]))
body.append(figure_placeholder("[GAMBAR 1: Grafik Pareto - bar chart jumlah tiap masalah (urut menurun) "
                               "+ garis persentase kumulatif, dengan garis bantu cut-off 80%]"))
body.append(para(
    "Berdasarkan analisa Pareto, tiga kendala terbesar yaitu Volume Gate In-Gate Out Tidak Update (45%), "
    "Data Card History Tidak Update (22%), dan Selisih Data Transaksi Mesin Struk POS dengan Website Pusat "
    "(20%) memberikan kontribusi kumulatif sebesar 86% dari total 533 tiket. Ketiga permasalahan tersebut "
    "memiliki keterkaitan yang sama, yaitu keterlambatan sinkronisasi data transaksi dari gate menuju "
    "server pusat. Oleh karena itu, tema perbaikan difokuskan pada peningkatan efektivitas monitoring "
    "sinkronisasi data gate.", spacing_after=160))

# 1.2 Menganalisa Dampak dan Harapan
body.append(heading("1.2  Menganalisa Dampak dan Harapan", 1))
body.append(para(
    "Keterlambatan sinkronisasi data gate ke server pusat merupakan permasalahan prioritas yang berdampak "
    "langsung terhadap keandalan data operasional perusahaan. Data transaksi gate digunakan sebagai dasar "
    "monitoring volume penumpang, pencatatan revenue, analisis operasional, serta pengambilan keputusan "
    "manajemen. Apabila terjadi keterlambatan sinkronisasi, informasi pada sistem pusat tidak dapat "
    "menggambarkan kondisi aktual secara realtime."))

body.append(para("Tabel 1.5  Dampak Masalah Prioritas", bold=True, size=10, spacing_after=60))
body.append(table([
    ["No", "Dampak Masalah", "Pihak yang Terdampak"],
    ["1", "Data volume penumpang dan revenue tidak tersedia secara realtime", "Divisi COC - Data Analysis Sales & Development Team"],
    ["2", "Laporan revenue penjualan KMT berpotensi tidak akurat atau terlambat", "Divisi CAF - Verification Administration Team"],
    ["3", "Monitoring gangguan gate menjadi lambat dan reaktif", "Tim IT Development"],
    ["4", "Pengambilan keputusan analisa tidak berdasarkan data terkini", "Divisi COC - Data Analysis Sales & Development Team"],
    ["5", "Potensi pendapatan belum tercatat tepat waktu", "Perusahaan PT KCI"],
    ["6", "Beban kerja meningkat karena pengecekan masih dilakukan manual", "Tim IT Development"],
], widths=[500, 5000, 3800]))

# Dampak finansial
body.append(para("Estimasi Dampak Finansial", bold=True, spacing_after=60))
body.append(para(
    "Berdasarkan estimasi awal, keterlambatan sinkronisasi data gate selama 1 hari berpotensi menyebabkan "
    "selisih pencatatan revenue hingga Rp500.000.000 (lima ratus juta rupiah). Nilai ini menggambarkan "
    "besarnya risiko apabila data transaksi tidak naik ke server pusat secara tepat waktu, baik terhadap "
    "keakuratan pelaporan revenue maupun pengambilan keputusan manajemen.",
    spacing_after=40))
body.append(para("*Catatan: angka Rp500.000.000 merupakan estimasi awal dan masih dalam proses validasi "
                 "lebih lanjut oleh tim.", italic=True, size=9, color="C00000", spacing_after=160))

# Before-After
body.append(para("Perbandingan Kondisi Sebelum dan Sesudah (Before - After)", bold=True, spacing_after=60))
body.append(para("Tabel 1.6  Perbandingan Kondisi Before - After", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Aspek", "SEBELUM (Eksisting)", "SESUDAH (dengan VolMon)"],
    ["Metode monitoring", "Manual, remote gate satu per satu", "Otomatis & terpusat melalui dashboard"],
    ["Waktu deteksi gangguan", "+- 3 hari (menunggu jadwal penyisiran/laporan)", "+- 5 menit (realtime + early warning)"],
    ["Cakupan & waktu pantau", "Terbatas jadwal penyisiran (Senin & Jumat)", "24/7 secara realtime"],
    ["Beban kerja tim", "+- 73 jam/orang/minggu", "Berkurang minimal 90%"],
    ["Sifat monitoring", "Reaktif", "Proaktif"],
    ["Risiko revenue", "Potensi selisih +- Rp500 juta / hari keterlambatan", "Diminimalkan, data tersedia tepat waktu"],
], widths=[2000, 3650, 3650]))
body.append(figure_placeholder("[GAMBAR: Ilustrasi Before-After - sisi kiri proses manual (petugas remote "
                               "banyak gate), sisi kanan dashboard VolMon terpusat dengan notifikasi]"))

body.append(para("Harapan", bold=True, spacing_after=60))
body.append(para("Harapan dari penyelesaian masalah ini adalah tersedianya sistem monitoring yang mampu:",
                 spacing_after=60))
body.append(bullet("Mendeteksi keterlambatan sinkronisasi data gate secara otomatis dan realtime."))
body.append(bullet("Menampilkan status sinkronisasi seluruh gate dalam satu dashboard terpusat."))
body.append(bullet("Memberikan early warning ketika terjadi gangguan sinkronisasi atau aplikasi pendukung berhenti."))
body.append(bullet("Mempercepat proses identifikasi akar masalah dan tindakan perbaikan."))
body.append(bullet("Menjamin ketersediaan data volume penumpang dan revenue yang lebih andal."))
body.append(bullet("Mengurangi ketergantungan terhadap monitoring manual."))

# 1.3 Menentukan Tema
body.append(heading("1.3  Menentukan Tema", 1))
body.append(para("Berdasarkan hasil identifikasi masalah dan analisa dampak, tema improvement yang ditetapkan adalah:",
                 spacing_after=60))
body.append(para(
    "\u201cPeningkatan Keandalan Data Revenue Gate KRL melalui Early Warning System Monitoring "
    "Sinkronisasi Data Terpusat di Stasiun KAI Commuter Tahun 2026\u201d",
    bold=True, italic=True, align="center", spacing_after=120))
body.append(para(
    "Tema tersebut dipilih karena permasalahan utama berkaitan dengan keterlambatan sinkronisasi data gate "
    "ke server pusat dan belum adanya sistem monitoring yang terintegrasi. Melalui implementasi sistem "
    "monitoring terpusat, proses pemantauan data gate dapat dilakukan secara realtime, lebih cepat, dan proaktif."))

# 1.4 Menetapkan Harapan dan Sasaran Tema
body.append(heading("1.4  Menetapkan Harapan dan Sasaran Tema", 1))
body.append(para(
    "Sasaran improvement ditetapkan menggunakan prinsip SMART (Specific, Measurable, Achievable, Relevant, "
    "Time Bound) dan disusun berdasarkan aspek mutu Quality, Cost, Delivery, HSSE, dan Morale."))
body.append(para("Tabel 1.7  Sasaran Tema (QCDHM)", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Aspek", "Kondisi Saat Ini", "Target / Sasaran", "Waktu", "Lingkup"],
    ["Quality", "Data sinkronisasi gate belum termonitor realtime & masih terdapat keterlambatan",
     "Menurunkan kasus keterlambatan sinkronisasi (Gate Pending) dari rata-rata 210 kasus menjadi maksimal 50 kasus",
     "3 Bulan", "Gate KRL area monitoring"],
    ["Cost", "Pengecekan manual membutuhkan waktu & tenaga teknis (+-73 jam/orang/minggu)",
     "Mengurangi kebutuhan pengecekan manual minimal 90%", "3 Bulan", "Tim IT Development"],
    ["Delivery", "Penanganan gangguan menunggu laporan/komplain",
     "Mempercepat waktu deteksi gangguan dari rata-rata 3 hari menjadi maksimal 5 menit",
     "3 Bulan", "Gate & server monitoring"],
    ["HSSE", "Gangguan data dapat menghambat layanan & monitoring operasional",
     "Meminimalkan potensi gangguan operasional akibat keterlambatan data", "3 Bulan", "Operasional stasiun"],
    ["Morale", "Tim teknis terbebani pengecekan manual berulang",
     "Meningkatkan efektivitas kerja tim melalui dashboard monitoring terpusat", "3 Bulan", "Tim IT Development"],
], widths=[1100, 2700, 3300, 900, 1300]))
body.append(para(
    "Catatan dasar data: angka rata-rata 210 kasus Gate Pending diperoleh dari rekapitulasi data kasus "
    "pending sinkronisasi periode Oktober-Desember 2025, dan baseline waktu deteksi 3 hari diperoleh dari "
    "rata-rata selisih waktu antara terjadinya gangguan dengan waktu penanganan pada periode yang sama. "
    "(Disarankan melampirkan sumber data pendukung agar sasaran lebih kuat dipertanggungjawabkan.)",
    italic=True, size=9, spacing_after=160))

# 1.5 Pengesahan Aktivitas
body.append(heading("1.5  Pengesahan Aktivitas", 1))
body.append(para(
    "Aktivitas improvement ini disahkan sebagai upaya peningkatan keandalan monitoring data gate dan "
    "percepatan penanganan gangguan operasional. Dukungan dari pimpinan, fasilitator, dan anggota tim "
    "diperlukan agar pelaksanaan improvement dapat berjalan sesuai rencana dan memberikan manfaat terhadap "
    "peningkatan efektivitas monitoring operasional perusahaan."))
body.append(para("Komentar Pimpinan:", bold=True, spacing_after=300))
body.append(table([
    ["Pimpinan", "Fasilitator", "Ketua"],
    ["Tanda Tangan:\n\nTanggal:", "Tanda Tangan:\n\nTanggal:", "Tanda Tangan:\n\nTanggal:"],
], widths=[3100, 3100, 3100]))

# Ringkasan perubahan
body.append(heading("Ringkasan Perubahan pada Revisi Ini", 2))
body.append(bullet("Ditambahkan penjelasan arsitektur gate single operated/standalone yang berjalan offline."))
body.append(bullet("Ditambahkan Alur Proses Monitoring Eksisting (6 langkah + percabangan Online/Offline)."))
body.append(bullet("Ditambahkan Tabel 1.1 kuantifikasi beban kerja penyisiran manual (84 stasiun, 15 menit/gate, +-73 jam/orang/minggu)."))
body.append(bullet("Data tiket dikonsistenkan menggunakan total 533 yang valid (angka 626 dihapus)."))
body.append(bullet("Urutan masalah pada tabel rekap & Pareto diselaraskan (Data Card History di posisi 2)."))
body.append(bullet("Ditambahkan estimasi dampak finansial Rp500 juta/hari keterlambatan (perlu validasi)."))
body.append(bullet("Ditambahkan Tabel 1.6 perbandingan Before-After secara visual."))
body.append(bullet("Ditambahkan catatan dasar data untuk sasaran 210 kasus & baseline 3 hari."))


# ---------- Bungkus jadi document.xml ----------
document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:document xmlns:w="{W}">'
    '<w:body>'
    + "".join(body) +
    '<w:sectPr>'
    '<w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1701" w:header="709" w:footer="709" w:gutter="0"/>'
    '</w:sectPr>'
    '</w:body></w:document>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
    '</Types>'
)

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>'
)

doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
    '</Relationships>'
)

styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:styles xmlns:w="{W}">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="22"/><w:szCs w:val="22"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
    '<w:pPr><w:jc w:val="both"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
    '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
    '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="1F3864"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
    '<w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="2E74B5"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/>'
    '<w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/></w:pPr></w:style>'
    '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
    '<w:tblPr><w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '</w:tblBorders></w:tblPr></w:style>'
    '</w:styles>'
)

numbering_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:numbering xmlns:w="{W}">'
    # abstract 0 = bullet
    '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
    '<w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>'
    # abstract 1 = decimal
    '<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0">'
    '<w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/>'
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    '<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>'
    '</w:numbering>'
)

out_name = "REVISI Langkah 1 - VOLMON.docx"
with zipfile.ZipFile(out_name, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/numbering.xml", numbering_xml)

print(f"OK -> {out_name}")
