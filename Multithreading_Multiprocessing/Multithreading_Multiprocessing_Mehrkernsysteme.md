In diesem Programm wird sowohl **Multithreading** als auch **Multiprocessing** verwendet, um die neuen Optimierungen von Python 3.13, insbesondere die Verbesserungen beim GIL (Global Interpreter Lock), zu testen. Lass uns das genauer erklären und analysieren, welche Konzepte wo im Code angewandt werden.

### 1. **Multiprocessing** im Code

**Multiprocessing** ermöglicht die parallele Ausführung von Prozessen, wobei jeder Prozess seinen eigenen Speicherbereich und seine eigenen Ressourcen hat. Dies ist besonders hilfreich für CPU-intensive Aufgaben, bei denen der **GIL** ein Flaschenhals sein kann.

#### Wo wird Multiprocessing im Code verwendet?
Multiprocessing wird verwendet, um die beiden GUI-Fenster (Erstes GUI und Zweites GUI) als separate Prozesse zu starten. Das bedeutet, dass beide GUIs unabhängig voneinander laufen und ihre eigenen CPU-Ressourcen verwenden können.

- **Erstellung der GUI-Prozesse**:
  
  ```python
  process_1 = multiprocessing.Process(target=start_first_gui, args=(counter, result_text_1, result_text_2))
  process_2 = multiprocessing.Process(target=start_second_gui, args=(counter, result_text_1, result_text_2))

  process_1.start()
  process_2.start()
  ```

  Hier werden zwei separate Prozesse für die beiden GUI-Anwendungen erstellt (`process_1` und `process_2`). Das **Multiprocessing-Modul** sorgt dafür, dass diese beiden Prozesse in getrennten Speicherbereichen laufen und unterschiedliche CPU-Kerne nutzen können, falls diese verfügbar sind.

- **Gemeinsame Zählervariable im Shared Memory**:
  
  ```python
  counter = multiprocessing.Value('i', 0)
  result_text_1 = multiprocessing.Array('u', 10000)  # Shared memory for results (GUI 1 to 2)
  result_text_2 = multiprocessing.Array('u', 10000)  # Shared memory for results (GUI 2 to 1)
  ```

  Der Zähler (`counter`) und die Ergebnisfelder (`result_text_1` und `result_text_2`) werden mit dem `multiprocessing.Value` bzw. `multiprocessing.Array` im **Shared Memory** gehalten. Diese gemeinsamen Speicherbereiche können von beiden Prozessen gelesen und geschrieben werden. Dadurch wird ermöglicht, dass Änderungen im Zählerwert oder den CPU-Task-Ergebnissen von einem GUI im anderen sichtbar werden.

### 2. **Multithreading** im Code

**Multithreading** ermöglicht es, mehrere Aufgaben (Threads) innerhalb eines Prozesses parallel auszuführen. In Python wird der Zugriff auf Threads jedoch durch den **GIL** beschränkt, was bedeutet, dass nur ein Thread zur gleichen Zeit Python-Bytecode ausführen kann. Bei CPU-intensiven Aufgaben kann der GIL ein Flaschenhals sein, aber durch die Optimierungen in Python 3.13 sollte der GIL weniger blockierend sein.

#### Wo wird Multithreading im Code verwendet?

- **Multithreading für CPU-intensive Aufgaben**:
  
  ```python
  def run_cpu_task_in_thread(task_id, result_text):
      threading.Thread(target=cpu_intensive_task, args=(task_id, result_text)).start()
  ```

  Hier wird die Funktion `cpu_intensive_task` in einem **separaten Thread** gestartet, um CPU-intensive Berechnungen durchzuführen. Der Thread führt eine große Anzahl an Iterationen aus, um die CPU zu belasten und den Einfluss des GIL auf die Parallelität zu testen.

