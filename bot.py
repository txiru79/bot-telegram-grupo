#!/usr/bin/env python3
"""Bot de Telegram para el grupo de la aplicación.

Qué hace:
  - Da la bienvenida a quien entra al grupo.
  - Contesta cuál es la última versión de la aplicación.
  - Explica cómo actualizar cuando alguien dice que no tiene la última versión.
  - Contesta si la aplicación no abre o se queda en blanco.
  - Explica cómo instalar la aplicación en el móvil.

Cómo se configura:
  No hay que tocar el código para cambiar el nombre de la aplicación,
  el enlace o la versión. Esos tres datos se ponen en Render, en
  Environment, con estos nombres:
    APP_NAME        Nombre de la aplicación
    APP_LINK        Enlace de la aplicación
    LATEST_VERSION  Última versión, por ejemplo 2.3
    TELEGRAM_TOKEN  Token que da @BotFather (secreto, no se comparte)

  Para cambiar los textos de las respuestas, edita las funciones
  mensaje_version, mensaje_actualizar, mensaje_no_abre y
  mensaje_instalar, más abajo. Para que el bot entienda más frases,
  añade frases a la lista REGLAS.
"""

import logging
import os
import unicodedata

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============ CONFIGURACIÓN ============
# Se leen de las variables de entorno de Render. Si no existen,
# se usan los valores de aquí abajo.
APP_NAME = os.environ.get("APP_NAME", "Ope IVAP 2026 - Personal de Apoyo")
APP_LINK = os.environ.get("APP_LINK", "https://txiru79.github.io/personal-de-apoyo/")
LATEST_VERSION = os.environ.get("LATEST_VERSION", "4.1")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
# Render da esta variable sola con la dirección pública del servicio.
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL", "")
PORT = int(os.environ.get("PORT", "8443"))

WELCOME_MESSAGE = (
    "¡Hola {nombre}! Bienvenido al grupo de {app}. "
    "Si necesitas ayuda, escribe /ayuda y te digo lo que puedo hacer."
)


# ============ RESPUESTAS ============
def mensaje_version():
    """Cuál es la última versión."""
    return (
        f"La última versión de {APP_NAME} es la {LATEST_VERSION}.\n"
        f"Puedes abrirla aquí: {APP_LINK}"
    )


def mensaje_actualizar():
    """Cómo actualizar cuando alguien no tiene la última versión."""
    return (
        "Para tener la última versión haz esto en el móvil:\n"
        "1. Borra el historial del navegador. "
        "En Chrome: toca los tres puntos, Historial, "
        "Borrar datos de navegación.\n"
        "2. Cierra el navegador del todo.\n"
        "3. Vuelve a entrar al enlace de la aplicación:\n"
        f"{APP_LINK}\n"
        "Si sigue sin salirte la última versión, prueba con otro "
        "navegador, por ejemplo Firefox."
    )


def mensaje_no_abre():
    """Qué hacer si la aplicación no abre o se queda en blanco."""
    return (
        "Si la aplicación no te abre o se queda en blanco, haz esto:\n"
        "1. Borra el historial y los datos del navegador.\n"
        "2. Cierra el navegador del todo.\n"
        "3. Vuelve a entrar aquí:\n"
        f"{APP_LINK}\n"
        "Si sigue igual, prueba con otro navegador. "
        "Y si nada funciona, escribe aquí qué te sale en la pantalla "
        "y te ayudamos."
    )


def mensaje_instalar():
    """Cómo instalar la aplicación en el móvil."""
    return (
        f"Para instalar {APP_NAME} en el móvil:\n"
        "1. Abre este enlace en Chrome:\n"
        f"{APP_LINK}\n"
        "2. Toca los tres puntos de arriba a la derecha.\n"
        "3. Toca «Añadir a pantalla de inicio» o "
        "«Instalar aplicación».\n"
        "Así la tendrás como una aplicación más, con su icono."
    )


