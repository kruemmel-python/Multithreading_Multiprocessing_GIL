# Multithreading und Multiprocessing mit Python 3.13

Dieses Projekt zeigt, wie Multithreading und Multiprocessing in Python 3.13 verwendet werden können, um parallele Aufgaben zu verarbeiten. Es werden zwei verschiedene Ansätze zur Parallelisierung in Python demonstriert:

1. **Code 1**: Multithreading und Multiprocessing in einem einfachen Setup ohne GUIs.
2. **Code 2**: Multithreading und Multiprocessing mit zwei parallelen GUIs, die auf eine gemeinsam genutzte Ressource zugreifen.

## Unterschiede zwischen Code 1 und Code 2 im Umgang mit dem Global Interpreter Lock (GIL)

### GIL in Python

Der **Global Interpreter Lock (GIL)** ist ein Mechanismus in der Python-Interpreter-Implementierung (CPython), der verhindert, dass mehrere native Threads gleichzeitig Python-Bytecode ausführen. Der GIL sorgt dafür, dass in einem multithreaded Python-Programm immer nur ein Thread zur gleichen Zeit Python-Code ausführen kann, was die parallele Ausführung auf Mehrkernsystemen einschränkt.

### **Code 1**: Multithreading und Multiprocessing ohne GUIs

In **Code 1** wird Multithreading innerhalb von Prozessen verwendet:

- **Verwendung von Threads und Prozessen**: Es werden zwei **Prozesse** erstellt, die jeweils **mehrere Threads** starten, um Aufgaben parallel auszuführen.
- **GIL-Beschränkungen**: Da Python-Threads denselben Prozess teilen, greift der GIL, was bedeutet, dass nur ein Thread gleichzeitig ausgeführt wird, selbst wenn mehrere CPU-Kerne verfügbar sind.
- **Nachteile bei CPU-gebundenen Aufgaben**: Bei CPU-intensiven Aufgaben kann der GIL die Ausführung verlangsamen, da nur ein Thread zur gleichen Zeit Python-Code ausführen kann. Auf Mehrkernsystemen wird echte Parallelität durch den GIL verhindert.
- **Geeignet für I/O-gebundene Aufgaben**: Für I/O-gebundene Aufgaben, wie Dateizugriffe oder Netzwerkoperationen, kann der GIL freigegeben werden, was die Effizienz von Multithreading erhöht.

### **Code 2**: Multithreading und Multiprocessing mit separaten GUIs

**Code 2** umgeht die GIL-Beschränkungen durch die Verwendung von **Multiprocessing** für die beiden GUIs:

- **Verwendung von Prozessen für GUIs**: In Code 2 werden zwei separate **Prozesse** gestartet, die jeweils ein GUI darstellen. Diese Prozesse laufen unabhängig voneinander und nutzen denselben Zähler, der über **shared memory** (gemeinsamer Speicher) synchronisiert wird.
- **Umgehung des GIL durch Prozesse**: Da jeder Prozess seinen eigenen Python-Interpreter und Speicherbereich hat, wird der GIL **pro Prozess** angewendet. Dies ermöglicht echte Parallelität auf Mehrkernsystemen, da jeder Prozess auf einem separaten CPU-Kern ausgeführt werden kann.
- **Effizienz bei CPU-gebundenen Aufgaben**: Da der GIL nur innerhalb eines Prozesses wirkt, können CPU-intensive Aufgaben auf verschiedene Prozesse aufgeteilt und parallel auf mehreren Kernen ausgeführt werden, ohne durch den GIL gebremst zu werden.
- **GUI-Reaktionsfähigkeit**: Innerhalb jedes Prozesses können weiterhin Threads verwendet werden, um GUI-Aufgaben wie die Verarbeitung von Benutzereingaben auszuführen. Da diese Aufgaben oft I/O-gebunden sind, wird die GIL-Beschränkung innerhalb eines Prozesses kaum spürbar sein.

### Zusammenfassung des Vergleichs

| Aspekt                      | **Code 1: Multithreading & Multiprocessing (ohne GUI)** | **Code 2: Multithreading & Multiprocessing mit GUIs** |
|-----------------------------|----------------------------------------------------------|-------------------------------------------------------|
| **GIL-Beschränkungen**       | Der GIL verhindert echte Parallelität innerhalb eines Prozesses. | Der GIL wird pro Prozess angewendet und behindert daher nicht die Parallelität zwischen Prozessen. |
| **Parallelität**             | Threads innerhalb eines Prozesses sind auf den GIL beschränkt. | Prozesse können auf mehreren CPU-Kernen unabhängig voneinander laufen und echte Parallelität erreichen. |
| **Effizienz bei CPU-Aufgaben**| CPU-intensive Threads werden durch den GIL gebremst. | CPU-intensive Aufgaben können in separaten Prozessen effizient ausgeführt werden. |
| **Speicherverwaltung**       | Threads teilen sich den Speicher im selben Prozess. | Jeder Prozess hat seinen eigenen Speicher. Gemeinsame Ressourcen werden über Shared Memory synchronisiert. |
| **Verwendete Techniken**     | Threads innerhalb von Prozessen für parallele Aufgaben. | Separate Prozesse für jede GUI, die parallel auf mehreren CPU-Kernen laufen können. |

### Wie Sphinx die Dokumentation integriert

Die Sphinx-Dokumentation dieses Projekts zeigt detailliert, wie Multithreading und Multiprocessing in den beiden Codes umgesetzt wird. Die wichtigsten Funktionen und Module sind dokumentiert, um die Implementierung von parallelen Prozessen und Threads verständlich zu machen.

## Installation und Ausführung

1. **Clone das Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
