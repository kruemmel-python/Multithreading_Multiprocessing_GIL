"""
Multithreading und Multiprocessing Beispiel in Python 3.13
==========================================================

Dieses Modul zeigt, wie man Multithreading und Multiprocessing in Python 3.13 kombinieren kann.
Es gibt mehrere Prozesse, die jeweils mehrere Threads innerhalb eines Prozesses starten, um Aufgaben parallel auszuführen.

Module:
-------
- `multiprocessing`: Bietet Unterstützung für die parallele Ausführung von Prozessen.
- `threading`: Ermöglicht die parallele Ausführung von Threads innerhalb eines Prozesses.

Funktionen:
-----------
- `thread_task(task_id)`: Führt eine simulierte Aufgabe aus, die durch einen Thread erledigt wird.
- `process_task(process_id)`: Erstellt mehrere Threads innerhalb eines Prozesses und führt sie aus.
- `main`: Erstellt mehrere Prozesse, die wiederum mehrere Threads enthalten, und synchronisiert deren Ausführung.
"""

import multiprocessing
import threading
import time

def thread_task(task_id):
    """
    Führt eine Aufgabe in einem separaten Thread aus.
    
    Jeder Thread simuliert eine Aufgabe, indem er für 2 Sekunden schläft, bevor er seine Arbeit beendet.

    Args:
    -----
    task_id (int): Die ID des Threads, um die Ausgabe zu kennzeichnen.

    Beispiel:
    ---------
    >>> thread_task(1)
    Thread 1 startet.
    (Nach 2 Sekunden)
    Thread 1 beendet.
    """
    print(f"Thread {task_id} startet.")
    time.sleep(2)
    print(f"Thread {task_id} beendet.")

def process_task(process_id):
    """
    Erstellt und startet mehrere Threads innerhalb eines Prozesses.
    
    Jeder Prozess startet 3 Threads, die parallel Aufgaben ausführen.

    Args:
    -----
    process_id (int): Die ID des Prozesses, um die Ausgabe zu kennzeichnen.

    Beispiel:
    ---------
    >>> process_task(1)
    Prozess 1 startet.
    Thread 0 startet.
    Thread 1 startet.
    Thread 2 startet.
    Thread 0 beendet.
    Thread 1 beendet.
    Thread 2 beendet.
    Prozess 1 beendet.
    """
    print(f"Prozess {process_id} startet.")
    
    # Liste zur Speicherung der Threads
    threads = []
    
    # Erstellen und Starten von 3 Threads
    for i in range(3):
        t = threading.Thread(target=thread_task, args=(i,))
        threads.append(t)
        t.start()

    # Warten auf das Ende aller Threads
    for t in threads:
        t.join()
    
    print(f"Prozess {process_id} beendet.")

if __name__ == "__main__":
    """
    Hauptfunktion des Programms.
    
    Erstellt mehrere Prozesse (in diesem Beispiel 2). Jeder Prozess führt 
    eine Funktion `process_task` aus, die wiederum Threads startet. Die 
    Prozesse und Threads laufen parallel und werden am Ende synchronisiert.

    Funktionsweise:
    ---------------
    1. Zwei Prozesse werden erstellt.
    2. Jeder Prozess startet drei Threads, die Aufgaben parallel ausführen.
    3. Das Hauptprogramm wartet darauf, dass alle Prozesse und Threads beendet werden.

    Beispiel:
    ---------
    >>> main()
    Prozess 0 startet.
    Thread 0 startet.
    Thread 1 startet.
    Thread 2 startet.
    Thread 0 beendet.
    Thread 1 beendet.
    Thread 2 beendet.
    Prozess 0 beendet.
    Prozess 1 startet.
    Thread 0 startet.
    Thread 1 startet.
    Thread 2 startet.
    Thread 0 beendet.
    Thread 1 beendet.
    Thread 2 beendet.
    Prozess 1 beendet.
    Alle Prozesse und Threads beendet.
    """
    # Anzahl der Prozesse
    num_processes = 2

    # Liste zur Speicherung der Prozesse
    processes = []
    
    # Erstellen und Starten von Prozessen
    for i in range(num_processes):
        p = multiprocessing.Process(target=process_task, args=(i,))
        processes.append(p)
        p.start()

    # Warten auf das Ende aller Prozesse
    for p in processes:
        p.join()

    print("Alle Prozesse und Threads beendet.")
