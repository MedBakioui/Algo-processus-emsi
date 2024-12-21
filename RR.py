import time
import subprocess

class Task:
    def __init__(self, name, path, execution_time):
        """
        Représente une tâche ou une application.
        :param name: Nom de l'application.
        :param path: Chemin absolu ou commande pour lancer l'application.
        :param execution_time: Temps d'exécution total en secondes.
        """
        self.name = name
        self.path = path
        self.remaining_time = execution_time  # Temps restant pour cette tâche

class RoundRobinScheduler:
    def __init__(self, quantum):
        """
        :param quantum: Durée fixe allouée à chaque tâche par cycle (en secondes).
        """
        self.tasks = []
        self.quantum = quantum  # Quantum de temps en secondes

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Tâche ajoutée : {task.name}, Temps total : {task.remaining_time}s")

    def execute_tasks(self):
        print("\nExécution des tâches selon l'algorithme Round Robin...")
        while self.tasks:
            for task in list(self.tasks):  # Copie pour modifier la liste pendant l'itération
                print(f"\nTraitement de la tâche : {task.name} (Temps restant : {task.remaining_time}s)")
                try:
                    # Lancer ou reprendre l'application
                    process = subprocess.Popen(task.path, shell=True)
                    # Exécuter pour un maximum de `quantum` ou le temps restant
                    execution_time = min(self.quantum, task.remaining_time)
                    time.sleep(execution_time)
                    task.remaining_time -= execution_time
                    process.terminate()  # Terminer le processus après le quantum
                    if task.remaining_time <= 0:
                        print(f"Tâche terminée : {task.name}")
                        self.tasks.remove(task)
                    else:
                        print(f"Tâche suspendue : {task.name} (Temps restant : {task.remaining_time}s)")
                except Exception as e:
                    print(f"Erreur lors de l'exécution de {task.name} : {e}")
                    self.tasks.remove(task)
        print("Toutes les tâches ont été exécutées.")

# Exemple d'utilisation
if __name__ == "__main__":
    quantum_time = 3  # Quantum de temps en secondes
    scheduler = RoundRobinScheduler(quantum=quantum_time)

    # Ajouter des tâches (nom, chemin ou commande, temps total d'exécution)
    scheduler.add_task(Task("Bloc-notes", "notepad.exe", 5))  # Pour Windows
    scheduler.add_task(Task("Calculatrice", "calc.exe", 6))   # Pour Windows
    scheduler.add_task(Task("Navigateur", "start chrome", 8))  # Navigateur Chrome (pour Windows)

    # Exécuter les tâches
    scheduler.execute_tasks()
