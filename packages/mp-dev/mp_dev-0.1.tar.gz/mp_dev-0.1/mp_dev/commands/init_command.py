# mp_dev/commands/init_command.py
from ..project_generator import generate_project_structure

def run():
    print("Génération de l'architecture de projet...")
    generate_project_structure()
    print("Architecture de projet générée avec succès.")
