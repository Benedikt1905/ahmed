import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# CSV-Datei Pfad
csv_datei = "C:\\Users\\AKH\\Downloads\\SOLDA_8_Projekt\\data\\Primärverbrauch DE.csv"

# Daten global laden
try:
    df_all = pd.read_csv(csv_datei, sep=';')
except Exception as e:
    df_all = pd.DataFrame()
    print("Fehler beim Laden der CSV:", e)

def update_dropdowns():
    if not df_all.empty:
        # Erste Spalte als Energieträger
        erste_spalte = df_all.columns[0]
        energietraeger_cb['values'] = sorted(df_all[erste_spalte].dropna().unique())
        # Jahr wie gehabt
        if 'Jahr' in df_all.columns:
            jahr_cb['values'] = sorted(df_all['Jahr'].dropna().unique())
        else:
            jahr_cb['values'] = []

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
        # Filter Energieträger (erste Spalte)
        erste_spalte = df.columns[0]
        if energietraeger_var.get():
            df = df[df[erste_spalte] == energietraeger_var.get()]
        # Filter Jahr
        if 'Jahr' in df.columns and jahr_var.get():
            df = df[df['Jahr'] == jahr_var.get()]

        # Tabelle leeren
        for row in treeview.get_children():
            treeview.delete(row)

        # Spalten setzen
        treeview["columns"] = list(df.columns)
        for col in df.columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=120, anchor="center")

        # Daten einfügen
        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))

        # Kreisdiagramm
        for widget in frame_chart.winfo_children():
            widget.destroy()
        # Pie nur wenn mindestens 2 Spalten und Werte vorhanden
        if len(df) > 0 and len(df.columns) > 1:
            labels = df[erste_spalte]
            # Nimm die zweite Spalte als Werte
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

# Event für Filter-Auswahl
def on_filter_selected(event):
    show_csv_data()

land_cb.bind("<<ComboboxSelected>>", on_land_selected)
energietraeger_cb.bind("<<ComboboxSelected>>", on_filter_selected)
jahr_cb.bind("<<ComboboxSelected>>", on_filter_selected)

# Filter-Button
filter_btn = tk.Button(frame_dropdown, text="Anzeigen", command=show_csv_data)
filter_btn.pack(side="left", padx=10)

# Frame für die Tabelle
frame_table = tk.Frame(root)
frame_table.pack(side="left", fill="both", expand=True)

treeview = ttk.Treeview(frame_table, show="headings")
treeview.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Frame für das Kreisdiagramm
frame_chart = tk.Frame(root)
frame_chart.pack(side="right", fill="both", expand=True)

# Standard: Land vorauswählen und Dropdowns/Daten anzeigen
land_var.set("Deutschland")
update_dropdowns()
show_csv_data()

root.mainloop()