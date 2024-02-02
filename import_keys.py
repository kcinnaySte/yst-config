import requests
import os

def fetch_github_ssh_keys(username):
    """Holt die öffentlichen SSH-Schlüssel eines GitHub-Benutzers."""
    url = f"https://api.github.com/users/{username}/keys"
    response = requests.get(url)
    response.raise_for_status()  # Löst eine Ausnahme aus, wenn der Request fehlschlägt
    keys = response.json()
    return {key['key']: key['key'] for key in keys}  # Verwende ein dict für schnelleres Suchen

def read_existing_keys(file_path):
    """Liest die existierenden SSH-Schlüssel und gibt sie als dict zurück."""
    existing_keys = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if "keep" not in line:
                    existing_keys[line.strip()] = line.strip()
                else:
                    # Schlüssel mit "keep" direkt behalten
                    existing_keys[line] = line
    return existing_keys

def update_authorized_keys(file_path, github_keys):
    """Aktualisiert die authorized_keys Datei basierend auf GitHub-Schlüsseln."""
    existing_keys = read_existing_keys(file_path)
    
    # Füge neue Schlüssel hinzu
    for key in github_keys:
        if key not in existing_keys:
            existing_keys[key] = github_keys[key]
    
    # Entferne nicht mehr vorhandene Schlüssel, außer sie enthalten "keep"
    keys_to_keep = {k: v for k, v in existing_keys.items() if v in github_keys or "keep" in k}
    
    # Schreibe die aktualisierten Schlüssel zurück in die Datei
    with open(file_path, 'w') as file:
        for key in keys_to_keep.values():
            file.write(key + '\n' if not key.endswith('\n') else key)
    print("authorized_keys aktualisiert.")