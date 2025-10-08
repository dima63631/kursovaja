from db import get_connection
import tkinter as tk
from tkinter import ttk, messagebox
from classes.Client import Client
from classes.Hall import Hall
from classes.Booking import Booking
from classes.Payment import Payment

app = tk.Tk()
app.title("Система управління банкетним залом")
app.geometry("900x600")

notebook = ttk.Notebook(app)
notebook.pack(fill="both", expand=True)

clients_tab = ttk.Frame(notebook)
notebook.add(clients_tab, text="Клієнти")

tk.Label(clients_tab, text="ПІБ:").pack()
name_entry = tk.Entry(clients_tab)
name_entry.pack()

tk.Label(clients_tab, text="Контактна інформація:").pack()
contact_entry = tk.Entry(clients_tab)
contact_entry.pack()

clients_table = ttk.Treeview(clients_tab, columns=("ID", "FullName", "ContactInfo"), show="headings")
for col in ("ID", "FullName", "ContactInfo"):
    clients_table.heading(col, text=col)
clients_table.pack(expand=True, fill="both")

def load_clients():
    for row in clients_table.get_children():
        clients_table.delete(row)
    try:
        clients = Client.get_all()
        for c in clients:
            clients_table.insert('', tk.END, values=(c.id, c.full_name, c.contact_info))
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити клієнтів:\n{e}")

def add_client():
    full_name = name_entry.get().strip()
    contact_info = contact_entry.get().strip()

    if not full_name:
        messagebox.showerror("Помилка", "Введіть повне ім'я клієнта")
        return

    client = Client(full_name=full_name, contact_info=contact_info)
    try:
        client.save()
        messagebox.showinfo("Успіх", "Клієнта додано")
        name_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
        load_clients()
        update_combos()
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося додати клієнта:\n{e}")

