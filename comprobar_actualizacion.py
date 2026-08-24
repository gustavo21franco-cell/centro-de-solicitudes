import json
import urllib.request
import urllib.error
import os
import shutil


# ============================================================
# CONFIGURACIÓN
# ============================================================

VERSION_LOCAL_INICIAL = "1.0.0"

URL_VERSION = (
    "https://raw.githubusercontent.com/"
    "gustavo21franco-cell/"
    "centro-de-solicitudes/"
    "main/version_datos.json"
)

URL_DATOS = (
    "https://raw.githubusercontent.com/"
    "gustavo21franco-cell/"
    "centro-de-solicitudes/"
    "main/DATOS/geografia_ecuador.json"
)


# ============================================================
# RUTAS LOCALES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CARPETA_DATOS = os.path.join(
    BASE_DIR,
    "DATOS"
)

ARCHIVO_DATOS = os.path.join(
    CARPETA_DATOS,
    "geografia_ecuador.json"
)

ARCHIVO_VERSION = os.path.join(
    CARPETA_DATOS,
    "version_local.json"
)

ARCHIVO_TEMPORAL = os.path.join(
    CARPETA_DATOS,
    "geografia_ecuador_actualizacion.tmp"
)

ARCHIVO_BACKUP = os.path.join(
    CARPETA_DATOS,
    "geografia_ecuador_backup.json"
)


# ============================================================
# OBTENER VERSIÓN LOCAL
# ============================================================

