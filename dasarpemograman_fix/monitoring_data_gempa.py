from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from bs4 import BeautifulSoup
import requests
import folium
import uvicorn

# Deklarasikan framework fastapi dengan variabel app
app = FastAPI()

# Membuat halaman dengan Metode GET
@app.get("/")
def read_main():
    # Mengambil data XML dari API BMKG
    response = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.xml")

    # Create Map dan default tampilannya dengan Folium
    map_gempa = folium.Map(location=[-2.5, 118.0], zoom_start=4)

    # Menggunakan 'lxml-xml' untuk parsing XML
    soup = BeautifulSoup(response.content, 'lxml-xml') 

    # Mendapatkan dan mendeklarasikan seluruh data dengan key 'gempa' dalam API BMKG ke variabel 'infogempa'
    infogempa = soup.find_all("gempa")

    # Mengambil data gempa dari API BMKG yang ada di variabel 'infogempa'
    for a in infogempa:
        tanggal = a.find("Tanggal").text if a.find("Tanggal") else "Tidak tersedia"
        jam = a.find("Jam").text if a.find("Jam") else "Tidak tersedia"
        koordinat = a.find("point").find("coordinates").text if a.find("point") and a.find("point").find("coordinates") else "Tidak tersedia"
        lintang, bujur = koordinat.split(",") if koordinat != "Tidak tersedia" else ("Tidak tersedia", "Tidak tersedia")
        magnitude = a.find("Magnitude").text if a.find("Magnitude") else "Tidak tersedia"
        kedalaman = a.find("Kedalaman").text if a.find("Kedalaman") else "Tidak tersedia"
        wilayah = a.find("Wilayah").text if a.find("Wilayah") else "Tidak tersedia"
        dirasakan = a.find("Dirasakan").text if a.find("Dirasakan") else "Tidak tersedia"

    # Membangun HTML secara manual
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Gempa Terkini</title>
    <style>
        /* Reset dan dasar */
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #74b9ff, #0984e3);
            color: #2d3436;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}

        /* Container utama */
        .container {{
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            width: 90%;
            max-width: 1000px;
        }}

        /* Header */
        .header {{
            background: #0984e3;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }}

        /* Konten */
        .content {{
            display: flex;
            flex-wrap: wrap;
        }}

        /* Peta */
        .map-container {{
            flex: 1 1 50%;
            min-width: 300px;
            height: 400px;
            border-right: 1px solid #dfe6e9;
        }}

        .map-container iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}

        /* Informasi Gempa */
        .info-container {{
            flex: 1 1 50%;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .info-container ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .info-container li {{
            margin: 10px 0;
            font-size: 16px;
        }}

        .info-container li strong {{
            color: #0984e3;
        }}

        /* Tombol */
        .button-container {{
            text-align: center;
            margin-top: 20px;
        }}

        .button-container a {{
            display: block; /* Membuat tombol menjadi block element, agar lebar 100% */
            width: 100%; /* Lebar tombol mengikuti container */
            text-decoration: none;
            color: white;
            background: #0984e3;
            padding: 15px 0; /* Padding vertikal untuk memberi ruang dalam tombol */
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}

        .button-container a:hover {{
            background: #74b9ff;
            color: #2d3436;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            Data Gempa Terkini
        </div>
        <div class="content">
            <!-- Peta -->
            <div class="map-container">
                <iframe 
                    src="http://127.0.0.1:8000/peta" 
                    frameborder="0">
                </iframe>
            </div>
            <!-- Informasi Gempa -->
            <div class="info-container">
                <ul>
                    <li><strong>Tanggal:</strong> {tanggal}</li>
                    <li><strong>Jam:</strong> {jam}</li>
                    <li><strong>Koordinat:</strong> {koordinat}</li>
                    <li><strong>Magnitude:</strong> {magnitude}</li>
                    <li><strong>Kedalaman:</strong> {kedalaman}</li>
                    <li><strong>Wilayah:</strong> {wilayah}</li>
                    <li><strong>Dirasakan:</strong> {dirasakan}</li>
                </ul>
                <!-- Tombol untuk membuka peta penuh -->
                <div class="button-container">
                    <a href="http://127.0.0.1:8000/peta" target="_blank">Lihat Peta Lengkap</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>

"""

    # Membuat popup info di titik gempa
    popup_content = f"""
                <b>Tanggal:</b> {tanggal}<br>
                <b>Jam:</b> {jam}<br>
                <b>Koordinat:</b> {float(lintang)}, {float(bujur)}<br>
                <b>Magnitude:</b> {magnitude}<br>
                <b>Kedalaman:</b> {kedalaman}<br>
                <b>Wilayah:</b> {wilayah}
                """
    popup = folium.Popup(popup_content, max_width=200)

    # Merender titik gempa dengan ikon dan popup ke peta
    folium.Marker(
                    location=[float(lintang), float(bujur)],
                    popup=popup,
                    icon=folium.Icon(color='red')
                ).add_to(map_gempa)

    # Menyimpan peta ke file HTML
    map_gempa.save("peta_gempa.html")

    # Merender html_content ke web dangan HTMLResponse
    return HTMLResponse(content=html_content)

# Membuat halaman untuk merender peta dengan Metode GET
@app.get("/peta")
def read_root():
    # Merender file peta_gempa.html yang sudah tercreate dengan FileResponse
    return FileResponse("peta_gempa.html")

# Membuat runner server, agar hanya dengan mengklik tombol run
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)