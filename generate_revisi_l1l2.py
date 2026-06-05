#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator dokumen .docx: REVISI LANGKAH 1 (data aktual) & PENGEMBANGAN LANGKAH 2
untuk makalah VOLMON. Dibangun via raw XML + zipfile (tanpa dependency eksternal).
"""
import zipfile
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def run(text, bold=False, italic=False, size=None, color=None):
    props = ""
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    if size:
        props += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
    if color:
        props += f'<w:color w:val="{color}"/>'
    rpr = f'<w:rPr>{props}</w:rPr>' if props else ""
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
    return para(text, style=f"Heading{level}", spacing_after=160)


def bullet(text):
    ppr = ('<w:pPr><w:pStyle w:val="ListParagraph"/>'
           '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="60"/></w:pPr>')
    return f'<w:p>{ppr}{run(text)}</w:p>'


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
    lines = str(text).split("\n")
    runs = ""
    for i, ln in enumerate(lines):
        if i > 0:
            runs += '<w:br/>'
        runs += run(ln, bold=bold)
    p = f'<w:p><w:pPr>{ppr_items}</w:pPr>{runs}</w:p>'
    return f'<w:tc>{tcpr}{p}</w:tc>'


def table(rows, widths=None, header_shade="D9E2F3"):
    n = len(rows[0])
    if not widths:
        widths = [int(9300 / n)] * n
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
    tblpr = ('<w:tblPr><w:tblStyle w:val="TableGrid"/>'
             '<w:tblW w:w="9300" w:type="dxa"/>'
             '<w:tblBorders>'
             '<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
             '</w:tblBorders></w:tblPr>')
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
    return out + para("", spacing_after=120)


def figref(text):
    ppr = ('<w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/>'
           '<w:pBdr>'
           '<w:top w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '<w:left w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '<w:bottom w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '<w:right w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>'
           '</w:pBdr></w:pPr>')
    return f'<w:p>{ppr}{run(text, italic=True, color="808080")}</w:p>'


body = []

# ===== JUDUL =====
body.append(para("REVISI LANGKAH 1 (DATA AKTUAL) & PENGEMBANGAN LANGKAH 2",
                 bold=True, size=16, align="center", spacing_after=40))
body.append(para("Makalah VOLMON (Volume Monitoring) - Tim VAMOS, IT KAI Commuter",
                 italic=True, size=10, align="center", spacing_after=160))
body.append(para(
    "Dokumen ini memuat: (A) koreksi Langkah 1 dengan data aktual hasil monitoring aplikasi VolMon "
    "menggantikan angka estimasi; dan (B) pengembangan Langkah 2 berupa pengelompokan penyebab, "
    "diagram fishbone, analisa Why-Why, serta penentuan akar penyebab dominan dengan pembobotan. "
    "Konten dapat langsung disalin ke file master VOLMON_FIX.docx.",
    italic=True, size=10, color="C00000", spacing_after=200))

# ===== PANDUAN PENEMPATAN =====
body.append(para("PANDUAN PENEMPATAN DI FILE MASTER (VOLMON_FIX.docx)", bold=True, size=14,
                 color="1F3864", spacing_after=120))
body.append(para(
    "Tabel berikut memetakan setiap tabel/gambar baru ke lokasi penyisipannya di file master, "
    "termasuk kalimat acuan setelah mana elemen tersebut diletakkan."))
body.append(para("Tabel P1  Panduan Penempatan Tabel & Gambar", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Elemen", "Letakkan setelah / pada", "Bagian"],
    ["Kalimat jembatan + Tabel A1 + Infografik data pending + Tabel A2 + kalimat penutup",
     "Kalimat penutup Pareto: \u201c...tema perbaikan difokuskan pada peningkatan efektivitas "
     "monitoring sinkronisasi data gate.\u201d (akhir sub-bab 1.1, setelah Gambar 3)", "1.1 Identifikasi Masalah"],
    ["Pembaruan baris Risiko Revenue (Before-After)",
     "Pada Tabel 6 Before-After yang sudah ada (ganti isi baris Risiko revenue)", "1.2 Dampak & Harapan"],
    ["Pembaruan baseline Aspek Quality",
     "Pada Tabel 7 Harapan dan Sasaran (ganti kolom Kondisi Saat Ini baris Quality)", "1.4 Sasaran Tema"],
    ["Tabel B1 (Pengelompokan 4M+1E)",
     "Menggantikan/menyempurnakan Tabel 9 Pengelompokan Penyebab", "2.1 / Memetakan Sebab Akibat"],
    ["Gambar 5 Fishbone (gambar5_fishbone.svg)",
     "Pada slot \u201cGambar 5 Fishbone Diagram\u201d di sub-bab Memetakan Sebab Akibat", "2.2"],
    ["Tabel B2 (Why-Why)",
     "Setelah fishbone, sebelum sub-bab \u201cMenganalisis Akar Penyebab\u201d", "2.3 (baru)"],
    ["Tabel B3 (Pembobotan akar penyebab)",
     "Menggantikan Tabel 10 Akar Penyebab agar penetapan \u2018dominan\u2019 lebih objektif", "2.4"],
], widths=[3000, 4800, 1500]))

body.append(para("Tabel P2  Pemetaan Nama File Gambar (SVG) ke Nomor Gambar di Master", bold=True, size=10, spacing_after=60))
body.append(table([
    ["File SVG", "Nomor Gambar di Master", "Keterangan"],
    ["gambar1_flowchart_eksisting.svg", "Gambar 1 Proses Eksisting", "Sudah ada slot"],
    ["gambar2_pareto.svg", "Gambar 3 Grafik Masalah Ticket HD", "Sudah ada slot"],
    ["gambar3_before_after.svg", "Gambar 4 Before - After", "Sudah ada slot (angka diperbarui)"],
    ["gambar4_data_pending.svg", "GAMBAR BARU (sisipkan di 1.1)", "Tambahkan ke Daftar Gambar & sesuaikan penomoran berikutnya"],
    ["gambar5_fishbone.svg", "Gambar 5 Fishbone Diagram", "Sudah ada slot"],
], widths=[3300, 3500, 2500]))
body.append(para(
    "Catatan penomoran: penyisipan infografik data pending di sub-bab 1.1 menambah satu gambar baru. "
    "Setelah disisipkan, perbarui Daftar Gambar dan geser penomoran gambar setelahnya (+1) atau beri "
    "nomor menyesuaikan urutan final di dokumen master.", italic=True, size=9, spacing_after=200))

# ============================================================
# BAGIAN A - KOREKSI LANGKAH 1
# ============================================================
body.append(para("BAGIAN A - KOREKSI LANGKAH 1 (DATA AKTUAL)", bold=True, size=14,
                 color="1F3864", spacing_after=120))

body.append(para(
    "Pada versi sebelumnya, besaran kasus pending dan dampak finansial masih menggunakan angka "
    "estimasi. Bagian ini menggantikannya dengan data aktual hasil penyisiran/observasi awal "
    "(baseline) periode Oktober-Desember 2025 sehingga identifikasi masalah menjadi lebih kuat dan "
    "dapat dipertanggungjawabkan. Catatan: data baseline yang sama akan digunakan kembali sebagai "
    "pembanding pada Langkah 6 (Mengevaluasi Solusi)."))

body.append(para(
    "Kalimat jembatan (sebelum Tabel A1): \u201cSelain tercermin dari tiket helpdesk, besarnya "
    "keterlambatan sinkronisasi data gate juga dapat diukur secara langsung dari kondisi data yang "
    "tertahan (pending) pada gate. Berdasarkan hasil monitoring penyisiran awal, rata-rata kondisi "
    "data pending per minggu adalah sebagai berikut.\u201d", italic=True, color="7F6000"))

body.append(para("Tabel A1  Rata-rata Kondisi Data Pending (Nyangkut) per Minggu", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Parameter", "Nilai", "Keterangan"],
    ["Total gate aktif", "1.024 gate", "Seluruh gate beroperasi"],
    ["Gate bermasalah (Problem)", "192 gate", "18,75% dari total gate"],
    ["- Pending", "149 gate", "Data tertahan belum tersinkron"],
    ["- Error", "43 gate", "Aplikasi sync / database error"],
    ["Transaksi Gate In tertahan", "337.358 transaksi", "Belum naik ke server pusat"],
    ["Transaksi Gate Out tertahan", "246.185 transaksi", "Belum naik ke server pusat"],
    ["Total transaksi tertahan", "583.543 transaksi", "Gate In + Gate Out"],
    ["Revenue tertahan (pending)", "Rp932.412.856", "Potensi revenue belum tercatat tepat waktu"],
], widths=[3100, 2400, 3800]))
body.append(para("Sumber: hasil penyisiran/observasi awal (data baseline), periode Okt-Des 2025.",
                 italic=True, size=9, spacing_after=120))

body.append(para(
    "Kalimat jembatan (antara Tabel A1 dan A2): \u201cSebagai gambaran kondisi pada level stasiun, "
    "berikut contoh detail gate yang terdeteksi mengalami pending data.\u201d", italic=True, color="7F6000"))

body.append(para("Tabel A2  Contoh Detail Data Pending per Stasiun", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Stasiun", "IP Gate", "Gate In Pending", "Gate Out Pending", "Revenue Tertahan (Rp)"],
    ["BJD 10", "10.10.23.20", "0", "1", "3.000"],
    ["BJD 13", "10.10.23.23", "7.151", "5.490", "21.608.000"],
    ["BJD 21", "10.10.23.31", "2.591", "72", "97.000"],
], widths=[1500, 2100, 1900, 1900, 1900]))
body.append(figref("[GAMBAR (baru): Infografik Rata-rata Kondisi Data Pending per Minggu - "
                   "file gambar4_data_pending.svg. Letakkan tepat setelah Tabel A2.]"))

body.append(para(
    "Kalimat jembatan (setelah Tabel A2 / Gambar, menuju 1.2 Dampak): \u201cBesarnya volume transaksi "
    "dan revenue yang tertahan tersebut menegaskan bahwa keterlambatan sinkronisasi data gate "
    "berdampak langsung terhadap keandalan data operasional dan pendapatan perusahaan, sebagaimana "
    "diuraikan pada analisa dampak berikut.\u201d", italic=True, color="7F6000"))

body.append(heading("Pembaruan Estimasi Dampak Finansial menjadi Data Aktual", 2))
body.append(para(
    "Keterlambatan sinkronisasi data gate berdampak langsung terhadap ketepatan waktu pencatatan "
    "revenue. Berdasarkan data aktual aplikasi VolMon, rata-rata terdapat Rp932.412.856 revenue yang "
    "tertahan (pending) setiap minggu karena belum tersinkron ke server pusat. Nilai ini menggantikan "
    "estimasi awal sebelumnya dan menunjukkan secara nyata besarnya risiko terhadap keakuratan "
    "pelaporan revenue serta pengambilan keputusan manajemen apabila data tidak segera disinkronkan.",
    spacing_after=160))

body.append(heading("Penyesuaian Tabel Before - After (baris Risiko Revenue)", 2))
body.append(para("Baris \u201cRisiko revenue\u201d pada tabel Before - After disesuaikan menjadi:", spacing_after=60))
body.append(table([
    ["Aspek", "SEBELUM (Eksisting)", "SESUDAH (dengan VolMon)"],
    ["Risiko revenue", "Rata-rata Rp932.412.856 revenue tertahan (pending) per minggu",
     "Revenue tertahan ditekan, data tersedia tepat waktu"],
], widths=[2000, 3650, 3650]))

body.append(heading("Penyesuaian Sasaran Tema - Aspek Quality", 2))
body.append(para(
    "Baseline aspek Quality yang sebelumnya menggunakan estimasi \u201crata-rata 210 kasus Gate Pending\u201d "
    "disesuaikan menjadi data aktual \u201crata-rata 192 gate bermasalah per minggu (149 pending + 43 error)\u201d.",
    spacing_after=60))
body.append(table([
    ["Aspek", "Kondisi Saat Ini (Aktual)", "Target / Sasaran", "Waktu"],
    ["Quality",
     "Rata-rata 192 gate bermasalah/minggu (149 pending + 43 error); 583.543 transaksi & Rp932.412.856 revenue tertahan",
     "Menurunkan rata-rata gate bermasalah menjadi maksimal 50 gate/minggu sehingga revenue tertahan ikut menurun signifikan",
     "3 Bulan"],
], widths=[1100, 3900, 3300, 1000]))

body.append(heading("Daftar Perubahan Bagian A", 2))
body.append(bullet("Menambahkan Tabel A1 (data baseline kondisi data pending per minggu hasil penyisiran/observasi awal)."))
body.append(bullet("Menambahkan kalimat jembatan sebelum, di antara, dan sesudah Tabel A1-A2 agar alur mengalir."))
body.append(bullet("Mengubah atribusi sumber data dari \u2018aplikasi VolMon\u2019 menjadi \u2018penyisiran/observasi awal (baseline)\u2019 untuk menjaga logika Langkah 1."))
body.append(bullet("Menambahkan Tabel A2 (contoh detail per stasiun: BJD 10, BJD 13, BJD 21)."))
body.append(bullet("Mengganti estimasi dampak finansial menjadi data aktual Rp932.412.856 revenue tertahan/minggu."))
body.append(bullet("Memperbarui baris Risiko Revenue pada tabel Before-After (hapus angka estimasi Rp500 juta/hari)."))
body.append(bullet("Memperbarui baseline sasaran Quality dari estimasi 210 kasus menjadi aktual 192 gate/minggu."))

# ============================================================
# BAGIAN B - PENGEMBANGAN LANGKAH 2
# ============================================================
body.append(para("BAGIAN B - PENGEMBANGAN LANGKAH 2: MENGIDENTIFIKASI PENYEBAB", bold=True, size=14,
                 color="1F3864", spacing_after=120))

body.append(heading("2.1  Pengelompokan Penyebab (Diagram Sebab-Akibat)", 2))
body.append(para(
    "Berdasarkan hasil tinjauan objek masalah, seluruh kemungkinan penyebab keterlambatan sinkronisasi "
    "data gate dikelompokkan menggunakan pendekatan 4M + 1E, yaitu Manusia, Metode, Mesin/Alat, Material, "
    "dan Lingkungan. Pengelompokan ini menjadi dasar penyusunan diagram fishbone."))
body.append(para("Tabel B1  Pengelompokan Penyebab (4M + 1E)", bold=True, size=10, spacing_after=60))
body.append(table([
    ["Faktor", "Kemungkinan Penyebab"],
    ["Manusia", "Monitoring & penanganan masih bergantung pada petugas; pengecekan manual dilakukan berulang"],
    ["Metode", "Belum ada monitoring realtime; belum ada early warning system; monitoring masih manual"],
    ["Mesin / Alat", "Belum tersedia dashboard monitoring terpusat; tidak ada notifikasi otomatis; aplikasi sinkronisasi tidak termonitor"],
    ["Material", "Database lokal masing-masing gate berdiri sendiri (standalone); data gagal terkirim"],
    ["Lingkungan", "Jumlah gate sangat banyak (1.024 unit) dan tersebar di 84 stasiun"],
], widths=[1700, 7600]))
body.append(figref("[GAMBAR 5: Diagram Fishbone / Ishikawa - file gambar5_fishbone.svg. "
                   "Akibat (kepala): Keterlambatan Sinkronisasi Data Gate ke Server Pusat]"))

body.append(heading("2.2  Analisa Akar Penyebab dengan Metode Why-Why", 2))
body.append(para(
    "Untuk memastikan penyebab yang ditemukan benar-benar merupakan akar masalah (bukan sekadar "
    "gejala), dilakukan analisa Why-Why pada situasi Not OK yang paling berpengaruh. Penelusuran "
    "dilakukan bertingkat hingga ditemukan akar penyebab yang dapat ditindaklanjuti."))
body.append(para("Tabel B2  Analisa Why-Why", bold=True, size=10, spacing_after=60))
body.append(table([
    ["No", "Situasi Not OK", "Mengapa? (1)", "Mengapa? (2)", "Mengapa? (3)", "Akar Penyebab"],
    ["1", "Data transaksi gate terlambat tersinkron ke server pusat",
     "Gangguan sinkronisasi (pending insert / sync berhenti / DB error) tidak segera diketahui",
     "Tidak ada pemantauan status sinkronisasi secara realtime",
     "Belum tersedia dashboard monitoring terpusat & early warning",
     "Belum tersedia dashboard monitoring terpusat + early warning system"],
    ["2", "Gangguan aplikasi sinkronisasi baru diketahui setelah ada laporan",
     "Tidak ada notifikasi otomatis saat aplikasi/DB berhenti atau error",
     "Status aplikasi sinkronisasi tiap gate tidak terpantau otomatis",
     "Sistem monitoring kesehatan aplikasi/DB belum dibangun",
     "Aplikasi sinkronisasi tidak termonitor otomatis"],
    ["3", "Monitoring dilakukan manual ke 1.024 gate satu per satu",
     "Tiap gate berdiri sendiri (single operated), status tidak teragregasi",
     "Database lokal tiap gate terpisah dan tidak saling terhubung",
     "Belum ada mekanisme yang mengumpulkan status seluruh gate",
     "Database lokal berdiri sendiri + belum ada agregasi terpusat"],
], widths=[400, 1900, 1750, 1750, 1750, 1750]))

body.append(heading("2.3  Penentuan Akar Penyebab Dominan (Pembobotan)", 2))
body.append(para(
    "Akar penyebab yang ditemukan dinilai menggunakan tiga kriteria dengan skala 1-5 "
    "(1 = sangat rendah, 5 = sangat tinggi): Frekuensi (seberapa sering penyebab muncul), "
    "Dampak (pengaruh terhadap sasaran tema), dan Kemudahan Kendali (kemampuan tim untuk "
    "mengendalikan/memperbaiki). Akar penyebab dinyatakan dominan apabila total skor >= 11."))
body.append(para("Tabel B3  Pembobotan Akar Penyebab", bold=True, size=10, spacing_after=60))
body.append(table([
    ["No", "Akar Penyebab", "Frekuensi", "Dampak", "Kemudahan Kendali", "Total", "Keterangan"],
    ["1", "Belum tersedia dashboard monitoring terpusat", "5", "5", "4", "14", "Dominan"],
    ["2", "Belum tersedia early warning system", "5", "5", "4", "14", "Dominan"],
    ["3", "Aplikasi sinkronisasi tidak termonitor otomatis", "4", "5", "4", "13", "Dominan"],
    ["4", "Database lokal berdiri sendiri di tiap gate", "4", "4", "3", "11", "Dominan"],
    ["5", "Monitoring bergantung pada petugas (manual)", "4", "3", "3", "10", "Tidak dominan"],
    ["6", "Jumlah gate banyak & tersebar (1.024 / 84 stasiun)", "3", "3", "2", "8", "Tidak dominan"],
], widths=[400, 3400, 1100, 900, 1700, 800, 1000]))
body.append(para(
    "Catatan: penyebab nomor 5 dan 6 merupakan gejala/faktor lingkungan yang sulit dikendalikan "
    "secara langsung dan pada dasarnya akan teratasi seiring tersedianya sistem monitoring terpusat; "
    "oleh karena itu tidak dijadikan akar penyebab dominan.", italic=True, size=9, spacing_after=160))

body.append(heading("2.4  Kesimpulan Akar Penyebab Dominan", 2))
body.append(para(
    "Berdasarkan analisa Why-Why dan hasil pembobotan, ditetapkan empat akar penyebab dominan "
    "keterlambatan sinkronisasi data gate ke server pusat, yaitu:"))
body.append(numbered("Belum tersedia dashboard monitoring terpusat (skor 14)."))
body.append(numbered("Belum tersedia early warning system (skor 14)."))
body.append(numbered("Aplikasi sinkronisasi tidak termonitor otomatis (skor 13)."))
body.append(numbered("Database lokal berdiri sendiri di tiap gate sehingga status tidak teragregasi (skor 11)."))
body.append(para(
    "Keempat akar penyebab tersebut menjadi dasar perumusan solusi pada Langkah 3, yang difokuskan "
    "pada pengembangan sistem monitoring sinkronisasi data gate berbasis dashboard terpusat dengan "
    "fitur early warning dan pemantauan status aplikasi/database secara realtime (VolMon).",
    spacing_after=160))

body.append(heading("Daftar Perubahan Bagian B", 2))
body.append(bullet("Menyusun pengelompokan penyebab dengan kerangka 4M + 1E (Tabel B1) sebagai dasar fishbone."))
body.append(bullet("Menyediakan diagram fishbone (Gambar 5) menggantikan placeholder yang sebelumnya keliru."))
body.append(bullet("Menambahkan analisa Why-Why (Tabel B2) untuk memastikan penyebab adalah akar, bukan gejala."))
body.append(bullet("Menambahkan pembobotan akar penyebab (Tabel B3) agar penetapan 'dominan' lebih objektif."))
body.append(bullet("Menegaskan 4 akar penyebab dominan yang menjadi dasar solusi pada Langkah 3."))


# ===== BUNGKUS =====
document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:document xmlns:w="{W}"><w:body>'
    + "".join(body) +
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1418" w:right="1134" w:bottom="1418" w:left="1418" w:header="709" w:footer="709" w:gutter="0"/>'
    '</w:sectPr></w:body></w:document>'
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
    '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/>'
    '<w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="1F3864"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/>'
    '<w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="2E74B5"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/>'
    '<w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/></w:pPr></w:style>'
    '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>'
    '</w:styles>'
)
numbering_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:numbering xmlns:w="{W}">'
    '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
    '<w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>'
    '<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0">'
    '<w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/>'
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    '<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>'
    '</w:numbering>'
)

out_name = "REVISI Langkah 1 & 2 - VOLMON.docx"
with zipfile.ZipFile(out_name, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/numbering.xml", numbering_xml)

print(f"OK -> {out_name}")
