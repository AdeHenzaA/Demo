import os
import time 
import pytest
import allure
import cv2  # Perlu install: pip opencv-python
import numpy as np
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def optimasi_gambar(screenshot_bytes):
    """Mengompres gambar agar ukurannya kecil dan diproses AI sangat cepat"""
    try:
        # Ubah bytes menjadi array gambar
        nparr = np.frombuffer(screenshot_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Perkecil resolusi ke lebar 800px (menjaga aspek rasio)
        tinggi, lebar = img.shape[:2]
        lebar_baru = 800
        tinggi_baru = int((lebar_baru / lebar) * tinggi)
        img_resized = cv2.resize(img, (lebar_baru, tinggi_baru), interpolation=cv2.INTER_AREA)
        
        # Kompres kualitas JPEG ke 60%
        _, buffer = cv2.imencode('.jpg', img_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 5])
        return buffer.tobytes(), "image/jpeg"
    except Exception:
        # Jika gagal kompres, kembalikan data asli apa adanya
        return screenshot_bytes, "image/png"

def terjemahkan_error_with_screenshot(error_log, screenshot_bytes):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gagal analisis: GEMINI_API_KEY tidak ditemukan."
        
    # 1. OPTIMASI LOG: Hanya ambil 30 baris terakhir (bagian paling krusial)
    log_lines = error_log.splitlines()
    pangkas_log = "\n".join(log_lines[-30:])
    
    # 2. OPTIMASI GAMBAR: Perkecil size gambar agar upload kilat
    gambar_kompres, mime_tipe = optimasi_gambar(screenshot_bytes)
    
    gambar = types.Part.from_bytes(
        data=gambar_kompres,
        mime_type=mime_tipe,
    )
    
    # 3. OPTIMASI PROMPT: Minta jawaban singkat, padat, to-the-point
    prompt = f"""
    Kamu QA Automation ahli. Analisis log & screenshot ini. 
    Berikan jawaban singkat, padat, dan langsung ke poin penting saja dalam Bahasa Indonesia.
    Format respons:
    - Penyebab: (1-2 kalimat saja)
    - Solusi Kode: (langsung berikan contoh perbaikan kodenya)
    
    LOG ERROR:
    {pangkas_log}
    """
    
    # --- IMPLEMENTASI RETRY OTOMATIS (MAKSIMAL 3 KALI) ---
    maks_retry = 3
    jeda = 2  # Jeda awal dalam detik
    
    for percobaan in range(1, maks_retry + 1):
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[prompt, gambar]
            )
            return response.text  # Jika sukses, langsung kembalikan hasil teks AI
            
        except Exception as e:
            # Cek jika error disebabkan karena server sibuk (503 / UNAVAILABLE)
            if "503" in str(e) or "UNAVAILABLE" in str(e).upper():
                if percobaan < maks_retry:
                    print(f"\n[Gemini AI] Server sibuk. Mencoba ulang dalam {jeda} detik... (Percobaan {percobaan}/{maks_retry})")
                    time.sleep(jeda)
                    jeda *= 2  # Jeda bertambah lama pada percobaan berikutnya (2s -> 4s)
                    continue
            
            # Jika bukan error 503, atau sudah mencapai batas 3x retry, kembalikan pesan error akhir
            return f"Gagal memanggil Gemini AI setelah {percobaan} percobaan: {str(e)}"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        error_log = report.longreprtext
        screenshot_data = b""
        
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_data = page.screenshot() 
            
        if screenshot_data:
             # --- TAMBAHKAN LOG UKURAN GAMBAR DI SINI ---
            ukuran_asli = len(screenshot_data) / 1024
            gambar_kompres, _ = optimasi_gambar(screenshot_data)
            ukuran_kompres = len(gambar_kompres) / 1024
            
            print("\n=== MONITORING UKURAN GAMBAR ===")
            print(f"Ukuran Screenshot Asli   : {ukuran_asli:.2f} KB")
            print(f"Ukuran Setelah Kompres 5%: {ukuran_kompres:.2f} KB")
            print("================================\n")
            
            print("\n=== HASIL ANALISIS REKOMENDASI AI ===")
            analisis_ai = terjemahkan_error_with_screenshot(error_log, screenshot_data)
            print(analisis_ai)
            print("=======================================\n")

            with open("ai_output.txt", "w", encoding="utf-8") as f:
                f.write("=== HASIL ANALISIS REKOMENDASI AI ===\n")
                f.write(analisis_ai)
                f.write("\n=======================================\n")
            
            allure.attach(screenshot_data, name="Screenshot Kegagalan", attachment_type=allure.attachment_type.PNG)
            allure.attach(analisis_ai, name="Analisis & Solusi Gemini AI", attachment_type=allure.attachment_type.TEXT)
