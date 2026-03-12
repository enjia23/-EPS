import tkinter as tk
from tkinter import ttk
import serial

# ⚙️ Serial configuration
SERIAL_PORT = '/dev/ttyUSB0'   # Example: 'COM3' (Windows) or '/dev/ttyUSB0' (Linux)
BAUD_RATE = 9600

# Try to connect to Arduino
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Connected to serial port: {SERIAL_PORT}")
except Exception as e:
    ser = None
    print("⚠️ Serial connection failed:", e)

# -------------------------
# 🖼️ Tkinter GUI setup
# -------------------------
root = tk.Tk()
root.title("Arduino Battery Voltage Monitor")
root.geometry("520x520")
root.configure(bg="#f0f2f5")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 12), background="#f0f2f5")
style.configure("Card.TFrame", background="white", relief="ridge", borderwidth=2)
style.configure("Title.TLabel", font=("Arial", 14, "bold"), background="white", foreground="#333")

voltage_labels = []
previous_voltages = [None] * 6  # Store last voltages

# -------------------------
# 🔋 Battery cards
# -------------------------
for i in range(6):
    frame = ttk.Frame(root, style="Card.TFrame", padding=15)
    frame.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="nsew")

    title = ttk.Label(frame, text=f"Battery {i+1}", style="Title.TLabel")
    title.pack(pady=5)

    label = ttk.Label(frame, text="Voltage: --- V", font=("Arial", 12))
    label.pack()
    voltage_labels.append(label)

# -------------------------
# ⚡ EPS (total voltage) card
# -------------------------
eps_frame = ttk.Frame(root, style="Card.TFrame", padding=15)
eps_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=15, sticky="nsew")

eps_title = ttk.Label(eps_frame, text="EPS (Total)", style="Title.TLabel")
eps_title.pack(pady=5)

eps_voltage_label = ttk.Label(eps_frame, text="Total Voltage: --- V", font=("Arial", 12))
eps_voltage_label.pack()

# -------------------------
# 🔄 Read Arduino data
# -------------------------
def read_from_arduino():
    if not ser:
        root.after(1000, read_from_arduino)
        return

    if ser.in_waiting:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            values = line.split(',')

            if len(values) == 6:
                for i in range(6):
                    try:
                        voltage = float(values[i])
                        prev_voltage = previous_voltages[i]
                        previous_voltages[i] = voltage

                        # Color logic (↑ red, ↓ green)
                        if prev_voltage is not None:
                            if voltage > prev_voltage:
                                color = "#b22222"  # red
                            elif voltage < prev_voltage:
                                color = "#006400"  # green
                            else:
                                color = "black"
                        else:
                            color = "black"

                        text = f"Voltage: {voltage:.2f} V"

                        # Per-cell voltage range check
                        if voltage < 3.0:
                            text += " ⚠️ Low"
                            color = "#b22222"
                        elif voltage > 4.25:
                            text += " ⚠️ High"
                            color = "#b22222"

                        voltage_labels[i].config(text=text, foreground=color)

                    except ValueError:
                        voltage_labels[i].config(text="Voltage: Error", foreground="black")

                # EPS total voltage (batteries 4–6)
                try:
                    if all(isinstance(v, (int, float)) for v in previous_voltages[3:6]):
                        eps_sum = sum(previous_voltages[3:6])
                        text = f"Total Voltage: {eps_sum:.2f} V"

                        # ⚙️ EPS voltage range check
                        if eps_sum < 24.0:
                            text += " ⚠️ Undervoltage"
                            color = "#b22222"
                        elif eps_sum > 26.0:
                            text += " ⚠️ Overvoltage"
                            color = "#b22222"
                        else:
                            color = "black"

                        eps_voltage_label.config(text=text, foreground=color)
                    else:
                        eps_voltage_label.config(text="Total Voltage: Calculating...", foreground="black")

                except Exception as e:
                    print("EPS calculation error:", e)
                    eps_voltage_label.config(text="Total Voltage: Error", foreground="#b22222")

        except Exception as e:
            print("Read error:", e)

    root.after(1000, read_from_arduino)

# Start reading loop
root.after(1000, read_from_arduino)
root.mainloop()
