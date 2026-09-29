def find_frequent_distances(data, tolerance=10):
    """
    Gruppiert eine flache Liste in (x, y) Paare und findet die häufigsten 
    Wertepaare unter Berücksichtigung einer kleinen Abweichung (Tolerance).
    """
    # 1. Flache Liste in (x, y) Tupel umwandeln
    pairs = list(zip(data[::2], data[1::2]))
    clusters = []
    
    # 2. Wertepaare basierend auf der Toleranz gruppieren
    for x, y in pairs:
        found = False
        for cluster in clusters:
            # Berechne den aktuellen Mittelwert des Clusters
            avg_x = sum(p[0] for p in cluster) / len(cluster)
            avg_y = sum(p[1] for p in cluster) / len(cluster)
            
            # Prüfen, ob der neue Punkt innerhalb der erlaubten Abweichung liegt
            if abs(x - avg_x) <= tolerance and abs(y - avg_y) <= tolerance:
                cluster.append((x, y))
                found = True
                break
        
        if not found:
            clusters.append([(x, y)])
            
    # 3. Ergebnisse aufbereiten und nach Häufigkeit sortieren
    results = []
    for cluster in clusters:
        avg_x = sum(p[0] for p in cluster) / len(cluster)
        avg_y = sum(p[1] for p in cluster) / len(cluster)
        results.append({
            "durchschnitt_xy": (round(avg_x, 1), round(avg_y, 1)),
            "anzahl": len(cluster),
            "original_werte": cluster
        })
        
    # Nach Häufigkeit (anzahl) absteigend sortieren
    results.sort(key=lambda item: item["anzahl"], reverse=True)
    return results



# Ihre Beispieldaten
#daten = [1109, 1121, 198, 180, 18, 18, 144, 180, 18, 18, 90, 234, 288, 252, 18, 18, 36, 18, 54, 90, 18, 18, 18, 36, 90, 90, #18, 18, 18, 18, 36, 18, 18, 18, 180, 54]


def get_distance(daten,top,tolerance):

    # Ausführung mit einer maximalen Abweichung von 20 Einheiten
    ergebnisse = find_frequent_distances(daten, tolerance=2)

    # Top 3 häufigste Werte anzeigen
    for i, erg in enumerate(ergebnisse[:top], 1):
        print(f"Platz {i}: {erg['durchschnitt_xy']} -> {erg['anzahl']}x vorkommend")

    if erg['durchschnitt_xy'][0] > 1 and erg['durchschnitt_xy'][0] < 2:
        return 2
    else:
        return int(erg['durchschnitt_xy'][0])


