import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import urllib.parse
import os
import json

from config import (
    CORREOS_DESTINO,
    DESTINATARIOS_POR_DEFECTO
)


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
# CASAS DE TRANSPORTE
# ============================================================

CASAS_TRANSPORTE = [
    "24 D SEPTIEMBRE",
    "ALIANZA",
    "ALUASI",
    "BAÑOS",
    "CALUMA",
    "CHIMBORAZO",
    "CHUNCHI",
    "CIFA INTERNACIONAL",
    "CITA EXPRESS",
    "C.I.C.A",
    "C.I.T.I.M",
    "COATUR",
    "COOPERATIVA 16 DE JUNIO",
    "COOPERATIVA 17 DE SEPTIEMBRE",
    "COOPERATIVA 7 DE NOVIEMBRE",
    "COOPERATIVA AEROTAXI",
    "COOPERATIVA ALAUSÍ",
    "COOPERATIVA CARLOS ALBERTO ARAY",
    "COOPERATIVA CENTINELA DEL SUR",
    "COOPERATIVA CIUDAD DE PIÑAS",
    "COOPERATIVA CIVA",
    "COOPERATIVA COACTUR",
    "COOPERATIVA COLTA",
    "COOPERATIVA COSTA AZUL",
    "COOPERATIVA CRUZ DEL SUR",
    "COOPERATIVA EJECUTIVO SAN LUIS",
    "COOPERATIVA EL DORADO",
    "COOPERATIVA EXPRESO MILAGRO",
    "COOPERATIVA FLOR DE LOS RÍOS",
    "COOPERATIVA JIPIJAPA",
    "COOPERATIVA LIBERTAD PENINSULAR",
    "COOPERATIVA LOJA",
    "COOPERATIVA MACAS LIMITADA",
    "COOPERATIVA MI PIEDACITA",
    "COOPERATIVA NAMBIJA",
    "COOPERATIVA ÑUCA LLACTA",
    "COOPERATIVA PEDRO CARBO",
    "COOPERATIVA REINA DEL CAMINO",
    "COOPERATIVA RÍO PAUTE",
    "COOPERATIVA RIOBAMBA",
    "COOPERATIVA RUTAS BALZAREÑAS",
    "COOPERATIVA RUTAS EMPALMEÑAS",
    "COOPERATIVA RUTAS MILAGREÑAS",
    "COOPERATIVA RUTAS VINCEÑAS",
    "COOPERATIVA SAN PEDRITO",
    "COOPERATIVA SANTA ANA",
    "COOPERATIVA SANTA LUCÍA",
    "COOPERATIVA SANTA ROSA DE COLIMES",
    "COOPERATIVA SEÑOR DE LOS MILAGROS",
    "COOPERATIVA SUPER TAXIS CUENCA",
    "COOPERATIVA TOURIS SAN FRANCISCO",
    "COOPERATIVA TRASANDINA",
    "COOPERATIVA TURISMO ORIENTAL",
    "COOPERATIVA VALENCIA",
    "COOPERATIVA ZARACAY",

    "COOP. EXPRESS SUCRE",
    "SAN LUIS",
    "ORIENTAL",
    "T.A.C",
    "VENTANAS",
    "TRANSPORTE SUCRE",
    "ECUATORIANOS PULLMAN",
    "FLOTA BABAHOYO",
    "T.I.A",
    "RUTAS PORTOVEJENSES",
    "RUTAS ORENSES",
    "SEMIERA CORRIER",
    "PANAMERICANA",
    "INTERNACIONAL",
    "TRANSPORTE PIÑAS",
    "SANTA",
    "PATRIA",
    "SAN CRISTOBAL",
    "OCCIDENTALES",
    "BAÑOS",
    "TURISMO ORIENTAL",
    "FLOTA PELILEO",
    "SALITRE A.T.I.S",
    "MARISCAL SUCRE",
    "SANTA MARTHA",
    "S.A.N",
    "F.B.I. BABAHOYO",
    "RIRCAY",
    "TRONCALEÑA",
    "F.I.F.A",
    "FLOTA IMBABURA",
    "TRANSPORTE ECUADOR",
    "FLOTA BOLIVAR",
    "SEMERIA INTERNACIONAL",
    "LIBERPESA",
    "TRANS ESMERALDAS",
    "EXPRESS ATENA",
    "RUTAS SALITRE L.A.S",
    "UNIÓN CARIAMANGA",
    "VALENCIA",
    "LA MANÁ",
    "KENNEDY",
    "EL DORADO",
    "ECUADOR EJECUTIVO",
    "MACAS",
    "PUTUMAYO",
    "POZA HONDA",
    "POSORJA",
    "VILLAMIL",
    "LOS ANDES",
    "ECUACOMPANY",
    "QUIMIS",
    "TRANSPORTE J J",
    "RÍO GUAYAS",
    "TRANSPORTE ORTIZ",
    "SULTANA",
    "ENETSA",
    "SERVITRANS",
    "SERVIURGILES",
    "TICAR",
    "ORO GUAYAS",
    "TRANSPORTE PICHINCHA",
    "TRANSPORTE COTURCIP",
    "TRANSFROSUR",
    "TRAMACO",
    "TRANSCORMOGAL"
]


