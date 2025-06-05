import tkinter as tk
from tkinter import messagebox


LOGIN = "Knur"
PASSWORD = "324"


user_list = ["Anna Kowalska", "Jan Nowak", "Michał Zieliński", "Karolina Wiśniewska"]

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logowanie")

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="Login:").grid(row=0, column=0, sticky="e")
        tk.Label(self.frame, text="Hasło:").grid(row=1, column=0, sticky="e")

        self.login_entry = tk.Entry(self.frame)
        self.password_entry = tk.Entry(self.frame, show="*")

        self.login_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.frame, text="Zaloguj", command=self.check_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def check_login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login == LOGIN and password == PASSWORD:
            self.show_user_list()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

    def show_user_list(self):

        self.frame.destroy()

        tk.Label(self.root, text="Lista użytkowników:", font=("Arial", 14)).pack(pady=10)

        for user in user_list:
            tk.Label(self.root, text=user, font=("Arial", 12)).pack(anchor="w", padx=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")
    app = LoginApp(root)
    root.mainloop()
