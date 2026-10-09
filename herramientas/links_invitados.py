#!/usr/bin/env python3
"""Genera el link personalizado y el link de WhatsApp de cada invitado.

Uso:
  python3 herramientas/links_invitados.py "Nombre" "+593 99 123 4567" 2
  python3 herramientas/links_invitados.py --csv invitados.csv > links.csv

El CSV lleva tres columnas: nombre, celular, cupos (separadas por coma,
punto y coma o tabulación; la primera fila puede ser de encabezados).

El código cifrado debe coincidir con el lector `INVITACION` de index.html;
la clave se lee de ahí para que no se desincronicen.
"""
import base64
import csv
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

SITIO = "https://boda-alejuanse.site/"
INDEX = Path(__file__).resolve().parent.parent / "index.html"


def clave():
    m = re.search(r"var CLAVE = '([^']+)'", INDEX.read_text(encoding="utf-8"))
    if not m:
        sys.exit("No encontré la clave en index.html")
    return m.group(1).encode()


def fnv(data):
    h = 2166136261
    for b in data:
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def keystream(key, nonce):
    s = (fnv(key + bytes([nonce])) | 1) & 0xFFFFFFFF
    while True:
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= s >> 17
        s ^= (s << 5) & 0xFFFFFFFF
        yield s & 255


def codigo(nombre, cupos, key):
    plano = f"{cupos}|{nombre}".encode()
    nonce = os.urandom(1)[0]
    ks = keystream(key, nonce)
    cuerpo = bytes(b ^ next(ks) for b in plano)
    firma = fnv(key + bytes([nonce]) + plano).to_bytes(4, "big")
    return base64.urlsafe_b64encode(bytes([nonce]) + cuerpo + firma).decode().rstrip("=")


def links(nombre, celular, cupos, key):
    nombre = nombre.strip()
    cupos = int(cupos)
    if not 1 <= cupos <= 10:
        raise ValueError(f"cupos de {nombre} debe estar entre 1 y 10")
    link = f"{SITIO}?c={codigo(nombre, cupos, key)}"
    if cupos == 1:
        texto = (f"¡Hola {nombre}! Con mucha alegría queremos compartir contigo nuestra "
                 f"invitación de boda. Ábrela aquí: {link}")
    else:
        texto = (f"¡Hola {nombre}! Con mucha alegría queremos compartir con ustedes nuestra "
                 f"invitación de boda. Ábranla aquí: {link}")
    texto += "\n\nCon cariño, Ale & JuanSe"
    telefono = re.sub(r"\D", "", celular)
    if telefono.startswith("0"):
        telefono = "593" + telefono[1:]
    return link, f"https://wa.me/{telefono}?text={quote(texto, safe='')}"


def main():
    key = clave()
    if len(sys.argv) == 3 and sys.argv[1] == "--csv":
        with open(sys.argv[2], newline="", encoding="utf-8-sig") as f:
            muestra = f.read(2048)
            f.seek(0)
            filas = list(csv.reader(f, csv.Sniffer().sniff(muestra, ",;\t")))
        if filas and not re.search(r"\d", filas[0][-1]):
            filas = filas[1:]
        out = csv.writer(sys.stdout)
        out.writerow(["nombre", "celular", "cupos", "link", "whatsapp"])
        for nombre, celular, cupos, *_ in filas:
            out.writerow([nombre, celular, cupos, *links(nombre, celular, cupos, key)])
    elif len(sys.argv) == 4:
        link, wa = links(*sys.argv[1:], key)
        print(f"Link:     {link}\nWhatsApp: {wa}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
