# Calculadora de IMC infantil con Streamlit

Aplicación para calcular el IMC de niñas y niños de 0 a 5 años y compararlo con una referencia de IMC para la edad y el sexo mediante puntaje Z.

## Archivos

- `app.py`: aplicación principal.
- `requirements.txt`: dependencias necesarias.

## Ejecutar localmente

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

En macOS o Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publicar desde GitHub en Streamlit Community Cloud

1. Crea un repositorio nuevo en GitHub.
2. Sube `app.py`, `requirements.txt` y este `README.md` a la raíz del repositorio.
3. Inicia sesión en Streamlit Community Cloud con tu cuenta de GitHub.
4. Selecciona **Create app**.
5. Elige el repositorio, la rama principal y `app.py` como archivo de entrada.
6. Pulsa **Deploy**.

## Advertencia

Es una herramienta educativa y de tamizaje. No sustituye la evaluación de pediatría o nutrición ni debe utilizarse como único criterio diagnóstico.
