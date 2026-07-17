import math
import streamlit as st
from pygrowup import Calculator

st.set_page_config(
    page_title="IMC infantil (0 a 5 años)",
    page_icon="👶",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main-title {text-align:center; margin-bottom:0.2rem;}
    .subtitle {text-align:center; color:#5f6b7a; margin-bottom:1.5rem;}
    .result-box {padding:1.2rem; border-radius:0.8rem; background:#f4f7fb; border:1px solid #dbe4ef;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-title">👶 Evaluación del IMC infantil</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Niñas y niños de 0 a 5 años, según IMC para la edad</p>',
    unsafe_allow_html=True,
)

st.info(
    "En menores de 5 años, el IMC no se interpreta con límites fijos de adultos. "
    "Debe compararse con la edad y el sexo mediante estándares de crecimiento."
)

with st.form("formulario_imc"):
    sexo_visible = st.selectbox("Sexo", ["Niña", "Niño"])

    col1, col2 = st.columns(2)
    with col1:
        edad_anios = st.number_input(
            "Edad: años cumplidos", min_value=0, max_value=5, value=2, step=1
        )
    with col2:
        max_meses = 0 if edad_anios == 5 else 11
        edad_meses_extra = st.number_input(
            "Meses adicionales", min_value=0, max_value=max_meses, value=0, step=1
        )

    peso = st.number_input(
        "Peso (kg)", min_value=1.0, max_value=40.0, value=12.0, step=0.1, format="%.1f"
    )
    talla_cm = st.number_input(
        "Talla o longitud (cm)", min_value=40.0, max_value=130.0, value=85.0,
        step=0.1, format="%.1f"
    )

    calcular = st.form_submit_button("Calcular IMC", use_container_width=True)


def clasificar_z(z: float) -> tuple[str, str, str]:
    """Clasificación orientativa de IMC/edad para menores de 5 años."""
    if z < -3:
        return "Bajo peso", "Delgadez severa", "🔴"
    if z < -2:
        return "Bajo peso", "Delgadez", "🟠"
    if z <= 1:
        return "Peso saludable", "IMC adecuado para la edad", "🟢"
    if z <= 2:
        return "Sobrepeso", "Riesgo de sobrepeso", "🟡"
    if z <= 3:
        return "Sobrepeso", "Sobrepeso", "🟠"
    return "Obesidad", "Obesidad", "🔴"


if calcular:
    edad_total_meses = int(edad_anios * 12 + edad_meses_extra)
    talla_m = talla_cm / 100
    imc = peso / (talla_m ** 2)
    sexo_codigo = "F" if sexo_visible == "Niña" else "M"

    errores = []
    if edad_total_meses > 60:
        errores.append("La edad debe estar entre 0 y 60 meses.")
    if not math.isfinite(imc) or imc <= 0:
        errores.append("Verifica el peso y la talla ingresados.")

    if errores:
        for error in errores:
            st.error(error)
    else:
        try:
            calculadora = Calculator()
            z_imc = calculadora.bmifa(
                measurement=imc,
                age_in_months=edad_total_meses,
                sex=sexo_codigo,
            )

            if z_imc is None or not math.isfinite(float(z_imc)):
                st.error(
                    "No fue posible comparar el resultado con la referencia para esta edad. "
                    "Revisa los datos ingresados."
                )
            else:
                z_imc = float(z_imc)
                categoria, detalle, icono = clasificar_z(z_imc)

                st.markdown("### Resultado")
                c1, c2, c3 = st.columns(3)
                c1.metric("IMC", f"{imc:.2f} kg/m²")
                c2.metric("Puntaje Z", f"{z_imc:.2f}")
                c3.metric("Edad", f"{edad_total_meses} meses")

                st.markdown(
                    f"""
                    <div class="result-box">
                        <h2 style="margin-top:0">{icono} {categoria}</h2>
                        <p style="font-size:1.1rem; margin-bottom:0"><strong>Interpretación:</strong> {detalle}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if z_imc < -2 or z_imc > 1:
                    st.warning(
                        "Se recomienda confirmar las mediciones y consultar con un profesional de salud "
                        "para una evaluación integral del crecimiento."
                    )
                else:
                    st.success(
                        "El resultado se encuentra dentro del intervalo esperado. "
                        "Debe interpretarse junto con la evolución de la curva de crecimiento."
                    )

                with st.expander("¿Cómo se obtuvo el resultado?"):
                    st.write(
                        f"IMC = peso / talla² = {peso:.1f} / ({talla_m:.3f})² = {imc:.2f} kg/m²."
                    )
                    st.write(
                        "Luego, el IMC se comparó con la referencia de IMC para la edad y el sexo, "
                        "expresada mediante un puntaje Z."
                    )
        except Exception as exc:
            st.error("Ocurrió un error al realizar el cálculo. Revisa los datos e inténtalo nuevamente.")
            st.caption(f"Detalle técnico: {exc}")

st.divider()
st.caption(
    "Herramienta educativa y de tamizaje. No establece diagnósticos ni sustituye la valoración "
    "de pediatría o nutrición. En menores de 2 años también suelen evaluarse peso para la longitud "
    "y otros indicadores antropométricos."
)
