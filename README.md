# thermal simulation of a human in space

Dieses Projekt untersucht das thermische Verhalten eines ungeschützten menschlichen Körpers im Weltraum.

Ziel ist es, mithilfe einer Python-Simulation verschiedene Szenarien zu vergleichen, darunter:

- freier interstellarer Raum
- Einfluss der Sonne
- Einfluss der Erde
- gemeinsamer Einfluss von Sonne und Erde
- Einfluss der Körperrotation
- Untersuchung eines thermischen Gleichgewichtes

## physical model

Der menschliche Körper wird geometrisch aus vereinfachten Grundkörpern zusammengesetzt und thermisch als ein System mit einheitlicher Temperatur betrachtet.

Die Energiebilanz berücksichtigt:
- Thermische Abstrahlung des Körpers
- Absorption der kosmischen Hintergrundstrahlung
- Direkte Sonnenstrahlung
- Infrarotstrahlung der Erde
- Von der Erde reflektierte Sonnenstrahlung (Albedo)
- Wärmeproduktion durch den Stoffwechsel

Welche Strahlungsquellen berücksichtigt werden, hängt vom gewählten Szenario ab.
Wärmeleitung und Konvektion werden vernachlässigt.

## numerical model

Die zeitliche Entwicklung der Körpertemperatur wird mit dem expliziten Euler-Verfahren berechnet.
- Zeitschritt: 1 Sekunde
- Simulationsdauer: 6 Stunden
Zusätzlich werden thermische Gleichgewichtsabstände numerisch bestimmt. Für das kombinierte Sonne-Erde-Szenario wird eine Gleichgewichtskurve berechnet.
Die Ergebnisse werden grafisch dargestellt.

## Model limitations

Die Simulation verwendet vereinfachte Annahmen und bildet nicht sämtliche physiologischen und physikalischen Prozesse eines menschlichen Körpers im Weltraum ab.
Insbesondere werden die Auswirkungen des Vakuums auf den menschlichen Organismus nicht simuliert. Außerdem ist die verwendete Körpergeometrie hinsichtlich der Armhaltung in Frontal- und Seitenansicht nicht vollständig konsistent.
Die Ergebnisse sind daher als Resultate eines vereinfachten thermischen Modells zu verstehen.

## dokumentation

Weitere Informationen befinden sich in den Dokumentationsdateien des Projekts:
- Projektplan
- Modellannahmen
- Modellparameter