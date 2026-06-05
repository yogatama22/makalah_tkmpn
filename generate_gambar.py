#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator 3 gambar (SVG) untuk Langkah 1 makalah VOLMON:
  1) gambar1_flowchart_eksisting.svg  -> Alur monitoring manual saat ini
  2) gambar2_pareto.svg               -> Grafik Pareto masalah tiket
  3) gambar3_before_after.svg         -> Perbandingan Before vs After
SVG murni (teks), tanpa dependency. Bisa di-insert ke Word 2016+.
"""
from xml.sax.saxutils import escape

FONT = "Segoe UI, Arial, sans-serif"


def esc(t):
    return escape(str(t))


# ============================================================
# GAMBAR 1 - FLOWCHART ALUR MONITORING EKSISTING
# ============================================================
def build_flowchart():
    W, H = 820, 900
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    s.append('<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" '
             'orient="auto" markerUnits="strokeWidth">'
             '<path d="M0,0 L8,3 L0,6 Z" fill="#444"/></marker></defs>')
    s.append(f'<text x="{W/2}" y="40" text-anchor="middle" font-size="20" font-weight="bold" '
             f'fill="#1F3864">Alur Proses Monitoring Sinkronisasi Data Gate (Eksisting)</text>')

    def multiline(cx, cy, text, fs=14, weight="normal"):
        lines = text.split("\n")
        lh = fs + 4
        start = cy - (len(lines) - 1) * lh / 2
        o = ""
        for i, ln in enumerate(lines):
            o += (f'<text x="{cx}" y="{start + i*lh + fs*0.35}" text-anchor="middle" '
                  f'font-size="{fs}" font-weight="{weight}" fill="#222">{esc(ln)}</text>')
        return o

    def proc(cx, cy, w, h, text, fill="#DDEBF7", stroke="#2E74B5", fs=14):
        x, y = cx - w / 2, cy - h / 2
        out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" ry="8" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out += multiline(cx, cy, text, fs=fs)
        return out

    def stadium(cx, cy, w, h, text, fill="#E2EFDA", stroke="#548235"):
        x, y = cx - w / 2, cy - h / 2
        out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" ry="{h/2}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out += multiline(cx, cy, text, fs=14, weight="bold")
        return out

    def decision(cx, cy, w, h, text, fill="#FFF2CC", stroke="#BF8F00", fs=13):
        pts = f'{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}'
        out = f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        out += multiline(cx, cy, text, fs=fs)
        return out

    def arrow(x1, y1, x2, y2):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444" '
                f'stroke-width="2" marker-end="url(#arr)"/>')

    def label(x, y, text, fill="#C00000"):
        return (f'<text x="{x}" y="{y}" font-size="12" font-weight="bold" '
                f'fill="{fill}">{esc(text)}</text>')

    cx = 300
    bx = 640

    s.append(stadium(cx, 90, 230, 44, "MULAI"))
    s.append(proc(cx, 165, 250, 50, "Petugas IT remote ke PC Gate"))
    s.append(decision(cx, 270, 180, 100, "Status Gate\nOnline?"))
    s.append(proc(bx, 270, 240, 70, "Lapor teknisi lapangan\nuntuk cek perangkat\nsecara langsung",
                  fill="#FCE4E4", stroke="#C00000"))
    s.append(proc(cx, 400, 280, 70, "Cek data di dalam gate:\naplikasi sync hang? /\ndatabase perlu restart?"))
    s.append(decision(cx, 530, 200, 110, "Perlu\nrestart?"))
    s.append(proc(bx, 530, 240, 70, "Restart aplikasi sync /\nrestart database\nPostgreSQL",
                  fill="#FCE4E4", stroke="#C00000"))
    s.append(proc(cx, 670, 290, 60, "Pastikan data transaksi\ntersinkron ke server pusat",
                  fill="#E2EFDA", stroke="#548235"))
    s.append(stadium(cx, 760, 220, 44, "SELESAI", fill="#E2EFDA", stroke="#548235"))

    s.append(arrow(cx, 112, cx, 140))
    s.append(arrow(cx, 190, cx, 220))
    s.append(arrow(cx, 320, cx, 365))
    s.append(label(cx + 10, 350, "Ya (Online)", "#548235"))
    s.append(arrow(cx, 435, cx, 475))
    s.append(arrow(cx, 585, cx, 640))
    s.append(label(cx + 10, 620, "Tidak", "#548235"))
    s.append(arrow(cx, 700, cx, 738))

    s.append(arrow(cx + 90, 270, bx - 120, 270))
    s.append(label(420, 258, "Tidak (Offline)"))
    s.append(f'<path d="M{bx},305 L{bx},400 L{cx+140},400" fill="none" stroke="#C00000" '
             f'stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr)"/>')
    s.append(label(bx - 70, 360, "Setelah online", "#C00000"))

    s.append(arrow(cx + 100, 530, bx - 120, 530))
    s.append(label(cx + 110, 518, "Ya"))
    s.append(f'<path d="M{bx},565 L{bx},670 L{cx+145},670" fill="none" stroke="#C00000" '
             f'stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arr)"/>')
    s.append(label(bx - 60, 625, "Selesai restart", "#C00000"))

    ly = 830
    s.append(f'<rect x="60" y="{ly}" width="22" height="14" rx="3" fill="#DDEBF7" stroke="#2E74B5"/>')
    s.append(f'<text x="88" y="{ly+12}" font-size="12" fill="#333">Proses</text>')
    s.append(f'<polygon points="200,{ly} 214,{ly+7} 200,{ly+14} 186,{ly+7}" fill="#FFF2CC" stroke="#BF8F00"/>')
    s.append(f'<text x="222" y="{ly+12}" font-size="12" fill="#333">Keputusan</text>')
    s.append(f'<rect x="330" y="{ly}" width="22" height="14" rx="7" fill="#E2EFDA" stroke="#548235"/>')
    s.append(f'<text x="358" y="{ly+12}" font-size="12" fill="#333">Mulai/Selesai</text>')
    s.append(f'<rect x="480" y="{ly}" width="22" height="14" rx="3" fill="#FCE4E4" stroke="#C00000"/>')
    s.append(f'<text x="508" y="{ly+12}" font-size="12" fill="#333">Tindakan perbaikan</text>')

    s.append('</svg>')
    return "\n".join(s)


# ============================================================
# GAMBAR 2 - GRAFIK PARETO
# ============================================================
def build_pareto():
    W, H = 860, 560
    L, R, T, B = 90, 700, 70, 430
    plot_w = R - L
    plot_h = B - T

    cats = [
        ("Volume Gate In-\nGate Out Tidak Update", 240),
        ("Data Card History\nTidak Update", 116),
        ("Selisih Data POS vs\nWebsite Pusat", 104),
        ("Kendala Akun Staff\nWebsite Pusat", 73),
    ]
    total = sum(c[1] for c in cats)
    cum = []
    running = 0
    for _, v in cats:
        running += v
        cum.append(running)

    n = len(cats)
    slot = plot_w / n

    def y_count(v):
        return B - (v / total) * plot_h

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    s.append('<defs><marker id="dot" markerWidth="8" markerHeight="8" refX="4" refY="4">'
             '<circle cx="4" cy="4" r="3.2" fill="#C00000"/></marker></defs>')
    s.append(f'<text x="{W/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" '
             f'fill="#1F3864">Diagram Pareto Kendala Tiket E-Ticketing (Okt-Des 2025)</text>')
    s.append(f'<text x="{W/2}" y="58" text-anchor="middle" font-size="13" fill="#555">'
             f'Total = {total} tiket</text>')

    for i in range(0, 6):
        frac = i / 5
        y = B - frac * plot_h
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{R}" y2="{y:.1f}" stroke="#E6E6E6" stroke-width="1"/>')
        cval = int(round(frac * total))
        s.append(f'<text x="{L-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="#333">{cval}</text>')
        pval = int(round(frac * 100))
        s.append(f'<text x="{R+12}" y="{y+4:.1f}" text-anchor="start" font-size="12" fill="#C00000">{pval}%</text>')

    y80 = B - 0.8 * plot_h
    s.append(f'<line x1="{L}" y1="{y80:.1f}" x2="{R}" y2="{y80:.1f}" stroke="#C00000" '
             f'stroke-width="1.5" stroke-dasharray="7,5" opacity="0.8"/>')
    s.append(f'<text x="{R-4}" y="{y80-6:.1f}" text-anchor="end" font-size="12" '
             f'font-weight="bold" fill="#C00000">Batas 80%</text>')

    s.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="#333" stroke-width="1.5"/>')
    s.append(f'<line x1="{R}" y1="{T}" x2="{R}" y2="{B}" stroke="#C00000" stroke-width="1.5"/>')
    s.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="#333" stroke-width="1.5"/>')

    s.append(f'<text x="26" y="{(T+B)/2}" text-anchor="middle" font-size="13" fill="#333" '
             f'transform="rotate(-90 26 {(T+B)/2})">Jumlah Tiket</text>')
    s.append(f'<text x="{W-20}" y="{(T+B)/2}" text-anchor="middle" font-size="13" fill="#C00000" '
             f'transform="rotate(90 {W-20} {(T+B)/2})">Persentase Kumulatif</text>')

    bar_w = slot * 0.56
    colors = ["#2E74B5", "#5B9BD5", "#8FAADC", "#BDD7EE"]
    centers = []
    for i, (name, val) in enumerate(cats):
        cxp = L + slot * (i + 0.5)
        centers.append(cxp)
        bx = cxp - bar_w / 2
        by = y_count(val)
        bh = B - by
        s.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" '
                 f'fill="{colors[i]}" stroke="#1F4E79" stroke-width="1"/>')
        s.append(f'<text x="{cxp:.1f}" y="{by-8:.1f}" text-anchor="middle" font-size="13" '
                 f'font-weight="bold" fill="#1F3864">{val}</text>')
        pct = val / total * 100
        s.append(f'<text x="{cxp:.1f}" y="{by+18:.1f}" text-anchor="middle" font-size="12" '
                 f'fill="#FFFFFF" font-weight="bold">{pct:.0f}%</text>')
        for j, ln in enumerate(name.split("\n")):
            s.append(f'<text x="{cxp:.1f}" y="{B+18+j*14:.1f}" text-anchor="middle" '
                     f'font-size="11" fill="#333">{esc(ln)}</text>')

    pts = []
    for i, c in enumerate(cum):
        x = centers[i]
        y = y_count(c)
        pts.append((x, y))
    poly = " ".join(f'{x:.1f},{y:.1f}' for x, y in pts)
    s.append(f'<polyline points="{poly}" fill="none" stroke="#C00000" stroke-width="2.5" '
             f'marker-start="url(#dot)" marker-mid="url(#dot)" marker-end="url(#dot)"/>')
    for i, (x, y) in enumerate(pts):
        pctc = cum[i] / total * 100
        s.append(f'<text x="{x+8:.1f}" y="{y-10:.1f}" font-size="12" font-weight="bold" '
                 f'fill="#C00000">{pctc:.0f}%</text>')

    s.append('</svg>')
    return "\n".join(s)


# ============================================================
# GAMBAR 3 - BEFORE / AFTER
# ============================================================
def build_before_after():
    W, H = 900, 540
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    s.append('<defs><marker id="bigarr" markerWidth="12" markerHeight="12" refX="6" refY="4" '
             'orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#548235"/></marker></defs>')
    s.append(f'<text x="{W/2}" y="40" text-anchor="middle" font-size="22" font-weight="bold" '
             f'fill="#1F3864">Perbandingan Kondisi Sebelum dan Sesudah VolMon</text>')

    def panel(x, w, headcolor, headtext, rows, body_fill):
        y0 = 80
        h = 380
        out = (f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" rx="10" ry="10" '
               f'fill="{body_fill}" stroke="{headcolor}" stroke-width="2"/>')
        out += (f'<path d="M{x},{y0+34} L{x},{y0+10} Q{x},{y0} {x+10},{y0} '
                f'L{x+w-10},{y0} Q{x+w},{y0} {x+w},{y0+10} L{x+w},{y0+34} Z" fill="{headcolor}"/>')
        out += (f'<text x="{x+w/2}" y="{y0+24}" text-anchor="middle" font-size="17" '
                f'font-weight="bold" fill="#FFFFFF">{esc(headtext)}</text>')
        ry = y0 + 70
        for icon, lab, val in rows:
            out += f'<text x="{x+24}" y="{ry}" font-size="16">{icon}</text>'
            out += (f'<text x="{x+50}" y="{ry-6}" font-size="13" font-weight="bold" '
                    f'fill="#333">{esc(lab)}</text>')
            out += (f'<text x="{x+50}" y="{ry+12}" font-size="13" fill="#555">{esc(val)}</text>')
            ry += 56
        return out

    left_rows = [
        ("\U0001F50D", "Metode", "Manual, remote gate satu per satu"),
        ("\u23F1", "Deteksi gangguan", "+- 3 hari"),
        ("\U0001F4C5", "Waktu pantau", "Senin & Jumat saja"),
        ("\U0001F4AA", "Beban tim", "+- 73 jam/orang/minggu"),
        ("\u26A0", "Sifat monitoring", "Reaktif"),
    ]
    right_rows = [
        ("\U0001F5A5", "Metode", "Otomatis & terpusat (dashboard)"),
        ("\u26A1", "Deteksi gangguan", "+- 5 menit (early warning)"),
        ("\U0001F504", "Waktu pantau", "24/7 realtime"),
        ("\u2705", "Beban tim", "Berkurang minimal 90%"),
        ("\U0001F680", "Sifat monitoring", "Proaktif"),
    ]

    s.append(panel(50, 350, "#C00000", "SEBELUM (Eksisting)", left_rows, "#FCEDED"))
    s.append(panel(500, 350, "#548235", "SESUDAH (VolMon)", right_rows, "#EDF7E8"))

    s.append(f'<line x1="410" y1="270" x2="495" y2="270" stroke="#548235" stroke-width="8" '
             f'marker-end="url(#bigarr)"/>')
    s.append(f'<text x="452" y="255" text-anchor="middle" font-size="12" font-weight="bold" '
             f'fill="#548235">VolMon</text>')

    s.append(f'<rect x="50" y="478" width="800" height="44" rx="8" fill="#FFF2CC" stroke="#BF8F00"/>')
    s.append(f'<text x="{W/2}" y="505" text-anchor="middle" font-size="14" font-weight="bold" '
             f'fill="#7F6000">Rata-rata Rp932.412.856 revenue tertahan (pending) per minggu '
             f'dapat diminimalkan</text>')

    s.append('</svg>')
    return "\n".join(s)


# ============================================================
# GAMBAR 4 - INFOGRAFIK DATA PENDING (NYANGKUT) RATA-RATA / MINGGU
# ============================================================
def build_pending():
    W, H = 880, 470
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    s.append(f'<text x="{W/2}" y="38" text-anchor="middle" font-size="20" font-weight="bold" '
             f'fill="#1F3864">Rata-rata Kondisi Data Pending (Nyangkut) per Minggu</text>')
    s.append(f'<text x="{W/2}" y="60" text-anchor="middle" font-size="12" fill="#666">'
             f'Sumber: hasil monitoring aplikasi VolMon (1.024 gate)</text>')

    # Kartu status gate (atas)
    def card(x, y, w, h, value, label, vcolor, fill, stroke):
        out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out += (f'<text x="{x+w/2}" y="{y+46}" text-anchor="middle" font-size="30" '
                f'font-weight="bold" fill="{vcolor}">{esc(value)}</text>')
        out += (f'<text x="{x+w/2}" y="{y+72}" text-anchor="middle" font-size="13" '
                f'fill="#333">{esc(label)}</text>')
        return out

    y0 = 82
    s.append(card(40, y0, 195, 92, "1.024", "Total Gate Aktif", "#1F3864", "#EAEFF7", "#2E74B5"))
    s.append(card(255, y0, 195, 92, "192", "Gate Bermasalah (18,75%)", "#BF8F00", "#FFF7E6", "#BF8F00"))
    s.append(card(470, y0, 175, 92, "149", "Pending", "#C55A11", "#FCEFE6", "#C55A11"))
    s.append(card(665, y0, 175, 92, "43", "Error", "#C00000", "#FCEDED", "#C00000"))

    # Panel volume transaksi & revenue tertahan (bawah)
    y1 = 200
    s.append(f'<rect x="40" y="{y1}" width="605" height="210" rx="10" fill="#F5F8FC" '
             f'stroke="#2E74B5" stroke-width="2"/>')
    s.append(f'<text x="60" y="{y1+30}" font-size="15" font-weight="bold" fill="#1F3864">'
             f'Volume Data Transaksi Tertahan</text>')

    def barrow(y, label, value, maxv, val_int, color):
        bx, bw = 60, 420
        s_ = (f'<text x="{bx}" y="{y-6}" font-size="13" fill="#333">{esc(label)}</text>')
        s_ += f'<rect x="{bx}" y="{y}" width="{bw}" height="22" rx="4" fill="#E2E8F0"/>'
        w = bw * (val_int / maxv)
        s_ += f'<rect x="{bx}" y="{y}" width="{w:.1f}" height="22" rx="4" fill="{color}"/>'
        s_ += (f'<text x="{bx+bw+10}" y="{y+17}" font-size="14" font-weight="bold" '
               f'fill="{color}">{esc(value)}</text>')
        return s_

    maxv = 337358
    s.append(barrow(y1 + 60, "Gate In Pending", "337.358", maxv, 337358, "#2E74B5"))
    s.append(barrow(y1 + 110, "Gate Out Pending", "246.185", maxv, 246185, "#5B9BD5"))
    s.append(barrow(y1 + 160, "Total Transaksi Tertahan", "583.543", maxv, 337358, "#1F3864"))

    # Kartu revenue tertahan (kanan bawah)
    s.append(f'<rect x="665" y="{y1}" width="175" height="210" rx="10" fill="#FCEDED" '
             f'stroke="#C00000" stroke-width="2"/>')
    s.append(f'<text x="752" y="{y1+34}" text-anchor="middle" font-size="13" '
             f'font-weight="bold" fill="#C00000">Revenue Tertahan</text>')
    s.append(f'<text x="752" y="{y1+44}" text-anchor="middle" font-size="11" fill="#C00000">'
             f'(pending / minggu)</text>')
    s.append(f'<text x="752" y="{y1+120}" text-anchor="middle" font-size="15" '
             f'font-weight="bold" fill="#C00000">Rp</text>')
    s.append(f'<text x="752" y="{y1+150}" text-anchor="middle" font-size="20" '
             f'font-weight="bold" fill="#C00000">932.412.856</text>')
    s.append('</svg>')
    return "\n".join(s)


# ============================================================
# GAMBAR 5 - FISHBONE / ISHIKAWA DIAGRAM (LANGKAH 2)
# ============================================================
def build_fishbone():
    W, H = 1040, 600
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    s.append('<defs><marker id="fa" markerWidth="12" markerHeight="12" refX="9" refY="4" '
             'orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#1F3864"/></marker></defs>')
    s.append(f'<text x="{W/2}" y="34" text-anchor="middle" font-size="20" font-weight="bold" '
             f'fill="#1F3864">Diagram Sebab-Akibat (Fishbone) Keterlambatan Sinkronisasi Data Gate</text>')

    spine_y = 320
    spine_x0 = 70
    spine_x1 = 770

    # Tulang punggung + kepala (akibat)
    s.append(f'<line x1="{spine_x0}" y1="{spine_y}" x2="{spine_x1}" y2="{spine_y}" '
             f'stroke="#1F3864" stroke-width="4" marker-end="url(#fa)"/>')
    hx, hy, hw, hh = 778, 262, 250, 116
    s.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="10" '
             f'fill="#1F3864" stroke="#13264a" stroke-width="2"/>')
    for i, ln in enumerate(["AKIBAT:", "Keterlambatan", "Sinkronisasi Data", "Gate ke Server Pusat"]):
        fw = "bold" if i == 0 else "normal"
        fs = 13 if i == 0 else 15
        s.append(f'<text x="{hx+hw/2}" y="{hy+26+i*24}" text-anchor="middle" font-size="{fs}" '
                 f'font-weight="{fw}" fill="#FFFFFF">{esc(ln)}</text>')

    # Definisi tulang: (label, anchor_x_on_spine, posisi atas/bawah, warna, list penyebab)
    bones = [
        ("MANUSIA", 250, "top", "#2E74B5",
         ["Monitoring bergantung", "pada petugas", "Pengecekan manual berulang"]),
        ("METODE", 470, "top", "#548235",
         ["Belum ada monitoring realtime", "Belum ada early warning", "Monitoring masih manual"]),
        ("LINGKUNGAN", 670, "top", "#BF8F00",
         ["Jumlah gate sangat banyak", "(1.024 unit)", "Tersebar di 84 stasiun"]),
        ("MESIN / ALAT", 360, "bot", "#C55A11",
         ["Belum ada dashboard terpusat", "Tidak ada notifikasi otomatis", "Aplikasi sync tak termonitor"]),
        ("MATERIAL", 580, "bot", "#7030A0",
         ["Database lokal tiap gate", "berdiri sendiri", "Data gagal terkirim"]),
    ]

    for label, ax, pos, color, causes in bones:
        if pos == "top":
            ey = 95
            lx = ax - 150
        else:
            ey = 545
            lx = ax - 150
        # garis tulang diagonal menuju spine
        s.append(f'<line x1="{lx}" y1="{ey}" x2="{ax}" y2="{spine_y}" '
                 f'stroke="{color}" stroke-width="2.5"/>')
        # kotak kategori di ujung tulang
        bw, bh = 150, 30
        bxx = lx - bw / 2
        byy = ey - bh if pos == "top" else ey
        s.append(f'<rect x="{bxx}" y="{byy}" width="{bw}" height="{bh}" rx="6" '
                 f'fill="{color}" stroke="#333" stroke-width="1"/>')
        s.append(f'<text x="{lx}" y="{byy+20}" text-anchor="middle" font-size="14" '
                 f'font-weight="bold" fill="#FFFFFF">{esc(label)}</text>')
        # teks penyebab di sepanjang tulang
        n = len(causes)
        for i, c in enumerate(causes):
            t = (i + 1) / (n + 1)
            px = lx + (ax - lx) * t
            py = ey + (spine_y - ey) * t
            tx = px + 12
            ty = (py - 4) if pos == "top" else (py + 12)
            s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3" fill="{color}"/>')
            s.append(f'<text x="{tx:.0f}" y="{ty:.0f}" font-size="11.5" fill="#333">{esc(c)}</text>')

    s.append('</svg>')
    return "\n".join(s)


outputs = {
    "gambar1_flowchart_eksisting.svg": build_flowchart(),
    "gambar2_pareto.svg": build_pareto(),
    "gambar3_before_after.svg": build_before_after(),
    "gambar4_data_pending.svg": build_pending(),
    "gambar5_fishbone.svg": build_fishbone(),
}
for fn, content in outputs.items():
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK ->", fn)
