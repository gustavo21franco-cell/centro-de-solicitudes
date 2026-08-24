import json
import os

ARCHIVO = os.path.join("DATOS", "geografia_ecuador.json")


def cargar_datos():
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )


def mostrar_provincias(datos):
    print("\nPROVINCIAS DISPONIBLES:\n")

    for i, provincia in enumerate(datos.keys(), 1):
        print(f"{i}. {provincia}")


def agregar_localidad():

    datos = cargar_datos()

    mostrar_provincias(datos)

    provincia = input("\nEscribe la provincia: ").strip().upper()

    if provincia not in datos:
        print("\n❌ Provincia no encontrada.")
        return

    print(f"\nCANTONES DE {provincia}:\n")

    for canton in datos[provincia]:
        print(f"- {canton}")

    canton = input("\nEscribe el cantón: ").strip().upper()

    if canton not in datos[provincia]:
        print("\n❌ Cantón no encontrado.")
        return

    localidad = input("\nEscribe la ciudad/localidad que quieres agregar: ").strip().upper()

    if not localidad:
        print("\n❌ No ingresaste ninguna localidad.")
        return

    if localidad in datos[provincia][canton]:
        print("\n⚠️ Esa localidad ya existe.")
        return

    datos[provincia][canton].append(localidad)

    guardar_datos(datos)

    print("\n" + "=" * 50)
    print("✅ LOCALIDAD AGREGADA CORRECTAMENTE")
    print("=" * 50)
    print(f"Provincia : {provincia}")
    print(f"Cantón    : {canton}")
    print(f"Localidad : {localidad}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        agregar_localidad()
    except FileNotFoundError:
        print("\n❌ No se encontró:")
        print(ARCHIVO)
    except json.JSONDecodeError:
        print("\n❌ El archivo geografia_ecuador.json tiene un error de formato.")
    except Exception as e:
        print(f"\n❌ Ocurrió un error: {e}")