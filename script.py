import itertools
import subprocess
import time
from pathlib import Path
from itertools import permutations
from typing import Dict, Set
from colorama import Fore, Style, init

init(autoreset=True)


# UTILIDADES 

def limpiar_terminal() -> None:
    """Limpia la terminal según el sistema operativo."""
    subprocess.run("cls" if subprocess.os.name == "nt" else "clear", shell=True)


def animacion_carga(mensaje: str = "Generando diccionario...") -> None:
    """Muestra una animación de carga simple."""
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    print(Fore.YELLOW + f"\n{mensaje}", end=" ", flush=True)
    for _ in range(20):
        print(next(spinner), end="\r", flush=True)
        time.sleep(0.15)


# INTERFAZ 

def mostrar_banner() -> None:
    """Muestra un banner decorativo."""
    banner = f"""
                                                                           
  ▗▄        █                   ▄▄ ▗▄▄▄▖▗▄ ▗▖▗▄▄▄▖▗▄▄▖   ▄  ▗▄▄▄▖ ▗▄▖ ▗▄▄▖ 
  ▟█        ▀                  █▀▀▌▐▛▀▀▘▐█ ▐▌▐▛▀▀▘▐▛▀▜▌ ▐█▌ ▝▀█▀▘ █▀█ ▐▛▀▜▌
 ▐▘█ ▐▙ ▟▌ ██                 ▐▌   ▐▌   ▐▛▌▐▌▐▌   ▐▌ ▐▌ ▐█▌   █  ▐▌ ▐▌▐▌ ▐▌
▗▛ █  █ █   █                 ▐▌▗▄▖▐███ ▐▌█▐▌▐███ ▐███  █ █   █  ▐▌ ▐▌▐███ 
▐███▌ ▜▄▛   █        ██▌      ▐▌▝▜▌▐▌   ▐▌▐▟▌▐▌   ▐▌▝█▖ ███   █  ▐▌ ▐▌▐▌▝█▖
   █  ▐█▌ ▗▄█▄▖                █▄▟▌▐▙▄▄▖▐▌ █▌▐▙▄▄▖▐▌ ▐▌▗█ █▖  █   █▄█ ▐▌ ▐▌
   ▀   ▀  ▝▀▀▀▘                 ▀▀ ▝▀▀▀▘▝▘ ▀▘▝▀▀▀▘▝▘ ▝▀▝▘ ▝▘  ▀   ▝▀▘ ▝▘ ▝▀

{Fore.MAGENTA}  Generador de Diccionario - 4vi
"""
    print(banner)


def solicitar_datos() -> Dict[str, str]:
    """Solicita datos opcionales al usuario y devuelve solo los no vacíos."""
    campos = [
        "nombre", "apellido", "apodo", "dni",
        "fecha de nacimiento (YYYYMMDD)", "dirección",
        "palabra clave", "nombre de mascota",
        "color favorito", "lugar de nacimiento"
    ]
    datos = {}
    print(Fore.CYAN + "\nPor favor, proporciona los siguientes datos (deja en blanco si no aplica):\n")
    for campo in campos:
        valor = input(f"{campo.capitalize()} -> ").strip()
        if valor:
            datos[campo] = valor
    return datos


# LÓGICA DE GENERACIÓN

def generar_variaciones(
    datos: Dict[str, str],
    incluir_numeros: bool = True,
    incluir_especiales: bool = False
) -> Set[str]:
    """Genera combinaciones de palabras a partir de los datos ingresados."""
    palabras = list(datos.values())
    variaciones: Set[str] = set()
    numeros_extra = ["123", "2024"]
    especiales = ["!", "@", "#", "$", "%", "&", "*"]

    # Variaciones individuales
    for p in palabras:
        variaciones.update({p, p.lower(), p.upper(), p.capitalize()})
        if incluir_numeros:
            variaciones.update({p + n for n in numeros_extra})

    # Combinaciones entre palabras
    for r in range(2, len(palabras) + 1):
        for comb in permutations(palabras, r):
            base = "".join(comb)
            cap = "".join([w.capitalize() for w in comb])
            variaciones.update({base, cap})
            if incluir_numeros:
                for n in numeros_extra:
                    variaciones.update({base + n, cap + n})

    # Caracteres especiales
    if incluir_especiales:
        for v in list(variaciones):
            for char in especiales:
                variaciones.add(v + char)

    return variaciones


