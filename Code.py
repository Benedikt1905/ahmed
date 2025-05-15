import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# CSV-Datei Pfad
csv_datei = r"C:\Users\bkrings\Documents\Berufsschule\2. Lehrjahr\SODAL 8\GUI-Projekt mit CSV\Ahmed\SOLDA_8_Projekt\data\Primärverbrauch DE.csv"

# Daten global laden
try:
    df_all = pd.read_csv(csv_datei, sep=';')
except Exception as e:
    df_all = pd.DataFrame()
    print("Fehler beim Laden der CSV:", e)

def update_dropdowns():
    if not df_all.empty:
        # Energieträger aus erster Spalte
        erste_spalte = df_all.columns[0]
        energietraeger_cb['values'] = sorted(df_all[erste_spalte].dropna().unique())
        if energietraeger_cb['values']:
            energietraeger_cb.current(0)
        else:
            energietraeger_cb.set('')
        # Jahre aus den Spaltennamen ab der zweiten Spalte
        jahre = list(df_all.columns[1:])
        jahr_cb['values'] = jahre
        jahr_cb.set('')  # Kein Jahr vorauswählen!

def update_table(dataframe):
    try:
        treeview.delete(*treeview.get_children())
        for i, (_, row) in enumerate(dataframe.iterrows()):
            values = [row["Jahr"]] + list(row[1:])
            tag = "even" if i % 2 == 0 else "odd"
            treeview.insert("", "end", values=values, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Fehler beim Aktualisieren der Tabelle", str(e))

def show_csv_data():
    try:
        if land_var.get() != "Deutschland":
            # Tabelle und Diagramm leeren
            for row in treeview.get_children():
                treeview.delete(row)
            for widget in frame_chart.winfo_children():
                widget.destroy()
            return

        df = df_all.copy()
        erste_spalte = df.columns[0]
        # Filter Energieträger nur, wenn einer gewählt ist
        if energietraeger_var.get():
            df = df[df[erste_spalte] == energietraeger_var.get()]
        # Filter Jahr: Nur die Spalte für das gewählte Jahr anzeigen
        if jahr_var.get():
            jahr = jahr_var.get()
            df = df[[erste_spalte, jahr]]

        # Tabelle aktualisieren
        update_table(df)

        # Spalten setzen
        treeview["columns"] = list(df.columns)
        for col in df.columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=120, anchor="center")

        # Kreisdiagramm
        for widget in frame_chart.winfo_children():
            widget.destroy()
        if len(df) > 0 and len(df.columns) > 1:
            labels = df[erste_spalte]
            werte_spalte = df.columns[1]
            values = df[werte_spalte]
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title("Kreisdiagramm")
            canvas = FigureCanvasTkAgg(fig, master=frame_chart)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# Tkinter Fenster erstellen
root = tk.Tk()
root.title("CSV-Datenanzeige mit Kreisdiagramm und Filter")
root.geometry("1200x700")

# Style für die Tabelle
style = ttk.Style()
style.configure("Treeview",
                rowheight=25,
                font=("Arial", 16),
                borderwidth=1,
                relief="solid",
                background="white",
                fieldbackground="white")
style.configure("Treeview.Heading",
                font=("Arial", 18, "bold"),
                borderwidth=1,
                relief="solid")
style.map("Treeview",
          background=[("selected", "lightblue")],
          foreground=[("selected", "black")])
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

# Dropdown-Frame
frame_dropdown = tk.Frame(root)
frame_dropdown.pack(fill="x", padx=10, pady=5)

# Dropdown-Variablen
land_var = tk.StringVar()
energietraeger_var = tk.StringVar()
jahr_var = tk.StringVar()

# Dropdown-Menüs
tk.Label(frame_dropdown, text="Land:").pack(side="left")
land_cb = ttk.Combobox(frame_dropdown, textvariable=land_var, state="readonly")
land_cb['values'] = ["Deutschland"]
land_cb.pack(side="left", padx=5)

tk.Label(frame_dropdown, text="Energieträger:").pack(side="left")
energietraeger_cb = ttk.Combobox(frame_dropdown, textvariable=energietraeger_var, state="readonly")
energietraeger_cb.pack(side="left", padx=5)

tk.Label(frame_dropdown, text="Jahr:").pack(side="left")
jahr_cb = ttk.Combobox(frame_dropdown, textvariable=jahr_var, state="readonly")
jahr_cb.pack(side="left", padx=5)

# Event für Land-Auswahl
def on_land_selected(event):
    if land_var.get() == "Deutschland":
        update_dropdowns()
        show_csv_data()
    else:
        energietraeger_cb.set('')
        jahr_cb.set('')
        energietraeger_cb['values'] = []
        jahr_cb['values'] = []
        show_csv_data()

# Event für Jahr-Auswahl (Tabelle aktualisieren)
def on_jahr_selected(event):
    show_csv_data()

land_cb.bind("<<ComboboxSelected>>", on_land_selected)
jahr_cb.bind("<<ComboboxSelected>>", on_jahr_selected)
# Kein Event für energietraeger_cb, damit Tabelle nicht bei Energieträger-Wechsel aktualisiert wird

# Table-Frame
table_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
table_frame.pack(padx=10, pady=10)

# Tabelle
treeview = ttk.Treeview(table_frame, show="headings", height=10, style="Treeview")
treeview.pack(side="left", padx=5, pady=5, fill="both", expand=True)

# Scrollbar hinzufügen
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbar.set)

# Frame für das Kreisdiagramm
frame_chart = tk.Frame(root)
frame_chart.pack(side="right", fill="both", expand=True)

# Standard: Land vorauswählen und Dropdowns/Daten anzeigen
land_var.set("Deutschland")
update_dropdowns()
show_csv_data()

root.mainloop()