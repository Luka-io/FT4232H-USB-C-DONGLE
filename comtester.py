
import serial
from serial.tools import list_ports
import time

print("COM FINDER AND TESTER")

vid = input("Enter VID (hex, e.g., 0403): ")
pid = input("Enter PID (hex, e.g., 6011): ")
writer = input("Enter Serial Writer COM port (e.g., COM17): ")
baud = int(input("Enter baud rate (e.g., 9600): "))

def find_ports():
    return [
        p.device
        for p in list_ports.comports()
        if p.vid == int(vid, 16) and p.pid == int(pid, 16)
        and p.device != writer
    ]

ser = serial.Serial(writer, baud, timeout=0.1)
ports = find_ports()

print(f"\nWriter: {writer}")
print(f"Listening on: {ports}")
print("Waiting for adapters to receive 'Test'...\n")

port_serials = {}

for port in ports:
    try:
        port_serials[port] = serial.Serial(port, baud, timeout=0.05)
    except serial.SerialException as e:
        print(f"Cannot open {port}: {e}")

try:
    while True:
        ser.write(b"Test\r\n")
        ser.flush()

        for port, device in port_serials.items():
            data = device.read(device.in_waiting or 1)

            if b"Test" in data:
                print(f"[MATCH] {port} received: {data!r}")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
    for device in port_serials.values():
        device.close()
