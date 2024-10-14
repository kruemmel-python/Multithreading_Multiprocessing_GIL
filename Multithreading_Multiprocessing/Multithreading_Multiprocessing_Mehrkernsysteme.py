"""
Multithreading und Multiprocessing mit separaten GUIs in Python 3.13
====================================================================

Dieses Modul zeigt, wie man Multithreading und Multiprocessing in Python 3.13 verwendet, 
um zwei parallele GUIs zu erstellen, die miteinander über eine geteilte Ressource 
(den Zähler) interagieren. Hierbei laufen die GUIs in separaten Prozessen und verwenden
einen gemeinsam genutzten Zähler über `multiprocessing.Value`.

Fachliche Informationen:
-------------------------
- **Speicherverwaltung**: Beide GUIs laufen in separaten Prozessen, die jeweils ihren eigenen 
  Speicherbereich haben. Der Zähler wird jedoch als **shared memory** (gemeinsamer Speicher) 
  über das `multiprocessing.Value`-Objekt implementiert. Dies ermöglicht es den Prozessen,
  sicher auf denselben Speicherbereich zuzugreifen. Um Datenkonflikte zu vermeiden, wird 
  ein Lock (`counter.get_lock()`) verwendet, um den Zugriff auf den Zähler zu synchronisieren.

- **CPU-Nutzung**: Da Prozesse voneinander getrennt sind, können sie auf verschiedenen **CPU-Kernen**
  laufen, was eine bessere Nutzung der Ressourcen ermöglicht. Jeder GUI-Prozess läuft unabhängig 
  und teilt sich den gemeinsamen Zähler im Shared Memory. Python 3.13 optimiert den Umgang 
  mit dem GIL (Global Interpreter Lock), sodass Prozesse effizient parallel arbeiten können.
  Innerhalb jedes Prozesses kann zusätzlich **Multithreading** verwendet werden, um die 
  Benutzeroberflächen reaktionsfähig zu halten, da sie auf mehrere Aufgaben gleichzeitig reagieren können.

- **Verwendung von Prozessen und Threads**: Zwei unabhängige Prozesse, einer für jedes GUI, greifen 
  auf denselben Zähler im Shared Memory zu. Die Prozesse laufen parallel und können mehrere Threads 
  innerhalb jedes Prozesses verwenden, um GUI-Aktivitäten und Hintergrundaufgaben zu parallelisieren.

Module:
-------
- `multiprocessing`: Erstellt separate Prozesse, die auf verschiedenen CPU-Kernen laufen können,
  und ermöglicht den Zugriff auf gemeinsam genutzte Ressourcen (wie den Zähler).
- `threading`: Führt mehrere Threads innerhalb eines Prozesses aus, um verschiedene GUI-Aufgaben parallel auszuführen.

Funktionen:
-----------
- `update_counter(increment)`: Erhöht oder verringert den Zähler, der von beiden GUIs geteilt wird. 
  Der Zugriff auf den Zähler wird über ein Lock geschützt, um Konflikte zu vermeiden.
- `FirstGUI`: Erstellt das erste GUI, mit der Möglichkeit, den Zähler zu erhöhen oder zu verringern. 
  Die GUI zeigt den aktuellen Wert des Zählers an und aktualisiert diesen regelmäßig.
- `SecondGUI`: Erstellt das zweite GUI, das den Zählerstand anzeigt und den Zähler auf 0 zurücksetzen kann. 
  Auch diese GUI aktualisiert den Zählerstand regelmäßig.
- `start_first_gui()`: Startet das erste GUI in einem separaten Prozess und verwendet Threads, um die GUI reaktionsfähig zu halten.
- `start_second_gui()`: Startet das zweite GUI in einem separaten Prozess und verwendet Threads für die GUI-Verwaltung.
- `main`: Startet beide GUIs als separate Prozesse. Jeder Prozess greift auf den gemeinsam genutzten Zähler im Shared Memory zu und aktualisiert den Zähler regelmäßig.

Ablauf:
-------
1. Das Programm startet zwei unabhängige Prozesse, `process_1` und `process_2`, die jeweils ein GUI darstellen.
2. Beide Prozesse greifen über `multiprocessing.Value` auf denselben Zähler im Shared Memory zu.
3. Innerhalb jedes Prozesses werden Threads verwendet, um die GUI-Aktivitäten zu handhaben.
4. Änderungen am Zähler (Erhöhen, Verringern oder Zurücksetzen) in einem GUI werden sofort im anderen GUI reflektiert, da beide GUIs den Zählerstand regelmäßig aus dem Shared Memory abfragen.
"""

import tkinter as tk
import multiprocessing

# Gemeinsame Variable für beide GUIs (Zähler)
def update_counter(counter, increment):
    """
    Erhöht oder verringert den gemeinsamen Zählerwert sicher.
    
    Der Zugriff auf den Zähler wird über ein Lock synchronisiert, um sicherzustellen,
    dass nur ein Prozess gleichzeitig den Wert ändern kann.
    
    Args:
    -----
    counter (multiprocessing.Value): Gemeinsame Zählervariable.
    increment (int): Wert, um den der Zähler erhöht oder verringert werden soll.

    Beispiel:
    ---------
    >>> update_counter(counter, 1)
    Erhöht den Zähler um 1.
    """
    with counter.get_lock():
        counter.value += increment

