import PIL.Image
#import xbrz

def process(image_path, block_size=20, output_scale=4):
    # 1. Bild laden
    img = PIL.Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # 2. Auf die ECHTE Pixel-Auflösung runterrechnen (z.B. von 400x400 auf 20x20)
    # Wichtig: Box-Resampling stellt sicher, dass der Durchschnitt des Blocks genommen wird
    logical_width = width // block_size
    logical_height = height // block_size
    small_img = img.resize((logical_width, logical_height), PIL.Image.Resampling.BOX)
    
    # 3. Jetzt mit xBRZ intelligent hochauflösend machen (z.B. 4x = 80x80 mit runden Kanten)
    # Das transformiert den harten Block-Look in einen glatten Vektor-Look
    #hd_img = xbrz.scale(small_img, output_scale)
    
    return small_img

# Ergebnis speichern oder in Python Arcade nutzen
# hd_sprite = process("mein_riesen_pixel_sprite.png", block_size=20)
# hd_sprite.save("sprite_glatt.png")
