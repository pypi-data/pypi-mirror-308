# mp_dev/project_generator.py
import os


def generate_project_structure():
    project_structure = {
        "README.txt": "Ceci est un fichier README pour votre projet.",
        "controller": {},
        "route": {},
        "models": {},
        "utils": {},
        "config": {},
    }

    for name, content in project_structure.items():
        if isinstance(content, dict):  # C'est un dossier
            os.makedirs(name, exist_ok=True)
        else:  # C'est un fichier
            with open(name, "w") as f:
                f.write(content)

    print("Architecture de base du projet générée avec succès.")
