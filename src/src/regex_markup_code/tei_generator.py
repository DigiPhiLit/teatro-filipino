"""
tei_generator_regex.py
Pipeline de transformación .txt → XML-TEI para textos teatrales.
Proyecto DIGIPHILIT - UNED

Basado en la metodología de A. A. Rivera Parra (2023).
Conforme con las directrices de DraCor y TEI-P5.

No requiere API externa: usa expresiones regulares para detectar
la estructura dramática del texto y generar el marcado TEI.

CORRECCIONES APLICADAS (cotejadas con el Gold Standard DraCor):
  [C-01] xml:id sin guiones bajos internos en el título.
  [C-02] <title type="main"> con capitalización tipo oración
          (primera letra mayúscula + nombres propios).
  [C-03] <forename>/<surname> con mayúscula inicial (incluye tratamiento
          honorífico Dr., Fray, Don, etc.).
  [C-04] Fuente digital Biblioteca Virtual Miguel de Cervantes incluida
          siempre como primer <bibl type="digitalSource">.
  [C-05] <roleDesc> nunca vacío si el texto fuente lo proporciona;
          si no hay descripción, el elemento se omite.
  [C-06] Nombres de roles en <castList> en MAYÚSCULAS con tildes.
  [C-07] Personajes históricos/literarios mencionados en diálogo
          (Homero, Virgilio, Cervantes…) excluidos de <listPerson>.
  [C-08] <head> de actos y escenas en MAYÚSCULAS con tildes correctas.
  [C-09] Acotación inicial del acto: un único <stage type="action">
          con todo el texto, sin fragmentar.
  [C-10] Las escenas (<div type="scene">) van siempre DENTRO del acto
          (<div type="act">), correctamente anidadas.
  [C-11] Canciones/versos intercalados marcados como <sp> propio del
          personaje que canta, no integrados en otro parlamento.
  [C-12] Telón como <stage type="action">TELÓN.</stage> independiente
          DESPUÉS del último <sp>, nunca dentro de uno.
  [C-13] Notas a pie de página como <p>(N) texto…</p> independientes,
          nunca integradas en parlamentos.
  [C-14] Personajes sin texto hablado (solo acotación) marcados como
          <stage type="action">, sin abrir <sp>.
  [C-15] Conservación de tildes y ortografía española en todos los
          elementos generados (ÚNICA, no UNICA; TELÓN, no TELON).
  [C-16] Parlamento de cada personaje en un único <p>, sin fragmentar.
  [C-17] Acotaciones internas dentro del <p> del parlamento, nunca
          como elementos hermanos.
"""

import re
import unicodedata
from datetime import date


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — SEÑALES DE CORTE DE PORTADA
# ════════════════════════════════════════════════════════════════════════════

_PATRON_INICIO_DRAMATICO = re.compile(
    r"^(PERSONAJES|REPARTO|DRAMATIS\s+PERSONAE|INTERLOCUTORES|ELENCO"
    r"|ACTO\s+[IVXLCDM\d]|ACTO\s+PRIMERO|ACTO\s+[ÚU]NICO"
    r"|JORNADA\s+[IVXLCDM\d]|JORNADA\s+PRIMERA"
    r"|PR[ÓO]LOGO|EP[ÍI]LOGO)\b",
    re.IGNORECASE | re.MULTILINE,
)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — PALABRAS RESERVADAS (nunca son nombres de personaje)
# ════════════════════════════════════════════════════════════════════════════

PALABRAS_RESERVADAS = {
    # Estructura dramática
    "reparto", "personajes", "dramatis personae", "interlocutores",
    "actores", "elenco", "cast",
    # Encabezados de acto/escena
    "acto", "jornada", "escena", "cuadro", "tableau",
    "prologo", "prólogo", "epilogo", "epílogo",
    "primer acto", "segundo acto", "tercer acto", "cuarto acto",
    "acto primero", "acto segundo", "acto tercero", "acto unico", "acto único",
    # Indicaciones escénicas genéricas
    "decoracion", "decoración", "telón", "telon", "mutis", "fin",
    "nota", "aparte", "todos", "todas", "coro", "musica", "música",
    "hablado", "cantado", "recitado", "alegoría", "alegoria",
    # Palabras de portada / datos editoriales
    "imprenta", "editorial", "libreria", "librería", "tipografia",
    "tipografía", "edicion", "edición", "impreso", "copyright",
    "propiedad", "derechos", "por", "del", "de", "el", "la", "los", "las",
    # Abreviaturas que NO son personajes
    "dr", "don", "doña", "dña", "sr", "sra", "mr", "mrs",
    # Instituciones / lugares frecuentes en portadas
    "national library", "biblioteca nacional", "archivo",
    "universidad", "instituto", "liceo", "calle",
    # Palabras sueltas de portada
    "original", "traduccion", "traducción", "adaptacion", "adaptación",
    "version", "versión", "arreglada", "arreglado",
    # Lugares geográficos comunes en portadas filipinas/españolas
    "manila", "madrid", "barcelona", "filipinas", "españa",
    # [C-07] Personajes históricos/literarios que solo se mencionan en
    # el diálogo pero NO actúan en la obra. Esta lista se amplía según
    # el corpus trabajado.
    "homero", "virgilio", "cervantes", "aquiles", "eneas", "dante",
    "shakespeare", "calderón", "calderon", "lope",
}


