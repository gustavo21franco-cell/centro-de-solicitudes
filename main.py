import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

# ============================================================
# IMPORTAR FORMULARIOS
# ============================================================

from formularios.transporte import abrir_transporte
from formularios.servientrega import abrir_servientrega
from formularios.mayor import abrir_mayor


# ============================================================
# CONFIGURACIÓN PRINCIPAL
# ============================================================

NOMBRE_APP = "Centro de Solicitudes"

ANCHO_NORMAL = 900
ALTO_NORMAL = 850

ANCHO_MINIMO = 450
ALTO_MINIMO = 425


# ============================================================
# COLORES
# ============================================================

AZUL_OSCURO = "#073B70"
AZUL = "#0B5FA5"
AZUL_CLARO = "#2D8FD5"

BLANCO = "#FFFFFF"
GRIS_CLARO = "#F4F7FA"
GRIS = "#6B7280"
GRIS_OSCURO = "#374151"

VERDE = "#168A45"
VERDE_HOVER = "#116D37"

NARANJA = "#E67E22"
NARANJA_HOVER = "#C96512"

SOMBRA = "#D8E0E8"


# ============================================================
# RUTA BASE DEL PROYECTO
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

root = tk.Tk()

root.title(NOMBRE_APP)

root.geometry(
    f"{ANCHO_NORMAL}x{ALTO_NORMAL}"
)

root.minsize(
    ANCHO_MINIMO,
    ALTO_MINIMO
)

# La ventana puede redimensionarse
root.resizable(
    True,
    True
)


# ============================================================
# ICONO DE WINDOWS
# ============================================================

RUTA_ICONO = os.path.join(
    BASE_DIR,
    "logo.ico"
)

if os.path.exists(RUTA_ICONO):

    try:

        root.iconbitmap(
            RUTA_ICONO
        )

    except Exception:
        pass


# ============================================================
# ESCALA
# ============================================================

escala_actual = 1.0


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def limitar(
    valor,
    minimo,
    maximo
):

    return max(
        minimo,
        min(
            valor,
            maximo
        )
    )


def obtener_escala():

    ancho = root.winfo_width()
    alto = root.winfo_height()

    if ancho <= 1 or alto <= 1:

        return 1.0

    escala_ancho = (
        ancho / ANCHO_NORMAL
    )

    escala_alto = (
        alto / ALTO_NORMAL
    )

    # Se utiliza la menor escala
    # para conservar proporciones.

    escala = min(
        escala_ancho,
        escala_alto
    )

    return limitar(
        escala,
        0.5,
        1.25
    )


# ============================================================
# FUENTES
# ============================================================

def fuente(
    tamano,
    negrita=False
):

    escala = obtener_escala()

    nuevo_tamano = int(
        tamano * escala
    )

    nuevo_tamano = max(
        8,
        nuevo_tamano
    )

    peso = (
        "bold"
        if negrita
        else "normal"
    )

    return (
        "Segoe UI",
        nuevo_tamano,
        peso
    )


# ============================================================
# HOVER
# ============================================================

def agregar_hover(
    widget,
    color_normal,
    color_hover
):

    def entrar(event):

        try:

            widget.configure(
                bg=color_hover,
                activebackground=color_hover
            )

        except Exception:
            pass

    def salir(event):

        try:

            widget.configure(
                bg=color_normal,
                activebackground=color_normal
            )

        except Exception:
            pass

    widget.bind(
        "<Enter>",
        entrar
    )

    widget.bind(
        "<Leave>",
        salir
    )


# ============================================================
# FECHA Y HORA
# ============================================================

DIAS = [
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo"
]

MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"
]


def actualizar_fecha_hora():

    ahora = datetime.now()

    dia = DIAS[
        ahora.weekday()
    ]

    mes = MESES[
        ahora.month - 1
    ]

    fecha = (
        f"{dia.capitalize()}, "
        f"{ahora.day} de "
        f"{mes} de "
        f"{ahora.year}"
    )

    hora = ahora.strftime(
        "%H:%M:%S"
    )

    fecha_label.config(
        text=fecha
    )

    hora_label.config(
        text=hora
    )

    root.after(
        1000,
        actualizar_fecha_hora
    )


# ============================================================
# FRAME PRINCIPAL
# ============================================================

