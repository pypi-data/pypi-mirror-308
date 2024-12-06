# Face Recognition Login System

Dieses Python-Paket ermöglicht eine Gesichtserkennung mit integrierter Login-Funktion und einer einfachen Verwaltung der gespeicherten Gesichter.

## Inhaltsverzeichnis
- [Features](#features)
- [Installation](#installation)
- [Installation von dlib (Problemlösungen)](#dlib-installations-schwierigkeiten-fix)
- [Verwendung](#verwendung)
- [Module](#module)
  - [Module: recognition.py](#module-recognitionpy)
  - [Module: faces.py](#module-facespy)
- [Beispiel](#beispiel)
- [Abhängigkeiten](#abhängigkeiten)
- [To-Do](#to-do)

## Features

- Gesichtserkennung zur Authentifizierung
- Verwaltung von Gesichtern (Hinzufügen, Löschen, Anzeigen)
- Möglichkeit zur Einstellung eines Vertrauensschwellenwerts für den Login

## Installation

1. Klone dieses Repository:
   ```bash
   git clone https://github.com/baulum/FaceGuard.git
   cd FaceGuard
   ```

2. Installiere die benötigten Pakete:
   ```bash
   pip install -r requirements.txt
   ```

## dlib-Installations-Schwierigkeiten-Fix

Die Installation von `dlib` kann problematisch sein, vor allem unter Windows. Hier eine Anleitung zur Lösung von Installationsproblemen:

1. **Überprüfe deine Python-Version**:
   - Öffne CMD und gib ein:
     ```bash
     python --version
     ```
     - Beispielausgabe: `Python 3.11.3`

2. **Lade die passende Wheel-Datei herunter**:
   - Besuche [dlib auf GitHub](https://github.com/Murtaza-Saeed/dlib) und lade die Wheel-Datei für deine Python-Version herunter.
   - Für Python 3.11.x wäre dies z.B. `dlib-19.24.1-cp311-cp311-win_amd64.whl`.
   - Für Python 3.10.x wäre es `dlib-19.22.99-cp310-cp310-win_amd64.whl`.

3. **Installiere die Wheel-Datei und weitere Abhängigkeiten**:
   - Installiere die heruntergeladene Datei mit folgendem Befehl:
     ```bash
     pip install <datei_name_der_wheel_datei>
     ```
   - Installiere `cmake` und `face_recognition`:
     ```bash
     pip install cmake
     pip install face_recognition
     ```

## Verwendung

1. **Hinzufügen und Verwalten von Gesichtern**:
   - Verwende `FaceManager` aus `faces.py`, um neue Gesichter hinzuzufügen oder zu löschen. Die Gesichter werden im Ordner `faces` gespeichert und für die Gesichtserkennung verwendet.

2. **Login mit Gesichtserkennung**:
   - Starte die Gesichtserkennung und den Login-Prozess über `FaceRecognition` in `recognition.py`.

## Module

### Module: `recognition.py`

Dieses Modul enthält die Hauptklasse `FaceRecognition`, die für die Gesichtserkennung und den Login verwendet wird.

#### `FaceRecognition`

- **Attribute**:
  - `face_locations`: Speicherorte der Gesichter im aktuellen Bild.
  - `face_encodings`: Gesichtseigenschaften (Encodings) der erkannten Gesichter im aktuellen Bild.
  - `face_names`: Namen der erkannten Gesichter.
  - `known_face_encodings`: Encodings der registrierten Gesichter.
  - `known_face_names`: Namen der registrierten Gesichter.
  
- **Methoden**:
  - `__init__(self, faces_dir="faces")`: Initialisiert die Klasse und lädt die gespeicherten Gesichter.
  - `encode_faces(self)`: Liest Gesichter aus dem angegebenen Verzeichnis (`faces_dir`) und berechnet deren Encodings.
  - `run_recognition(self)`: Startet die Gesichtserkennung über die Kamera.
  - `login(self, required_confidence=85.0)`: Führt die Gesichtserkennung für den Login durch. Gibt `True` und den Namen des Benutzers zurück, wenn das Gesicht mit ausreichender Vertrauenswürdigkeit erkannt wird.

#### Beispiel für die Gesichtserkennung und Login

```python
from FaceGuard.recognition import FaceRecognition

fr = FaceRecognition(faces_dir="faces")
login_success, user_name = fr.login(required_confidence=85.0)
if login_success:
    print(f"Willkommen, {user_name}!")
else:
    print("Login fehlgeschlagen.")
```

### Module: `faces.py`

Das Modul `faces.py` bietet Funktionen zum Verwalten der Gesichter, die für die Gesichtserkennung registriert sind.

#### `FaceManager`

- **Methoden**:
  - `add_face(self, name)`: Fügt ein neues Gesicht zur Datenbank hinzu, indem es ein Bild über die Kamera aufnimmt und im `faces`-Ordner speichert. Das Gesicht wird unter dem angegebenen Namen gespeichert.
  - `delete_face(self, name)`: Löscht das Gesicht mit dem angegebenen Namen aus der Datenbank.
  - `list_faces(self)`: Gibt eine Liste aller im Verzeichnis `faces` gespeicherten Gesichter zurück.

#### Beispiel zur Verwaltung der Gesichter

```python
from FaceGuard.faces import FaceManager

face_manager = FaceManager(faces_dir="faces")

# Neues Gesicht hinzufügen
name = input("Namen für das neue Gesicht eingeben: ")
face_manager.add_face(name)

# Gesicht löschen
name = input("Namen für zu löschendes Gesicht eingeben: ")
face_manager.delete_face(name)

# Liste der vorhandenen Gesichter anzeigen
print("Vorhandene Gesichter:", face_manager.list_faces())
```

## Beispiel

Hier ist ein vollständiges Beispielprogramm, das das Hinzufügen und Löschen von Gesichtern sowie den Login-Prozess kombiniert.

```python
from FaceGuard.recognition import FaceRecognition
from FaceGuard.faces import FaceManager

def main():
    # Gesicht-Manager initialisieren
    face_manager = FaceManager(faces_dir="faces")
    
    # Vorhandene Gesichter anzeigen
    print("Vorhandene Gesichter:", face_manager.list_faces())
    
    # Neues Gesicht hinzufügen
    new_name = input("Namen für neues Gesicht eingeben: ")
    if face_manager.add_face(new_name):
        print(f"{new_name} erfolgreich hinzugefügt.")
    
    # Gesicht löschen
    del_name = input("Namen für zu löschendes Gesicht eingeben: ")
    if face_manager.delete_face(del_name):
        print(f"{del_name} erfolgreich gelöscht.")
    
    # Gesichtserkennung und Login
    fr = FaceRecognition(faces_dir="faces")
    login_success, user_name = fr.login(required_confidence=85.0)
    if login_success:
        print(f"Willkommen, {user_name}!")
    else:
        print("Login fehlgeschlagen.")

if __name__ == "__main__":
    main()
```

## Abhängigkeiten

- `face_recognition`: Für Gesichtserkennung und -analyse.
- `opencv-python`: Für die Bild- und Videoverarbeitung.
- `numpy`: Für mathematische Operationen.
- `dlib`: Für das Training und die Analyse von Gesichtsdaten.

## To-Do

- Unterstützung für mehrere Benutzer und gleichzeitige Gesichtserkennung
- Verbesserte Fehlertoleranz und Verwaltung für den Fall, dass keine Kamera erkannt wird
- Speichern der Gesichtsdaten in einer Datenbank anstelle von Bildern