def delete_client():
    selected = clients_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть клієнта.")
        return

    client_id = clients_table.item(selected[0])["values"][0]
    try:
        c = Client.get_by_id(client_id)
        c.delete()
        load_clients()
        update_combos()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def edit_client():
    selected = clients_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть клієнта для редагування.")
        return

    client_id = clients_table.item(selected[0])["values"][0]
    try:
        c = Client.get_by_id(client_id)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))
        return

    edit_win = tk.Toplevel(app)
    edit_win.title(f"Редагувати клієнта: {c.full_name}")

    tk.Label(edit_win, text="ПІБ:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    edit_name_entry = tk.Entry(edit_win)
    edit_name_entry.grid(row=0, column=1, padx=5, pady=5)
    edit_name_entry.insert(0, c.full_name)

    tk.Label(edit_win, text="Контактна інформація:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    edit_contact_entry = tk.Entry(edit_win)
    edit_contact_entry.grid(row=1, column=1, padx=5, pady=5)
    edit_contact_entry.insert(0, c.contact_info)

    def save_changes():
        new_name = edit_name_entry.get().strip()
        new_contact = edit_contact_entry.get().strip()

        if not new_name or not new_contact:
            messagebox.showwarning("Помилка", "Усі поля мають бути заповнені.")
            return

        c.full_name = new_name
        c.contact_info = new_contact
        try:
            c.save()
            load_clients()
            update_combos()
            edit_win.destroy()
            messagebox.showinfo("Успіх", "Дані клієнта оновлено.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    tk.Button(edit_win, text="Зберегти", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(clients_tab, text="Додати клієнта", command=add_client).pack(pady=5)
tk.Button(clients_tab, text="Редагувати клієнта", command=edit_client).pack(pady=5)
tk.Button(clients_tab, text="Видалити клієнта", command=delete_client).pack(pady=5)

halls_tab = ttk.Frame(notebook)
notebook.add(halls_tab, text="Зали")

tk.Label(halls_tab, text="Назва зали:").pack()
hall_name_entry = tk.Entry(halls_tab)
hall_name_entry.pack()

tk.Label(halls_tab, text="Площа:").pack()
hall_area_entry = tk.Entry(halls_tab)
hall_area_entry.pack()

tk.Label(halls_tab, text="Послуги:").pack()
hall_services_entry = tk.Entry(halls_tab)
hall_services_entry.pack()

tk.Label(halls_tab, text="Тариф/год:").pack()
hall_rate_entry = tk.Entry(halls_tab)
hall_rate_entry.pack()

halls_table = ttk.Treeview(halls_tab, columns=("ID", "Назва", "Площа", "Послуги", "Тариф", "Статус"), show="headings")
for col in ("ID", "Назва", "Площа", "Послуги", "Тариф", "Статус"):
    halls_table.heading(col, text=col)
halls_table.pack(expand=True, fill="both")

def load_hall():
    halls_table.delete(*halls_table.get_children())
    for h in Hall.get_all():
        halls_table.insert('', tk.END, values=(h.id, h.name, h.area, h.additional_services, h.hourly_rate, h.status))

def add_hall():
    try:
        name = hall_name_entry.get()
        area = float(hall_area_entry.get())
        services = hall_services_entry.get()
        rate = float(hall_rate_entry.get())

        hall = Hall(name, area, services, rate)
        hall.save()

        load_hall()
        hall_name_entry.delete(0, tk.END)
        hall_area_entry.delete(0, tk.END)
        hall_services_entry.delete(0, tk.END)
        hall_rate_entry.delete(0, tk.END)
        update_combos()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def edit_hall():
    selected = halls_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть залу для редагування.")
        return

    hall_id = halls_table.item(selected[0])["values"][0]
    try:
        h = Hall.get_by_id(hall_id)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))
        return

    edit_window = tk.Toplevel(app)
    edit_window.title(f"Редагувати залу: {h.name}")

    tk.Label(edit_window, text="Назва:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    name_entry.insert(0, h.name)

    tk.Label(edit_window, text="Площа:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    area_entry = tk.Entry(edit_window)
    area_entry.grid(row=1, column=1, padx=5, pady=5)
    area_entry.insert(0, str(h.area))

    tk.Label(edit_window, text="Послуги:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    services_entry = tk.Entry(edit_window)
    services_entry.grid(row=2, column=1, padx=5, pady=5)
    services_entry.insert(0, h.additional_services)

    tk.Label(edit_window, text="Тариф/год:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    rate_entry = tk.Entry(edit_window)
    rate_entry.grid(row=3, column=1, padx=5, pady=5)
    rate_entry.insert(0, str(h.hourly_rate))

    def save_changes():
        try:
            new_name = name_entry.get()
            new_area = float(area_entry.get())
            new_services = services_entry.get()
            new_rate = float(rate_entry.get())

            if not new_name:
                messagebox.showwarning("Помилка", "Назва не може бути порожньою.")
                return

            h.name = new_name
            h.area = new_area
            h.additional_services = new_services
            h.hourly_rate = new_rate
            h.save()

            load_hall()
            update_combos()
            edit_window.destroy()
        except ValueError:
            messagebox.showerror("Помилка", "Площа та тариф повинні бути числом.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    tk.Button(edit_window, text="Зберегти", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)

def delete_hall():
    selected = halls_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть залу.")
        return

    hall_id = halls_table.item(selected[0])["values"][0]
    try:
        h = Hall.get_by_id(hall_id)
        if messagebox.askyesno("Підтвердження", f"Видалити залу '{h.name}'?"):
            h.delete()
            load_hall()
            update_combos()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def change_hall_status():
    selected = halls_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть залу.")
        return

    hall_id = halls_table.item(selected[0])["values"][0]
    try:
        h = Hall.get_by_id(hall_id)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))
        return

    def save_status():
        new_status = status_var.get()
        h.status = new_status
        h.save()
        load_hall()
        status_win.destroy()

    status_win = tk.Toplevel(app)
    status_win.title("Змінити статус зали")

    status_var = tk.StringVar(value=h.status)
    statuses = ["Вільний", "Ремонт", "Заброньований"]
    for s in statuses:
        tk.Radiobutton(status_win, text=s, variable=status_var, value=s).pack(anchor="w")

    tk.Button(status_win, text="Зберегти", command=save_status).pack()

tk.Button(halls_tab, text="Додати залу", command=add_hall).pack(pady=5)
tk.Button(halls_tab, text="Редагувати залу", command=edit_hall).pack(pady=5)
tk.Button(halls_tab, text="Видалити залу", command=delete_hall).pack(pady=5)
tk.Button(halls_tab, text="Змінити статус зали", command=change_hall_status).pack(pady=5)

booking_tab = ttk.Frame(notebook)
notebook.add(booking_tab, text="Бронювання")

tk.Label(booking_tab, text="Клієнт:").pack()
client_combo = ttk.Combobox(booking_tab, state="readonly")
client_combo.pack()

tk.Label(booking_tab, text="Зала:").pack()
hall_combo = ttk.Combobox(booking_tab, state="readonly")
hall_combo.pack()

tk.Label(booking_tab, text="Дата бронювання (YYYY-MM-DD):").pack()
date_entry = tk.Entry(booking_tab)
date_entry.pack()

tk.Label(booking_tab, text="година:").pack()
hours_entry = tk.Entry(booking_tab)
hours_entry.pack()

bookings_table = ttk.Treeview(booking_tab, columns=("ID", "Client", "Hall", "Date", "Hours", "Cost", "Status"),
                              show="headings")
for col in ("ID", "Client", "Hall", "Date", "Hours", "Cost", "Status"):
    bookings_table.heading(col, text=col)
bookings_table.pack(expand=True, fill="both")

def update_combos():
    try:
        clients = Client.get_all()
        client_combo['values'] = [f"{c.id}: {c.full_name}" for c in clients]

        halls = Hall.get_all()
        hall_combo['values'] = [f"{h.id}: {h.name}" for h in halls if h.status == "Вільний"]
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося оновити списки:\n{e}")

def load_bookings():
    bookings_table.delete(*bookings_table.get_children())
    for b in Booking.get_all():
        client_name = Client.get_by_id(b.client_id).full_name if Client.get_by_id(b.client_id) else "??"
        hall_name = Hall.get_by_id(b.hall_id).name if Hall.get_by_id(b.hall_id) else "??"

        time_display = b.time
        if hasattr(b.time, 'total_seconds'):
            time_display = b.time.total_seconds() / 3600

        try:
            total_cost = b.total_cost
        except (TypeError, AttributeError):
            hall = Hall.get_by_id(b.hall_id)
            if hall and hasattr(b.time, 'total_seconds'):
                hours = b.time.total_seconds() / 3600
                total_cost = hours * hall.hourly_rate
            else:
                total_cost = 0

        bookings_table.insert('', tk.END,
                              values=(b.id, client_name, hall_name, b.date, time_display, total_cost, b.status))

def add_booking():
    client_val = client_combo.get()
    hall_val = hall_combo.get()
    date_str = date_entry.get().strip()
    hours = hours_entry.get().strip()

    if not client_val or not hall_val or not date_str or not hours:
        messagebox.showerror("Помилка", "Заповніть усі поля бронювання.")
        return

    try:
        client_id = int(client_val.split(":")[0])
        hall_id = int(hall_val.split(":")[0])
        duration = float(hours)

        booking = Booking(client_id=client_id, hall_id=hall_id, date=date_str, time=duration)
        booking.save()

        messagebox.showinfo("Успіх", "Бронювання додано.")
        date_entry.delete(0, tk.END)
        hours_entry.delete(0, tk.END)
        update_combos()
        load_bookings()
        load_hall()  # оновити статус зали
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def delete_booking():
    selected = bookings_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть бронювання.")
        return

    booking_id = bookings_table.item(selected[0])["values"][0]
    try:
        b = Booking.get_by_id(booking_id)
        if messagebox.askyesno("Підтвердження", "Видалити бронювання?"):
            b.delete()
            load_bookings()
            load_hall()
            update_combos()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def change_booking_status():
    selected = bookings_table.selection()
    if not selected:
        messagebox.showwarning("Увага", "Виберіть бронювання.")
        return

    booking_id = bookings_table.item(selected[0])["values"][0]
    try:
        b = Booking.get_by_id(booking_id)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))
        return

    status_win = tk.Toplevel(app)
    status_win.title("Змінити статус бронювання")

    tk.Label(status_win, text="Статус:").pack(pady=5)
    sv = tk.StringVar(value=b.status)
    tk.Radiobutton(status_win, text="Активне", variable=sv, value="Активне").pack(anchor="w")
    tk.Radiobutton(status_win, text="Скасоване", variable=sv, value="Скасоване").pack(anchor="w")

    def save_status():
        b.status = sv.get()
        b.save()
        load_bookings()
        load_hall()
        update_combos()
        status_win.destroy()

    tk.Button(status_win, text="Зберегти", command=save_status).pack(pady=10)

tk.Button(booking_tab, text="Змінити статус", command=change_booking_status).pack(pady=5)
tk.Button(booking_tab, text="Додати бронювання", command=add_booking).pack(pady=5)
tk.Button(booking_tab, text="Видалити бронювання", command=delete_booking).pack(pady=5)

# Вкладка "Історія"
history_tab = ttk.Frame(notebook)
notebook.add(history_tab, text="Історія")

search_frame = tk.Frame(history_tab)
search_frame.pack(pady=5)

search_label = tk.Label(search_frame, text="Пошук за ПІБ клієнта або назвою зали:")
search_label.pack(side="left")

search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=5)

history_table = ttk.Treeview(history_tab, columns=("ID", "Клієнт", "Зала", "Дата", "Тривалість", "Ціна", "Статус"),
                             show="headings")
for col in ("ID", "Клієнт", "Зала", "Дата", "Тривалість", "Ціна", "Статус"):
    history_table.heading(col, text=col)
history_table.pack(expand=True, fill="both")


def load_history(filter_term=""):
    history_table.delete(*history_table.get_children())
    bookings = Booking.get_all()
    for b in bookings:
        client = Client.get_by_id(b.client_id)
        hall = Hall.get_by_id(b.hall_id)

        client_name = client.full_name if client else "??"
        hall_name = hall.name if hall else "??"

        time_display = b.time
        if hasattr(b.time, 'total_seconds'):
            time_display = b.time.total_seconds() / 3600

        try:
            total_cost = b.total_cost
        except (TypeError, AttributeError):
            if hall and hasattr(b.time, 'total_seconds'):
                hours = b.time.total_seconds() / 3600
                total_cost = hours * hall.hourly_rate
            else:
                total_cost = 0

        if filter_term.lower() in client_name.lower() or filter_term.lower() in hall_name.lower():
            history_table.insert('', tk.END,
                                 values=(b.id, client_name, hall_name, b.date, time_display, total_cost, b.status))

def search_history():
    term = search_entry.get().strip()
    load_history(term)

tk.Button(search_frame, text="Пошук", command=search_history).pack(side="left")

payments_tab = ttk.Frame(notebook)
notebook.add(payments_tab, text="Платежі")

tk.Label(payments_tab, text="Бронювання:").pack()
payment_booking_combo = ttk.Combobox(payments_tab, state="readonly")
payment_booking_combo.pack()

tk.Label(payments_tab, text="Сума:").pack()
payment_amount_entry = tk.Entry(payments_tab)
payment_amount_entry.pack()

payments_table = ttk.Treeview(payments_tab, columns=("ID", "BookingID", "Amount", "Status"), show="headings")
for col in ("ID", "BookingID", "Amount", "Status"):
    payments_table.heading(col, text=col)
payments_table.pack(expand=True, fill="both")

def load_payments():
    payments_table.delete(*payments_table.get_children())
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Payment")
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    for row in rows:
        payments_table.insert(
            '', tk.END,
            values=(row['ID'], row['BookingID'], row['Amount'], row['Status'])
        )

def update_payment_booking_combo():
    # список бронювань
    vals = [f"{b.id}: {Client.get_by_id(b.client_id).full_name} / {Hall.get_by_id(b.hall_id).name}"
            for b in Booking.get_all()]
    payment_booking_combo['values'] = vals

def add_payment():
    sel = payment_booking_combo.get()
    amount = payment_amount_entry.get().strip()

    if not sel or not amount:
        messagebox.showwarning("Помилка", "Оберіть бронювання і введіть суму.")
        return

    booking_id = int(sel.split(":")[0])
    try:
        amt = float(amount)
        p = Payment(booking_id=booking_id, amount=amt)
        p.save()
        messagebox.showinfo("Успіх", "Платіж додано.")
        payment_amount_entry.delete(0, tk.END)
        load_payments()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))