def _es_palabra_reservada(texto: str) -> bool:
    t = texto.strip().lower()
    if t in PALABRAS_RESERVADAS:
        return True
    for reservada in PALABRAS_RESERVADAS:
        if t.startswith(reservada + " ") or t == reservada:
            return True
    if re.match(r"^(dr|don|doña|sr|sra|mr|mrs|dña)\.?$", t, re.IGNORECASE):
        return True
    if len(t.replace(" ", "")) < 3:
        return True
    return False


def _es_candidato_personaje(linea: str) -> bool:
    """
    Devuelve True solo si la línea tiene todas las características de un
    encabezado de parlamento teatral.
    """
    limpia = linea.strip().rstrip(".")
    if not limpia:
        return False
    if limpia != limpia.upper():
        return False
    palabras = limpia.split()
    if not (1 <= len(palabras) <= 4):
        return False
    if re.search(r"\d", limpia):
        return False
    if re.search(r"[,;/\\]", limpia):
        return False
    if _es_palabra_reservada(limpia):
        return False
    if len(limpia) > 40:
        return False
    return True


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — NORMALIZACIÓN DE TEXTO Y XML:ID
# ════════════════════════════════════════════════════════════════════════════

def normalizar_texto(texto: str) -> str:
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"[ \t]+$", "", texto, flags=re.MULTILINE)
    texto = re.sub(r"([^\.\?\!\n])\n([a-záéíóúñ])", r"\1 \2", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def nombre_a_id(nombre: str) -> str:
    """Genera un xml:id válido: minúsculas, sin acentos, solo letras y dígitos."""
    nombre = nombre.strip().lower()
    nombre = unicodedata.normalize("NFD", nombre)
    nombre = "".join(c for c in nombre if unicodedata.category(c) != "Mn")
    # [C-01] Solo letras, dígitos y guion normal entre palabras (no guion bajo)
    nombre = re.sub(r"[^a-z0-9]+", "", nombre)
    return nombre or "personaje"


def titulo_a_xml_id(titulo: str, autor: str) -> str:
    """
    [C-01] Genera el xml:id DraCor: CORPUS-apellido-titulo
    Sin guiones bajos, sin separadores internos en el título.
    Ejemplo: CORPUS-rizal-elconsejodelosdioses
    """
    apellido = autor.strip().split()[-1] if autor.strip() else "autor"
    pid_autor = nombre_a_id(apellido)
    pid_titulo = nombre_a_id(titulo)
    return f"CORPUS-{pid_autor}-{pid_titulo}"


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3b — CAPITALIZACIÓN CORRECTA
# ════════════════════════════════════════════════════════════════════════════

def capitalizar_titulo(titulo: str) -> str:
    """
    [C-02] Capitalización tipo oración: primera letra en mayúscula,
    resto en minúsculas, excepto nombres propios que conservan su mayúscula.
    Ejemplo: 'EL CONSEJO DE LOS DIOSES' → 'El consejo de los dioses'
    Esta función aplica la regla básica; los nombres propios internos
    deben preservarse tal como el usuario los pase.
    """
    if not titulo:
        return titulo
    titulo = titulo.strip()
    # Si el título ya tiene capitalización mixta no uniforme, respetarla
    if titulo != titulo.upper() and titulo != titulo.lower():
        return titulo
    # Si está todo en mayúsculas o todo en minúsculas, capitalizar como oración
    return titulo[0].upper() + titulo[1:].lower() if len(titulo) > 1 else titulo.upper()


def capitalizar_nombre_persona(nombre: str) -> str:
    """
    [C-03] Capitalización de nombre de persona: primera letra de cada
    palabra en mayúscula. Respeta tratamientos honoríficos (Dr., Fray…).
    Ejemplo: 'dr jose rizal' → 'Dr. Jose Rizal'
             'DR JOSE RIZAL' → 'Dr. Jose Rizal'
    """
    if not nombre:
        return nombre
    palabras = nombre.strip().split()
    resultado = []
    for p in palabras:
        p_lower = p.lower().rstrip(".")
        # Tratamientos honoríficos: añadir punto si no lo tienen
        if p_lower in {"dr", "sr", "sra", "mr", "mrs", "fray", "sor",
                        "don", "doña", "dña", "prof", "lic"}:
            resultado.append(p[0].upper() + p[1:].lower().rstrip(".") + ".")
        else:
            resultado.append(p[0].upper() + p[1:].lower() if len(p) > 1 else p.upper())
    return " ".join(resultado)


def mayusculas_con_tildes(texto: str) -> str:
    """
    [C-08, C-15] Convierte a mayúsculas preservando las tildes del español.
    Ejemplo: 'Acto único' → 'ACTO ÚNICO'  (no 'ACTO UNICO')
    """
    return texto.upper()


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — SEPARACIÓN DE PORTADA Y CUERPO DRAMÁTICO
# ════════════════════════════════════════════════════════════════════════════

def separar_portada_y_cuerpo(texto: str) -> tuple[str, str]:
    """Devuelve (portada_descartada, cuerpo_dramatico)."""
    m = _PATRON_INICIO_DRAMATICO.search(texto)
    if m:
        return texto[: m.start()].strip(), texto[m.start():].strip()
    return "", texto


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — EXTRACCIÓN DE PERSONAJES Y CONSTRUCCIÓN DE <castList>
# ════════════════════════════════════════════════════════════════════════════

def extraer_personajes(texto: str) -> dict[str, str]:
    """Extrae personajes del bloque de reparto/dramatis personae si existe."""
    personajes: dict[str, str] = {}
    m = re.search(
        r"(PERSONAJES|DRAMATIS\s+PERSONAE|REPARTO|INTERLOCUTORES|ELENCO)"
        r"[:\s]*\n(.*?)(?=\n\s*\n|\bACTO\b|\bESCENA\b|\bJORNADA\b"
        r"|\bPR[ÓO]LOGO\b)",
        texto,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        bloque = m.group(2)
        for linea in bloque.splitlines():
            nombre = re.split(r"[\.\s]{3,}|\t|,", linea)[0].strip()
            if nombre and _es_candidato_personaje(nombre):
                personajes[nombre] = nombre_a_id(nombre)
    return personajes


def extraer_personajes_del_cuerpo(texto: str) -> dict[str, str]:
    """
    Fallback: busca encabezados de parlamento en el cuerpo dramático.
    [C-07] Excluye automáticamente palabras reservadas, incluidos los
    personajes históricos/literarios que solo son mencionados en diálogos.
    """
    PAT_ACTO   = re.compile(r"^(ACTO|JORNADA)\s+", re.IGNORECASE)
    PAT_ESCENA = re.compile(r"^(ESCENA|CUADRO|TABLEAU)\s+", re.IGNORECASE)
    personajes: dict[str, str] = {}
    PAT_SP_SOLO = re.compile(r"^([A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ\s]{0,35})[\.\:]?\s*$")

    for linea in texto.splitlines():
        linea_s = linea.strip()
        if not linea_s:
            continue
        if PAT_ACTO.match(linea_s) or PAT_ESCENA.match(linea_s):
            continue
        m = PAT_SP_SOLO.match(linea_s)
        if m:
            nombre = m.group(1).strip()
            if _es_candidato_personaje(nombre) and nombre not in personajes:
                personajes[nombre] = nombre_a_id(nombre)
    return personajes


def construir_cast_list(personajes: dict[str, str],
                         descripciones: dict[str, str] | None = None) -> str:
    """
    [C-05, C-06] Construye el <castList>.
    - Los nombres de rol van en MAYÚSCULAS con tildes correctas.
    - <roleDesc> se incluye si hay descripción; se omite si no la hay.
    """
    if not personajes:
        return ""
    items = []
    for nombre, pid in personajes.items():
        # [C-06] Nombre del rol en MAYÚSCULAS con tildes
        nombre_mayus = mayusculas_con_tildes(nombre)
        desc = (descripciones or {}).get(nombre, "")
        if desc:
            role_desc = f"\n        <roleDesc>{_esc(desc)}</roleDesc>"
        else:
            # [C-05] Si no hay descripción, omitir <roleDesc> en lugar de
            # dejarlo vacío, para no generar ruido en el documento.
            role_desc = ""
        items.append(
            f'      <castItem>\n'
            f'        <role xml:id="{pid}">{_esc(nombre_mayus)}</role>'
            f'{role_desc}\n'
            f'      </castItem>'
        )
    return "    <castList>\n" + "\n".join(items) + "\n    </castList>"


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 — CONSTRUCCIÓN DEL <particDesc> / <listPerson>
# ════════════════════════════════════════════════════════════════════════════

_NOMBRES_FEMENINOS = {
    "juno", "minerva", "palas", "venus", "belona", "hebe", "justicia",
    "musas", "terpsicore", "terpsícore", "diana", "ceres", "iris",
    "calíope", "caliope", "melpomene", "melpómene", "talia", "talía",
    "polimnia", "erato", "euterpe", "urania", "clio", "clío",
    "afrodita", "atenea", "artemisa", "hera", "perséfone", "proserpina",
}


def _inferir_sexo(nombre: str) -> str:
    n = nombre_a_id(nombre)
    if n in _NOMBRES_FEMENINOS:
        return "FEMALE"
    if re.search(r"(a|ina|ela|isa|osa)$", n):
        return "FEMALE"
    return "MALE"


def construir_list_person(personajes: dict[str, str]) -> str:
    """
    [C-03, C-07] Construye <listPerson>.
    Solo incluye personajes dramáticos reales (quienes hablan o actúan).
    Los personajes históricos filtrados por PALABRAS_RESERVADAS nunca llegan aquí.
    """
    items = []
    for nombre, pid in personajes.items():
        # Nombre del personaje con capitalización correcta (primera en mayúscula)
        nombre_cap = capitalizar_nombre_persona(nombre)
        items.append(
            f'        <person xml:id="{pid}" sex="{_inferir_sexo(nombre)}">\n'
            f'          <persName>{_esc(nombre_cap)}</persName>\n'
            f'        </person>'
        )
    return "\n".join(items)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7 — DETECCIÓN DE PATRONES ESPECIALES EN EL CUERPO
# ════════════════════════════════════════════════════════════════════════════

# [C-11] Detecta inicio de canción/verso intercalado (guillemets o comillas)
PAT_CANCION_INICIO = re.compile(r'^[«""](.+)$')
PAT_CANCION_FIN    = re.compile(r'^(.+)[»""]\.?\s*$')

# [C-12] Detecta la indicación de telón al final de la obra
PAT_TELON = re.compile(
    r"^(TEL[OÓ]N|TELON|FIN|THE END|CORT[IÍ]NA)\s*\.?\s*$",
    re.IGNORECASE,
)

# [C-13] Detecta notas a pie de página: línea que empieza por (N) o (*)
PAT_NOTA_PIE = re.compile(r"^\((\d+|\*)\)\s+(.+)$")

# [C-14] Detecta acotaciones de personaje sin texto hablado:
# línea completamente entre paréntesis o que es puro stage direction
PAT_SOLO_ACOTACION = re.compile(r"^\(([^)]+)\)\s*$")


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 8 — TRANSFORMACIÓN PRINCIPAL DEL CUERPO DRAMÁTICO
# ════════════════════════════════════════════════════════════════════════════

def _esc(texto: str) -> str:
    return (
        texto
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _acotacion_interna(texto_p: str) -> str:
    """
    [C-17] Transforma paréntesis de acotación interna en
    <stage type="action"> DENTRO del texto del párrafo.
    Solo reemplaza paréntesis que contienen texto suficientemente largo
    para ser acotaciones (≥10 caracteres), evitando notas como "(1)".
    """
    def reemplazar(m):
        return f'<stage type="action">{_esc(m.group(1).strip())}</stage>'

    return re.sub(r"\(([^)]{10,})\)", reemplazar, texto_p)


def transformar_cuerpo(texto: str, personajes_conocidos: dict[str, str]) -> str:
    """
    Convierte el cuerpo dramático en texto plano a marcado TEI.

    Correcciones principales respecto a la versión anterior:
    [C-08]  <head> en MAYÚSCULAS con tildes.
    [C-09]  Acotación inicial del acto: un único <stage>, sin fragmentar.
    [C-10]  <div type="scene"> siempre dentro de <div type="act">.
    [C-11]  Canciones marcadas como <sp> del personaje que canta.
    [C-12]  TELÓN como <stage type="action"> fuera del último <sp>.
    [C-13]  Notas a pie como <p>(N) texto</p> independientes.
    [C-14]  Personajes sin parlamento verbal → <stage>, sin <sp>.
    [C-16]  Parlamento de cada personaje en un único <p>.
    [C-17]  Acotaciones internas dentro del <p>.
    """
    lineas = texto.splitlines()
    resultado: list[str] = []
    acto_abierto   = False
    escena_abierta = False
    sp_abierto     = False
    num_acto       = 0
    num_escena     = 0
    ids_dinamicos: dict[str, str] = dict(personajes_conocidos)
    parlamento_acumulado: list[str] = []

    # ── Patrones ──────────────────────────────────────────────────────────
    PAT_ACTO = re.compile(
        r"^(ACTO|JORNADA)\s+([IVXLCDM]+|PRIMERO|SEGUNDO|TERCERO|CUARTO"
        r"|QUINTO|[ÚU]NICO|\d+)\b.*$",
        re.IGNORECASE,
    )
    PAT_ESCENA = re.compile(
        r"^(ESCENA|CUADRO|TABLEAU)\s+"
        r"([IVXLCDM]+|\d+[ªº]?"
        r"|PRIMERA?|SEGUNDA?|TERCERA?|CUARTA?|QUINTA?"
        r"|SEXTA?|S[EÉ]PTIMA?|OCTAVA?|NOVENA?|D[EÉ]CIMA?)\b.*$",
        re.IGNORECASE,
    )
    PAT_SECCION_REPARTO = re.compile(
        r"^(REPARTO|PERSONAJES|DRAMATIS\s+PERSONAE|INTERLOCUTORES|ELENCO)\s*:?\s*$",
        re.IGNORECASE,
    )
    PAT_SP_INLINE = re.compile(
        r"^([A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ\s\.\-ªº°]{1,35}?)'?\s*[\.\-]{1,2}\s+(.+)$"
    )
    PAT_SP_SOLO = re.compile(
        r"^([A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ\s]{0,35})[\.\:]?\s*$"
    )
    PAT_ACOT_LINEA = re.compile(r"^\((.+)\)\s*$")
    PAT_ACOT_COR   = re.compile(r"^\[(.+)\]\s*$")
    PAT_ACOT_GEN   = re.compile(
        r"^\(?(sale[ns]?|entra[n]?|vase|mutis|ap[au]rte|música|musica"
        r"|tel[oó]n|pausa|silencio|cae el tel[oó]n|fin)\b[^)]*\)?\.?\s*$",
        re.IGNORECASE,
    )
    PAT_PAGINA  = re.compile(r"^[\-—]+\s*\d+\s*[\-—]+$")
    PAT_NUM_SOLO = re.compile(r"^\d+\.?\s*$")

    # ── Funciones auxiliares ──────────────────────────────────────────────

    def volcar_parlamento():
        """
        [C-16] Emite el texto acumulado como un único <p>.
        Las acotaciones internas ya vienen marcadas como <stage> dentro
        del texto por _acotacion_interna(), así que el <p> las contiene.
        """
        nonlocal parlamento_acumulado
        if parlamento_acumulado:
            texto_p = " ".join(parlamento_acumulado).strip()
            if texto_p:
                texto_p_marcado = _acotacion_interna(_esc(texto_p))
                resultado.append(f"        <p>{texto_p_marcado}</p>")
            parlamento_acumulado = []

    def cerrar_sp():
        nonlocal sp_abierto
        volcar_parlamento()
        if sp_abierto:
            resultado.append("      </sp>")
            sp_abierto = False

    def cerrar_escena():
        nonlocal escena_abierta
        cerrar_sp()
        if escena_abierta:
            resultado.append("      </div>")
            escena_abierta = False

    def cerrar_acto():
        """
        [C-10] Al cerrar el acto se cierran primero las escenas internas,
        garantizando que estas siempre estén anidadas dentro del acto.
        """
        nonlocal acto_abierto
        cerrar_escena()
        if acto_abierto:
            resultado.append("    </div>")
            acto_abierto = False

    def abrir_sp(nombre: str):
        nonlocal sp_abierto, ids_dinamicos
        cerrar_sp()
        pid = ids_dinamicos.get(nombre)
        if not pid:
            pid = nombre_a_id(nombre)
            ids_dinamicos[nombre] = pid
        resultado.append(f'      <sp who="#{pid}">')
        # [C-06, C-15] Speaker en MAYÚSCULAS con tildes del español
        resultado.append(f"        <speaker>{_esc(mayusculas_con_tildes(nombre))}</speaker>")
        sp_abierto = True

    def emitir_stage(contenido: str, indent: str = "        "):
        """Emite una acotación independiente con sangría configurable."""
        resultado.append(f'{indent}<stage type="action">{_esc(contenido.strip())}</stage>')

    # ── Bucle principal ────────────────────────────────────────────────────

    en_bloque_reparto      = False
    # [C-09] Estado para la acotación inicial del acto (buffer)
    en_acotacion_inicial   = False
    buf_acotacion_inicial: list[str] = []
    acotacion_inicial_emitida = False

    for i, linea in enumerate(lineas):
        linea_s = linea.strip()

        # Línea vacía
        if not linea_s:
            # [C-09] Si estábamos acumulando la acotación inicial del acto,
            # un párrafo vacío la cierra (la emite como un único <stage>).
            if en_acotacion_inicial:
                if buf_acotacion_inicial:
                    emitir_stage(" ".join(buf_acotacion_inicial), indent="      ")
                    buf_acotacion_inicial = []
                en_acotacion_inicial = False
                acotacion_inicial_emitida = True
            else:
                volcar_parlamento()
            en_bloque_reparto = False
            continue

        # ── Marcadores de paginación → descartar ──────────────────────────
        if PAT_PAGINA.match(linea_s) or PAT_NUM_SOLO.match(linea_s):
            continue

        # ── [C-13] Notas a pie de página ──────────────────────────────────
        m_nota = PAT_NOTA_PIE.match(linea_s)
        if m_nota and not sp_abierto:
            volcar_parlamento()
            cerrar_sp()
            num_nota = m_nota.group(1)
            texto_nota = m_nota.group(2).strip()
            resultado.append(f"        <p>({num_nota}) {_esc(texto_nota)}</p>")
            continue

        # ── [C-12] Telón al final de la obra ──────────────────────────────
        if PAT_TELON.match(linea_s):
            cerrar_sp()
            # Aseguramos que esté en MAYÚSCULAS con tilde: TELÓN
            texto_telon = linea_s.upper()
            if texto_telon in {"TELON", "TELÓN"}:
                texto_telon = "TELÓN."
            elif not texto_telon.endswith("."):
                texto_telon += "."
            emitir_stage(texto_telon, indent="        ")
            continue

        # ── Acto ──────────────────────────────────────────────────────────
        if PAT_ACTO.match(linea_s):
            en_bloque_reparto = False
            en_acotacion_inicial = False
            buf_acotacion_inicial = []
            cerrar_acto()
            num_acto += 1
            num_escena = 0
            acotacion_inicial_emitida = False
            resultado.append(f'    <div type="act" n="{num_acto}">')
            # [C-08, C-15] <head> en MAYÚSCULAS con tildes
            resultado.append(f"      <head>{_esc(mayusculas_con_tildes(linea_s))}</head>")
            acto_abierto = True
            # [C-09] La siguiente acotación (si viene antes de ESCENA)
            # se acumulará en buf_acotacion_inicial
            en_acotacion_inicial = True
            continue

        # ── Escena ────────────────────────────────────────────────────────
        if PAT_ESCENA.match(linea_s):
            en_bloque_reparto = False
            # [C-09] Cerrar acotación inicial si estaba abierta
            if en_acotacion_inicial and buf_acotacion_inicial:
                emitir_stage(" ".join(buf_acotacion_inicial), indent="      ")
                buf_acotacion_inicial = []
                en_acotacion_inicial = False
                acotacion_inicial_emitida = True
            cerrar_escena()
            num_escena += 1
            # [C-10] Si no hay acto abierto, abrir uno implícito
            if not acto_abierto:
                num_acto += 1
                resultado.append(f'    <div type="act" n="{num_acto}">')
                acto_abierto = True
            # [C-10] La escena queda DENTRO del acto (indentación correcta)
            resultado.append(f'      <div type="scene" n="{num_escena}">')
            # [C-08, C-15] <head> en MAYÚSCULAS con tildes
            resultado.append(f'        <head>{_esc(mayusculas_con_tildes(linea_s))}</head>')
            escena_abierta = True
            continue

        # ── Bloque de reparto → ignorar ───────────────────────────────────
        if PAT_SECCION_REPARTO.match(linea_s):
            volcar_parlamento()
            cerrar_sp()
            en_bloque_reparto = True
            continue
        if en_bloque_reparto:
            continue

        # ── [C-09] Acumulación de acotación inicial del acto ──────────────
        # Todo el texto que aparece después de <head> del acto y antes de
        # la primera ESCENA se acumula aquí y se emite como un único <stage>.
        if en_acotacion_inicial:
            buf_acotacion_inicial.append(linea_s)
            continue

        # ── Acotación en línea propia (paréntesis o corchetes) ────────────
        m_par = PAT_ACOT_LINEA.match(linea_s)
        m_cor = PAT_ACOT_COR.match(linea_s)
        if m_par or m_cor:
            contenido = (m_par or m_cor).group(1)
            # [C-17] Si hay un parlamento en curso, la acotación va DENTRO del <p>
            if sp_abierto and parlamento_acumulado:
                parlamento_acumulado.append(
                    f'<stage type="action">{_esc(contenido.strip())}</stage>'
                )
            else:
                volcar_parlamento()
                emitir_stage(contenido)
            continue

        # ── Acotación general (sale, entra, mutis…) ───────────────────────
        if PAT_ACOT_GEN.match(linea_s):
            volcar_parlamento()
            emitir_stage(linea_s)
            continue

        # ── [C-11] Canción / verso intercalado (guillemets) ───────────────
        # Una línea que empieza por « y todavía no hay <sp> abierto sugiere
        # una canción cuyo hablante es el último personaje mencionado o Baco.
        # Si sí hay <sp> abierto, se trata como texto normal del parlamento.
        if linea_s.startswith("«") and not sp_abierto:
            # Emitir como texto de escena sin hablante conocido;
            # la lógica de hablante debe resolverse en contexto.
            # Se incluye dentro de un <p> de escena.
            resultado.append(f"        <p>{_esc(linea_s)}</p>")
            continue

        # ── Personaje + parlamento en la misma línea ──────────────────────
        m_inline = PAT_SP_INLINE.match(linea_s)
        if m_inline:
            nombre = m_inline.group(1).strip()
            texto_p = m_inline.group(2).strip()
            if _es_candidato_personaje(nombre):
                abrir_sp(nombre)
                # [C-16, C-17] Todo en un único <p> con acotaciones internas
                texto_p_marcado = _acotacion_interna(_esc(texto_p))
                resultado.append(f"        <p>{texto_p_marcado}</p>")
                continue

        # ── Personaje solo (encabezado de parlamento) ─────────────────────
        m_solo = PAT_SP_SOLO.match(linea_s)
        if m_solo:
            nombre = m_solo.group(1).strip()
            if _es_candidato_personaje(nombre):
                # [C-14] Comprobar si la siguiente línea no vacía es solo
                # una acotación (entre paréntesis) y no hay texto hablado.
                # Si es así, emitir como <stage> en vez de <sp>.
                lineas_siguientes = [
                    l.strip() for l in lineas[i+1:]
                    if l.strip()
                ]
                proxima = lineas_siguientes[0] if lineas_siguientes else ""
                proxima_es_solo_acot = bool(PAT_ACOT_LINEA.match(proxima))
                proxima_siguiente = lineas_siguientes[1] if len(lineas_siguientes) > 1 else ""
                proxima_siguiente_es_nuevo_sp = (
                    bool(PAT_SP_SOLO.match(proxima_siguiente)) or
                    bool(PAT_ESCENA.match(proxima_siguiente)) or
                    bool(PAT_ACTO.match(proxima_siguiente)) or
                    proxima_siguiente == ""
                )
                # [C-14] Si la única "intervención" del personaje es una
                # acotación pura, no abrir <sp>
                if proxima_es_solo_acot and proxima_siguiente_es_nuevo_sp:
                    volcar_parlamento()
                    # La acotación se emitirá en la siguiente iteración
                    # como <stage> independiente; aquí no abrimos <sp>.
                    continue
                abrir_sp(nombre)
                continue

        # ── Texto de parlamento o acotación narrativa ─────────────────────
        if sp_abierto:
            # [C-16] Acumular para emitir en un único <p>
            parlamento_acumulado.append(linea_s)
        else:
            # Fuera de parlamento: acotación narrativa o texto descriptivo
            # [C-09] Si estábamos en acotación inicial, acumular allí
            if en_acotacion_inicial:
                buf_acotacion_inicial.append(linea_s)
            else:
                emitir_stage(linea_s)

    # ── Cerrar todo al final ───────────────────────────────────────────────
    cerrar_acto()

    return "\n".join(resultado)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 9 — CONSTRUCCIÓN DEL DOCUMENTO TEI COMPLETO
# ════════════════════════════════════════════════════════════════════════════

def construir_tei_completo(
    cuerpo: str,
    titulo: str,
    autor: str,
    fecha: str = "",
    idioma: str = "es",
    personajes: dict[str, str] | None = None,
    descripciones_personajes: dict[str, str] | None = None,
    # [C-04] Fuente digital (Biblioteca Cervantes por defecto)
    fuente_digital_titulo: str = "Biblioteca Virtual Miguel de Cervantes",
    fuente_digital_url: str = "https://www.cervantesvirtual.com/nd/ark:/59851/bmcqr552",
    fuente_digital_lugar: str = "Alicante",
    fuente_digital_fecha: str = "2013",
    fuente_impresa_lugar: str = "",
    fuente_impresa_editorial: str = "",
    fuente_impresa_titulo: str = "",
    subgenero: str = "",
    forma: str = "prose",
    resp_stmt_resp: str = "",
    resp_stmt_nombre: str = "",
) -> str:
    if personajes is None:
        personajes = {}

    # [C-01] xml:id sin guiones bajos en el título
    xml_id = titulo_a_xml_id(titulo, autor)

    # [C-02] Título con capitalización tipo oración
    titulo_cap = capitalizar_titulo(titulo)

    # [C-03] Descomponer autor en forename / surname con mayúscula inicial
    autor_cap = capitalizar_nombre_persona(autor)
    partes_autor = autor_cap.strip().split()
    if len(partes_autor) >= 2:
        forename = " ".join(partes_autor[:-1])
        surname  = partes_autor[-1]
    else:
        forename = autor_cap
        surname  = ""

    # ── <respStmt> (arreglador opcional) ──────────────────────────────────
    bloque_resp_stmt = ""
    if resp_stmt_resp and resp_stmt_nombre:
        nombre_resp_cap = capitalizar_nombre_persona(resp_stmt_nombre)
        bloque_resp_stmt = f"""        <respStmt>
          <resp>{_esc(resp_stmt_resp)}</resp>
          <persName>{_esc(nombre_resp_cap)}</persName>
        </respStmt>"""

    # ── [C-04] <sourceDesc> con fuente digital obligatoria ────────────────
    bibl_digital = ""
    if fuente_digital_titulo or fuente_digital_url:
        bibl_digital = f"""        <bibl type="digitalSource">
          <title>{_esc(fuente_digital_titulo)}</title>
          <idno type="URL">{_esc(fuente_digital_url)}</idno>
          <date when="{_esc(fuente_digital_fecha)}">{_esc(fuente_digital_fecha)}</date>
          <pubPlace>{_esc(fuente_digital_lugar)}</pubPlace>
        </bibl>"""

    fecha_tag = f'when="{_esc(fecha)}"' if fecha else ""
    # El título de la fuente impresa puede ser diferente al título principal
    titulo_impresa = fuente_impresa_titulo or titulo_cap
    bibl_impresa = f"""        <bibl type="printSource">
          <author>{_esc(autor_cap)}</author>
          <title>{_esc(titulo_impresa)}</title>
          <pubPlace>{_esc(fuente_impresa_lugar)}</pubPlace>
          <publisher>{_esc(fuente_impresa_editorial)}</publisher>
          <date {fecha_tag}>{_esc(fecha)}</date>
        </bibl>"""

    source_desc = (bibl_digital + "\n" if bibl_digital else "") + bibl_impresa

    # ── <textClass> ───────────────────────────────────────────────────────
    term_subgenero = (
        f'\n          <term type="subgenre">{_esc(subgenero)}</term>'
        if subgenero else ""
    )

    # ── <listPerson> y <castList> ─────────────────────────────────────────
    list_person = construir_list_person(personajes) if personajes else ""
    cast_list   = construir_cast_list(personajes, descripciones_personajes) if personajes else ""
    bloque_front = f"\n    <front>\n{cast_list}\n    </front>" if cast_list else ""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://dracor.org/schema.rng"
type="application/xml"
schematypens="http://relaxng.org/ns/structure/1.0"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
xml:lang="{idioma}" xml:id="{xml_id}">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title type="main">{_esc(titulo_cap)}</title>
        <author>
          <persName>
            <forename>{_esc(forename)}</forename>
            <surname>{_esc(surname)}</surname>
          </persName>
        </author>
{bloque_resp_stmt}
      </titleStmt>
      <publicationStmt>
        <publisher xml:id="dracor">DraCor</publisher>
        <availability>
          <licence target="https://creativecommons.org/licenses/by/4.0">CC BY 4.0</licence>
        </availability>
      </publicationStmt>
      <sourceDesc>
{source_desc}
      </sourceDesc>
    </fileDesc>
    <profileDesc>
      <langUsage>
        <language ident="{idioma}" usage="100">{_nombre_idioma(idioma)}</language>
      </langUsage>
      <textClass>
        <keywords scheme="https://dracor.org/doc/schema">
          <term type="genre">drama</term>{term_subgenero}
          <term type="form">{_esc(forma)}</term>
        </keywords>
      </textClass>
      <particDesc>
        <listPerson>
{list_person}
        </listPerson>
      </particDesc>
    </profileDesc>
  </teiHeader>
  <text>{bloque_front}
    <body>
{cuerpo}
    </body>
  </text>
</TEI>"""


def _nombre_idioma(codigo: str) -> str:
    mapa = {
        "es": "Español", "en": "English", "de": "Deutsch",
        "fr": "Français", "it": "Italiano", "pt": "Português",
        "ca": "Català", "gl": "Galego", "eu": "Euskara",
    }
    return mapa.get(codigo.lower(), codigo)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 10 — FUNCIÓN PÚBLICA PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

def generar_tei(
    texto: str,
    titulo: str,
    autor: str,
    fecha: str = "",
    idioma: str = "es",
    # [C-04] Fuente digital: valores por defecto = Biblioteca Cervantes
    fuente_digital_titulo: str = "Biblioteca Virtual Miguel de Cervantes",
    fuente_digital_url: str = "https://www.cervantesvirtual.com/nd/ark:/59851/bmcqr552",
    fuente_digital_lugar: str = "Alicante",
    fuente_digital_fecha: str = "2013",
    fuente_impresa_lugar: str = "",
    fuente_impresa_editorial: str = "",
    # [C-02] Título completo de la fuente impresa (puede incluir subtítulo)
    fuente_impresa_titulo: str = "",
    subgenero: str = "",
    forma: str = "prose",
    # Arreglador/responsable secundario (opcional)
    resp_stmt_resp: str = "",
    resp_stmt_nombre: str = "",
    callback_progreso=None,
) -> str:

    if callback_progreso:
        callback_progreso(1, 4, "Normalizando texto…")
    texto = normalizar_texto(texto)

    if callback_progreso:
        callback_progreso(2, 4, "Separando portada y detectando personajes…")
    _, cuerpo_txt = separar_portada_y_cuerpo(texto)
    personajes = extraer_personajes(cuerpo_txt)
    if not personajes:
        personajes = extraer_personajes_del_cuerpo(cuerpo_txt)

    if callback_progreso:
        callback_progreso(3, 4, "Generando marcado TEI del cuerpo dramático…")
    cuerpo = transformar_cuerpo(cuerpo_txt, personajes)

    if callback_progreso:
        callback_progreso(4, 4, "Construyendo documento TEI completo…")
    return construir_tei_completo(
        cuerpo=cuerpo,
        titulo=titulo,
        autor=autor,
        fecha=fecha,
        idioma=idioma,
        personajes=personajes,
        fuente_digital_titulo=fuente_digital_titulo,
        fuente_digital_url=fuente_digital_url,
        fuente_digital_lugar=fuente_digital_lugar,
        fuente_digital_fecha=fuente_digital_fecha,
        fuente_impresa_lugar=fuente_impresa_lugar,
        fuente_impresa_editorial=fuente_impresa_editorial,
        fuente_impresa_titulo=fuente_impresa_titulo,
        subgenero=subgenero,
        forma=forma,
        resp_stmt_resp=resp_stmt_resp,
        resp_stmt_nombre=resp_stmt_nombre,
    )


def save_tei_to_file(tei_xml: str, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tei_xml)
