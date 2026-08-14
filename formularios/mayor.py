import tkinter as tk
from tkinter import messagebox
import webbrowser
import urllib.parse
import os

from config import CORREOS_DESTINO, DESTINATARIOS_POR_DEFECTO


# ============================================================
# COLORES DEL DISEÑO
# ============================================================

AZUL_OSCURO = "#073B70"
AZUL = "#0B5FA5"
AZUL_CLARO = "#2D8FD5"
AZUL_SUAVE = "#EAF4FC"

BLANCO = "#FFFFFF"
FONDO = "#F4F7FA"
BORDE = "#D8E0E8"

TEXTO = "#243447"
TEXTO_SECUNDARIO = "#6B7280"

VERDE = "#168A45"
VERDE_HOVER = "#116D37"


# ============================================================
# FUNCIONES VISUALES
# ============================================================

def crear_label(parent, texto, obligatorio=False):

    frame = tk.Frame(
        parent,
        bg=BLANCO
    )

    frame.pack(
        fill="x",
        padx=35,
        pady=(5, 3)
    )

    etiqueta = tk.Label(
        frame,
        text=texto + (" *" if obligatorio else ""),
        bg=BLANCO,
        fg=TEXTO,
        font=("Segoe UI", 10, "bold"),
        anchor="w"
    )

    etiqueta.pack(
        anchor="w"
    )

    return frame


def estilizar_entry(entry):

    entry.configure(
        bg=BLANCO,
        fg=TEXTO,
        insertbackground=AZUL,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDE,
        highlightcolor=AZUL,
        font=("Segoe UI", 10)
    )


