import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import threading, time, json, statistics, requests, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =============================
# CONFIGURATION
# =============================
BASELINE_FILE = "baseline.json"
RECORD_SECONDS = 10
THRESHOLD = 0.35

# =============================
# ALERT FUNCTIONS
# =============================
def send_telegram_alert(bot_token, chat_id, text):
    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": text})
        except:
            pass

def send_discord_alert(webhook_url, text):
    if webhook_url:
        try:
            requests.post(webhook_url, json={"content": text, "username": "Keystroke Monitor"})
        except:
            pass

# =============================
# MAIN CLASS
# =============================
class KeystrokeTool:
    def __init__(self, master):
        self.master = master
        master.title("Keystroke Dynamics Monitor")
        master.geometry("800x600")
        master.configure(bg="#121212")

        self.iki_data = []
        self.telegram_token = ""
        self.telegram_chat_id = ""
        self.discord_webhook = ""

        # ========== TITLE ==========
        ttk.Label(master, text="Keystroke Dynamics Monitor", font=("Segoe UI", 18, "bold")).pack(pady=10)

        # ========== CONTROL FRAME ==========
        frame = ttk.Frame(master)
        frame.pack(pady=10)

        ttk.Button(frame, text="Enroll Baseline", command=self.start_baseline_thread).grid(row=0, column=0, padx=10)
        ttk.Button(frame, text="Start Monitoring", command=self.start_protection_thread).grid(row=0, column=1, padx=10)
        ttk.Button(frame, text="Settings", command=self.open_settings).grid(row=0, column=2, padx=10)
        ttk.Button(frame, text="Show Graph", command=self.show_graph).grid(row=0, column=3, padx=10)

        # ========== PROGRESS + STATUS ==========
        self.progress = ttk.Progressbar(master, length=500, mode='determinate')
        self.progress.pack(pady=15)

        self.status_label = ttk.Label(master, text="Status: Idle", font=("Segoe UI", 11))
        self.status_label.pack(pady=5)

        # ========== GRAPH AREA ==========
        self.figure, self.ax = plt.subplots(figsize=(6, 3), facecolor="#222222")
        self.ax.set_title("Live IKI Values", color="white")
        self.ax.set_facecolor("#121212")
        self.ax.tick_params(colors="white")
        self.line, = self.ax.plot([], [], color="#00BFFF")

        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack(pady=10)

        # ========== STYLE ==========
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#121212")
        style.configure("TLabel", background="#121212", foreground="white")
        style.configure("TButton", background="#1f1f1f", foreground="white", padding=6)
        style.configure("Horizontal.TProgressbar", troughcolor='#2b2b2b', background='#00BFFF')

    # ======================================================
    # THREAD HANDLERS
    # ======================================================
    def start_baseline_thread(self):
        threading.Thread(target=self.enroll_baseline, daemon=True).start()

    def start_protection_thread(self):
        threading.Thread(target=self.start_protection, daemon=True).start()

    # ======================================================
    # BASELINE ENROLLMENT
    # ======================================================
    def enroll_baseline(self):
        self.status_label.config(text="Recording baseline... Type normally for 10 seconds.")
        self.progress["value"] = 0
        timestamps = []

        def on_press(key):
            timestamps.append(time.time())

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        start_time = time.time()
        while time.time() - start_time < RECORD_SECONDS:
            self.progress["value"] = ((time.time() - start_time) / RECORD_SECONDS) * 100
            self.master.update_idletasks()
            time.sleep(0.1)

        listener.stop()

        if len(timestamps) < 2:
            messagebox.showerror("Error", "No typing activity detected.")
            return

        ikis = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        mean_iki = statistics.mean(ikis)
        stdev_iki = statistics.stdev(ikis) if len(ikis) > 1 else 0.001

        with open(BASELINE_FILE, "w") as f:
            json.dump({"mean": mean_iki, "stdev": stdev_iki}, f, indent=2)

        self.status_label.config(text=f"Baseline saved. Mean IKI: {mean_iki:.4f}s")
        messagebox.showinfo("Baseline", f"Baseline saved!\nMean IKI: {mean_iki:.4f}s")

    # ======================================================
    # MONITORING SESSION
    # ======================================================
    def start_protection(self):
        if not os.path.exists(BASELINE_FILE):
            messagebox.showwarning("Missing Baseline", "Please create a baseline first.")
            return

        with open(BASELINE_FILE, "r") as f:
            baseline = json.load(f)

        mean_ref = baseline["mean"]
        stdev_ref = baseline["stdev"] or 0.001

        self.status_label.config(text="Monitoring active... Type normally.")
        self.iki_data = []
        timestamps = []

        def on_press(key):
            timestamps.append(time.time())
            if len(timestamps) > 1:
                ikis = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
                current_mean = statistics.mean(ikis[-10:])
                self.iki_data.append(current_mean)
                deviation = abs(current_mean - mean_ref) / stdev_ref

                # Update Graph
                self.update_graph()

                if deviation > THRESHOLD:
                    alert = f"⚠️ Anomaly detected!\nMean IKI: {current_mean:.4f}s\nDeviation: {deviation:.2f}"
                    send_telegram_alert(self.telegram_token, self.telegram_chat_id, alert)
                    send_discord_alert(self.discord_webhook, alert)
                    self.status_label.config(text="ALERT! Typing anomaly detected.")
                    messagebox.showwarning("ALERT", alert)

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        start_time = time.time()
        while time.time() - start_time < 60:
            self.progress["value"] = ((time.time() - start_time) / 60) * 100
            time.sleep(0.2)
            self.master.update_idletasks()

        listener.stop()
        self.status_label.config(text="Monitoring session complete.")
        messagebox.showinfo("Protection", "Monitoring finished successfully.")

    # ======================================================
    # REAL-TIME GRAPH
    # ======================================================
    def update_graph(self):
        self.ax.clear()
        self.ax.set_title("Live IKI Values", color="white")
        self.ax.set_facecolor("#121212")
        self.ax.tick_params(colors="white")
        if self.iki_data:
            self.ax.plot(self.iki_data, color="#00BFFF")
        self.canvas.draw()

    def show_graph(self):
        if not self.iki_data:
            messagebox.showinfo("Graph", "No typing data to display yet.")
            return
        self.update_graph()

    # ======================================================
    # SETTINGS
    # ======================================================
    def open_settings(self):
        settings = tk.Toplevel(self.master)
        settings.title("Settings")
        settings.geometry("400x300")
        settings.configure(bg="#121212")

        ttk.Label(settings, text="Telegram Bot Token:").pack(pady=5)
        token_entry = ttk.Entry(settings, width=40)
        token_entry.insert(0, self.telegram_token)
        token_entry.pack()

        ttk.Label(settings, text="Telegram Chat ID:").pack(pady=5)
        chat_entry = ttk.Entry(settings, width=40)
        chat_entry.insert(0, self.telegram_chat_id)
        chat_entry.pack()

        ttk.Label(settings, text="Discord Webhook URL:").pack(pady=5)
        webhook_entry = ttk.Entry(settings, width=40)
        webhook_entry.insert(0, self.discord_webhook)
        webhook_entry.pack()

        def save_settings():
            self.telegram_token = token_entry.get()
            self.telegram_chat_id = chat_entry.get()
            self.discord_webhook = webhook_entry.get()
            messagebox.showinfo("Settings", "Settings saved successfully.")
            settings.destroy()

        ttk.Button(settings, text="Save", command=save_settings).pack(pady=20)

# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    root = tk.Tk()
    app = KeystrokeTool(root)
    root.mainloop()




