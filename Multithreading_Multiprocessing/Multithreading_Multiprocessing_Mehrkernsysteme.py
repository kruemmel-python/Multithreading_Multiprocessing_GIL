import tkinter as tk
import multiprocessing
import threading
import time
import psutil  # Modul zur Überwachung der CPU-Auslastung

def cpu_intensive_task(task_id, result_text):
    result_list = []
    result_list.append(f"Thread {task_id} startet.\n")
    result_list.append(f"Erklärung: Thread {task_id} wird vom Betriebssystem eingeplant.\n")
    checkpoint = 10**6

    for i in range(1, 10**7 + 1):
        if i % checkpoint == 0:
            result_list.append(f"Erklärung: Thread {task_id} hat {i} Iterationen abgeschlossen.\n")
    
    result_list.append(f"Thread {task_id} beendet.\n")
    result_list.append(f"Erklärung: Thread {task_id} hat seine Berechnungen abgeschlossen.\n")

    # Kopiere die Ergebnisse in das Shared Memory Array
    result_str = ''.join(result_list)
    result_str = result_str[:len(result_text)]  # Schneide den Text auf die Größe des Arrays zu
    result_text[:] = result_str.ljust(len(result_text))  # Fülle den Rest mit Leerzeichen auf

def run_cpu_task_in_thread(task_id, result_text):
    """
    Starte die CPU-intensive Aufgabe in einem separaten Thread, um die GUI nicht zu blockieren.
    """
    threading.Thread(target=cpu_intensive_task, args=(task_id, result_text)).start()

class FirstGUI:
    def __init__(self, master, counter, result_text_1, result_text_2):
        self.master = master
        self.counter = counter
        self.result_text_1 = result_text_1
        self.result_text_2 = result_text_2

        self.master.title("Erstes GUI")
        self.master.geometry("400x450+500+200")

        self.label = tk.Label(master, text="Zählerstand: 0", font=("Helvetica", 16))
        self.label.pack()

        self.increment_button = tk.Button(master, text="Zähler erhöhen", command=self.increment_counter)
        self.increment_button.pack()

        self.decrement_button = tk.Button(master, text="Zähler verringern", command=self.decrement_counter)
        self.decrement_button.pack()

        # CPU-intensive Berechnungen starten und Ergebnis in der TextView des anderen GUI anzeigen
        self.calc_button = tk.Button(master, text="CPU-Task starten", command=self.start_cpu_task)
        self.calc_button.pack()

        self.textview = tk.Text(master, height=10, width=40)
        self.textview.pack()

        # Label zur Anzeige der CPU-Auslastung
        self.cpu_label = tk.Label(master, text="CPU-Auslastung: 0%", font=("Helvetica", 14))
        self.cpu_label.pack()

        # Beginne die Hintergrundüberwachung für die CPU-Auslastung
        self.update_cpu_usage()
        self.update_display()

    def increment_counter(self):
        update_counter(self.counter, 1)

    def decrement_counter(self):
        update_counter(self.counter, -1)

    def start_cpu_task(self):
        # Starte die CPU-intensive Aufgabe in einem separaten Thread
        run_cpu_task_in_thread(1, self.result_text_2)

    def update_display(self):
        # Aktualisiere die Zähleranzeige und TextView alle 1000 ms
        self.label.config(text=f"Zählerstand: {self.counter.value}")
        self.textview.delete(1.0, tk.END)
        self.textview.insert(tk.END, ''.join(self.result_text_1).strip())
        self.master.after(1000, self.update_display)

    def update_cpu_usage(self):
        # Hole die CPU-Auslastung und aktualisiere das Label
        cpu_usage = psutil.cpu_percent(interval=None)
        self.cpu_label.config(text=f"CPU-Auslastung: {cpu_usage}%")
        # Rufe die Funktion nach 1000 ms erneut auf
        self.master.after(1000, self.update_cpu_usage)

class SecondGUI:
    def __init__(self, master, counter, result_text_1, result_text_2):
        self.master = master
        self.counter = counter
        self.result_text_1 = result_text_1
        self.result_text_2 = result_text_2

        self.master.title("Zweites GUI")
        self.master.geometry("400x450+500+400")

        self.label = tk.Label(master, text="Live-Zählerstand: 0", font=("Helvetica", 16))
        self.label.pack()

        self.reset_button = tk.Button(master, text="Zähler zurücksetzen", command=self.reset_counter)
        self.reset_button.pack()

        # CPU-intensive Berechnungen starten und Ergebnis in der TextView des anderen GUI anzeigen
        self.calc_button = tk.Button(master, text="CPU-Task starten", command=self.start_cpu_task)
        self.calc_button.pack()

        self.textview = tk.Text(master, height=10, width=40)
        self.textview.pack()

        # Label zur Anzeige der CPU-Auslastung
        self.cpu_label = tk.Label(master, text="CPU-Auslastung: 0%", font=("Helvetica", 14))
        self.cpu_label.pack()

        # Beginne die Hintergrundüberwachung für die CPU-Auslastung
        self.update_cpu_usage()
        self.update_display()

    def reset_counter(self):
        with self.counter.get_lock():
            self.counter.value = 0

    def start_cpu_task(self):
        # Starte die CPU-intensive Aufgabe in einem separaten Thread
        run_cpu_task_in_thread(2, self.result_text_1)

    def update_display(self):
        # Aktualisiere die Zähleranzeige und TextView alle 1000 ms
        self.label.config(text=f"Live-Zählerstand: {self.counter.value}")
        self.textview.delete(1.0, tk.END)
        self.textview.insert(tk.END, ''.join(self.result_text_2).strip())
        self.master.after(1000, self.update_display)

    def update_cpu_usage(self):
        # Hole die CPU-Auslastung und aktualisiere das Label
        cpu_usage = psutil.cpu_percent(interval=None)
        self.cpu_label.config(text=f"CPU-Auslastung: {cpu_usage}%")
        # Rufe die Funktion nach 1000 ms erneut auf
        self.master.after(1000, self.update_cpu_usage)

def start_first_gui(counter, result_text_1, result_text_2):
    root = tk.Tk()
    app = FirstGUI(root, counter, result_text_1, result_text_2)
    root.mainloop()

def start_second_gui(counter, result_text_1, result_text_2):
    root = tk.Tk()
    app = SecondGUI(root, counter, result_text_1, result_text_2)
    root.mainloop()

def update_counter(counter, increment):
    with counter.get_lock():
        counter.value += increment

if __name__ == "__main__":
    # Erstellen einer gemeinsamen Zählervariable im Shared Memory
    counter = multiprocessing.Value('i', 0)
    result_text_1 = multiprocessing.Array('u', 10000)  # Shared memory for results (GUI 1 to 2)
    result_text_2 = multiprocessing.Array('u', 10000)  # Shared memory for results (GUI 2 to 1)

    process_1 = multiprocessing.Process(target=start_first_gui, args=(counter, result_text_1, result_text_2))
    process_2 = multiprocessing.Process(target=start_second_gui, args=(counter, result_text_1, result_text_2))

    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()

    print("Beide GUIs wurden beendet.")