def guardar_diccionario(variaciones: Set[str], archivo: Path) -> None:
    """Guarda las variaciones en un archivo .txt."""
    animacion_carga("Generando archivo...")
    archivo.write_text("\n".join(sorted(variaciones)), encoding="utf-8")
    print(f"\n{Fore.GREEN}✓ Diccionario generado con éxito en '{archivo}' con {len(variaciones)} contraseñas.")


# BÚSQUEDA 

def buscar_palabra_en_diccionario(archivo: Path) -> None:
    """Permite buscar una palabra o fragmento en el diccionario generado."""
    if not archivo.exists():
        print(Fore.RED + f"\nEl archivo '{archivo}' no existe.")
        return

    palabra = input(Fore.YELLOW + "\nPalabra a buscar: ").strip()
    tipo = input("¿Exacta (e) o incluye texto (i)? [e/i]: ").strip().lower()

    resultados = []
    with archivo.open(encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if (tipo == "e" and linea == palabra) or (tipo != "e" and palabra in linea):
                resultados.append(linea)

    if resultados:
        print(Fore.GREEN + f"\nSe encontraron {len(resultados)} coincidencias:")
        for r in resultados:
            print("  -", r)
    else:
        print(Fore.RED + f"\nNo se encontraron resultados para '{palabra}'.")


# MENÚ

def menu_principal() -> None:
    opciones = {
        "1": ("Verificar dependencias", verificar_dependencias),
        "2": ("Verificar actualizaciones desde el repositorio", verificar_actualizaciones),
        "3": ("Crear diccionario", crear_diccionario),
        "4": ("Buscar palabra en diccionario", opcion_buscar),
        "5": ("Salir", None),
    }

    while True:
        print(Fore.GREEN + "\n******* Generador de contraseñas *******")
        for k, (desc, _) in opciones.items():
            print(f"{k}. {desc}")

        opcion = input("\nSelecciona una opción: ").strip()
        accion = opciones.get(opcion)

        if not accion:
            print(Fore.RED + "Opción inválida. Intenta de nuevo.")
            continue

        if opcion == "5":
            print(Fore.YELLOW + "\nSaliendo del programa...")
            break

        accion[1]()
        input(Fore.YELLOW + "\nPresiona Enter para continuar...")
        limpiar_terminal()
        mostrar_banner()


# ACCIONES DEL MENÚ

def verificar_dependencias() -> None:
    """Comprueba si las dependencias requeridas están instaladas."""
    print(Fore.YELLOW + "\nVerificando dependencias...")
    try:
        import colorama  # noqa
        print(Fore.GREEN + "✓ Todas las dependencias están instaladas.")
    except ImportError as e:
        print(Fore.RED + f"Error: {e}. Instala las dependencias necesarias.")


def verificar_actualizaciones() -> None:
    """Verifica actualizaciones del repositorio (si existe git)."""
    print(Fore.YELLOW + "\nVerificando actualizaciones desde el repositorio...")
    resultado = subprocess.run(
        ["git", "pull", "https://github.com/simoncherry9/dictionary-generator.git"],
        capture_output=True, text=True
    )
    if "Already up to date." in resultado.stdout:
        print(Fore.GREEN + "✓ El repositorio ya está actualizado.")
    else:
        print(Fore.GREEN + "✓ Repositorio actualizado con éxito.")


def crear_diccionario() -> None:
    """Crea un diccionario basado en los datos ingresados."""
    datos = solicitar_datos()
    incluir_numeros = input("¿Incluir números? (s/n): ").lower().startswith("s")
    incluir_especiales = input("¿Incluir caracteres especiales? (s/n): ").lower().startswith("s")
    variaciones = generar_variaciones(datos, incluir_numeros, incluir_especiales)

    nombre_archivo = input("Nombre del archivo de salida (ej: diccionario.txt): ").strip()
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"

    guardar_diccionario(variaciones, Path(nombre_archivo))


def opcion_buscar() -> None:
    """Busca una palabra en un archivo de diccionario existente."""
    nombre_archivo = input("\nNombre del archivo de diccionario: ").strip()
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"
    buscar_palabra_en_diccionario(Path(nombre_archivo))


# MAIN

if __name__ == "__main__":
    limpiar_terminal()
    mostrar_banner()
    menu_principal()