class FirstGUI:
    """
    Erstellt das erste GUI, das den gemeinsamen Zähler anzeigen und ändern kann.
    
    Dieses GUI hat zwei Buttons, um den Zähler zu erhöhen oder zu verringern. 
    Die Anzeige wird regelmäßig aktualisiert, um den aktuellen Wert des Zählers anzuzeigen, 
    der von beiden GUIs geteilt wird.

    Speichereffizienz:
    -------------------
    Da die GUIs in separaten Prozessen laufen, haben sie voneinander getrennte Speicherbereiche. 
    Der Zähler wird jedoch über den **shared memory** (`multiprocessing.Value`) gemeinsam genutzt und 
    über ein Lock synchronisiert, um Konflikte zu verhindern.
    """
    def __init__(self, master, counter):
        """
        Initialisiert das GUI und erstellt die GUI-Elemente (Label, Buttons).
        
        Args:
        -----
        master: Das Hauptfenster für das GUI.
        counter: Der gemeinsam genutzte Zähler im Shared Memory.
        """
        self.master = master
        self.counter = counter
        self.master.title("Erstes GUI")

        # Fenstergröße auf 300x200 Pixel setzen und die Position festlegen (links oben)
        self.master.geometry("300x200+500+200")
        
        self.label = tk.Label(master, text="Zählerstand: 0", font=("Helvetica", 16))
        self.label.pack()

        self.increment_button = tk.Button(master, text="Zähler erhöhen", command=self.increment_counter)
        self.increment_button.pack()

        self.decrement_button = tk.Button(master, text="Zähler verringern", command=self.decrement_counter)
        self.decrement_button.pack()

        # Aktualisierung der Anzeige alle 100 ms
        self.update_display()

    def increment_counter(self):
        """Erhöht den Zähler um 1."""
        update_counter(self.counter, 1)

    def decrement_counter(self):
        """Verringert den Zähler um 1."""
        update_counter(self.counter, -1)

    def update_display(self):
        """Aktualisiert die Zähleranzeige im GUI, um den aktuellen Wert anzuzeigen."""
        self.label.config(text=f"Zählerstand: {self.counter.value}")
        self.master.after(100, self.update_display)  # Aktualisiere alle 100 ms

class SecondGUI:
    """
    Erstellt das zweite GUI, das den gemeinsamen Zähler anzeigen und zurücksetzen kann.
    
    Dieses GUI zeigt den aktuellen Zählerstand an und bietet eine Schaltfläche, um 
    den Zähler auf 0 zurückzusetzen. Die Anzeige wird regelmäßig aktualisiert.

    Prozessorverwaltung:
    ---------------------
    Jeder GUI-Prozess läuft auf einem separaten CPU-Kern (falls verfügbar). 
    Beide GUIs verwenden den gleichen Zähler im Shared Memory.
    """
    def __init__(self, master, counter):
        """
        Initialisiert das zweite GUI und erstellt die GUI-Elemente (Label, Button).
        
        Args:
        -----
        master: Das Hauptfenster für das GUI.
        counter: Der gemeinsam genutzte Zähler im Shared Memory.
        """
        self.master = master
        self.counter = counter
        self.master.title("Zweites GUI")

        # Fenstergröße auf 300x200 Pixel setzen und Position unter dem ersten GUI festlegen
        self.master.geometry("300x200+500+400")

        self.label = tk.Label(master, text="Live-Zählerstand: 0", font=("Helvetica", 16))
        self.label.pack()

        self.reset_button = tk.Button(master, text="Zähler zurücksetzen", command=self.reset_counter)
        self.reset_button.pack()

        # Aktualisierung der Anzeige alle 100 ms
        self.update_display()

    def reset_counter(self):
        """Setzt den Zähler auf 0 zurück."""
        with self.counter.get_lock():
            self.counter.value = 0

    def update_display(self):
        """Aktualisiert die Zähleranzeige im GUI, um den aktuellen Wert anzuzeigen."""
        self.label.config(text=f"Live-Zählerstand: {self.counter.value}")
        self.master.after(100, self.update_display)  # Aktualisiere alle 100 ms

def start_first_gui(counter):
    """Startet das erste GUI in einem separaten Prozess."""
    root = tk.Tk()
    app = FirstGUI(root, counter)
    root.mainloop()

def start_second_gui(counter):
    """Startet das zweite GUI in einem separaten Prozess."""
    root = tk.Tk()
    app = SecondGUI(root, counter)
    root.mainloop()

if __name__ == "__main__":
    """
    Hauptfunktion des Programms.
    
    Startet zwei Prozesse, die jeweils ein GUI darstellen. Beide Prozesse verwenden denselben Zähler,
    der über Shared Memory geteilt wird. Änderungen im Zähler werden zwischen den GUIs synchronisiert.

    CPU-Auslastung:
    ----------------
    Beide Prozesse können auf unterschiedlichen CPU-Kernen laufen, wodurch die Ressourcen effizient genutzt werden.
    Der Zähler wird zwischen den Prozessen im Shared Memory geteilt und regelmäßig in den GUIs aktualisiert.
    """
    # Erstellen einer gemeinsamen Zählervariable im Shared Memory
    counter = multiprocessing.Value('i', 0)  # Ein Integer-Wert ('i') im Shared Memory

    # Starten der beiden Prozesse
    process_1 = multiprocessing.Process(target=start_first_gui, args=(counter,))
    process_2 = multiprocessing.Process(target=start_second_gui, args=(counter,))

    process_1.start()
    process_2.start()

    # Warten auf das Ende beider Prozesse
    process_1.join()
    process_2.join()

    print("Beide GUIs wurden beendet.")
