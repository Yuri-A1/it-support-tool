"""
Herramienta de diagnóstico rápido de conectividad y métricas del sistema.
Orientada a soporte técnico L1/L2 para agilizar la resolución de incidencias.
"""

import os
import platform
import socket
import datetime

def obtener_info_sistema():
    print("=" * 55)
    print("          DIAGNÓSTICO BÁSICO DEL SISTEMA")
    print("=" * 55)
    print(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema Operativo: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Nombre del equipo (Hostname): {platform.node()}")
    print(f"Arquitectura: {platform.machine()}")

def verificar_conectividad():
    print("\n" + "=" * 55)
    print("          PRUEBAS DE RED Y CONECTIVIDAD")
    print("=" * 55)

    # 1. Comprobar dirección IP local asignada
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        print(f"[OK] Dirección IP local detectada: {ip_local}")
    except Exception:
        print("[ALERTA] No se pudo determinar la IP local.")

    # 2. Prueba de resolución DNS
    dominios_prueba = ["google.com", "iesanclemente.net"]
    print("\nComprobando resolución de nombres (DNS):")
    for dominio in dominios_prueba:
        try:
            ip_resuelta = socket.gethostbyname(dominio)
            print(f"  [OK] {dominio} -> {ip_resuelta}")
        except socket.gaierror:
            print(f"  [ERROR] Falló la resolución para {dominio}")

    # 3. Comprobación de salida a Internet mediante Ping (ICMP)
    print("\nComprobando conexión a Internet (Ping a 8.8.8.8)...")
    parametro_ping = "-n 2" if platform.system().lower() == "windows" else "-c 2"
    comando = f"ping {parametro_ping} 8.8.8.8 > nul 2>&1" if platform.system().lower() == "windows" else f"ping {parametro_ping} 8.8.8.8 > /dev/null 2>&1"
    
    respuesta = os.system(comando)

    if respuesta == 0:
        print("[OK] Conexión a Internet activa y respondiendo.")
    else:
        print("[ERROR] Paquetes perdidos o sin salida a Internet.")

if __name__ == "__main__":
    obtener_info_sistema()
    verificar_conectividad()
