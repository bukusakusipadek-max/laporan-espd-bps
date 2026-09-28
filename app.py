import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import base64
import pandas as pd

st.set_page_config(page_title="Aplikasi Laporan Perjalanan Dinas BPS Kabupaten Tanjung Jabung Timur", layout="wide")

# --- CUSTOM CSS UNTUK NUANSA WARNA PROFESIONAL BPS (ORANYE & EMAS SE) ---
st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #f39c12;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1rem;
        }
        div.stButton > button:first-child:hover {
            background-color: #d68910;
            color: white;
        }
        div.stDownloadButton > button:first-child {
            background-color: #e67e22;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            border: none;
        }
        div.stDownloadButton > button:first-child:hover {
            background-color: #ca6f1e;
            color: white;
        }
        .stInfo {
            background-color: #fef5e7;
            border-color: #f39c12;
            color: #784212;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📋 Aplikasi Generator Laporan Perjalanan Dinas (Multi-Survei BPS)")
st.write("Gunakan aplikasi ini untuk mencatat perjalanan dinas berbagai kegiatan/survei BPS secara fleksibel dan rapi.")

with st.form("form_spd_dinamis"):
    st.subheader("1. Identitas Pelaksana Perjalanan Dinas")
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap & Gelar", "Cth. Tohap Marihot Simatupang, A.Md.Kom")
        nip = st.text_input("NIP", "Cth. 198509232024211003")
    with col2:
        jabatan = st.text_input("Jabatan", "Cth. Pranata Komputer Terampil / Pegawai PPPK BPS")
        lokasi_tanggal_ttd = st.text_input("Kota & Tanggal TTD Laporan", "Cth. Muara Sabak, 27 Juli 2026")

    st.subheader("2. Detail Jenis Kegiatan / Survei & Tempat")
    col3, col4 = st.columns(2)
    with col3:
        jenis_kegiatan = st.text_input(
            "Jenis Kegiatan / Nama Survei", 
            "Sensus Ekonomi 2026 (atau Susenas Februari 2026 / Sakernas)"
        )
        tujuan_tugas = st.text_input("Tujuan Tugas / Lokasi Tujuan", "Cth. Nipah Panjang")
    with col4:
        tanggal_pelaksanaan = st.text_input("Tanggal Pelaksanaan", "Cth. 27 Juli 2026")
        gdrive_link = st.text_input(
            "Link Folder Google Drive (Arsip Dokumentasi)", 
            "Cth. https://drive.google.com/drive/folders/1xq9hogofGd15OuW7IWkGxULmuRujSZh?usp=sharing"
        )

    pejabat_instansi_multi = st.text_area(
        "Daftar Instansi, Pejabat & Stempel yang Dikunjungi", 
        "1. Kantor POS Nipah Panjang: Edi Trisno Prasetyo / BM POS Indonesia\n"
        "2. Pondok Pesantren Daaru Ikhlas: Pimpinan / Pengelola Ponpes\n"
        "3. Puskesmas Nipah Panjang: Pihak Pengelola / Kepala Puskesmas",
        height=100
    )

    nama_tugas = st.text_area(
        "Nama/Judul Tugas Utama", 
        "Cth. Task Force Pendataan Lengkap dan Cawi dan Pendampingan Penyelesaian Anomali di Lapangan"
    )

    st.subheader("3. Rincian Kegiatan (Tabel Interaktif)")
    st.info("💡 Anda bisa langsung mengetik, menambah baris, atau mengubah isi Waktu, Kegiatan, dan Solusi pada tabel di bawah ini.")
    
    data_default = pd.DataFrame([
        {"Waktu": "08.00 - 10.00", "Uraian Kegiatan": "Berangkat dari Kantor ke Lokasi", "Solusi": "-"},
        {"Waktu": "10.00 - 11.00", "Uraian Kegiatan": "Mencari Data Responden yang tidak ditemukan", "Solusi": "Mencari Informasi ke ketua RT Terlebih dahulu"}
    ])
    
    tabel_kegiatan = st.data_editor(data_default, num_rows="dynamic", use_container_width=True)

    st.subheader("4. Galeri Foto Dokumentasi")
    st.write("Unggah foto dokumentasi kegiatan harian: Minimal 1 Foto, Ambil dari Galeri Devices Anda, Usahakan Foto Ada TimeMark dan Geo-Tag")
    uploaded_files = st.file_uploader("Pilih Foto Dokumentasi", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    submitted = st.form_submit_button("🚀 Generate Laporan Perjalanan Dinas")

if submitted:
    st.success("Laporan Perjalanan Dinas berhasil dibuat!")
    
    # --- QR CODE BERSIH & FOKUS KE LINK GOOGLE DRIVE (SANGAT PEKA DI-SCAN) ---
    qr_data = gdrive_link.strip()
    if not qr_data.startswith("http"):
        qr_data = "https://drive.google.com"
    
    # Perbesar box_size dan border agar QR code lebih renggang dan mudah dipindai kamera HP
    qr = qrcode.QRCode(box_size=5, border=3)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img_qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    foto_html_list = []
    if uploaded_files:
        for file in uploaded_files:
            b_data = file.getvalue()
            b64_img = base64.b64encode(b_data).decode("utf-8")
            foto_html_list.append(b64_img)

    instansi_items_html = ""
    for baris in pejabat_instansi_multi.split("\n"):
        baris_bersih = baris.strip()
        if baris_bersih:
            instansi_items_html += f'<div style="margin-bottom: 4px;">{baris_bersih}</div>'

    kegiatan_rows_html = ""
    for index, row in tabel_kegiatan.iterrows():
        waktu = str(row["Waktu"]).strip()
        uraian = str(row["Uraian Kegiatan"]).strip()
        solusi = str(row["Solusi"]).strip()
        
        if waktu or uraian or solusi:
            kegiatan_rows_html += f"""
            <tr>
                <td style="border: 1px solid black; padding: 6px 8px; width: 22%; text-align: center; vertical-align: top; font-size: 10pt;">{waktu}</td>
                <td style="border: 1px solid black; padding: 6px 8px; width: 39%; vertical-align: top; font-size: 10pt;">{uraian}</td>
                <td style="border: 1px solid black; padding: 6px 8px; width: 39%; vertical-align: top; font-size: 10pt;">{solusi}</td>
            </tr>
            """

    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Laporan Perjalanan Dinas - {nama}</title>
        <style>
            body {{ background: #eee; font-family: 'Times New Roman', Times, serif; color: black; margin: 0; padding: 20px; }}
            .page {{
                width: 210mm;
                min-height: 297mm;
                padding: 15mm;
                margin: auto;
                background: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
                box-sizing: border-box;
                font-size: 10.5pt;
            }}
            .header-title {{
                text-align: center;
                font-weight: bold;
                font-size: 13pt;
                margin-bottom: 20px;
                text-decoration: underline;
                line-height: 1.4;
            }}
            table.data-table, table.kegiatan-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 15px;
            }}
            table.data-table td, table.kegiatan-table td, table.kegiatan-table th {{
                border: 1px solid black;
                padding: 6px 8px;
                vertical-align: top;
            }}
            table.kegiatan-table th {{
                background-color: #f39c12;
                color: white;
                text-align: center;
                font-weight: bold;
                font-size: 10.5pt;
            }}
            .gallery-grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
                margin-top: 10px;
            }}
            .gallery-item {{
                width: 45%;
                border: 1px solid #777;
                padding: 5px;
                text-align: center;
                background: #fafafa;
                box-sizing: border-box;
                margin-bottom: 10px;
            }}
            .gallery-item img {{
                width: 100%;
                height: auto;
                object-fit: contain;
            }}
            @media print {{
                body {{ background: white; padding: 0; }}
                .page {{ box-shadow: none; margin: 0; width: 100%; padding: 10mm; }}
                .no-print {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="header-title">
                LAPORAN PERJALANAN DINAS<br>
                <span style="font-size: 11pt; font-weight: normal;">({jenis_kegiatan})</span>
            </div>
            
            <p><b>Yang melakukan perjalanan dinas:</b></p>
            <table class="data-table">
                <tr><td style="width: 30%;"><b>Nama</b></td><td>{nama}</td></tr>
                <tr><td><b>NIP</b></td><td>{nip}</td></tr>
                <tr><td><b>Jabatan</b></td><td>{jabatan}</td></tr>
                <tr><td><b>Instansi & Pemberi Stempel</b></td><td>{instansi_items_html}</td></tr>
                <tr><td><b>Tujuan Dinas</b></td><td><b>{tujuan_tugas}</b></td></tr>
                <tr><td><b>Nama Tugas</b></td><td>{nama_tugas}</td></tr>
                <tr><td><b>Tanggal Pelaksanaan</b></td><td>{tanggal_pelaksanaan}</td></tr>
                <tr><td><b>Arsip Google Drive</b></td><td><a href="{gdrive_link}" target="_blank" style="color: #d68910; word-break: break-all;">{gdrive_link}</a></td></tr>
            </table>

            <p><b>Hasil / Rincian Kegiatan Perjalanan Dinas:</b></p>
            <table class="kegiatan-table">
                <thead>
                    <tr>
                        <th>Waktu</th>
                        <th>Uraian Kegiatan</th>
                        <th>Solusi</th>
                    </tr>
                </thead>
                <tbody>
                    {kegiatan_rows_html}
                </tbody>
            </table>

            <p style="text-align: center; font-weight: bold; margin-top: 10px; text-decoration: underline;">DOKUMENTASI KEGIATAN</p>
            <div class="gallery-grid">
    """

    if foto_html_list:
        for idx, f_base64 in enumerate(foto_html_list):
            html_report += f"""
                <div class="gallery-item">
                    <img src="data:image/jpeg;base64,{f_base64}"/>
                    <p style="font-size: 9pt; margin: 4px 0 0 0;">Dokumentasi {idx+1} ({tanggal_pelaksanaan})</p>
                </div>
            """
    else:
        html_report += '<p style="color: gray; font-style: italic; text-align: center;">Tidak ada foto yang diunggah.</p>'

    html_report += f"""
            </div>

            <table style="width: 100%; border-collapse: collapse; margin-top: 20px; border: none;">
                <tr>
                    <td style="width: 50%; border: none;"></td>
                    <td style="width: 50%; border: 1px solid black; text-align: center; padding: 8px; background: #fff;">
                        <div style="font-size: 10pt; margin-bottom: 2px;">{lokasi_tanggal_ttd}</div>
                        <div style="font-size: 10pt; font-weight: bold; margin-bottom: 5px;">Yang membuat Laporan,</div>
                        
                        <div style="height: 50px;"></div>
                        
                        <u><b>{nama}</b></u><br>
                        <span style="font-size: 9pt;">NIP. {nip}</span>
                        
                        <div style="margin-top: 8px; border-top: 1px dashed #999; padding-top: 6px; display: flex; align-items: center; justify-content: center; gap: 10px;">
                            <img src="data:image/png;base64,{qr_base64}" style="width: 75px; height: 75px;" />
                            <div style="text-align: left; font-size: 7.5pt; color: #333; line-height: 1.2;">
                                <b>TTE RESMI BPS</b><br>
                                Kegiatan: {jenis_kegiatan}<br>
                                Petugas: {nama}<br>
                                <i>[ Scan untuk Buka Arsip ]</i>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """

    st.markdown("---")
    st.subheader("📥 Unduh & Cetak Laporan Resmi")
    st.write("Klik tombol di bawah ini untuk mengunduh laporan siap cetak:")
    
    st.download_button(
        label="📥 Download File Laporan Resmi",
        data=html_report,
        file_name=f"Laporan_SPD_{jenis_kegiatan.replace(' ', '_')}_{nama.replace(' ', '_')}.html",
        mime="text/html"
    )