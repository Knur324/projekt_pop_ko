from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup


class LocationEntity:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

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


class Person(LocationEntity):
    def __init__(self, name, surname, location):
        super().__init__(name + " " + surname, location)
        self.surname = surname


airports = []


def add_airport():
    name = entry_name.get()
    location = entry_location.get()
    airports.append(Airport(name, location))
    refresh_list()
    clear_entries()


def add_staff():
    if not airports:
        return
    selected_airport = airports[listbox_list.index(ACTIVE)]
    name = entry_name.get()
    surname = entry_surname.get()
    location = entry_location.get()
    person = Person(name, surname, location)
    selected_airport.staff.append(person)
    refresh_list()
    clear_entries()


def add_client():
    if not airports:
        return
    selected_airport = airports[listbox_list.index(ACTIVE)]
    name = entry_name.get()
    surname = entry_surname.get()
    location = entry_location.get()
    person = Person(name, surname, location)
    selected_airport.clients.append(person)
    refresh_list()
    clear_entries()


def refresh_list():
    listbox_list.delete(0, END)
    for i, airport in enumerate(airports):
        listbox_list.insert(END, f"{i + 1}. Lotnisko: {airport.name}")
        for s in airport.staff:
            listbox_list.insert(END, f"   - Pracownik: {s.name}")
        for c in airport.clients:
            listbox_list.insert(END, f"   - Klient: {c.name}")


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
                break
    elif typ == 'client':
        entity.marker.delete()
        for ap in airports:
            if entity in ap.clients:
                ap.clients.remove(entity)
                break
    refresh_list()


def flatten_data():
    flat = []
    for ap in airports:
        flat.append((ap, 'airport'))
        for s in ap.staff:
            flat.append((s, 'staff'))
        for c in ap.clients:
            flat.append((c, 'client'))
    return flat


def clear_entries():
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_location.delete(0, END)


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

# Map frame
map_widget = tkintermapview.TkinterMapView(frame_map, width=800, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()