contenedor = tk.Frame(
    root,
    bg=GRIS_CLARO
)

contenedor.pack(
    fill="both",
    expand=True
)


# ============================================================
# ENCABEZADO
# ============================================================

encabezado = tk.Frame(
    contenedor,
    bg=AZUL_OSCURO,
    height=170
)

encabezado.pack(
    fill="x"
)

encabezado.pack_propagate(
    False
)


# ============================================================
# LOGO
# ============================================================

logo_frame = tk.Frame(
    encabezado,
    bg=AZUL_OSCURO
)

logo_frame.place(
    relx=0.055,
    rely=0.5,
    anchor="w"
)


logo_label = None
logo_imagen = None


# ============================================================
# CARGAR LOGO
# ============================================================

RUTA_LOGO = os.path.join(
    BASE_DIR,
    "logo all colors (6).png"
)


if os.path.exists(RUTA_LOGO):

    try:

        logo_imagen = tk.PhotoImage(
            file=RUTA_LOGO
        )

        ancho_logo = (
            logo_imagen.width()
        )

        alto_logo = (
            logo_imagen.height()
        )

        # Reducir si la imagen es demasiado grande

        if (
            ancho_logo > 130
            or alto_logo > 100
        ):

            factor_x = max(
                1,
                ancho_logo // 130
            )

            factor_y = max(
                1,
                alto_logo // 100
            )

            factor = max(
                factor_x,
                factor_y
            )

            logo_imagen = (
                logo_imagen.subsample(
                    factor,
                    factor
                )
            )

        logo_label = tk.Label(
            logo_frame,
            image=logo_imagen,
            bg=AZUL_OSCURO
        )

        logo_label.pack()

    except Exception:

        logo_label = None


# ============================================================
# TEXTO JETELL
# ============================================================

jetell_label = tk.Label(
    encabezado,
    text="JETELL",
    bg=AZUL_OSCURO,
    fg=BLANCO,
    font=(
        "Segoe UI",
        30,
        "bold"
    )
)

jetell_label.place(
    relx=0.22,
    rely=0.32,
    anchor="w"
)


# ============================================================
# TÍTULO
# ============================================================

titulo_label = tk.Label(
    encabezado,
    text="CENTRO DE SOLICITUDES",
    bg=AZUL_OSCURO,
    fg=BLANCO,
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

titulo_label.place(
    relx=0.22,
    rely=0.62,
    anchor="w"
)


# ============================================================
# FECHA
# ============================================================

fecha_label = tk.Label(
    encabezado,
    text="",
    bg=AZUL_OSCURO,
    fg="#DCEBFA",
    font=(
        "Segoe UI",
        12
    )
)

fecha_label.place(
    relx=0.95,
    rely=0.30,
    anchor="e"
)


# ============================================================
# HORA
# ============================================================

hora_label = tk.Label(
    encabezado,
    text="",
    bg=AZUL_OSCURO,
    fg=BLANCO,
    font=(
        "Segoe UI",
        22,
        "bold"
    )
)

hora_label.place(
    relx=0.95,
    rely=0.62,
    anchor="e"
)


# ============================================================
# ÁREA CENTRAL
# ============================================================

area_principal = tk.Frame(
    contenedor,
    bg=GRIS_CLARO
)

area_principal.pack(
    fill="both",
    expand=True
)


# ============================================================
# TÍTULO CENTRAL
# ============================================================

subtitulo = tk.Label(
    area_principal,
    text="Seleccione el tipo de solicitud",
    bg=GRIS_CLARO,
    fg=AZUL_OSCURO,
    font=(
        "Segoe UI",
        21,
        "bold"
    )
)

subtitulo.pack(
    pady=(30, 5)
)


# ============================================================
# DESCRIPCIÓN
# ============================================================

descripcion = tk.Label(
    area_principal,
    text="Seleccione una de las opciones para continuar",
    bg=GRIS_CLARO,
    fg=GRIS,
    font=(
        "Segoe UI",
        11
    )
)

descripcion.pack(
    pady=(0, 20)
)


# ============================================================
# CONTENEDOR DE TARJETAS
# ============================================================

tarjetas = tk.Frame(
    area_principal,
    bg=GRIS_CLARO
)

tarjetas.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=10
)


tarjetas.grid_columnconfigure(
    0,
    weight=1
)

