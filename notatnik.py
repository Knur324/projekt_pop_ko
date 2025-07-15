from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# GLOBALNA ZMIENNA FILTRA
current_filter = None


class LocationEntity:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [lat, lon]


class Airport(LocationEntity):
    def __init__(self, name, location):
        super().__init__(name, location)
        self.staff = []
        self.clients = []

    def update_marker_label(self):
        label = f"{self.name}\n"
        if self.staff:
            label += "Pracownicy:\n" + "\n".join(f" - {s.name}" for s in self.staff) + "\n"
        if self.clients:
            label += "Klienci:\n" + "\n".join(f" - {c.name}" for c in self.clients)
        self.marker.set_text(label)


class Person(LocationEntity):
    def __init__(self, name, surname, location):
        super().__init__(name + " " + surname, location)
        self.surname = surname


airports = []


def add_airport():
    name = entry_name.get()
    location = entry_location.get()
    airport = Airport(name, location)
    airports.append(airport)
    refresh_list()
    clear_entries()


def add_staff():
    index = listbox_list.index(ACTIVE)
    flat_list = flatten_data()
    if index >= len(flat_list):
        return
    entity, typ = flat_list[index]
    if typ != 'airport':
        return

    name = entry_name.get()
    surname = entry_surname.get()
    location = entry_location.get()
    person = Person(name, surname, location)
    entity.staff.append(person)
    entity.update_marker_label()
    refresh_list()
    clear_entries()


def add_client():
    index = listbox_list.index(ACTIVE)
    flat_list = flatten_data()
    if index >= len(flat_list):
        return
    entity, typ = flat_list[index]
    if typ != 'airport':
        return

    name = entry_name.get()
    surname = entry_surname.get()
    location = entry_location.get()
    person = Person(name, surname, location)
    entity.clients.append(person)
    entity.update_marker_label()
    refresh_list()
    clear_entries()


def edit_selected():
    index = listbox_list.index(ACTIVE)
    flat_list = flatten_data()
    if index >= len(flat_list):
        return
    entity, typ = flat_list[index]
    new_name = entry_name.get()
    new_surname = entry_surname.get()
    new_location = entry_location.get()
    if not new_name or not new_location:
        return

    if typ == 'airport':
        entity.name = new_name
        entity.location = new_location
        entity.coordinates = entity.get_coordinates()
        entity.marker.set_position(entity.coordinates[0], entity.coordinates[1])
        entity.update_marker_label()

    elif typ in ['staff', 'client']:
        entity.name = new_name + " " + new_surname
        entity.surname = new_surname
        entity.location = new_location
        entity.coordinates = entity.get_coordinates()
        entity.marker.set_position(entity.coordinates[0], entity.coordinates[1])
        entity.marker.set_text(entity.name)

    refresh_list()
    clear_entries()


def delete_selected():
    index = listbox_list.index(ACTIVE)
    flat_list = flatten_data()
    if index >= len(flat_list):
        return
    entity, typ = flat_list[index]
    if typ == 'airport':
        entity.marker.delete()
        airports.remove(entity)
    elif typ == 'staff':
        entity.marker.delete()
        for ap in airports:
            if entity in ap.staff:
                ap.staff.remove(entity)
                ap.update_marker_label()
                break
    elif typ == 'client':
        entity.marker.delete()
        for ap in airports:
            if entity in ap.clients:
                ap.clients.remove(entity)
                ap.update_marker_label()
                break
    refresh_list()


def flatten_data():
    flat = []
    filtered_airports = airports
    if current_filter:
        filtered_airports = [ap for ap in airports if current_filter.lower() in ap.name.lower()]
    sorted_airports = sorted(filtered_airports, key=lambda ap: ap.name.lower())
    for ap in sorted_airports:
        flat.append((ap, 'airport'))
        for s in sorted(ap.staff, key=lambda x: x.name.lower()):
            flat.append((s, 'staff'))
        for c in sorted(ap.clients, key=lambda x: x.name.lower()):
            flat.append((c, 'client'))
    return flat


def refresh_list():
    listbox_list.delete(0, END)
    filtered_airports = airports

    if current_filter:
        filtered_airports = [ap for ap in airports if current_filter.lower() in ap.name.lower()]

    sorted_airports = sorted(filtered_airports, key=lambda ap: ap.name.lower())
    for i, airport in enumerate(sorted_airports):
        listbox_list.insert(END, f"{i + 1}. Lotnisko: {airport.name}")
        sorted_staff = sorted(airport.staff, key=lambda s: s.name.lower())
        sorted_clients = sorted(airport.clients, key=lambda c: c.name.lower())
        for s in sorted_staff:
            listbox_list.insert(END, f"   - Pracownik: {s.name}")
        for c in sorted_clients:
            listbox_list.insert(END, f"   - Klient: {c.name}")


def clear_entries():
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_location.delete(0, END)


def apply_filter():
    global current_filter
    current_filter = entry_filter.get()
    refresh_list()


def clear_filter():
    global current_filter
    current_filter = None
    entry_filter.delete(0, END)
    refresh_list()


# --- GUI SETUP ---
root = Tk()
root.geometry("1200x800")
root.title("Airport Management")

frame_list = Frame(root)
frame_form = Frame(root)
frame_map = Frame(root)

frame_list.grid(row=0, column=0, rowspan=2)
frame_form.grid(row=0, column=1)
frame_map.grid(row=1, column=1)

# List frame
listbox_list = Listbox(frame_list, width=50, height=30)
listbox_list.pack()
Button(frame_list, text="Usuń zaznaczone", command=delete_selected).pack()
Button(frame_list, text="Edytuj zaznaczone", command=edit_selected).pack()

# Form frame
Label(frame_form, text="Imię/Nazwa").grid(row=0, column=0)
entry_name = Entry(frame_form)
entry_name.grid(row=0, column=1)

Label(frame_form, text="Nazwisko (dla osób)").grid(row=1, column=0)
entry_surname = Entry(frame_form)
entry_surname.grid(row=1, column=1)

Label(frame_form, text="Miejscowość").grid(row=2, column=0)
entry_location = Entry(frame_form)
entry_location.grid(row=2, column=1)

Button(frame_form, text="Dodaj lotnisko", command=add_airport).grid(row=3, column=0, columnspan=2)
Button(frame_form, text="Dodaj pracownika", command=add_staff).grid(row=4, column=0, columnspan=2)
Button(frame_form, text="Dodaj klienta", command=add_client).grid(row=5, column=0, columnspan=2)

Label(frame_form, text="Filtruj lotnisko").grid(row=6, column=0)
entry_filter = Entry(frame_form)
entry_filter.grid(row=6, column=1)

Button(frame_form, text="Filtruj", command=apply_filter).grid(row=7, column=0)
Button(frame_form, text="Pokaż wszystkie", command=clear_filter).grid(row=7, column=1)

# Map frame
map_widget = tkintermapview.TkinterMapView(frame_map, width=800, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()

