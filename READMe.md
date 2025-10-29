# 🧠 Key Stroke Tool

A **secure, privacy-respecting keystroke dynamics analysis tool** built in Python with a modern GUI.  
It measures **typing behavior** (the timing patterns between key presses) to detect anomalies and generate meaningful insights — ideal for behavioral biometrics, insider threat detection, and secure access validation.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Reports](#reports)
- [Alerts](#alerts)
- [Tech Stack](#tech-stack)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Author](#author)

---

## 🧩 Overview
The **Key Stroke Tool** captures your typing rhythm — measuring time intervals between key presses and releases — and learns your unique behavioral pattern.  
Once a baseline is established, it can continuously monitor typing activity to **detect anomalies** that might indicate unauthorized access or unusual behavior.

---

## ✨ Features
✅ **Baseline Enrollment** – Records multiple sessions to learn your unique typing profile  
✅ **Anomaly Detection** – Compares live data against your baseline to detect deviations  
✅ **GUI Dashboard** – Smooth, responsive Tkinter interface with Matplotlib graphs  
✅ **Reports** – Generates detailed `.json` and `.html` reports  
✅ **Alert System** – Sends summarized results to **Telegram** or **Discord** webhooks  
✅ **Privacy-Focused** – All detailed data is stored locally; no external logging  
✅ **Installer** – Distributed as a clean `.exe` installer built via Inno Setup  

---

## ⚙️ How It Works
1. **Data Capture** – Logs the time between each key press and release  
2. **Feature Extraction** – Computes statistical metrics (mean, deviation, etc.)  
3. **Baseline Modeling** – Creates a profile representing your normal typing pattern  
4. **Anomaly Detection** – Calculates deviations in real-time  
5. **Reporting & Alerts** – Summarizes the results and optionally sends alerts

🚀 Usage

Launch the tool:
Key Stroke Tool.exe

Click Enroll Baseline and type the sample text N times

Start Protection Mode to monitor typing

View Reports in JSON or HTML format

(Optional) Configure Telegram/Discord Webhooks for alerts

📊 Reports

Reports include:

Typing Session Metadata

Average Key Interval

Outlier Analysis

Anomaly Score

Timestamped Summary

Example file:

reports/session_2025-10-26_17-30.html

🔔 Alerts

You can integrate your Telegram Bot or Discord webhook to receive summarized anomaly alerts in real time:

TELEGRAM_WEBHOOK_URL = "https://api.telegram.org/bot<token>/sendMessage"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/<id>/<token>"

🧱 Tech Stack
Component	Technology
Language	Python
GUI	Tkinter
Graphs	Matplotlib
Packaging	PyInstaller
Installer	Inno Setup
Data Format	JSON / HTML
Alerts	Telegram & Discord Webhooks
🚧 Future Enhancements

AI-based adaptive anomaly scoring

Keyboard layout–independent profiling

Cloud-based dashboard for central monitoring

Secure profile encryption

📜 License

This project is licensed under the MIT License.
See the LICENSE
 file for more details.

👩‍💻 Author

Abiha
🔗 Abiha0421

💬 For feedback or contributions, open an issue or pull request.
