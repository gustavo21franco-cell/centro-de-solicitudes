import os
import random
import string
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_CONTADOR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "contador_solicitudes.txt"
)


# ============================================================
# OBTENER SIGUIENTE NÚMERO
# ============================================================

def obtener_siguiente_numero():

    numero_actual = 0

    if os.path.exists(ARCHIVO_CONTADOR):

        try:
            with open(
                ARCHIVO_CONTADOR,
                "r",
                encoding="utf-8"
            ) as archivo:

                contenido = archivo.read().strip()

                if contenido:
                    numero_actual = int(contenido)

        except (ValueError, OSError):
            numero_actual = 0

    siguiente = numero_actual + 1

    try:

        with open(
            ARCHIVO_CONTADOR,
            "w",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                str(siguiente)
            )

    except OSError:
        pass

    return siguiente


# ============================================================
# GENERAR CÓDIGO DE VERIFICACIÓN
# ============================================================

def generar_codigo_verificacion():

    caracteres = string.ascii_uppercase + string.digits

    codigo = "".join(
        random.choice(caracteres)
        for _ in range(6)
    )

    return f"JTL-{codigo}"


# ============================================================
# GENERAR DATOS DE LA SOLICITUD
# ============================================================

def generar_datos_solicitud():

    ahora = datetime.now()

    numero = obtener_siguiente_numero()

    solicitud = (
        f"CS-{ahora.strftime('%Y%m%d')}-"
        f"{numero:07d}"
    )

    codigo = generar_codigo_verificacion()

    fecha_generada = ahora.strftime(
        "%d/%m/%Y %H:%M"
    )

    return {
        "solicitud": solicitud,
        "codigo": codigo,
        "generado": fecha_generada
    }


# ============================================================
# ENCABEZADO PARA EL CORREO
# ============================================================

def obtener_encabezado_solicitud(datos):

    return f"""JETELL
CENTRO DE SOLICITUDES

Solicitud: {datos["solicitud"]}
Código de verificación: {datos["codigo"]}
Generado: {datos["generado"]}
"""