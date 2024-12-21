import time
import subprocess

class Task:
    def __init__(self, name, path, execution_time):
        """
        Représente une tâche ou une application.
        :param name: Nom de l'application.
        :param path: Chemin absolu ou commande pour lancer l'application.
        :param execution_time: Temps d'exécution en secondes.
        """
        self.name = name
        self.path = path
        self.execution_time = execution_time

class SJFScheduler:
    def __init__(self):
        self.tasks = []  # Liste des tâches

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Tâche ajoutée : {task.name}, Temps d'exécution : {task.execution_time}s")

    def execute_tasks(self):
        # Trier les tâches par temps d'exécution croissant
        self.tasks.sort(key=lambda t: t.execution_time)
        print("\nExécution des tâches selon l'algorithme Shortest Job First...")
        for task in self.tasks:
            print(f"\nOuverture de l'application : {task.name} (Temps d'exécution : {task.execution_time}s)")
            try:
                # Lancer l'application
                process = subprocess.Popen(task.path, shell=True)
                time.sleep(task.execution_time)  # Temps d'exécution avant de passer à la tâche suivante
                process.terminate()  # Fermer le processus après le temps défini
                print(f"Tâche terminée : {task.name}")
            except Exception as e:
                print(f"Erreur lors de l'exécution de {task.name} : {e}")
        self.tasks.clear()
        print("Toutes les tâches ont été exécutées.")

# Exemple d'utilisation
if __name__ == "__main__":
    scheduler = SJFScheduler()

    # Ajouter des tâches (nom, chemin ou commande, temps d'exécution)
    scheduler.add_task(Task("Bloc-notes", "notepad.exe", 5))  # Pour Windows
    scheduler.add_task(Task("Calculatrice", "calc.exe", 2))   # Pour Windows
    scheduler.add_task(Task("Navigateur", "start chrome", 8))  # Navigateur Chrome (pour Windows)

    # Exécuter les tâches
    scheduler.execute_tasks()
