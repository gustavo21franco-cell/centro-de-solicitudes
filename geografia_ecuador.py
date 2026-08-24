import json
from pathlib import Path


# ============================================================
# UBICACIÓN DEL ARCHIVO DE DATOS
# ============================================================

ARCHIVO_GEOGRAFIA = (
    Path(__file__).resolve().parent
    / "datos"
    / "geografia_ecuador.json"
)


# ============================================================
# CARGAR GEOGRAFÍA
# ============================================================

def cargar_geografia():

    if not ARCHIVO_GEOGRAFIA.exists():

        raise FileNotFoundError(
            f"No se encontró el archivo:\n"
            f"{ARCHIVO_GEOGRAFIA}"
        )

    with open(
        ARCHIVO_GEOGRAFIA,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)


# ============================================================
# DATOS
# ============================================================

GEOGRAFIA_ECUADOR = cargar_geografia()


# ============================================================
# PROVINCIAS
# ============================================================

def obtener_provincias():

    return sorted(
        GEOGRAFIA_ECUADOR.keys()
    )


# ============================================================
# CANTONES
# ============================================================

def obtener_cantones(provincia):

    if not provincia:
        return []

    return sorted(
        GEOGRAFIA_ECUADOR
        .get(provincia, {})
        .keys()
    )


# ============================================================
# LOCALIDADES
# ============================================================

def obtener_localidades(
    provincia,
    canton
):

    if not provincia or not canton:
        return []

    localidades = (
        GEOGRAFIA_ECUADOR
        .get(provincia, {})
        .get(canton, [])
    )

    return sorted(
        localidades
    )


# ============================================================
# BUSCAR LOCALIDAD
# ============================================================

def localidad_existe(
    provincia,
    canton,
    localidad
):

    localidades = obtener_localidades(
        provincia,
        canton
    )

    return localidad.upper() in [
        x.upper()
        for x in localidades
    ]


# ============================================================
# PRUEBA
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print(" GEOGRAFÍA DEL ECUADOR - JETELL")
    print("=" * 50)
    print()

    provincias = obtener_provincias()

    print(
        f"Provincias cargadas: "
        f"{len(provincias)}"
    )

    print()

    for provincia in provincias:

        print(
            f"- {provincia}"
        )

    print()

    print("Cantones de GUAYAS:")

    for canton in obtener_cantones(
        "GUAYAS"
    ):

        print(
            f" - {canton}"
        )

    print()

    print(
        "Localidades de SANTA ELENA:"
    )

    for localidad in obtener_localidades(
        "SANTA ELENA",
        "SANTA ELENA"
    ):

        print(
            f" - {localidad}"
        )