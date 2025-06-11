
from tkinter import *
import tkintermapview

users: list = []


class User:
    def __init__(self, name, surname, location, posts):
        self.name = name
        self.surname = surname
        self.location = location
        self.posts = posts
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))

        return [latitude, longitude]


def add_user():
    zmienna_imie = entry_name.get()
    zmienna_nazwisko = entry_surname.get()
    zmienna_miejscowosc = entry_location.get()
    zmienna_posty = entry_posts.get()

    users.append(User(name=zmienna_imie, surname=zmienna_nazwisko, location=zmienna_miejscowosc, posts=zmienna_posty))

    print(users)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_location.delete(0, END)
    entry_posts.delete(0, END)
    entry_name.focus()
    show_users()


def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f"{idx + 1}. {user.name} {user.surname}")


def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()


def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    user_name = users[i].name
    user_surname = users[i].surname
    user_location = users[i].location
    user_posts = users[i].posts
    label_name_szczegoly_obiektow_wartosc.config(text=user_name)
    label_surname_szczegoly_obiektow_wartosc.config(text=user_surname)
    label_location_szczegoly_obiektow_wartosc.config(text=user_location)
    label_posts_szczegoly_obiektow_wartosc.config(text=user_posts)
    map_widget.set_position(users[i].coordinates[0], users[i].coordinates[1])
    map_widget.set_zoom(12)


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    user_name = users[i].name
    user_surname = users[i].surname
    user_location = users[i].location
    user_posts = users[i].posts
    entry_name.insert(0, user_name)
    entry_surname.insert(0, user_surname)
    entry_location.insert(0, user_location)
    entry_posts.insert(0, user_posts)

    button_dodaj_obiekt.config(text='Zapisz', command=lambda: update_users(i))


def update_users(i):
    zmienna_imie = entry_name.get()
    zmienna_nazwisko = entry_surname.get()
    zmienna_miejscowosc = entry_location.get()
    zmienna_posty = entry_posts.get()
    users[i].name = zmienna_imie
    users[i].surname = zmienna_nazwisko
    users[i].location = zmienna_miejscowosc
    users[i].post = zmienna_posty
    users[i].marker.delete()
    users[i].coordinates = users[i].get_coordinates()
    users[i].marker = map_widget.set_marker(users[i].coordinates[0], users[i].coordinates[1])
    print(users[i].coordinates)
    show_users()

    button_dodaj_obiekt.config(text='Dodaj pracownika', command=add_user)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_location.delete(0, END)
    entry_posts.delete(0, END)
    entry_name.focus()


root = Tk()
root.geometry("1200x800")
root.title("mapbook_kn")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=60, height=15)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=show_user_details)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz
label_ramka_formularz = Label(ramka_formularz, text="Formularz")
label_ramka_formularz.grid(row=0, column=0, columnspan=2)
label_name = Label(ramka_formularz, text="Imię:")
label_name.grid(row=1, column=0, sticky=W)
label_surname = Label(ramka_formularz, text="Nazwisko:")
label_surname.grid(row=2, column=0, sticky=W)
label_location = Label(ramka_formularz, text="Miejscowość:")
label_location.grid(row=3, column=0, sticky=W)
label_posts = Label(ramka_formularz, text="Posty")
label_posts.grid(row=4, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=3, column=1)
entry_posts = Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj użytkownika", command=add_user)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

# ramka_szczegoly_obiektu
label_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Szczegóły obiektu:")
label_szczegoly_obiektow.grid(row=0, column=0)
label_name_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Imię:")
label_name_szczegoly_obiektow.grid(row=1, column=0)
label_name_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text=".....")
label_name_szczegoly_obiektow_wartosc.grid(row=1, column=1)
label_surname_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Nazwisko:")
label_surname_szczegoly_obiektow.grid(row=1, column=2)
label_surname_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text=".....")
label_surname_szczegoly_obiektow_wartosc.grid(row=1, column=3)
label_location_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Miejscowość:")
label_location_szczegoly_obiektow.grid(row=1, column=4)
label_location_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text=".....")
label_location_szczegoly_obiektow_wartosc.grid(row=1, column=5)
label_posts_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Posty:")
label_posts_szczegoly_obiektow.grid(row=1, column=6)
label_posts_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text=".....")
label_posts_szczegoly_obiektow_wartosc.grid(row=1, column=7)


map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=2)

root.mainloop()