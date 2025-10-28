import tkinter as tk
from tkinter import messagebox
from collections import Counter
import threading
import psutil
import queue


class IDSAlerts:
    def __init__(self):
        self.root = None
        self.gui_ready = threading.Event()
        self.setup_gui()
        self.alert_queue = queue.Queue()
        self.cache = {}

        self.listbox = tk.Listbox(self.alert_frame, width=80, height=10)
        self.listbox.pack(padx=10, pady=5)

        self.terminate_button = None
        self.terminate_all_button = None
        self.show_features_button = None

    def setup_gui(self):
        def gui_thread():
            self.root = tk.Tk()
            self.root.withdraw()
            self._create_alert_window()
            self.gui_ready.set()
            self.root.mainloop()

        threading.Thread(target=gui_thread, daemon=True).start()
        self.gui_ready.wait()

    def _create_alert_window(self):
        self.alert_frame = tk.Toplevel(self.root)
        self.alert_frame.title("Sızma Tespit Edildi!")
        self.alert_frame.protocol("WM_DELETE_WINDOW", self._hide_alert_window)
        self.alert_frame.geometry("600x400")

        main_frame = tk.Frame(self.alert_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.alert_label = tk.Label(main_frame, text="", wraplength=580, justify="left", anchor="w", padx=10, pady=10)
        self.alert_label.pack(fill="x", expand=True)

        def on_resize(event):
            new_width = event.width
            self.alert_label.config(wraplength=new_width - 20)

        self.alert_frame.bind("<Configure>", on_resize)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=5)

        self.terminate_button = tk.Button(button_frame, text="Seçileni Durdur", command=self.terminate_selected,
                                          font=("Segoe UI", 10))
        self.terminate_button.pack(side="left", padx=5)

        self.terminate_all_button = tk.Button(button_frame, text="Tümünü Durdur", command=self.terminate_all,
                                              font=("Segoe UI", 10))
        self.terminate_all_button.pack(side="left", padx=5)

        self.show_features_button = tk.Button(button_frame, text="Akış Özelliklerini Göster",
                                              command=self.show_flow_features, font=("Segoe UI", 10))
        self.show_features_button.pack(side="left", padx=5)

        self._hide_alert_window()

    def _hide_alert_window(self):
        self.alert_frame.withdraw()

    def _is_alert_showing(self):
        return(hasattr(self, "alert_frame") and self.alert_frame.winfo_exists()
               and self.alert_frame.state() != "withdrawn")

    def start_monitor(self):
        def _check_queue():
            if not self._is_alert_showing() and not self.alert_queue.empty():
                self.show_alert()

            self.root.after(100, _check_queue)

        _check_queue()

    def add_alert(self, attack_type, batch_info, flow_features):
        self.alert_queue.put({"attack_type": attack_type, "batch_info": batch_info, "flow_features": flow_features})

    def terminate_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı!", "İşlem seçilmedi")
            return

        for i in reversed(selection):
            item = self.listbox.get(i)
            self._terminate_by_pid(item)
            self.listbox.delete(i)

    def terminate_all(self):
        while self.listbox.size() != 0:
            item = self.listbox.get(0)
            self._terminate_by_pid(item)
            self.listbox.delete(0)

        self._hide_alert_window()

    def show_flow_features(self):
        alert_data = self.cache
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı!", "Akış özelliklerini görmek istediğiniz işlemi seçiniz.")
            return

        for i in reversed(selection):
            messagebox.showinfo("Özellikler", f"{alert_data['flow_features'][i]}")

    def show_alert(self):
        if not self.gui_ready.is_set():
            return

        alert_data = self.alert_queue.get()
        self.cache = alert_data
        self.root.after(0, self._show_alert_window, alert_data["attack_type"], alert_data["batch_info"])

    def _terminate_by_pid(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
        except ProcessLookupError as e:
            messagebox.showerror("Hata!", f"İşlem bulunamadı -> Pid: {pid}, {str(e)}")
        except Exception as e:
            messagebox.showerror("Hata!", f"Durdurma başarısız -> Pid: {pid} , {str(e)}")

    def _show_alert_window(self, attack_type, batch_info):
        counts = Counter(attack_type)
        self.listbox.delete(0, tk.END)

        for pid in batch_info["pid"]:
            self.listbox.insert(tk.END, pid)

        full_text = f"Muhtemel tehditler tespit edildi: \n"

        for item, count in counts.items():
            full_text += f"{item} ({count}) "

        full_text += f"\nTehditlerle ilişkili işlemlerin bilgileri: \n"
        full_text += f"{batch_info}"

        self.alert_label.config(text=full_text, font=("Segoe UI", 10))

        self.alert_frame.deiconify()
        self.alert_frame.lift()