tarjetas.grid_columnconfigure(
    1,
    weight=1
)

tarjetas.grid_columnconfigure(
    2,
    weight=1
)

tarjetas.grid_rowconfigure(
    0,
    weight=1
)


# ============================================================
# CREAR TARJETA
# ============================================================

def crear_tarjeta(
    columna,
    titulo,
    descripcion_texto,
    icono,
    color,
    color_hover,
    comando
):

    # ========================================================
    # MARCO EXTERIOR
    # ========================================================

    tarjeta = tk.Frame(
        tarjetas,
        bg=SOMBRA,
        bd=0,
        highlightthickness=0
    )

    tarjeta.grid(
        row=0,
        column=columna,
        sticky="nsew",
        padx=12,
        pady=20
    )

    tarjeta.grid_rowconfigure(
        0,
        weight=1
    )

    tarjeta.grid_columnconfigure(
        0,
        weight=1
    )


    # ========================================================
    # MARCO INTERNO
    # ========================================================

    interior = tk.Frame(
        tarjeta,
        bg=BLANCO,
        bd=0
    )

    interior.pack(
        fill="both",
        expand=True,
        padx=2,
        pady=2
    )


    # ========================================================
    # ICONO
    # ========================================================

    icono_label = tk.Label(
        interior,
        text=icono,
        bg=BLANCO,
        fg=color,
        font=(
            "Segoe UI Emoji",
            42
        )
    )

    icono_label.pack(
        pady=(30, 10)
    )


    # ========================================================
    # TÍTULO
    # ========================================================

    titulo_widget = tk.Label(
        interior,
        text=titulo,
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=(
            "Segoe UI",
            15,
            "bold"
        )
    )

    titulo_widget.pack(
        pady=5
    )


    # ========================================================
    # DESCRIPCIÓN
    # ========================================================

    descripcion_widget = tk.Label(
        interior,
        text=descripcion_texto,
        bg=BLANCO,
        fg=GRIS,
        font=(
            "Segoe UI",
            10
        ),
        wraplength=210,
        justify="center"
    )

    descripcion_widget.pack(
        padx=15,
        pady=(5, 20)
    )


    # ========================================================
    # BOTÓN
    # ========================================================

    boton = tk.Button(
        interior,
        text="ABRIR",
        command=comando,
        bg=color,
        fg=BLANCO,
        activebackground=color_hover,
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        padx=20,
        pady=9
    )

    boton.pack(
        pady=(0, 25)
    )


    # ========================================================
    # HOVER DEL BOTÓN
    # ========================================================

    agregar_hover(
        boton,
        color,
        color_hover
    )


    # ========================================================
    # HOVER DE LA TARJETA
    # ========================================================

    def hover_tarjeta_entrar(event):

        try:

            tarjeta.configure(
                bg="#C8D3DE"
            )

        except Exception:
            pass


    def hover_tarjeta_salir(event):

        try:

            tarjeta.configure(
                bg=SOMBRA
            )

        except Exception:
            pass


    tarjeta.bind(
        "<Enter>",
        hover_tarjeta_entrar
    )

    tarjeta.bind(
        "<Leave>",
        hover_tarjeta_salir
    )


    return tarjeta


# ============================================================
# TARJETA TRANSPORTE
# ============================================================

tarjeta_transporte = crear_tarjeta(
    0,
    "Transporte",
    "Solicitudes de envío mediante casas de transporte.",
    "🚚",
    AZUL,
    AZUL_CLARO,
    abrir_transporte
)


# ============================================================
# TARJETA SERVIENTREGA
# ============================================================

tarjeta_servientrega = crear_tarjeta(
    1,
    "Servientrega",
    "Solicitudes de envío mediante Servientrega.",
    "📦",
    VERDE,
    VERDE_HOVER,
    abrir_servientrega
)


# ============================================================
# TARJETA POR MAYOR
# ============================================================

tarjeta_mayor = crear_tarjeta(
    2,
    "Por Mayor",
    "Solicitudes relacionadas con ventas por mayor.",
    "🛒",
    NARANJA,
    NARANJA_HOVER,
    abrir_mayor
)


# ============================================================
# PIE DE VENTANA
# ============================================================

pie = tk.Frame(
    contenedor,
    bg=BLANCO,
    height=55
)

pie.pack(
    fill="x"
)

