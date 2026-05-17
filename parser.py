import re
import argparse
import json
import csv

parser = argparse.ArgumentParser(description="Detecta fuerza bruta SSH en logs")
parser.add_argument("--archivo", type=str, required=True, help="Ruta al archivo log")
parser.add_argument("--umbral", type=int, default=3, help="Intentos mínimos para alerta (default: 3) ")
parser.add_argument("--formato", type=str, choices=['txt', 'json', 'csv'], default='txt', help="Formato de salida")

args = parser.parse_args()

with open(args.archivo) as f:
    contenido = f.read()

# Regex para hacer una lista de IPs
ip = re.findall(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)", contenido)

conteo_ip = {}
for x in ip:
    # Hacemos diccionario a partir de la lista de IP
    conteo_ip[x] = conteo_ip.get(x, 0) + 1 

if args.formato == 'json':
    # Creamos un diccionario limpio solo con las sospechosas para el JSON
    reporte_json = {}
    for key, value in conteo_ip.items():
        if value > args.umbral:
            reporte_json[key] = value
    #Convertimos el diccionario a JSON si hemos elegido JSON
    with open("reporte.json", "w") as f:
        json.dump(reporte_json, f, indent=4)
    print("[+] Reporte generado: reporte.json")

elif args.formato == 'csv':
    with open("reporte.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Intentos_Fallidos"])
        
        for key, value in conteo_ip.items():
            if value > args.umbral:
                writer.writerow([key, value])
    print("[+] Reporte generado: reporte.csv")

else:
    mensajes_peligrosos = []
    for key, value in conteo_ip.items():
        if value > args.umbral:
            mensaje = f"La IP: {key} ha hecho {value} intentos SSH.\n"
            mensajes_peligrosos.append(mensaje)

    with open("ip_peliglosas.txt", "w") as f:
        f.write("".join(mensajes_peligrosos))

    print("[+] Reporte generado: ip_peliglosas.txt")
    with open("ip_peliglosas.txt") as f:
        print(f.read())