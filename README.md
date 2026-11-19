# Bot de Telegram para el grupo

## Qué hace el bot

- Da la bienvenida a cada persona que entra al grupo.
- Contesta cuál es la última versión de la aplicación.
- Explica cómo actualizar cuando alguien dice que no tiene la última versión: borrar el historial del móvil y volver a entrar al enlace de la aplicación.
- Contesta si la aplicación no abre o se queda en blanco.
- Explica cómo instalar la aplicación en el móvil.
- También entiende estos comandos en el grupo: `/version` y `/ayuda`.

## Archivos de esta carpeta

- `bot.py`: el bot. Ahí están los mensajes que contesta y las frases que entiende.
- `requirements.txt`: la librería que necesita el bot para funcionar.
- `render.yaml`: los datos que hay que poner en Render (el token, el nombre de la aplicación, el enlace y la versión).

## Lo que necesitas antes de empezar

1. Telegram en el móvil.
2. Una cuenta en GitHub (la tuya: txiru79).
3. Una cuenta en Render, gratis. Se crea entrando con GitHub.
4. El enlace de la aplicación y su última versión.

## Paso 1. Crear el bot con BotFather

1. Abre Telegram en el móvil.
2. En la lupa de buscar, escribe `@BotFather` y abre el chat. Es el bot oficial de Telegram, tiene el tick azul.
3. Toca el botón de abajo que pone `Empezar` o escribe `/start`.
4. Escribe `/newbot` y envíalo.
5. Te pide un nombre para el bot. Por ejemplo: `Ayuda Mi Aplicación`. Escríbelo y envíalo.
6. Te pide un nombre de usuario para el bot. Tiene que terminar en `bot`. Por ejemplo: `ayuda_mi_aplicacion_bot`. Escríbelo y envíalo.
7. Te contesta con un mensaje que incluye un código largo llamado token. Es algo parecido a esto: `123456789:AAE...`. Cópialo y guárdalo.
8. El token es como una contraseña. No lo compartas con nadie y no lo subas a GitHub. Si alguien lo tiene, puede controlar tu bot. Si se te filtra, vuelve a hablar con `@BotFather`, escribe `/revoke` y te da uno nuevo.

## Paso 2. Dejar que el bot lea los mensajes del grupo

Si no haces este paso, el bot no verá lo que escribe la gente y no podrá contestar.

1. En el chat de `@BotFather`, escribe `/setprivacy`.
2. Te muestra tus bots. Toca el nombre de tu bot.
3. Toca `Disable` (desactivar).
4. Listo. Ahora el bot puede leer los mensajes del grupo.

## Paso 3. Subir los archivos a GitHub

1. Entra en github.com con tu cuenta.
2. Arriba a la derecha, toca el `+` y luego `New repository`.
3. En `Repository name` escribe `bot-telegram-grupo`.
4. Déjalo en `Public`.
5. Toca `Create repository`.
6. En la página del repositorio, toca `uploading an existing file`.
7. Arrastra los tres archivos de esta carpeta: `bot.py`, `requirements.txt` y `render.yaml`. O toca `choose your files` y elígelos.
8. Abajo, toca el botón verde `Commit changes`.

## Paso 4. Poner el bot en Render (gratis)

Render es donde el bot va a estar corriendo todo el día. La versión gratis vale para esto.

1. Entra en render.com.
2. Toca `Get Started` y entra con GitHub. Te pedirá permiso para conectar tu cuenta de GitHub. Acepta.
3. En el panel de Render, toca `New` y luego `Blueprint`.
4. Te muestra tus repositorios de GitHub. Elige `bot-telegram-grupo`.
5. Render lee el archivo `render.yaml` y te muestra los datos a rellenar. El nombre de la aplicación, el enlace y la versión ya vienen puestos (`Ope IVAP 2026 - Personal de Apoyo`, `https://txiru79.github.io/personal-de-apoyo/` y `4.1`). Solo te falta pegar el token:
   - `TELEGRAM_TOKEN`: pega el token que te dio `@BotFather` en el paso 1.
6. Toca `Apply`.
7. Espera unos minutos a que termine. Cuando arriba ponga `Live`, el bot ya está corriendo.
8. Nota: en la versión gratis, si nadie escribe en un rato, el servicio se duerme. Cuando alguien escriba, se despierta solo, pero ese primer mensaje puede tardar unos 30 segundos en contestarse. Los siguientes ya van rápido.

## Paso 5. Añadir el bot al grupo

1. Abre el grupo en Telegram.
2. Toca el nombre del grupo arriba.
3. Toca `Añadir miembros` o `Add Members`.
4. Busca el nombre de usuario de tu bot (el que termina en `bot`) y añádelo.
5. Listo. El bot ya está dentro del grupo.

## Paso 6. Probar que funciona

1. Que alguien entre al grupo. Tiene que salir un mensaje de bienvenida con su nombre.
2. Escribe en el grupo: `¿Cuál es la última versión de la aplicación?` Tiene que contestar con la versión que pusiste en Render.
3. Escribe en el grupo: `No tengo la última versión`. Tiene que contestar con los pasos para actualizar.
4. Escribe `/ayuda` en el grupo. Tiene que contestar con la lista de cosas que sabe hacer.

## Cambiar la versión de la aplicación

Cuando saques una versión nueva, no hay que tocar el código:

1. Entra en render.com y abre tu servicio `bot-telegram-grupo`.
2. A la izquierda, toca `Environment`.
3. Busca `LATEST_VERSION` y cambia el valor por la versión nueva.
4. Toca `Save Changes`.
5. El bot se reinicia solo y ya contesta con la versión nueva.

Lo mismo vale para cambiar el nombre (`APP_NAME`) o el enlace (`APP_LINK`).

## Añadir más respuestas al bot

Si quieres que el bot entienda más frases:

1. Abre `bot.py` y busca la parte que pone `REGLAS`.
2. Cada regla tiene una lista de frases y el mensaje que contesta.
3. Añade tu frase a la lista que toca. Por ejemplo, si quieres que entienda «no me llegan los avisos», añádela a la lista que corresponda.
4. Sube el archivo nuevo a GitHub, al mismo repositorio. Render lo coge solo y reinicia el bot.

Si quieres que el bot conteste una cosa nueva, con un mensaje nuevo, dímelo y te lo añado.

## Si algo falla

- **El bot no contesta nada**: entra en Render y mira que el servicio esté en `Live`. Si pone `Failed`, abre `Logs` y mira la última línea: casi siempre es el token mal copiado o una variable vacía.
- **El bot no ve los mensajes del grupo**: repite el paso 2. El modo privado tiene que estar en `Disable`.
- **La bienvenida no sale**: el bot tiene que estar dentro del grupo (paso 5). La bienvenida solo sale cuando entra alguien después de añadir el bot.
- **El primer mensaje tarda mucho**: es normal en la versión gratis de Render. Espera unos 30 segundos y prueba otra vez.
