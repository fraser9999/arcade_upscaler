from PIL import Image, ImageFilter


def smooth_edges_gaussian(image_path, radius=1.0):
        """
        Macht das gesamte Bild und seine Kanten durch einen 
        Gaußschen Weichzeichner gleichmäßig runder und softer.
        
        :param image_path: Pfad zum hochskalierten Eingangsbild
        :param output_path: Pfad, unter dem das Ergebnis gespeichert wird
        :param radius: Stärke des Effekts (Standard: 1.0. Höhere Werte = runder/unschärfer)
        """
        with Image.open(image_path) as img:
            smoothed = img.filter(ImageFilter.GaussianBlur(radius=radius))
            #smoothed.save(output_path)

            return smoothed


def smooth_edges_median(image_path, size=3):
        """
        Nutzt einen Median-Filter. Dieser eignet sich besonders gut, um Flächen
        glatt und Kanten runder zu machen, ohne dass das Bild komplett "verschwimmt".
        Ideal für einen sauberen, leicht comic-artigen Look.
        
        :param image_path: Pfad zum hochskalierten Eingangsbild
        :param output_path: Pfad, unter dem das Ergebnis gespeichert wird
        :param size: Filtergröße (Muss eine ungerade Zahl sein, z.B. 3 oder 5)
        """
        with Image.open(image_path) as img:
            smoothed = img.filter(ImageFilter.MedianFilter(size=size))
            #smoothed.save(output_path)

            return smoothed 