def mensaje_ayuda():
    """Qué sabe hacer el bot."""
    return (
        f"Soy el bot de {APP_NAME}. Puedo ayudarte con esto:\n"
        "- Pregúntame cuál es la última versión.\n"
        "- Si no tienes la última versión, te digo cómo actualizar.\n"
        "- Si la aplicación no te abre, te digo qué hacer.\n"
        "- Si quieres instalarla en el móvil, te digo cómo.\n"
        "También puedes usar estos comandos: /version y /ayuda."
    )


# ============ REGLAS: QUÉ FRASES ENTIENDE EL BOT ============
# El orden importa: primero se miran las frases de actualizar,
# porque «no tengo la última versión» también contiene
# «última versión». Cada regla es una lista de frases y la
# función que contesta. Las frases se comparan sin tildes y
# en minúsculas, así que valen con y sin tildes.
REGLAS = [
    (
        [
            "no tengo la ultima version",
            "no se actualiza",
            "no me actualiza",
            "version antigua",
            "sigo en la version",
            "no me sale la ultima",
            "no me sale la version nueva",
        ],
        mensaje_actualizar,
    ),
    (
        [
            "ultima version",
            "que version",
            "version actual",
            "version mas reciente",
            "version nueva",
        ],
        mensaje_version,
    ),
    (
        [
            "no me abre",
            "no abre",
            "no carga",
            "se queda en blanco",
            "pantalla en blanco",
            "no me funciona",
            "no funciona la app",
        ],
        mensaje_no_abre,
    ),
    (
        [
            "como instalo",
            "instalar la app",
            "anadir a inicio",
            "poner en el movil",
            "descargar la app",
        ],
        mensaje_instalar,
    ),
]


def normalizar(texto):
    """Pasa el texto a minúsculas y le quita las tildes."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto


def buscar_respuesta(texto):
    """Busca qué contestar a un mensaje. Devuelve None si no hay nada."""
    texto = normalizar(texto)
    for frases, funcion in REGLAS:
        for frase in frases:
            if frase in texto:
                return funcion()
    return None


# ============ COMPORTAMIENTO EN EL GRUPO ============
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saluda a cada persona que entra al grupo."""
    for miembro in update.message.new_chat_members:
        if miembro.is_bot:
            continue
        nombre = miembro.first_name or "amigo"
        await update.message.reply_text(
            WELCOME_MESSAGE.format(nombre=nombre, app=APP_NAME)
        )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contesta a los mensajes del grupo según las reglas."""
    mensaje = update.message
    if mensaje is None or not mensaje.text:
        return
    if mensaje.from_user is not None and mensaje.from_user.is_bot:
        return
    respuesta = buscar_respuesta(mensaje.text)
    if respuesta:
        await mensaje.reply_text(respuesta)


async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contesta a /start."""
    await update.message.reply_text(mensaje_ayuda())


async def comando_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contesta a /version."""
    await update.message.reply_text(mensaje_version())


async def comando_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contesta a /ayuda."""
    await update.message.reply_text(mensaje_ayuda())


def main():
    """Arranca el bot."""
    if not TELEGRAM_TOKEN:
        logger.error("Falta TELEGRAM_TOKEN en las variables de entorno.")
        raise SystemExit("Falta TELEGRAM_TOKEN en las variables de entorno.")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida)
    )
    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(CommandHandler("version", comando_version))
    app.add_handler(CommandHandler("ayuda", comando_ayuda))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
            responder,
        )
    )

    if WEBHOOK_URL:
        # En Render: Telegram llama al bot cada vez que hay un mensaje.
        logger.info("Arrancando con webhook en %s", WEBHOOK_URL)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="webhook",
            webhook_url=WEBHOOK_URL + "/webhook",
        )
    else:
        # Sin dirección pública (por ejemplo, en tu ordenador para probar).
        logger.info("Arrancando con polling.")
        app.run_polling()


if __name__ == "__main__":
    main()
