import tkinter as tk
from tkinter import font, ttk
import platform
import subprocess
from datetime import datetime, timedelta
import sv_ttk

countdown_job_id = None

def schedule():
    global countdown_job_id
    
    if countdown_job_id:
        window.after_cancel(countdown_job_id)
        countdown_job_id = None

    try:
        mode = mode_var.get()
        if mode == "countdown":
            hours = int(entry_hours.get() or 0)
            minutes = int(entry_minutes.get() or 0)
            seconds = int(entry_seconds.get() or 0)
            total_seconds = (hours * 3600) + (minutes * 60) + seconds
        else: 
            target_hour = int(entry_target_hour.get() or 0)
            target_minute = int(entry_target_minute.get() or 0)
            
            now = datetime.now()
            target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            
            if now >= target_time:
                target_time += timedelta(days=1)
            
            total_seconds = int((target_time - now).total_seconds())

        if total_seconds <= 0:
            update_status("Błąd: Czas docelowy musi być w przyszłości.", "orange")
            return

        action_choice = action_var.get()
        command = ["shutdown"]
        
        if action_choice == "Uruchom Ponownie":
            command.append("/r")
        else: 
            command.append("/s")

        if force_var.get():
            command.append("/f")

        command.extend(["/t", str(total_seconds)])

        subprocess.run(command, check=True)
        
        final_target_time = datetime.now() + timedelta(seconds=total_seconds)
        start_countdown(final_target_time)
        toggle_ui_elements(disabled=True)

    except ValueError:
        update_status("Błąd: Proszę wprowadzić poprawne liczby.", "red")
    except subprocess.CalledProcessError:
        update_status("Błąd: Uruchom program jako administrator.", "red")
    except Exception as e:
        update_status(f"Nieznany błąd: {e}", "red")

def cancel_shutdown():
    global countdown_job_id
    try:
        subprocess.run(["shutdown", "/a"], check=True)
        
        if countdown_job_id:
            window.after_cancel(countdown_job_id)
            countdown_job_id = None
        
        update_status("Anulowano planowane zadanie.", "blue")
        toggle_ui_elements(disabled=False)

    except subprocess.CalledProcessError:
        update_status("Brak zadania do anulowania.", "orange")

def start_countdown(target_time):
    update_status_countdown(target_time)

