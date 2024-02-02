import subprocess
import os
import platform
from os import environ as env
import os
from pathlib import Path

from import_keys import fetch_github_ssh_keys, update_authorized_keys

def install_packages_debian(packages):
  # apt packages:
  for package in packages:
    print(f"Installiere {package}")
    subprocess.run(["sudo", "apt-get", "install", "-y",package], check=True)

def install_packages_mac(packages):
  # apt packages:
  for package in packages:
    print(f"Installiere {package}")
    subprocess.run(["brew", "install", package], check=True)

def link_file(source_dir, target_dir):
    # Erstelle das Zielverzeichnis, falls es nicht existiert
    os.makedirs(os.path.expanduser(target_dir), exist_ok=True)
    
    # Gehe durch alle Dateien im Quellverzeichnis (auch Unterordner)
    for dirpath, dirnames, filenames in os.walk(source_dir):
       
       for filename in filenames:
        # Verlinken der Dateien ins Zielverzeichnis
        source_file = os.path.join(dirpath, filename)
        target_file = os.path.join(target_dir, "." + filename)
        if not os.path.exists(target_file):
          os.symlink(source_file, target_file)
        print(f"Link erstellt: {source_file} -> {target_file}")

def link_dir(source_dir, target_dir):
    # Erstelle das Zielverzeichnis, falls es nicht existiert
    os.makedirs(os.path.expanduser(target_dir), exist_ok=True)
    
    # Iteriere durch alle Dateien im Quellverzeichnis
    for dir_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, dir_name)
        target_file = os.path.join(os.path.expanduser(target_dir),  dir_name)
        
        # Prüfe, ob die Quelldatei tatsächlich eine Datei ist (kein Verzeichnis)
        if os.path.isdir(source_file):
            # Erstelle einen symbolischen Link, falls noch nicht vorhanden
            if not os.path.exists(target_file):
                os.symlink(source_file, target_file)
                print(f"Link erstellt: {target_file} -> {source_file}")
            else:
                print(f"Folder existiert bereits: {target_file}")

def install_pip_packages(packages):
    for package in packages:
        print(f"Installiere {package}")
        subprocess.run(["pip3", "install", package], check=True)

def install_font(url, font_name):
    import requests
    # Pfad zum Fonts-Ordner
    fonts_dir = Path.home() / 'Library/Fonts'
    font_path = fonts_dir / font_name
    
    # Prüfe, ob die Font bereits installiert ist
    if font_path.exists():
        print(f"{font_name} ist bereits installiert.")
        return

    # Font herunterladen
    response = requests.get(url)
    if response.status_code == 200:
        # Schreibe die Font-Datei
        with open(font_path, 'wb') as font_file:
            font_file.write(response.content)
        print(f"{font_name} wurde erfolgreich installiert.")
    else:
        print("Fehler beim Herunterladen der Font.")

if __name__ == "__main__":
  if platform.system() == "Darwin":  # macOS
    #install_packages_mac(["vim", "neovim", "tmux", "git", "zsh"])
    pass
  elif platform.system() == "Linux":
    install_packages_debian(["vim", "neovim", "tmux", "git", "zsh"])

  # Installiere tpm
  target_path = os.path.join( os.path.expanduser('~'), ".tmux", "plugins", "tpm")
  if not os.path.exists(target_path):
    subprocess.run(["git", "clone", "https://github.com/tmux-plugins/tpm", target_path], check=True)

  #Kopieren der Konfigurationen
  config_path = env.get("XDG_CONFIG_HOME", None)
  if config_path:
    link_dir(
      os.path.join(os.getcwd(), "dotfiles"), 
      config_path
    )
  else:
    link_file(
      os.path.join(os.getcwd(), "dotfiles"), 
      os.path.expanduser('~')
    )
  
  #Installieren der tmux plugins
  subprocess.run(
     os.path.join(os.path.expanduser('~'), ".tmux", "plugins", "tpm", "bin", "install_plugins"),
     check=True)
  
  #Installation der Schriftart JetBrains auf MacOS
  if platform.system() == "Darwin":  # macOS
    install_pip_packages(["requests"])

    install_font(
      "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/JetBrainsMono.zip",
      "JetBrainsMono.zip"
    )

  # Installiere quck.nvim
  target_path = os.path.join( os.path.expanduser('~'), ".config", "nvim")
  if not os.path.exists(target_path):
    subprocess.run(["git", "clone", "https://github.com/albingroen/quick.nvim", target_path], check=True)
  subprocess.run(["nvim", "--headless", "'+Lazy! sync'", "+qa"], check=True)

  # Update SSH Keys
  github_keys = fetch_github_ssh_keys("kcinnayste")
  update_authorized_keys(os.path.expanduser("~/.ssh/authorized_keys"), github_keys)

  # Installiere oh-my-zsh
  subprocess.run(["sh", "-c", "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"])
  print("Oh-My-Zsh wurde erfolgreich installiert.")

  # Setze zsh als Standard shell
  if (not env.get("SHELL").endswith("zsh")):
    subprocess.run(["chsh", "-s", "$(which zsh)"])
    print("Zsh wurde als Standard-Shell eingestellt.")#



  
