# 🎟️ Plataforma de Lotería — arquitectura en capas

Aplicación web simple que muestra cómo interactúan varias capas para procesar una petición (request).

## Capas

| Capa | Archivos | Responsabilidad |
|------|----------|-----------------|
| Presentación (UI) | `templates/index.html`, `static/app.js`, `static/style.css` | Dibuja la pantalla y envía peticiones HTTP |
| API / Controlador | `app.py` | Recibe el request, llama a la lógica y responde JSON |
| Lógica de negocio | `lottery.py` | Reglas: validar boleto, sortear, evaluar premio |

No usa base de datos.

## Flujo de una jugada

```
Navegador (app.js)  --POST /api/jugar-->  app.py  -->  lottery.py
                    <------ JSON -------  app.py  <--  (validate, draw, evaluate)
```

La pantalla muestra, debajo del resultado, el **recorrido de la petición** con la capa que ejecutó cada paso y su tiempo en ms.

## Ejecutar localmente

```bash
pip install -r requirements.txt
python app.py
```

Abre http://localhost:5000

## Ejecutar desde GitHub (Codespaces)

1. Sube este proyecto a un repositorio.
2. Botón verde **Code → Codespaces → Create codespace**.
3. En la terminal: `pip install -r requirements.txt && python app.py`
4. Abre el puerto 5000 que Codespaces te propone.

> GitHub Pages no sirve aquí porque solo aloja archivos estáticos y esta app necesita un backend Python.

## Endpoints

- `GET /` — pantalla principal
- `GET /api/quickpick` — boleto aleatorio
- `POST /api/jugar` — body `{"ticket":[1,2,3,4,5,6]}`, devuelve resultado y traza