def update_status_countdown(target_time):
    global countdown_job_id
    
    time_remaining = target_time - datetime.now()
    
    if time_remaining.total_seconds() > 0:
        hours, rem = divmod(int(time_remaining.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        countdown_text = f"Pozostało: {hours:02d}:{minutes:02d}:{seconds:02d}"
        status_label.config(text=countdown_text, foreground="green")
        
        countdown_job_id = window.after(1000, lambda: update_status_countdown(target_time))
    else:
        update_status("Czas minął. Wykonywanie akcji...", "green")
        toggle_ui_elements(disabled=False)

def update_status(message, color):
    status_label.config(text=message, foreground=color)

def toggle_ui_elements(disabled):
    all_widgets = [action_menu, mode_countdown, mode_specific_time,
                   entry_hours, entry_minutes, entry_seconds,
                   entry_target_hour, entry_target_minute,
                   force_checkbox, schedule_button] + preset_buttons

    for widget in all_widgets:
        if disabled:
            widget.config(state="disabled")
        else:
            if widget == action_menu:
                widget.config(state="readonly")
            else:
                widget.config(state="enabled")

def toggle_mode(*args):
    if mode_var.get() == "countdown":
        countdown_frame.pack(pady=5, fill="x", expand=True)
        specific_time_frame.pack_forget()
    else:
        countdown_frame.pack_forget()
        specific_time_frame.pack(pady=5, fill="x", expand=True)

def set_preset(minutes):
    hours, mins = divmod(minutes, 60)
    entry_hours.delete(0, 'end'); entry_hours.insert(0, str(hours))
    entry_minutes.delete(0, 'end'); entry_minutes.insert(0, str(mins))
    entry_seconds.delete(0, 'end'); entry_seconds.insert(0, "0")
    update_status(f"Ustawiono preset: {minutes} minut.", "gray")

def reset_fields():
    entry_hours.delete(0, 'end'); entry_hours.insert(0, "0")
    entry_minutes.delete(0, 'end'); entry_minutes.insert(0, "0")
    entry_seconds.delete(0, 'end'); entry_seconds.insert(0, "0")
    entry_target_hour.delete(0, 'end'); entry_target_hour.insert(0, "23")
    entry_target_minute.delete(0, 'end'); entry_target_minute.insert(0, "00")
    update_status("Pola zresetowane.", "gray")

window = tk.Tk()
window.title("Zaawansowany Planer Systemu")
window.geometry("420x450")
window.resizable(False, False)
sv_ttk.set_theme("dark")

action_frame = ttk.LabelFrame(window, text="1. Wybierz Akcję")
action_frame.pack(pady=10, padx=10, fill="x")
action_var = tk.StringVar(value="Zamknij")
action_menu = ttk.Combobox(action_frame, textvariable=action_var, values=["Zamknij", "Uruchom Ponownie"], state="readonly")
action_menu.pack(pady=5, padx=10, fill="x")

time_frame = ttk.LabelFrame(window, text="2. Ustaw Czas")
time_frame.pack(pady=10, padx=10, fill="x")

mode_var = tk.StringVar(value="countdown")
mode_countdown = ttk.Radiobutton(time_frame, text="Odliczanie", variable=mode_var, value="countdown", command=toggle_mode)
mode_countdown.pack(anchor="w", padx=10)
mode_specific_time = ttk.Radiobutton(time_frame, text="Konkretna Godzina", variable=mode_var, value="specific_time", command=toggle_mode)
mode_specific_time.pack(anchor="w", padx=10)

countdown_frame = ttk.Frame(time_frame)
countdown_inputs_frame = ttk.Frame(countdown_frame)
ttk.Label(countdown_inputs_frame, text="H:").grid(row=0, column=0); entry_hours = ttk.Entry(countdown_inputs_frame, width=5, justify='center'); entry_hours.grid(row=0, column=1); entry_hours.insert(0, "0")
ttk.Label(countdown_inputs_frame, text="M:").grid(row=0, column=2); entry_minutes = ttk.Entry(countdown_inputs_frame, width=5, justify='center'); entry_minutes.grid(row=0, column=3); entry_minutes.insert(0, "0")
ttk.Label(countdown_inputs_frame, text="S:").grid(row=0, column=4); entry_seconds = ttk.Entry(countdown_inputs_frame, width=5, justify='center'); entry_seconds.grid(row=0, column=5); entry_seconds.insert(0, "0")
countdown_inputs_frame.pack(pady=5)

preset_frame = ttk.Frame(countdown_frame)
preset_buttons = [
    ttk.Button(preset_frame, text="30 min", command=lambda: set_preset(30)),
    ttk.Button(preset_frame, text="1 godz.", command=lambda: set_preset(60)),
    ttk.Button(preset_frame, text="2 godz.", command=lambda: set_preset(120))
]
for btn in preset_buttons: btn.pack(side="left", padx=5, expand=True, fill="x")
preset_frame.pack(pady=5)

specific_time_frame = ttk.Frame(time_frame)
ttk.Label(specific_time_frame, text="Godzina (HH:MM):").pack(side="left", padx=10)
entry_target_hour = ttk.Entry(specific_time_frame, width=5, justify='center'); entry_target_hour.pack(side="left"); entry_target_hour.insert(0, "23")
ttk.Label(specific_time_frame, text=":").pack(side="left")
entry_target_minute = ttk.Entry(specific_time_frame, width=5, justify='center'); entry_target_minute.pack(side="left"); entry_target_minute.insert(0, "00")

options_frame = ttk.LabelFrame(window, text="3. Opcje i Kontrola")
options_frame.pack(pady=10, padx=10, fill="x")

force_var = tk.BooleanVar()
force_checkbox = ttk.Checkbutton(options_frame, text="Wymuś zamknięcie (ignoruj niezapisane programy)", variable=force_var)
force_checkbox.pack(anchor="w", padx=10)

button_frame = ttk.Frame(options_frame)
schedule_button = ttk.Button(button_frame, text="✅ Zaplanuj", style="Accent.TButton", command=schedule)
schedule_button.pack(side="left", padx=5, ipadx=10, ipady=5, fill="x", expand=True)
cancel_button = ttk.Button(button_frame, text="❌ Anuluj", command=cancel_shutdown)
cancel_button.pack(side="left", padx=5, ipadx=10, ipady=5, fill="x", expand=True)
reset_button = ttk.Button(button_frame, text="🔄 Resetuj", command=reset_fields)
reset_button.pack(side="left", padx=5, ipadx=10, ipady=5, fill="x", expand=True)
button_frame.pack(pady=10, fill="x")

status_label = ttk.Label(window, text="Witaj! Wybierz akcję i ustaw czas.", font=("Segoe UI", 12, "italic"), anchor="center")
status_label.pack(pady=20, padx=10, fill="x")

toggle_mode()
window.mainloop()