import wmi
import qrcode
import urllib.parse
import platform
import os
from datetime import datetime

print("Generando QR minimalista con fecha...")

try:
    # --- 1. OBTENER INFORMACIÓN ESENCIAL ---
    c = wmi.WMI()
    system_info = c.Win32_ComputerSystem()[0]
    bios_info = c.Win32_BIOS()[0]
    processor_info = c.Win32_Processor()[0]
    ram_gb = round(int(system_info.TotalPhysicalMemory) / (1024**3), 2)
    # Obtener almacenamiento total (sumando todos los discos físicos)
    storage_total_gb = 0
    for disk in c.Win32_DiskDrive():
        if disk.Size:
            storage_total_gb += int(disk.Size) / (1024**3)
    storage_total_gb = round(storage_total_gb, 2)

    marca = system_info.Manufacturer
    modelo = system_info.Model
    numero_serie = bios_info.SerialNumber.strip()
    nombre_equipo = platform.node()
    procesador = processor_info.Name.strip()
    fecha_registro = datetime.now().strftime("%Y-%m-%d")

    # --- 2. FORMATEAR TEXTO MÍNIMO ---
    info_texto_minimal = f"""
    PC: {nombre_equipo}
    S/N: {numero_serie}
    Marca/Modelo: {marca} {modelo}
    Procesador: {procesador}
    RAM: {ram_gb} GB
    Almacenamiento: {storage_total_gb} GB
    Registro: {fecha_registro}
    """
    print("Información recolectada:")
    print(info_texto_minimal.strip())

    # --- 3. CREAR EL DATA URI PARA EL ARCHIVO .TXT ---
    texto_codificado = urllib.parse.quote(info_texto_minimal.strip())
    data_uri = f"data:text/plain;charset=utf-8,{texto_codificado}"

    # --- 4. GENERAR EL CÓDIGO QR CON BAJA CORRECCIÓN DE ERRORES ---
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(info_texto_minimal.strip())
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")

    # Obtener ruta del escritorio
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    nombre_archivo = f"QR_MIN_{nombre_equipo}_{numero_serie}.png".replace(" ", "_")
    ruta_completa = os.path.join(escritorio, nombre_archivo)
    img_qr.save(ruta_completa)

    print(f"\n¡Éxito! Se ha guardado el código QR en '{ruta_completa}'")

except Exception as e:
    print(f"Ocurrió un error: {e}")