def obtener_version_local():

    # --------------------------------------------------------
    # Si ya existe una versión guardada
    # --------------------------------------------------------

    if os.path.exists(
        ARCHIVO_VERSION
    ):

        try:

            with open(
                ARCHIVO_VERSION,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(
                    archivo
                )

            version = datos.get(
                "version"
            )

            if version:

                return str(
                    version
                )

        except Exception:

            pass

    # --------------------------------------------------------
    # Primera ejecución
    # --------------------------------------------------------

    return VERSION_LOCAL_INICIAL


# ============================================================
# GUARDAR VERSIÓN LOCAL
# ============================================================

def guardar_version_local(
    version
):

    os.makedirs(
        CARPETA_DATOS,
        exist_ok=True
    )

    datos = {
        "version": str(
            version
        )
    }

    archivo_temporal_version = (
        ARCHIVO_VERSION + ".tmp"
    )

    with open(
        archivo_temporal_version,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    os.replace(
        archivo_temporal_version,
        ARCHIVO_VERSION
    )


# ============================================================
# COMPARAR VERSIONES
# ============================================================

def version_es_mayor(
    version_remota,
    version_local
):

    try:

        remota = tuple(
            int(x)
            for x in str(
                version_remota
            ).split(".")
        )

        local = tuple(
            int(x)
            for x in str(
                version_local
            ).split(".")
        )

        return remota > local

    except Exception:

        return (
            str(version_remota)
            != str(version_local)
        )


# ============================================================
# DESCARGAR DATOS
# ============================================================

def descargar_datos():

    with urllib.request.urlopen(
        URL_DATOS,
        timeout=20
    ) as respuesta:

        contenido = respuesta.read()

    # --------------------------------------------------------
    # COMPROBAR QUE EL ARCHIVO NO ESTÉ VACÍO
    # --------------------------------------------------------

    if not contenido:

        raise Exception(
            "GitHub devolvió un archivo vacío."
        )

    texto = contenido.decode(
        "utf-8"
    )

    # --------------------------------------------------------
    # COMPROBAR JSON
    # --------------------------------------------------------

    datos = json.loads(
        texto
    )

    # --------------------------------------------------------
    # COMPROBAR ESTRUCTURA
    # --------------------------------------------------------

    if not isinstance(
        datos,
        dict
    ):

        raise Exception(
            "El archivo descargado no contiene "
            "una estructura geográfica válida."
        )

    # --------------------------------------------------------
    # COMPROBAR 24 PROVINCIAS
    # --------------------------------------------------------

    if len(datos) != 24:

        raise Exception(
            f"El archivo descargado contiene "
            f"{len(datos)} provincias "
            "en lugar de 24."
        )

    # --------------------------------------------------------
    # CONTAR CANTONES
    # --------------------------------------------------------

    total_cantones = sum(
        len(provincia)
        for provincia in datos.values()
        if isinstance(
            provincia,
            dict
        )
    )

    # --------------------------------------------------------
    # CONTAR LOCALIDADES
    # --------------------------------------------------------

    total_localidades = sum(
        len(localidades)
        for provincia in datos.values()
        if isinstance(
            provincia,
            dict
        )
        for localidades in provincia.values()
        if isinstance(
            localidades,
            list
        )
    )

    print(
        f"Provincias descargadas: {len(datos)}"
    )

    print(
        f"Cantones descargados: "
        f"{total_cantones}"
    )

    print(
        f"Localidades descargadas: "
        f"{total_localidades}"
    )

    # --------------------------------------------------------
    # GUARDAR ARCHIVO TEMPORAL
    # --------------------------------------------------------

    with open(
        ARCHIVO_TEMPORAL,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    return True


# ============================================================
# COMPROBAR ACTUALIZACIÓN
# ============================================================

def comprobar_actualizacion():

    try:

        # ----------------------------------------------------
        # CREAR CARPETA DATOS
        # ----------------------------------------------------

        os.makedirs(
            CARPETA_DATOS,
            exist_ok=True
        )

        # ----------------------------------------------------
        # OBTENER VERSIÓN LOCAL
        # ----------------------------------------------------

        version_local = (
            obtener_version_local()
        )

        print(
            f"Versión local: "
            f"{version_local}"
        )

        # ----------------------------------------------------
        # OBTENER VERSIÓN REMOTA
        # ----------------------------------------------------

        with urllib.request.urlopen(
            URL_VERSION,
            timeout=10
        ) as respuesta:

            datos_version = json.loads(
                respuesta.read().decode(
                    "utf-8"
                )
            )

        version_remota = (
            datos_version.get(
                "version"
            )
        )

        if not version_remota:

            raise Exception(
                "GitHub no indicó una versión válida."
            )

        print(
            f"Versión remota: "
            f"{version_remota}"
        )

        # ----------------------------------------------------
        # COMPROBAR SI YA ESTÁ ACTUALIZADO
        # ----------------------------------------------------

        if not version_es_mayor(
            version_remota,
            version_local
        ):

            print()
            print(
                "✓ Los datos ya están actualizados."
            )

            return False

        # ----------------------------------------------------
        # EXISTE UNA NUEVA VERSIÓN
        # ----------------------------------------------------

        print()
        print(
            "¡Nueva versión de datos disponible!"
        )

        print(
            f"Versión anterior: "
            f"{version_local}"
        )

        print(
            f"Nueva versión: "
            f"{version_remota}"
        )

        print(
            "Descargando nueva información..."
        )

        # ----------------------------------------------------
        # DESCARGAR Y VALIDAR
        # ----------------------------------------------------

        descargar_datos()

        # ----------------------------------------------------
        # CREAR COPIA DE SEGURIDAD
        # ----------------------------------------------------

        if os.path.exists(
            ARCHIVO_DATOS
        ):

            shutil.copy2(
                ARCHIVO_DATOS,
                ARCHIVO_BACKUP
            )

            print(
                "✓ Copia de seguridad creada."
            )

        # ----------------------------------------------------
        # REEMPLAZAR ARCHIVO ACTUAL
        # ----------------------------------------------------

        os.replace(
            ARCHIVO_TEMPORAL,
            ARCHIVO_DATOS
        )

        print(
            "✓ Archivo geográfico actualizado."
        )

        # ----------------------------------------------------
        # GUARDAR NUEVA VERSIÓN
        # ----------------------------------------------------

        guardar_version_local(
            version_remota
        )

        print(
            "✓ Versión local actualizada."
        )

        print()
        print(
            "✓ Datos actualizados correctamente."
        )

        print(
            f"✓ Nueva versión: "
            f"{version_remota}"
        )

        print(
            f"✓ Archivo: "
            f"{ARCHIVO_DATOS}"
        )

        # ----------------------------------------------------
        # DEVOLVER INFORMACIÓN DE ACTUALIZACIÓN
        # ----------------------------------------------------

        return {
            "actualizado": True,
            "version_anterior": version_local,
            "version_nueva": str(
                version_remota
            )
        }

    except urllib.error.HTTPError as error:

        print()
        print(
            "⚠️ Error HTTP al comprobar "
            "la actualización."
        )

        print(
            f"Código: {error.code}"
        )

        return False

    except urllib.error.URLError as error:

        print()
        print(
            "⚠️ No se pudo conectar con GitHub."
        )

        print(
            error
        )

        return False

    except Exception as error:

        print()
        print(
            "⚠️ No se pudo comprobar "
            "la actualización."
        )

        print(
            error
        )

        # ----------------------------------------------------
        # ELIMINAR TEMPORAL SI QUEDÓ
        # ----------------------------------------------------

        if os.path.exists(
            ARCHIVO_TEMPORAL
        ):

            try:

                os.remove(
                    ARCHIVO_TEMPORAL
                )

            except Exception:

                pass

        return False


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 60
    )

    print(
        " ACTUALIZADOR DE DATOS - JETELL"
    )

    print(
        "=" * 60
    )

    print()

    resultado = (
        comprobar_actualizacion()
    )

    if isinstance(
        resultado,
        dict
    ):

        print()
        print(
            "ACTUALIZACIÓN REALIZADA:"
        )

        print(
            f"{resultado['version_anterior']}"
            f" → "
            f"{resultado['version_nueva']}"
        )