# ============================================================
# CARGAR GEOGRAFÍA
# ============================================================

def cargar_geografia():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    archivo_geografia = os.path.join(
        base_dir,
        "DATOS",
        "geografia_ecuador.json"
    )

    if not os.path.exists(archivo_geografia):

        messagebox.showerror(
            "Error de datos",
            "No se encontró el archivo:\n\n"
            "DATOS/geografia_ecuador.json\n\n"
            "Verifique la instalación del programa."
        )

        return {}

    try:

        with open(
            archivo_geografia,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

        if not isinstance(datos, dict):

            raise ValueError(
                "El archivo de geografía no tiene "
                "una estructura válida."
            )

        if len(datos) != 24:

            raise ValueError(
                f"El archivo contiene {len(datos)} "
                "provincias. Se esperaban 24."
            )

        return datos

    except Exception as error:

        messagebox.showerror(
            "Error de geografía",
            "No se pudo cargar la información geográfica.\n\n"
            f"Detalle:\n{error}"
        )

        return {}


# ============================================================
# CONSTRUIR LISTA DE CIUDADES Y LOCALIDADES
# ============================================================

def construir_provincias_ciudades(datos):

    resultado = {}

    for provincia, cantones in datos.items():

        localidades_provincia = []

        if not isinstance(cantones, dict):
            continue

        for canton, localidades in cantones.items():

            # ------------------------------------------------
            # AGREGAR CANTÓN
            # ------------------------------------------------

            if (
                isinstance(canton, str)
                and canton.strip()
                and canton.strip()
                not in localidades_provincia
            ):

                localidades_provincia.append(
                    canton.strip()
                )

            # ------------------------------------------------
            # AGREGAR LOCALIDADES
            # ------------------------------------------------

            if isinstance(localidades, list):

                for localidad in localidades:

                    if not isinstance(
                        localidad,
                        str
                    ):
                        continue

                    localidad = localidad.strip()

                    if (
                        localidad
                        and localidad
                        not in localidades_provincia
                    ):

                        localidades_provincia.append(
                            localidad
                        )

        resultado[provincia] = localidades_provincia

    return resultado


# ============================================================
# FUNCIONES VISUALES
# ============================================================

def crear_label(
    parent,
    texto,
    obligatorio=False
):

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
        text=texto + (
            " *"
            if obligatorio
            else ""
        ),
        bg=BLANCO,
        fg=TEXTO,
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
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
        font=(
            "Segoe UI",
            10
        )
    )