def mark_paid():
    sel = payments_table.selection()
    if not sel:
        messagebox.showwarning("Увага", "Виберіть платіж.")
        return

    pay_id = payments_table.item(sel[0])['values'][0]
    p = Payment(booking_id=None, amount=None, payment_id=pay_id)
    try:
        p.mark_paid()
        load_payments()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

tk.Button(payments_tab, text="Додати платіж", command=add_payment).pack(pady=5)
tk.Button(payments_tab, text="Відмітити сплачено", command=mark_paid).pack(pady=5)

queries_tab = ttk.Frame(notebook)
notebook.add(queries_tab, text="Запит")


def clear_table():
    results_table.delete(*results_table.get_children())
    results_table["columns"] = []
    results_table["show"] = ""


def execute_custom_query(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        if query.lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            clear_table()
            results_table["columns"] = columns
            results_table["show"] = "headings"

            for col in columns:
                results_table.heading(col, text=col)
                results_table.column(col, width=120)

            for row in rows:
                results_table.insert("", tk.END, values=row)
        else:
            conn.commit()
            messagebox.showinfo("Успіх", "Запит виконано")
            clear_table()

        cursor.close()
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося виконати запит:\n{e}")
    finally:
        if conn:
            conn.close()

def count_payments():
    query = "SELECT COUNT(*) AS Кількість_оплат FROM Payment;"
    execute_custom_query(query)

btn_count_payments = tk.Button(queries_tab, text="Підрахунок оплат", command=count_payments)
btn_count_payments.pack(pady=5)

results_table = ttk.Treeview(queries_tab)
results_table.pack(expand=True, fill="both", pady=10)

load_clients()
load_hall()
load_bookings()
load_history()
update_combos()
update_payment_booking_combo()
load_payments()

app.mainloop()