pie.pack_propagate(
    False
)


pie_label = tk.Label(
    pie,
    text="JETELL  •  Centro de Solicitudes",
    bg=BLANCO,
    fg=GRIS,
    font=(
        "Segoe UI",
        9
    )
)

pie_label.pack(
    pady=18
)


# ============================================================
# REDIMENSIONAMIENTO
# ============================================================

def actualizar_diseno(event=None):

    global escala_actual

    ancho = root.winfo_width()
    alto = root.winfo_height()

    if ancho <= 1 or alto <= 1:
        return

    nueva_escala = obtener_escala()


    # ========================================================
    # EVITAR ACTUALIZACIONES INNECESARIAS
    # ========================================================

    if (
        abs(
            nueva_escala
            - escala_actual
        ) < 0.01
    ):

        return


    escala_actual = nueva_escala


    # ========================================================
    # ENCABEZADO
    # ========================================================

    alto_encabezado = int(
        170 * nueva_escala
    )

    alto_encabezado = limitar(
        alto_encabezado,
        95,
        170
    )

    encabezado.configure(
        height=alto_encabezado
    )


    # ========================================================
    # JETELL
    # ========================================================

    tam_jetell = int(
        30 * nueva_escala
    )

    tam_jetell = max(
        18,
        min(
            tam_jetell,
            30
        )
    )

    jetell_label.configure(
        font=(
            "Segoe UI",
            tam_jetell,
            "bold"
        )
    )


    # ========================================================
    # TÍTULO
    # ========================================================

    tam_titulo = int(
        16 * nueva_escala
    )

    tam_titulo = max(
        10,
        min(
            tam_titulo,
            16
        )
    )

    titulo_label.configure(
        font=(
            "Segoe UI",
            tam_titulo,
            "bold"
        )
    )


    # ========================================================
    # FECHA
    # ========================================================

    tam_fecha = int(
        12 * nueva_escala
    )

    tam_fecha = max(
        8,
        min(
            tam_fecha,
            12
        )
    )

    fecha_label.configure(
        font=(
            "Segoe UI",
            tam_fecha
        )
    )


    # ========================================================
    # HORA
    # ========================================================

    tam_hora = int(
        22 * nueva_escala
    )

    tam_hora = max(
        12,
        min(
            tam_hora,
            22
        )
    )

    hora_label.configure(
        font=(
            "Segoe UI",
            tam_hora,
            "bold"
        )
    )


    # ========================================================
    # SUBTÍTULO
    # ========================================================

    tam_subtitulo = int(
        21 * nueva_escala
    )

    tam_subtitulo = max(
        12,
        min(
            tam_subtitulo,
            21
        )
    )

    subtitulo.configure(
        font=(
            "Segoe UI",
            tam_subtitulo,
            "bold"
        )
    )


    # ========================================================
    # DESCRIPCIÓN
    # ========================================================

    tam_descripcion = int(
        11 * nueva_escala
    )

    tam_descripcion = max(
        8,
        min(
            tam_descripcion,
            11
        )
    )

    descripcion.configure(
        font=(
            "Segoe UI",
            tam_descripcion
        )
    )


    # ========================================================
    # MÁRGENES DE LAS TARJETAS
    # ========================================================

    if nueva_escala < 0.65:

        tarjetas.configure(
            padx=15
        )

    elif nueva_escala < 0.85:

        tarjetas.configure(
            padx=25
        )

    else:

        tarjetas.configure(
            padx=45
        )


# ============================================================
# EVENTO DE REDIMENSIONAMIENTO
# ============================================================

root.bind(
    "<Configure>",
    actualizar_diseno
)


# ============================================================
# INICIAR FECHA Y HORA
# ============================================================

actualizar_fecha_hora()


# ============================================================
# CENTRAR VENTANA
# ============================================================

def centrar_ventana():

    root.update_idletasks()

    ancho = root.winfo_width()
    alto = root.winfo_height()

    pantalla_ancho = (
        root.winfo_screenwidth()
    )

    pantalla_alto = (
        root.winfo_screenheight()
    )

    x = int(
        (pantalla_ancho - ancho) / 2
    )

    y = int(
        (pantalla_alto - alto) / 2
    )

    root.geometry(
        f"{ancho}x{alto}+{x}+{y}"
    )


centrar_ventana()


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

root.mainloop()