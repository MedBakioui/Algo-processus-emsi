import time
import subprocess
import heapq

class Task:
    def __init__(self, name, path, arrival_time, burst_time, priority):
        """
        Représente une tâche ou une application.
        :param name: Nom de la tâche ou de l'application.
        :param path: Commande ou chemin pour exécuter l'application.
        :param arrival_time: Temps d'arrivée de la tâche.
        :param burst_time: Temps total requis pour exécuter la tâche.
        :param priority: Priorité de la tâche (plus petit = plus prioritaire).
        """
        self.name = name
        self.path = path
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.priority = priority
        self.start_time = None
        self.completion_time = None
        self.process = None

class PriorityScheduler:
    def __init__(self):
        self.tasks = []  # Liste des tâches à exécuter
        self.current_time = 0  # Temps actuel de la simulation
        self.current_task = None  # Tâche en cours

    def add_task(self, task):
        heapq.heappush(self.tasks, (task.arrival_time, task.priority, task))
        print(f"Tâche ajoutée : {task.name}, Arrivée : {task.arrival_time}, "
              f"Durée : {task.remaining_time}s, Priorité : {task.priority}")

    def execute_tasks(self):
        ready_queue = []  # File d'attente des tâches prêtes
        print("\nExécution des tâches selon l'algorithme Priorité Préemptive...")

        while self.tasks or ready_queue or self.current_task:
            # Ajouter les tâches arrivées au temps actuel dans la file d'attente prête
            while self.tasks and self.tasks[0][0] <= self.current_time:
                _, priority, task = heapq.heappop(self.tasks)
                heapq.heappush(ready_queue, (priority, task))
                print(f"Tâche disponible : {task.name} au temps {self.current_time}")

            # Vérifier si une tâche plus prioritaire est arrivée
            if ready_queue and (self.current_task is None or ready_queue[0][0] < self.current_task.priority):
                # Suspendre la tâche en cours (si existante)
                if self.current_task:
                    print(f"Interruption de la tâche : {self.current_task.name}")
                    heapq.heappush(ready_queue, (self.current_task.priority, self.current_task))
                    self.current_task.process.terminate()  # Suspendre l'application

                # Lancer la tâche la plus prioritaire
                _, self.current_task = heapq.heappop(ready_queue)
                if self.current_task.start_time is None:
                    self.current_task.start_time = self.current_time

                print(f"Lancement de l'application : {self.current_task.name}")
                self.current_task.process = subprocess.Popen(self.current_task.path, shell=True)

            # Exécuter la tâche en cours pendant 1 unité de temps
            if self.current_task:
                print(f"Exécution de la tâche : {self.current_task.name} (Temps restant : {self.current_task.remaining_time})")
                time.sleep(1)
                self.current_task.remaining_time -= 1
                self.current_time += 1

                # Si la tâche est terminée
                if self.current_task.remaining_time <= 0:
                    print(f"Tâche terminée : {self.current_task.name} au temps {self.current_time}")
                    self.current_task.process.terminate()  # Fermer l'application
                    self.current_task.completion_time = self.current_time
                    self.current_task = None
            else:
                # Aucun processus prêt, avancer le temps
                print("Aucune tâche prête, avancée du temps...")
                self.current_time += 1

        print("\nToutes les tâches ont été exécutées.")

# Exemple d'utilisation
if __name__ == "__main__":
    scheduler = PriorityScheduler()

    # Ajouter des tâches (nom, chemin/commande, temps d'arrivée, durée totale, priorité)
    scheduler.add_task(Task("Bloc-notes", "notepad.exe", 0, 6, 2))  # Windows
    scheduler.add_task(Task("Calculatrice", "calc.exe", 1, 3, 1))   # Windows
    scheduler.add_task(Task("Navigateur", "start chrome", 2, 8, 3)) # Windows

    # Exécuter les tâches
    scheduler.execute_tasks()
