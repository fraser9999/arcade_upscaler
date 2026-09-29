import os
from PIL import Image
from esrgan_x4 import ESRGANUpscaler

def upscale_8x_chaining(input_path, output_path, model_path):
    """
    Skaliert ein Bild per Chaining (4x * 4x = 16x) hoch und verkleinert es auf 8x.
    """
    # Temporäre Datei für die erste Stufe (4x)
    temp_4x_path = "temp_upscale_4x.png"
    
    # 1. Bilddimensionen der Originaldatei auslesen, um die 8x-Zielgröße zu berechnen
    with Image.open(input_path) as orig_img:
        orig_width, orig_height = orig_img.size
    
    target_width = orig_width * 8
    target_height = orig_height * 8
    
    print(f"Starte 8x-Chaining für: {input_path}")
    print(f"Zielauflösung: {target_width}x{target_height}")

    # 2. Upscaler initialisieren
    upscaler = ESRGANUpscaler(model_path=model_path)

    try:
        # --- STUFE 1: Erster 4x-Durchgang ---
        print("\n[1/3] Starte ersten 4x-Durchgang...")
        upscaler.upscale_image(input_path, temp_4x_path)
        
        # --- STUFE 2: Zweiter 4x-Durchgang (Ergibt 16x) ---
        print("[2/3] Starte zweiten 4x-Durchgang (Skalierung auf 16x)...")
        # Wir nutzen das temporäre 4x-Bild als neuen Input
        upscaler.upscale_image(temp_4x_path, output_path)

        # --- STUFE 3: Downsamplen auf exakt 8x ---
        print("[3/3] Passe Auflösung von 16x auf 8x an (Lanczos-Filter)...")
        with Image.open(output_path) as final_img:
            # Hochwertiger Lanczos-Filter für optimale Downscaling-Qualität
            downscaled_img = final_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            downscaled_img.save(output_path)

        print(f"\nFertig! Das 8x-Bild wurde erfolgreich gespeichert unter: {output_path}")

    finally:
        # Temporäre Datei aufräumen, falls sie existiert
        if os.path.exists(temp_4x_path):
            os.remove(temp_4x_path)

# --- ANWENDUNGSBEISPIEL ---
#if __name__ == "__main__":
#    # Pfade an deine Dateien anpassen
#    MODEL = "RRDB_ESRGAN_x4.pth"
#    INPUT = "mein_kleines_bild.jpg"
#    OUTPUT = "mein_hochaufgeloestes_8x_bild.png"
#
#    upscale_8x_chaining(input_path=INPUT, output_path=OUTPUT, model_path=MODEL)
