# realtime/views.py
import serial
import serial.tools.list_ports
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from collections import deque
import json
import threading

buffer = deque(maxlen=100)

ser = serial.Serial('COM11', 115200)

def read_serial():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            data = json.loads(line)  # Pastikan format data sesuai: {'Fp1': 123, 'F3': 456, ...}
            buffer.append(data)
            print(data)
        except:
            continue

threading.Thread(target=read_serial, daemon=True).start()

def chart_view(request):
    return render(request, 'chart.html')

def api_data(request):
    if buffer:
        return JsonResponse(buffer[-1], safe=False)
    return JsonResponse({}, safe=False)

serial_conn = None
serial_thread = None
buffer = deque(maxlen=100)
port_config = {"port": "COM3", "baudrate": 115200}

def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

@csrf_exempt
def connect_serial(request):
    global serial_conn, serial_thread, port_config

    if request.method == 'POST':
        data = json.loads(request.body)
        port_config["port"] = data.get("port", "COM3")
        port_config["baudrate"] = int(data.get("baudrate", 115200))

        if serial_conn and serial_conn.is_open:
            serial_conn.close()

        try:
            serial_conn = serial.Serial(port_config["port"], port_config["baudrate"])
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

        def read_serial():
            while True:
                try:
                    line = serial_conn.readline().decode('utf-8').strip()
                    data = json.loads(line)
                    buffer.append(data)
                except:
                    continue

        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()
        return JsonResponse({"status": "connected"})
    return JsonResponse({"status": "invalid"})
    
def serial_ports_api(request):
    return JsonResponse({"ports": list_serial_ports()})

def chart_view(request):
    return render(request, 'chart.html')

def api_data(request):
    if buffer:
        return JsonResponse(buffer[-1], safe=False)
    return JsonResponse({}, safe=False)