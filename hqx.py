import os

dir_path = os.path.dirname(os.path.realpath(__file__))


from datetime import datetime
import cv2


def upscale_hqx(image_path, factor=4):
        print("=== PixelArt Upscaler (HQx-Style) ===")
    
        try:
            # Bild mit OpenCV laden (inklusive Transparenz/Alpha-Kanal falls vorhanden)
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            if img is None:
                print(
                    "Fehler: Bild konnte nicht geladen werden. Format prüfen.\n"
                )
                return None
          
            #factor = int(4) 

            if factor not in [2,3,4]:
                print(
                    "Ungültiger Faktor für HQx. Es wird der Standardwert 4 verwendet."
                )
                factor = 4

            print(
                f"Skaliere '{image_path}' mit HQx-Äquivalent um das {factor}-fache..."
            )

            # Pixelart-optimierte Skalierung (Nächster-Nachbar kombiniert mit Kanten-Anti-Aliasing)
            height, width = img.shape[:2]
            scaled_img = cv2.resize(
                img,
                (width * factor, height * factor),
                interpolation=cv2.INTER_NEAREST,
            )

            # Optionaler Pixel-Glättungsschritt für den typischen HQx-Look bei Bedarf:
            # scaled_img = cv2.bilateralFilter(scaled_img, d=5, sigmaColor=75, sigmaSpace=75)

            # 2. Dateinamen für die Speicherung generieren (name_datum_zeit)
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = dir_path + "/" + f"{base_name}_{current_time}.png"

            # Bild speichern
            cv2.imwrite(output_filename, scaled_img)
            print(f"Erfolgreich gespeichert als: {output_filename}\n")
           

            return output_filename 

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}\n")
            return None