- **CPU-intensive Aufgaben (Multithreading)**:

  Die Funktion `cpu_intensive_task` führt eine Simulation einer CPU-belastenden Aufgabe aus. Bei jeder Million Iterationen wird eine Ausgabe generiert, die beschreibt, was im Hintergrund passiert:

  ```python
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
  ```

  Diese Threads laufen innerhalb der GUI-Prozesse. Da beide GUI-Prozesse als separate Prozesse laufen, blockieren sie sich nicht gegenseitig, sondern nutzen ihre eigenen Ressourcen (auf unterschiedlichen CPU-Kernen, wenn möglich).

  Das ist der Vorteil von **Multiprocessing**: Während in jedem Prozess mehrere Threads ausgeführt werden, blockieren sich die Prozesse nicht gegenseitig, da sie ihren eigenen Speicher haben.

![image](https://github.com/user-attachments/assets/95362a46-c825-47ae-95fb-b17553f99168)



# Beschreibung der GUI-Elemente und deren Funktionen

Im Folgenden beschreibe ich die verschiedenen Elemente der GUIs und ihre jeweilige Funktion.

## 1. Erstes GUI (FirstGUI)
Das erste GUI ermöglicht es, den Zählerstand zu verändern, CPU-intensive Aufgaben zu starten und die CPU-Auslastung anzuzeigen. Hier sind die GUI-Elemente im Detail:

### a) Zählerstand (Label)
- **Element:** `self.label = tk.Label(master, text="Zählerstand: 0", font=("Helvetica", 16))`
- **Beschreibung:** Dieses Label zeigt den aktuellen Wert des Zählers an. Es wird regelmäßig aktualisiert, um den neuesten Stand des Zählers, der im Shared Memory gespeichert ist, anzuzeigen.
- **Aktualisierung:** Die Funktion `update_display()` sorgt dafür, dass dieses Label alle 500 ms aktualisiert wird.

### b) Zähler erhöhen (Button)
- **Element:** `self.increment_button = tk.Button(master, text="Zähler erhöhen", command=self.increment_counter)`
- **Beschreibung:** Dies ist ein Button, der den Zähler um 1 erhöht, wenn er geklickt wird. Die Aktion wird von der Methode `increment_counter()` ausgeführt, die den Zählerwert um 1 erhöht und den neuen Wert im Shared Memory speichert.
- **Aktion:** Ruft `update_counter(self.counter, 1)` auf, um den Zähler zu erhöhen.

### c) Zähler verringern (Button)
- **Element:** `self.decrement_button = tk.Button(master, text="Zähler verringern", command=self.decrement_counter)`
- **Beschreibung:** Ein Button, der den Zähler um 1 verringert, wenn er geklickt wird. Die Methode `decrement_counter()` wird ausgeführt und reduziert den Zählerstand im Shared Memory.
- **Aktion:** Ruft `update_counter(self.counter, -1)` auf, um den Zähler zu verringern.

### d) CPU-Task starten (Button)
- **Element:** `self.calc_button = tk.Button(master, text="CPU-Task starten", command=self.start_cpu_task)`
- **Beschreibung:** Dieser Button startet eine CPU-intensive Aufgabe in einem separaten Thread, wenn er geklickt wird. Diese Aufgabe führt Berechnungen durch, die die CPU stark beanspruchen. Das Ergebnis der Berechnung wird in der TextView des anderen GUIs angezeigt.
- **Aktion:** Ruft `start_cpu_task()` auf, was einen neuen Thread mit der Funktion `cpu_intensive_task()` startet, die den anderen GUI-Prozess mit Ergebnissen versorgt.

### e) TextView (Text)
- **Element:** `self.textview = tk.Text(master, height=10, width=40)`
- **Beschreibung:** Dies ist ein Textfeld, das die Ergebnisse des CPU-intensiven Tasks anzeigt. Es wird mit den Texten aktualisiert, die vom zweiten GUI über Shared Memory gesendet werden.
- **Aktualisierung:** Die Methode `update_display()` aktualisiert dieses Textfeld alle 500 ms, um die neuesten Berechnungsergebnisse anzuzeigen.

### f) CPU-Auslastung (Label)
- **Element:** `self.cpu_label = tk.Label(master, text="CPU-Auslastung: 0%", font=("Helvetica", 14))`
- **Beschreibung:** Dieses Label zeigt die aktuelle CPU-Auslastung des Systems in Prozent an. Die Anzeige wird jede Sekunde aktualisiert.
- **Aktualisierung:** Die Methode `update_cpu_usage()` verwendet die Funktion `psutil.cpu_percent(interval=1)`, um die CPU-Auslastung zu messen und das Label entsprechend zu aktualisieren.

---

## 2. Zweites GUI (SecondGUI)
Das zweite GUI hat ähnliche Funktionen wie das erste, allerdings gibt es Unterschiede in der Art, wie der Zähler verwendet wird. Auch hier werden CPU-intensive Aufgaben ausgeführt und die CPU-Auslastung angezeigt.

### a) Live-Zählerstand (Label)
- **Element:** `self.label = tk.Label(master, text="Live-Zählerstand: 0", font=("Helvetica", 16))`
- **Beschreibung:** Dieses Label zeigt den aktuellen Zählerstand an, der im Shared Memory gespeichert ist. Es wird kontinuierlich aktualisiert, um den neuesten Wert zu reflektieren.
- **Aktualisierung:** Genau wie im ersten GUI wird dieses Label durch die Methode `update_display()` alle 500 ms aktualisiert.

### b) Zähler zurücksetzen (Button)
- **Element:** `self.reset_button = tk.Button(master, text="Zähler zurücksetzen", command=self.reset_counter)`
- **Beschreibung:** Dieser Button setzt den Zähler auf 0 zurück, wenn er geklickt wird. Die Methode `reset_counter()` wird verwendet, um den Wert im Shared Memory auf 0 zu setzen.
- **Aktion:** Setzt den Zähler durch `self.counter.value = 0` auf 0 zurück.

### c) CPU-Task starten (Button)
- **Element:** `self.calc_button = tk.Button(master, text="CPU-Task starten", command=self.start_cpu_task)`
- **Beschreibung:** Startet eine CPU-intensive Berechnung, ähnlich wie im ersten GUI. Diese Aufgabe wird in einem separaten Thread ausgeführt, und die Ergebnisse werden in der TextView des anderen GUIs angezeigt.
- **Aktion:** Startet die Funktion `cpu_intensive_task()` in einem separaten Thread, der die Ergebnisse in das Shared Memory schreibt.

### d) TextView (Text)
- **Element:** `self.textview = tk.Text(master, height=10, width=40)`
- **Beschreibung:** Dieses Textfeld zeigt die Ergebnisse der CPU-intensiven Aufgaben, die vom ersten GUI gesendet wurden, an. Es wird regelmäßig aktualisiert, um die neuesten Informationen anzuzeigen.
- **Aktualisierung:** Die Methode `update_display()` wird verwendet, um den Textinhalt alle 500 ms zu aktualisieren.

### e) CPU-Auslastung (Label)
- **Element:** `self.cpu_label = tk.Label(master, text="CPU-Auslastung: 0%", font=("Helvetica", 14))`
- **Beschreibung:** Dieses Label zeigt die aktuelle CPU-Auslastung des Systems in Prozent an und wird jede Sekunde aktualisiert.
- **Aktualisierung:** Die Methode `update_cpu_usage()` verwendet auch hier die `psutil`-Bibliothek, um die CPU-Auslastung zu messen und das Label zu aktualisieren.

---

## 3. Gemeinsame Funktionen in beiden GUIs

### a) Zähler synchronisieren
Beide GUIs teilen sich den Zähler im Shared Memory. Der Zähler wird durch die Funktionen `increment_counter()`, `decrement_counter()` und `reset_counter()` verändert. Durch die Verwendung von `multiprocessing.Value('i', 0)` können beide Prozesse sicher auf denselben Zähler zugreifen, ohne Datenkorruption zu verursachen.

### b) Ergebnisanzeige über Shared Memory
Die Ergebnisse der CPU-intensiven Aufgaben werden in `multiprocessing.Array('u', 10000)` gespeichert. Diese Arrays ermöglichen es, Text zwischen den beiden Prozessen auszutauschen, sodass das Ergebnis einer CPU-Berechnung, die im einen GUI gestartet wurde, im anderen GUI angezeigt wird.

### c) Hintergrundüberwachung der CPU-Auslastung
In beiden GUIs wird die CPU-Auslastung regelmäßig überwacht und auf dem Bildschirm angezeigt. Die Methode `update_cpu_usage()` sorgt dafür, dass die aktuelle CPU-Auslastung angezeigt wird, und gibt einen Eindruck davon, wie stark die CPU durch die Berechnungen belastet wird.

---

## Fazit
Jedes GUI enthält Elemente zur Manipulation des Zählers, zum Starten CPU-intensiver Aufgaben und zur Überwachung der CPU-Auslastung. Durch die Verwendung von Multiprocessing können beide GUIs unabhängig voneinander agieren, während der Zählerstand und die Berechnungsergebnisse über das Shared Memory synchronisiert werden.




### 3. **Global Interpreter Lock (GIL)** und Python 3.13

Der **Global Interpreter Lock (GIL)** in Python sorgt dafür, dass immer nur ein Thread zur gleichen Zeit Python-Bytecode ausführen kann. Dies kann bei CPU-intensiven Berechnungen zu Engpässen führen, insbesondere wenn mehrere Threads versuchen, gleichzeitig zu laufen. 

**Was wurde in Python 3.13 geändert?**

- **Optimierung des GIL**: In Python 3.13 wurden Änderungen vorgenommen, um den GIL bei CPU-intensiven Aufgaben effizienter zu machen, sodass Threads weniger Zeit blockiert werden. Dies sollte eine Verbesserung der Multithreading-Leistung bei CPU-lastigen Anwendungen bringen.
  
### Zusammenfassung: Wie wird GIL, Multithreading und Multiprocessing verwendet?

1. **Multiprocessing**: Du startest zwei unabhängige Prozesse für die beiden GUIs. Jeder Prozess läuft auf einem eigenen CPU-Kern, was bedeutet, dass sie parallele Aufgaben unabhängig voneinander durchführen können. Dies zeigt die Stärke von Multiprocessing, da der GIL keine Rolle zwischen Prozessen spielt.

2. **Multithreading**: Innerhalb jedes GUI-Prozesses verwendest du **Multithreading**, um CPU-intensive Aufgaben in separaten Threads auszuführen. Dies testet die Effizienz des GIL, insbesondere bei CPU-lastigen Aufgaben. Durch die Verbesserungen in Python 3.13 sollte der GIL weniger blockierend sein, was sich in einer besseren Leistung bei der Ausführung mehrerer Threads zeigt.

3. **GIL in Python 3.13**: Da jeder Prozess (in diesem Fall jede GUI) unabhängig auf verschiedenen CPU-Kernen laufen kann, profitieren die Threads von den neuen Optimierungen des GIL in Python 3.13. Wenn du die CPU-intensive Berechnung in einem Thread ausführst, wird der GIL weniger blockiert, und die Threads sollten effizienter laufen als in früheren Python-Versionen.

### Fazit:
- **Multiprocessing** sorgt dafür, dass die beiden GUIs parallel laufen, unabhängig voneinander agieren und von der Optimierung des Betriebssystems für verschiedene CPU-Kerne profitieren.
- **Multithreading** wird innerhalb der GUI-Prozesse verwendet, um rechenintensive Aufgaben parallel auszuführen. Hierbei wird der Einfluss des **GIL** auf die Parallelität getestet. Die Verbesserungen in Python 3.13 sollen dazu führen, dass diese Threads flüssiger und mit weniger Blockierungen durch den GIL laufen.
