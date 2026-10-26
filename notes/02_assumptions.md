# Modellannahmen

## Allgemein

- Der menschliche Körper wird geometrisch in mehrere vereinfachte Körperteile aufgeteilt, thermisch jedoch als ein homogenes System betrachtet.
- Der gesamte Körper besitzt zu jedem Zeitpunkt eine einheitliche Temperatur.
- Es wird kein Raumanzug berücksichtigt.
- Der Körper befindet sich im Vakuum.

## Wärmeaustausch

- Wärmeleitung und Konvektion werden vernachlässigt.
- Der Wärmeaustausch erfolgt ausschließlich durch Wärmestrahlung.
- Der Stoffwechsel wird zunächst als konstant angenommen.

## Geometrisches Körpermodell

- Der Kopf wird als Kugel modelliert.
- Der Rumpf wird als Quader modelliert.
- Arme und Beine werden als Zylinder modelliert.
- Alle Körperteile besitzen zu jedem Zeitpunkt dieselbe Temperatur.
- Die Oberflächen der einzelnen Körperteile werden zu einer gesamten abstrahlenden Körperoberfläche zusammengefasst.
- Kontaktflächen zwischen den Körperteilen werden zunächst vernachlässigt, dafür werden bei Beinen und Armen nur mit einer Stirnfläche gerechnet.
- Es wird davon ausgegangen, dass der Körper frontal zur Sonne/Erde (ohne Rotation) ausgerichtet ist. 
- Bei der seitlichen Projektionsfläche wird die Überlappung zwischen Arm und Rumpf näherungsweise berücksichtigt.

## Strahlungsberechnung

- Die Sonnenstrahlung wird über das Abstandsquadratgesetz bestimmt.
- Die Erdinfrarotstrahlung wird über das Abstandsquadratgesetz bestimmt.
- Die Albedostrahlung wird vereinfacht mit einer konstanten Albedo von 0,3 berechnet.

## Szenario: Freier interstellarer Raum

- Direkte Sonnenstrahlung wird nicht berücksichtigt.
- Der Einfluss von Planeten wird nicht berücksichtigt.
- Als äußere Strahlungsquelle wird ausschließlich die kosmische Hintergrundstrahlung betrachtet.
- Zusätzlich wird die Wärmeproduktion durch den eigenen Stoffwechsel berücksichtigt.
- Der Körper tauscht Wärme ausschließlich durch Wärmestrahlung mit seiner Umgebung aus.

## Szenario: Nur Sonne

- Die direkte Sonnenstrahlung wird berücksichtigt.
- Der Einfluss der Erde und anderer Himmelskörper wird vernachlässigt.
- Der Abstand zur Sonne kann verändert werden.

## Szenario: Nur Erde

- Die Wärmestrahlung der Erde wird berücksichtigt.
- Die direkte Sonnenstrahlung wird nicht berücksichtigt.
- Die von der Erde reflektierte Sonnenstrahlung wird nicht berücksichtigt.
- Der Abstand zur Erde kann verändert werden.
- Der Abstand zur Erde muss größer als 6471 km sein. (Erdradius+Kármán-Linie) Physikalisch gibt es keinen festen Übergang zwischen Atmosphäre und Weltraum 

## Szenario: Sonne und Erde

- Die direkte Sonnenstrahlung wird berücksichtigt.
- Die Wärmestrahlung der Erde wird berücksichtigt.
- Die von der Erde reflektierte Sonnenstrahlung wird berücksichtigt.
- Die Abstände zur Sonne und zur Erde können verändert werden.

## Rotation

- Die Rotation kann in den Umgebungsszenarien: nur Sonne, nur Erde, Sonne und Erde aktiviert werden. Im Fall interstellarer Raum hat Rotation keinen Einfluss.
- Die Rotationsgeschwindigkeit ist über die Periodendauer einer vollständigen Umdrehung veränderbar.
- Bei aktivierter Rotation verändert sich die projizierte Fläche zeitabhängig. Die gesamte abstrahlende Körperoberfläche bleibt dabei konstant.
- Die projizierte Fläche wird aus Frontal- und Seitenansicht gebildet.

## Aufgefallene Einschränkungen
- Die Armhaltung ist in der Frontal- und Seitenansicht nicht vollständig konsistent modelliert.
- In der Frontalansicht wird eine T-Pose mit seitlich ausgestreckten Armen angenommen.
- In der Seitenansicht wird dagegen eine Überlappung zwischen Arm und Rumpf berücksichtigt, die eher einer Haltung mit am Körper anliegenden Armen entspricht.
- Da die projizierte Fläche bei Rotation über A = A_front * |cos(w*t)| + A_side * |sin(w*t)| berechnet wird, wird eine unmögliche Körperhaltung von ausgestreckten Armen und nach unten gerichteten Armen angenommen. 