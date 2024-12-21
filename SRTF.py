import time
import subprocess
import heapq

class Task:
    def __init__(self, name, path, arrival_time, burst_time):
        """
        Représente une tâche ou une application dans l'algorithme SRTF.
        :param name: Nom de la tâche ou de l'application.
        :param path: Commande ou chemin pour exécuter l'application.
        :param arrival_time: Temps d'arrivée de la tâche.
        :param burst_time: Temps total requis pour exécuter la tâche.
        """
        self.name = name
        self.path = path
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.process = None

class SRTFScheduler:
    def __init__(self):
        self.tasks = []  # Liste des tâches à exécuter
        self.current_time = 0  # Temps actuel de la simulation

    def add_task(self, task):
        heapq.heappush(self.tasks, (task.arrival_time, task))
        print(f"Tâche ajoutée : {task.name}, Arrivée : {task.arrival_time}, Durée : {task.remaining_time}s")

    def execute_tasks(self):
        ready_queue = []  # File d'attente des tâches prêtes
        print("\nExécution des tâches selon l'algorithme SRTF...")

        while self.tasks or ready_queue:
            # Ajouter les tâches arrivées au temps actuel dans la file d'attente prête
            while self.tasks and self.tasks[0][0] <= self.current_time:
                _, task = heapq.heappop(self.tasks)
                heapq.heappush(ready_queue, (task.remaining_time, task))
                print(f"Tâche disponible : {task.name} au temps {self.current_time}")

            if ready_queue:
                # Récupérer la tâche avec le temps restant le plus court
                _, current_task = heapq.heappop(ready_queue)

                if current_task.start_time is None:
                    current_task.start_time = self.current_time

                # Lancer ou reprendre l'application
                if current_task.process is None:
                    print(f"Lancement de l'application : {current_task.name}")
                    current_task.process = subprocess.Popen(current_task.path, shell=True)

                # Exécuter la tâche pendant 1 unité de temps
                execution_time = 1
                print(f"Exécution de la tâche : {current_task.name} (Temps restant : {current_task.remaining_time})")
                time.sleep(execution_time)
                self.current_time += execution_time
                current_task.remaining_time -= execution_time

                # Vérifier si la tâche est terminée
                if current_task.remaining_time <= 0:
                    print(f"Tâche terminée : {current_task.name} au temps {self.current_time}")
                    current_task.process.terminate()  # Fermer l'application
                    current_task.completion_time = self.current_time
                else:
                    # Réinsérer la tâche avec le temps restant mis à jour
                    heapq.heappush(ready_queue, (current_task.remaining_time, current_task))
            else:
                # Aucun processus prêt, avancer le temps
                print("Aucune tâche prête, avancée du temps...")
                self.current_time += 1

        print("\nToutes les tâches ont été exécutées.")

# Exemple d'utilisation
if __name__ == "__main__":
    scheduler = SRTFScheduler()

    # Ajouter des tâches (nom, chemin/commande, temps d'arrivée, durée totale)
    scheduler.add_task(Task("Bloc-notes", "notepad.exe", 0, 6))  # Windows
    scheduler.add_task(Task("Calculatrice", "calc.exe", 1, 2))   # Windows
    scheduler.add_task(Task("Navigateur", "start chrome", 2, 8)) # Windows

    # Exécuter les tâches
    scheduler.execute_tasks()