def agregar_hover(
    boton,
    normal,
    hover
):

    boton.bind(
        "<Enter>",
        lambda e: boton.configure(
            bg=hover
        )
    )

    boton.bind(
        "<Leave>",
        lambda e: boton.configure(
            bg=normal
        )
    )


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def abrir_transporte():

    # ========================================================
    # CARGAR GEOGRAFÍA ACTUALIZADA
    # ========================================================

    datos_geografia = cargar_geografia()

    if not datos_geografia:
        return

    PROVINCIAS_CIUDADES = (
        construir_provincias_ciudades(
            datos_geografia
        )
    )

    # ========================================================
    # CREAR VENTANA
    # ========================================================

    ventana = tk.Toplevel()

    ventana.title(
        "Envío por Transporte"
    )

    ventana.geometry(
        "620x900"
    )

    ventana.minsize(
        560,
        760
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

    if os.path.exists(
        ruta_icono
    ):

        try:

            ventana.iconbitmap(
                ruta_icono
            )

        except Exception:
            pass

    # ========================================================
    # ESTILO COMBOBOX
    # ========================================================

    estilo = ttk.Style()

    try:

        estilo.theme_use(
            "clam"
        )

    except Exception:
        pass

    estilo.configure(
        "Transporte.TCombobox",
        fieldbackground=BLANCO,
        background=BLANCO,
        foreground=TEXTO,
        bordercolor=BORDE,
        lightcolor=BORDE,
        darkcolor=BORDE,
        padding=7,
        font=(
            "Segoe UI",
            10
        )
    )

    estilo.map(
        "Transporte.TCombobox",
        fieldbackground=[
            (
                "readonly",
                BLANCO
            )
        ],
        foreground=[
            (
                "readonly",
                TEXTO
            )
        ]
    )

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

    if os.path.exists(
        ruta_logo
    ):

        try:

            logo_imagen = tk.PhotoImage(
                file=ruta_logo
            )

            ancho = logo_imagen.width()
            alto = logo_imagen.height()

            if (
                ancho > 100
                or alto > 80
            ):

                factor_x = max(
                    1,
                    ancho // 100
                )

                factor_y = max(
                    1,
                    alto // 80
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
                encabezado,
                image=logo_imagen,
                bg=AZUL_OSCURO
            )

            logo_label.place(
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
        font=(
            "Segoe UI",
            22,
            "bold"
        )
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
        text="SOLICITUD DE ENVÍO POR TRANSPORTE",
        bg=AZUL_OSCURO,
        fg="#DCEBFA",
        font=(
            "Segoe UI",
            10,
            "bold"
        )
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

    scrollbar = ttk.Scrollbar(
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

    # ========================================================
    # ACTUALIZAR SCROLL
    # ========================================================

    def actualizar_scroll(
        event=None
    ):

        canvas.configure(
            scrollregion=canvas.bbox(
                "all"
            )
        )

    contenido.bind(
        "<Configure>",
        actualizar_scroll
    )

    # ========================================================
    # AJUSTAR ANCHO DEL CONTENIDO
    # ========================================================

    def ajustar_ancho(
        event
    ):

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
        font=(
            "Segoe UI",
            11,
            "bold"
        )
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

    predeterminados = (
        DESTINATARIOS_POR_DEFECTO.get(
            "Transporte",
            []
        )
    )

    for nombre, correo in (
        CORREOS_DESTINO.items()
    ):

        variable = tk.BooleanVar(
            value=(
                nombre
                in predeterminados
            )
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
            font=(
                "Segoe UI",
                10
            ),
            anchor="w",
            cursor="hand2"
        )

        casilla.pack(
            anchor="w",
            padx=25,
            pady=2
        )

        seleccion_correo[
            nombre
        ] = variable

    tk.Frame(
        tarjeta_destino,
        bg=BLANCO,
        height=8
    ).pack()

    # ========================================================
    # VARIABLES
    # ========================================================

    cliente_var = tk.StringVar()
    vendedor_var = tk.StringVar()
    cedula_var = tk.StringVar()
    telefono_var = tk.StringVar()
    transporte_var = tk.StringVar()
    provincia_var = tk.StringVar()
    ciudad_var = tk.StringVar()
    direccion_var = tk.StringVar()
    correo_var = tk.StringVar()

    # ========================================================
    # VALIDACIONES
    # ========================================================

    def validar_cedula(
        valor
    ):

        if valor == "":
            return True

        return len(valor) <= 13

    def validar_telefono(
        valor
    ):

        if valor == "":
            return True

        return (
            len(valor) <= 13
            and valor.isdigit()
        )

    validar_cedula_cmd = (
        ventana.register(
            validar_cedula
        )
    )

    validar_telefono_cmd = (
        ventana.register(
            validar_telefono
        )
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
        text="INFORMACIÓN DEL ENVÍO",
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=(
            "Segoe UI",
            11,
            "bold"
        )
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
        pady=(0, 6)
    )

    estilizar_entry(
        entrada_cliente
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
        pady=(0, 6)
    )

    estilizar_entry(
        entrada_vendedor
    )

    # ========================================================
    # CÉDULA
    # ========================================================

    crear_label(
        tarjeta_info,
        "Cédula",
        True
    )

    entrada_cedula = tk.Entry(
        tarjeta_info,
        textvariable=cedula_var,
        validate="key",
        validatecommand=(
            validar_cedula_cmd,
            "%P"
        )
    )

    entrada_cedula.pack(
        fill="x",
        padx=35,
        pady=(0, 6)
    )

    estilizar_entry(
        entrada_cedula
    )

    # ========================================================
    # TELÉFONO
    # ========================================================

    crear_label(
        tarjeta_info,
        "Teléfono",
        True
    )

    entrada_telefono = tk.Entry(
        tarjeta_info,
        textvariable=telefono_var,
        validate="key",
        validatecommand=(
            validar_telefono_cmd,
            "%P"
        )
    )

    entrada_telefono.pack(
        fill="x",
        padx=35,
        pady=(0, 6)
    )

    estilizar_entry(
        entrada_telefono
    )

    # ========================================================
    # CASA DE TRANSPORTE
    # ========================================================

    crear_label(
        tarjeta_info,
        "Casa de Transporte",
        True
    )

    combo_transporte = ttk.Combobox(
        tarjeta_info,
        textvariable=transporte_var,
        values=CASAS_TRANSPORTE,
        state="normal",
        style="Transporte.TCombobox"
    )

    combo_transporte.pack(
        fill="x",
        padx=35,
        pady=(0, 6)
    )

    # ========================================================
    # BUSCAR TRANSPORTE
    # ========================================================

    def buscar_transporte(
        event=None
    ):

        texto = (
            transporte_var
            .get()
            .strip()
            .lower()
        )

        if not texto:

            combo_transporte[
                "values"
            ] = CASAS_TRANSPORTE

            return

        resultados = [
            transporte
            for transporte
            in CASAS_TRANSPORTE
            if texto
            in transporte.lower()
        ]

        combo_transporte[
            "values"
        ] = resultados

    combo_transporte.bind(
        "<KeyRelease>",
        buscar_transporte
    )

    # ========================================================
    # PROVINCIA
    # ========================================================

    crear_label(
        tarjeta_info,
        "Provincia",
        True
    )

    combo_provincia = ttk.Combobox(
        tarjeta_info,
        textvariable=provincia_var,
        values=list(
            PROVINCIAS_CIUDADES.keys()
        ),
        state="readonly",
        style="Transporte.TCombobox"
    )

    combo_provincia.pack(
        fill="x",
        padx=35,
        pady=(0, 6)
    )

    # ========================================================
    # CIUDAD
    # ========================================================

    crear_label(
        tarjeta_info,
        "Ciudad",
        True
    )

    combo_ciudad = ttk.Combobox(
        tarjeta_info,
        textvariable=ciudad_var,
        state="readonly",
        style="Transporte.TCombobox"
    )

    combo_ciudad.pack(
        fill="x",
        padx=35,
        pady=(0, 6)
    )

    # ========================================================
    # ACTUALIZAR CIUDADES
    # ========================================================

    def actualizar_ciudades(
        event=None
    ):

        provincia = (
            provincia_var.get()
        )

        ciudades = (
            PROVINCIAS_CIUDADES.get(
                provincia,
                []
            )
        )

        combo_ciudad[
            "values"
        ] = ciudades

        ciudad_var.set("")

    combo_provincia.bind(
        "<<ComboboxSelected>>",
        actualizar_ciudades
    )

    # ========================================================
    # DIRECCIÓN
    # ========================================================

    crear_label(
        tarjeta_info,
        "Dirección"
    )

    entrada_direccion = tk.Entry(
        tarjeta_info,
        textvariable=direccion_var
    )

    entrada_direccion.pack(
        fill="x",
        padx=35,
        pady=(0, 6)
    )

    estilizar_entry(
        entrada_direccion
    )

    # ========================================================
    # CORREO ELECTRÓNICO
    # ========================================================

    crear_label(
        tarjeta_info,
        "Correo Electrónico"
    )

    entrada_correo = tk.Entry(
        tarjeta_info,
        textvariable=correo_var
    )

    entrada_correo.pack(
        fill="x",
        padx=35,
        pady=(0, 15)
    )

    estilizar_entry(
        entrada_correo
    )

    # ========================================================
    # OBSERVACIONES
    # ========================================================

    tarjeta_observaciones = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tarjeta_observaciones.pack(
        fill="x",
        padx=35,
        pady=12
    )

    tk.Label(
        tarjeta_observaciones,
        text="OBSERVACIONES",
        bg=BLANCO,
        fg=AZUL_OSCURO,
        font=(
            "Segoe UI",
            11,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 8)
    )

    tk.Frame(
        tarjeta_observaciones,
        bg=AZUL,
        height=2
    ).pack(
        fill="x",
        padx=20
    )

    entrada_observaciones = tk.Text(
        tarjeta_observaciones,
        height=4,
        wrap="word",
        bg=BLANCO,
        fg=TEXTO,
        insertbackground=AZUL,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDE,
        highlightcolor=AZUL,
        font=(
            "Segoe UI",
            10
        )
    )

    entrada_observaciones.pack(
        fill="x",
        padx=35,
        pady=(10, 20)
    )

    # ========================================================
    # GENERAR CORREO
    # ========================================================

    def generar_correo():

        # ----------------------------------------------------
        # VALIDAR CAMPOS OBLIGATORIOS
        # ----------------------------------------------------

        campos_obligatorios = [
            (
                "Cliente",
                cliente_var.get()
            ),
            (
                "Vendedor",
                vendedor_var.get()
            ),
            (
                "Cédula",
                cedula_var.get()
            ),
            (
                "Teléfono",
                telefono_var.get()
            ),
            (
                "Casa de Transporte",
                transporte_var.get()
            ),
            (
                "Provincia",
                provincia_var.get()
            ),
            (
                "Ciudad",
                ciudad_var.get()
            )
        ]

        for nombre, valor in (
            campos_obligatorios
        ):

            if not valor.strip():

                messagebox.showwarning(
                    "Campo obligatorio",
                    "Debe completar el campo:\n\n"
                    f"{nombre}"
                )

                return

        # ----------------------------------------------------
        # VALIDACIÓN CÉDULA
        # ----------------------------------------------------

        cedula = (
            cedula_var
            .get()
            .strip()
        )

        if len(cedula) > 13:

            messagebox.showwarning(
                "Cédula inválida",
                "La Cédula no puede tener "
                "más de 13 caracteres."
            )

            entrada_cedula.focus()

            return

        # ----------------------------------------------------
        # VALIDACIÓN TELÉFONO
        # ----------------------------------------------------

        telefono = (
            telefono_var
            .get()
            .strip()
        )

        if (
            not telefono.isdigit()
            or len(telefono) > 13
        ):

            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono debe contener "
                "únicamente números y tener "
                "máximo 13 dígitos."
            )

            entrada_telefono.focus()

            return

        # ----------------------------------------------------
        # VALIDAR DESTINATARIOS
        # ----------------------------------------------------

        correos_seleccionados = []

        for (
            nombre,
            variable
        ) in seleccion_correo.items():

            if variable.get():

                correo = (
                    CORREOS_DESTINO.get(
                        nombre,
                        ""
                    )
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

        # ----------------------------------------------------
        # OBSERVACIONES
        # ----------------------------------------------------

        observaciones = (
            entrada_observaciones
            .get(
                "1.0",
                "end-1c"
            )
            .strip()
        )

        # ----------------------------------------------------
        # DATOS DEL FORMULARIO
        # ----------------------------------------------------

        datos = f"""
Cliente: {cliente_var.get()}
Vendedor: {vendedor_var.get()}
Cédula: {cedula_var.get()}
Teléfono: {telefono_var.get()}
Casa de Transporte: {transporte_var.get()}
Origen: Guayaquil
Provincia: {provincia_var.get()}
Ciudad: {ciudad_var.get()}
Dirección: {direccion_var.get()}
Correo Electrónico: {correo_var.get()}
Observaciones: {observaciones}
"""

        # ----------------------------------------------------
        # DESTINATARIOS
        # ----------------------------------------------------

        correo_destino = ",".join(
            correos_seleccionados
        )

        # ----------------------------------------------------
        # ASUNTO
        # ----------------------------------------------------

        asunto = (
            "ENVIO POR TRANSPORTE "
            f"{vendedor_var.get().strip()} - "
            f"{cliente_var.get().strip()}"
        )

        # ----------------------------------------------------
        # CUERPO DEL CORREO
        # ----------------------------------------------------

        cuerpo = f"""Buenos días,

Solicito apoyo con el siguiente envío:

{datos}

El origen del envío es Guayaquil.

Agradezco su apoyo con la gestión y confirmación.

Gracias.
"""

        # ----------------------------------------------------
        # ABRIR GMAIL
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # CERRAR FORMULARIO
        # ----------------------------------------------------

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
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
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
    # SCROLL DEL FORMULARIO
    # ========================================================

    def scroll_mouse(event):

        # ----------------------------------------------------
        # NO MOVER COMBOBOX CON LA RUEDA
        # ----------------------------------------------------

        if event.widget in (
            combo_provincia,
            combo_ciudad,
            combo_transporte
        ):

            return "break"

        # ----------------------------------------------------
        # MOVER EL FORMULARIO
        # ----------------------------------------------------

        if event.delta:

            canvas.yview_scroll(
                int(
                    -1 *
                    (
                        event.delta / 120
                    )
                ),
                "units"
            )

        return "break"

    # --------------------------------------------------------
    # SCROLL GENERAL
    # --------------------------------------------------------

    canvas.bind_all(
        "<MouseWheel>",
        scroll_mouse
    )

    # --------------------------------------------------------
    # BLOQUEAR RUEDA EN COMBOBOX
    # --------------------------------------------------------

    combo_provincia.bind(
        "<MouseWheel>",
        lambda event: "break"
    )

    combo_ciudad.bind(
        "<MouseWheel>",
        lambda event: "break"
    )

    combo_transporte.bind(
        "<MouseWheel>",
        lambda event: "break"
    )

    # ========================================================
    # CENTRAR VENTANA
    # ========================================================

    ventana.update_idletasks()

    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    pantalla_ancho = (
        ventana.winfo_screenwidth()
    )

    pantalla_alto = (
        ventana.winfo_screenheight()
    )

    x = int(
        (
            pantalla_ancho
            - ancho
        ) / 2
    )

    y = int(
        (
            pantalla_alto
            - alto
        ) / 2
    )

    ventana.geometry(
        f"{ancho}x{alto}+{x}+{y}"
    )

    # ========================================================
    # ENFOCAR CLIENTE
    # ========================================================

    entrada_cliente.focus()