def agregar_hover(boton, normal, hover):

    boton.bind(
        "<Enter>",
        lambda e: boton.configure(bg=hover)
    )

    boton.bind(
        "<Leave>",
        lambda e: boton.configure(bg=normal)
    )


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def abrir_mayor():

    ventana = tk.Toplevel()

    ventana.title("Por Mayor")

    ventana.geometry("620x850")

    ventana.minsize(
        560,
        700
    )

    ventana.resizable(
        True,
        True
    )

    ventana.configure(
        bg=FONDO
    )


    # ========================================================
    # ICONO DE WINDOWS
    # ========================================================

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    ruta_icono = os.path.join(
        base_dir,
        "logo.ico"
    )

    if os.path.exists(ruta_icono):

        try:

            ventana.iconbitmap(
                ruta_icono
            )

        except Exception:
            pass


    # ========================================================
    # ENCABEZADO
    # ========================================================

    encabezado = tk.Frame(
        ventana,
        bg=AZUL_OSCURO,
        height=120
    )

    encabezado.pack(
        fill="x"
    )

    encabezado.pack_propagate(
        False
    )


    # ========================================================
    # LOGO
    # ========================================================

    ruta_logo = os.path.join(
        base_dir,
        "logo all colors (6).png"
    )

    logo_imagen = None

    if os.path.exists(ruta_logo):

        try:

            logo_imagen = tk.PhotoImage(
                file=ruta_logo
            )

            ancho_logo = logo_imagen.width()
            alto_logo = logo_imagen.height()

            if ancho_logo > 100 or alto_logo > 80:

                factor_x = max(
                    1,
                    ancho_logo // 100
                )

                factor_y = max(
                    1,
                    alto_logo // 80
                )

                factor = max(
                    factor_x,
                    factor_y
                )

                logo_imagen = logo_imagen.subsample(
                    factor,
                    factor
                )

            tk.Label(
                encabezado,
                image=logo_imagen,
                bg=AZUL_OSCURO
            ).place(
                x=25,
                rely=0.5,
                anchor="w"
            )

        except Exception:
            pass


    # ========================================================
    # JETELL
    # ========================================================

    tk.Label(
        encabezado,
        text="JETELL",
        bg=AZUL_OSCURO,
        fg=BLANCO,
        font=("Segoe UI", 22, "bold")
    ).place(
        x=145,
        y=38,
        anchor="w"
    )


    # ========================================================
    # SUBTÍTULO
    # ========================================================

    tk.Label(
        encabezado,
        text="SOLICITUD POR MAYOR",
        bg=AZUL_OSCURO,
        fg="#DCEBFA",
        font=("Segoe UI", 10, "bold")
    ).place(
        x=145,
        y=70,
        anchor="w"
    )


    # ========================================================
    # CANVAS + SCROLL
    # ========================================================

    canvas = tk.Canvas(
        ventana,
        bg=FONDO,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        ventana,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )


    contenido = tk.Frame(
        canvas,
        bg=FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )


    def actualizar_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )


    contenido.bind(
        "<Configure>",
        actualizar_scroll
    )


    def ajustar_ancho(event):

        canvas.itemconfigure(
            ventana_canvas,
            width=event.width
        )


    canvas.bind(
        "<Configure>",
        ajustar_ancho
    )


    # ========================================================
    # DESTINATARIOS
    # ========================================================

    tarjeta_destino = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tarjeta_destino.pack(
        fill="x",
        padx=35,
        pady=(25, 12)
    )


    tk.Label(
        tarjeta_destino,
        text="DESTINATARIOS",
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=("Segoe UI", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )


    tk.Frame(
        tarjeta_destino,
        bg=AZUL,
        height=2
    ).pack(
        fill="x",
        padx=20
    )


    seleccion_correo = {}

    predeterminados = DESTINATARIOS_POR_DEFECTO.get(
        "Por Mayor",
        []
    )


    for nombre, correo in CORREOS_DESTINO.items():

        variable = tk.BooleanVar(
            value=nombre in predeterminados
        )

        casilla = tk.Checkbutton(
            tarjeta_destino,
            text=nombre,
            variable=variable,
            bg=BLANCO,
            fg=TEXTO,
            activebackground=BLANCO,
            activeforeground=AZUL_OSCURO,
            selectcolor=AZUL_SUAVE,
            font=("Segoe UI", 10),
            anchor="w",
            cursor="hand2"
        )

        casilla.pack(
            anchor="w",
            padx=25,
            pady=2
        )

        seleccion_correo[nombre] = variable


    tk.Frame(
        tarjeta_destino,
        bg=BLANCO,
        height=8
    ).pack()


    # ========================================================
    # VARIABLES
    # ========================================================

    vendedor_var = tk.StringVar()

    cliente_var = tk.StringVar()

    cliente_tienda_var = tk.BooleanVar(
        value=False
    )

    cliente_horas_var = tk.BooleanVar(
        value=False
    )

    cliente_manana_var = tk.BooleanVar(
        value=False
    )

    horas_var = tk.StringVar()

    solicitar_video_var = tk.BooleanVar(
        value=False
    )

    urgente_var = tk.BooleanVar(
        value=False
    )


    # ========================================================
    # TARJETA INFORMACIÓN
    # ========================================================

    tarjeta_info = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tarjeta_info.pack(
        fill="x",
        padx=35,
        pady=12
    )


    tk.Label(
        tarjeta_info,
        text="INFORMACIÓN DE LA SOLICITUD",
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=("Segoe UI", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )


    tk.Frame(
        tarjeta_info,
        bg=AZUL,
        height=2
    ).pack(
        fill="x",
        padx=20
    )


    # ========================================================
    # VENDEDOR
    # ========================================================

    crear_label(
        tarjeta_info,
        "Vendedor",
        True
    )


    entrada_vendedor = tk.Entry(
        tarjeta_info,
        textvariable=vendedor_var
    )

    entrada_vendedor.pack(
        fill="x",
        padx=35,
        pady=(0, 8)
    )

    estilizar_entry(
        entrada_vendedor
    )


    # ========================================================
    # CLIENTE
    # ========================================================

    crear_label(
        tarjeta_info,
        "Cliente",
        True
    )


    entrada_cliente = tk.Entry(
        tarjeta_info,
        textvariable=cliente_var
    )

    entrada_cliente.pack(
        fill="x",
        padx=35,
        pady=(0, 15)
    )

    estilizar_entry(
        entrada_cliente
    )


    # ========================================================
    # TARJETA CONDICIÓN DEL CLIENTE
    # ========================================================

    tarjeta_condicion = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tarjeta_condicion.pack(
        fill="x",
        padx=35,
        pady=12
    )


    tk.Label(
        tarjeta_condicion,
        text="CONDICIÓN DEL CLIENTE",
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=("Segoe UI", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )


    tk.Frame(
        tarjeta_condicion,
        bg=AZUL,
        height=2
    ).pack(
        fill="x",
        padx=20
    )


    # ========================================================
    # FRAME HORAS
    # ========================================================

    frame_horas = tk.Frame(
        tarjeta_condicion,
        bg=BLANCO
    )

    frame_horas.pack(
        fill="x",
        padx=35,
        pady=(12, 4)
    )


    # ========================================================
    # VALIDACIÓN DE HORAS
    # ========================================================

    def validar_horas(valor):

        if valor == "":
            return True

        return valor.isdigit()


    validar_horas_cmd = ventana.register(
        validar_horas
    )


    # ========================================================
    # FUNCIONES CONDICIÓN CLIENTE
    # ========================================================

    def seleccionar_tienda():

        if cliente_tienda_var.get():

            cliente_horas_var.set(
                False
            )

            cliente_manana_var.set(
                False
            )

            horas_var.set("")

            entrada_horas.config(
                state="disabled"
            )


    def seleccionar_horas():

        if cliente_horas_var.get():

            cliente_tienda_var.set(
                False
            )

            cliente_manana_var.set(
                False
            )

            entrada_horas.config(
                state="normal"
            )

            entrada_horas.focus()

        else:

            horas_var.set("")

            entrada_horas.config(
                state="disabled"
            )


    def seleccionar_manana():

        if cliente_manana_var.get():

            cliente_tienda_var.set(
                False
            )

            cliente_horas_var.set(
                False
            )

            horas_var.set("")

            entrada_horas.config(
                state="disabled"
            )


    # ========================================================
    # CLIENTE RETIRA EN HORAS
    # ========================================================

    tk.Checkbutton(
        frame_horas,
        text="Cliente retira en",
        variable=cliente_horas_var,
        command=seleccionar_horas,
        bg=BLANCO,
        fg=TEXTO,
        activebackground=BLANCO,
        activeforeground=AZUL_OSCURO,
        selectcolor=AZUL_SUAVE,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    ).pack(
        side="left"
    )


    entrada_horas = tk.Entry(
        frame_horas,
        textvariable=horas_var,
        width=7,
        state="disabled",
        validate="key",
        validatecommand=(
            validar_horas_cmd,
            "%P"
        )
    )

    entrada_horas.pack(
        side="left",
        padx=7
    )

    estilizar_entry(
        entrada_horas
    )

    entrada_horas.configure(
        disabledbackground="#EEF2F5",
        disabledforeground=TEXTO_SECUNDARIO
    )


    tk.Label(
        frame_horas,
        text="horas",
        bg=BLANCO,
        fg=TEXTO,
        font=("Segoe UI", 10)
    ).pack(
        side="left"
    )


    # ========================================================
    # CLIENTE EN TIENDA
    # ========================================================

    tk.Checkbutton(
        tarjeta_condicion,
        text="Cliente en tienda",
        variable=cliente_tienda_var,
        command=seleccionar_tienda,
        bg=BLANCO,
        fg=TEXTO,
        activebackground=BLANCO,
        activeforeground=AZUL_OSCURO,
        selectcolor=AZUL_SUAVE,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    ).pack(
        anchor="w",
        padx=35,
        pady=4
    )


    # ========================================================
    # CLIENTE REGRESA MAÑANA
    # ========================================================

    tk.Checkbutton(
        tarjeta_condicion,
        text="Cliente regresa (al medio día de mañana)",
        variable=cliente_manana_var,
        command=seleccionar_manana,
        bg=BLANCO,
        fg=TEXTO,
        activebackground=BLANCO,
        activeforeground=AZUL_OSCURO,
        selectcolor=AZUL_SUAVE,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    ).pack(
        anchor="w",
        padx=35,
        pady=(4, 15)
    )


    # ========================================================
    # TARJETA PROCESO
    # ========================================================

    tarjeta_proceso = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tarjeta_proceso.pack(
        fill="x",
        padx=35,
        pady=12
    )


    tk.Label(
        tarjeta_proceso,
        text="PROCESO - SOLICITUD DE VIDEO",
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=("Segoe UI", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )


    tk.Frame(
        tarjeta_proceso,
        bg=AZUL,
        height=2
    ).pack(
        fill="x",
        padx=20
    )


    # ========================================================
    # SOLICITAR VIDEO
    # ========================================================

    tk.Checkbutton(
        tarjeta_proceso,
        text="SOLICITO VIDEO DEL PEDIDO ANTES DEL DESPACHO",
        variable=solicitar_video_var,
        bg=BLANCO,
        fg=TEXTO,
        activebackground=BLANCO,
        activeforeground=AZUL_OSCURO,
        selectcolor=AZUL_SUAVE,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    ).pack(
        anchor="w",
        padx=35,
        pady=(12, 8)
    )


    # ========================================================
    # URGENTE
    # ========================================================

    tk.Checkbutton(
        tarjeta_proceso,
        text="URGENTE",
        variable=urgente_var,
        bg=BLANCO,
        fg=TEXTO,
        activebackground=BLANCO,
        activeforeground=AZUL_OSCURO,
        selectcolor=AZUL_SUAVE,
        font=("Segoe UI", 11, "bold"),
        cursor="hand2"
    ).pack(
        anchor="w",
        padx=35,
        pady=(4, 15)
    )


    # ========================================================
    # GENERAR CORREO
    # ========================================================

    def generar_correo():

        # ----------------------------------------------------
        # VALIDAR VENDEDOR
        # ----------------------------------------------------

        vendedor = vendedor_var.get().strip()

        if not vendedor:

            messagebox.showwarning(
                "Campo obligatorio",
                "Debe ingresar el nombre del vendedor."
            )

            entrada_vendedor.focus()

            return


        # ----------------------------------------------------
        # VALIDAR CLIENTE
        # ----------------------------------------------------

        cliente = cliente_var.get().strip()

        if not cliente:

            messagebox.showwarning(
                "Campo obligatorio",
                "Debe ingresar el nombre del cliente."
            )

            entrada_cliente.focus()

            return


        # ----------------------------------------------------
        # VALIDAR CONDICIÓN
        # ----------------------------------------------------

        if not (
            cliente_tienda_var.get()
            or cliente_horas_var.get()
            or cliente_manana_var.get()
        ):

            messagebox.showwarning(
                "Condición del cliente",
                "Debe seleccionar una condición del cliente."
            )

            return


        # ----------------------------------------------------
        # VALIDAR HORAS
        # ----------------------------------------------------

        if cliente_horas_var.get():

            horas = horas_var.get().strip()

            if not horas:

                messagebox.showwarning(
                    "Campo obligatorio",
                    "Indique en cuántas horas retira el cliente."
                )

                entrada_horas.focus()

                return

        else:

            horas = ""


        # ----------------------------------------------------
        # DESTINATARIOS
        # ----------------------------------------------------

        correos_seleccionados = []

        for nombre_destino, variable in seleccion_correo.items():

            if variable.get():

                correo = CORREOS_DESTINO.get(
                    nombre_destino,
                    ""
                )

                if correo:

                    correos_seleccionados.append(
                        correo
                    )


        if not correos_seleccionados:

            messagebox.showwarning(
                "Falta destinatario",
                "Seleccione al menos un destinatario."
            )

            return


        # ====================================================
        # ASUNTO
        # ====================================================

        asunto = (
            f"POR MAYOR "
            f"{vendedor.upper()}-"
            f"{cliente.upper()}"
        )


        # ====================================================
        # CUERPO
        # ====================================================

        cuerpo = ""

        cuerpo += (
            f"POR MAYOR "
            f"{vendedor.upper()}-"
            f"{cliente.upper()}\n"
        )

        cuerpo += "\n"

        cuerpo += (
            f"Vendedor: "
            f"{vendedor.upper()}\n"
        )

        cuerpo += (
            f"Cliente: "
            f"{cliente.upper()}\n"
        )

        cuerpo += "\n"


        # ====================================================
        # CONDICIÓN DEL CLIENTE
        # ====================================================

        cuerpo += (
            "CONDICIÓN DEL CLIENTE\n"
        )


        if cliente_tienda_var.get():

            cuerpo += (
                "☑ Cliente en tienda\n"
            )


        elif cliente_horas_var.get():

            cuerpo += (
                f"☑ Cliente retira en "
                f"{horas} horas\n"
            )


        elif cliente_manana_var.get():

            cuerpo += (
                "☑ Cliente regresa "
                "(al medio día de mañana)\n"
            )


        # ====================================================
        # SOLICITUD DE VIDEO
        # ====================================================

        cuerpo += "\n"

        cuerpo += (
            "PROCESO - SOLICITUD DE VIDEO\n"
        )


        if solicitar_video_var.get():

            cuerpo += (
                "☑ SOLICITO VIDEO DEL PEDIDO "
                "ANTES DEL DESPACHO\n"
            )

        else:

            cuerpo += (
                "☐ NO SOLICITO VIDEO DEL PEDIDO "
                "ANTES DEL DESPACHO\n"
            )


        # ====================================================
        # URGENTE
        # ====================================================

        if urgente_var.get():

            cuerpo += "\n"

            cuerpo += (
                "URGENTE\n"
            )


        # ====================================================
        # DESTINATARIOS
        # ====================================================

        correo_destino = ",".join(
            correos_seleccionados
        )


        # ====================================================
        # ABRIR GMAIL
        # ====================================================

        enlace = (
            "https://mail.google.com/mail/?view=cm"
            "&fs=1"
            f"&to={urllib.parse.quote(correo_destino)}"
            f"&su={urllib.parse.quote(asunto)}"
            f"&body={urllib.parse.quote(cuerpo)}"
        )


        webbrowser.open(
            enlace
        )


        # Cerrar únicamente Por Mayor
        ventana.destroy()


    # ========================================================
    # BOTÓN GENERAR CORREO
    # ========================================================

    espacio_boton = tk.Frame(
        contenido,
        bg=FONDO
    )

    espacio_boton.pack(
        fill="x",
        pady=(5, 30)
    )


    boton = tk.Button(
        espacio_boton,
        text="✉  GENERAR CORREO",
        width=25,
        height=2,
        font=("Segoe UI", 11, "bold"),
        bg=AZUL,
        fg=BLANCO,
        activebackground=AZUL_CLARO,
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=generar_correo
    )

    boton.pack()


    agregar_hover(
        boton,
        AZUL,
        AZUL_CLARO
    )


    # ========================================================
    # SCROLL CON RUEDA DEL MOUSE
    # ========================================================

    def scroll_mouse(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    canvas.bind_all(
        "<MouseWheel>",
        scroll_mouse
    )


    # ========================================================
    # CENTRAR VENTANA
    # ========================================================

    ventana.update_idletasks()

    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    x = int(
        (pantalla_ancho - ancho) / 2
    )

    y = int(
        (pantalla_alto - alto) / 2
    )

    ventana.geometry(
        f"{ancho}x{alto}+{x}+{y}"
    )


    # ========================================================
    # ENFOCAR CLIENTE
    # ========================================================

    entrada_cliente.focus()