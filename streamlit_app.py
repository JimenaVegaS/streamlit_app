import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from PIL import Image

# Data del 2023 (falta diciembre)
df1 = pd.read_csv("2023_parte1.csv")
df2 = pd.read_csv("2023_parte2.csv")
df3 = pd.read_csv("2023_parte3.csv")
df4 = pd.read_csv("2023_parte4.csv")

# Data del 2022
df5_1 = pd.read_csv("marzo2022_parte1.csv")
df5_2 = pd.read_csv("marzo2022_parte2.csv")
df6= pd.read_csv("Junio2022de18a80años.csv")
df6 = df6.rename(columns={"C_Donacion": "Donacion"})
df7 = pd.read_csv("septiembre2022de18a80años.csv")
df7 = df7.rename(columns={"C_Donacion": "Donacion"})
df8 = pd.read_csv("diciembre2022de18a80años.csv")

titulos_pestanas = ['Página principal', 'Nacional', 'Internacional','Departamentos','Países','Sobre nosotras']
pestaña1, pestaña2, pestaña3, pestaña4, pestaña5, pestaña6 = st.tabs(titulos_pestanas)

with pestaña1:
    st.title('Análisis de Población identificada con DNI de mayor de edad por condición de donante de órganos')
    st.write("")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.button("Nacional", type="secondary")
            def display_and_count_donacion_column_st(df, name):
                donacion_column = 'Donacion' if 'Donacion' in df.columns else 'C_Donacion'

                if donacion_column in df.columns:
                    df = df[df[donacion_column] != "No acepta"]
                    donation_counts = df[donacion_column].value_counts()
                    donation_percentages = (donation_counts / donation_counts.sum()) * 100
                    donation_percentages = donation_percentages.round(2)
                    grafica = pd.DataFrame({'Donation Status': donation_counts.index, 'Donation Counts': donation_counts, 'Percentage': donation_percentages})
                    c = alt.Chart(grafica).mark_arc().encode(theta="Percentage:Q", color="Donation Status:N")
                    st.altair_chart(c, use_container_width=True)
                    st.write("Durante los años 2022 y 2023, a nivel nacional, el 31.64""%"" de las personas aceptó donar sus órganos; el 55.72""%"", no acepto; y el 13.63""%"", no especifica.")
                    st.write("Donadores y Porcentaje:")
                    st.write(grafica[['Donation Counts', 'Percentage']])
                    df_with_percentages = pd.DataFrame({'Donation Status': donation_counts.index, 'Percentage': donation_percentages})

                    return df_with_percentages

                else:
                 st.write(f"No donation column found in {name} DataFrame.")

            df_merged = pd.concat([df1, df2, df3,df4,df5_1 , df5_2,df6,df7,df8], ignore_index=True)
            df_merged  = df_merged [(df_merged ['Residencia'] == "Nacional")]
            merged_donation_stats = display_and_count_donacion_column_st(df_merged, "Merged Data")

        with right_column:
            st.button("Internacional", type="secondary")
            def display_and_count_donacion_column_st(df, name):
                donacion_column = 'Donacion' if 'Donacion' in df.columns else 'C_Donacion'

                if donacion_column in df.columns:
                    donation_counts = df[donacion_column].value_counts()
                    donation_percentages = (donation_counts / donation_counts.sum()) * 100
                    donation_percentages = donation_percentages.round(2)
                    grafica = pd.DataFrame({'Donation Status': donation_counts.index, 'Donation Counts': donation_counts, 'Percentage': donation_percentages})
                    c = alt.Chart(grafica).mark_arc().encode(theta="Percentage:Q", color="Donation Status:N")
                    st.altair_chart(c, use_container_width=True)
                    st.write("Durante los años 2022 y 2023, a nivel internacional, el 39.59""%"" de las personas aceptó donar sus órganos; el 46.49""%"", no acepto; y el 13.92""%"", no especifica.")                    
                    
                    st.write("Donadores y Porcentaje:")
                    st.write(grafica[['Donation Counts', 'Percentage']])
                    st.caption("Este gráfico no incluye los datos del cuarto trimestre del 2023")
                    df_with_percentages = pd.DataFrame({'Donation Status': donation_counts.index, 'Percentage': donation_percentages})
                    return df_with_percentages
                else:
                 st.write(f"No donation column found in {name} DataFrame.")

            df_merged = pd.concat([df1, df2, df3,df4,df5_1 , df5_2,df6,df7,df8], ignore_index=True)
            df_merged  = df_merged [(df_merged ['Residencia'] == "Extranjero")]
            merged_donation_stats = display_and_count_donacion_column_st(df_merged, "Merged Data")

with pestaña2:
    st.title("Condición de donante de órganos a nivel nacional")
    st.write("Todos los departamentos")

    # Crear gráfico para el año 2022
    st.subheader(f"Gráfico para 2022")
    chart_data_2022 = pd.concat([df5_1 , df5_2, df6, df7, df8], ignore_index=True)
    filtered_df_2022 = chart_data_2022[(chart_data_2022['Edad'] > 17) & (chart_data_2022['Edad'] < 81)]
    nacional = filtered_df_2022[(filtered_df_2022['Donacion'] == 'Si acepta donar') & (filtered_df_2022['Residencia'] == 'Nacional')]
    repeticiones_por_fila = nacional.groupby(['Departamento', 'Sexo']).size().reset_index(name='Donantes')
    fila_max_repeticiones = repeticiones_por_fila.loc[repeticiones_por_fila.groupby(['Departamento', 'Sexo'])['Donantes'].idxmax()]
    departamentos = fila_max_repeticiones['Departamento'].unique()
    data_dict = {'Departamento': departamentos, 'Mujer': [], 'Hombre': []}

    for departamento in departamentos:
        df_departamento = fila_max_repeticiones[fila_max_repeticiones['Departamento'] == departamento]
        data_dict['Mujer'].append(df_departamento[df_departamento['Sexo'] == 'Mujer']['Donantes'].iloc[0])
        data_dict['Hombre'].append(df_departamento[df_departamento['Sexo'] == 'Hombre']['Donantes'].iloc[0])
    chart_data = pd.DataFrame(data_dict)
    st.bar_chart(chart_data.set_index('Departamento'))
    st.write("Durante el año 2022, varias personas, entre hombres y mujeres, aceptaron donar sus órganos por todo el país.")
    nacional = chart_data_2022[(chart_data_2022['Donacion'] == "Si acepta donar") & (chart_data_2022['Residencia'] == "Nacional")]
    conteo_sexo = nacional.groupby(['Departamento', 'Sexo']).size().unstack(fill_value=0).reset_index()
    conteo_sexo.columns.name = None
    conteo_sexo = conteo_sexo.rename(columns={'Mujer': 'Mujeres', 'Hombre': 'Hombres'}) 
    st.write(conteo_sexo)


    st.subheader(f"Gráfico para 2023")
    chart_data_2023 = pd.concat([df1, df2, df3,df4 ], ignore_index=True)
    filtered_df_2023 = chart_data_2023[(chart_data_2023['Edad'] > 17) & (chart_data_2023['Edad'] < 81)]
    nacional3 = filtered_df_2023[(filtered_df_2023['Donacion'] == 'Si acepta donar') & (filtered_df_2023['Residencia'] == 'Nacional')]
    repeticiones_por_fila3 = nacional3.groupby(['Departamento', 'Sexo']).size().reset_index(name='Donantes')
    fila_max_repeticiones = repeticiones_por_fila3.loc[repeticiones_por_fila3.groupby(['Departamento', 'Sexo'])['Donantes'].idxmax()]
    departamentos = fila_max_repeticiones['Departamento'].unique()
    data_dict = {'Departamento': departamentos, 'Mujer': [], 'Hombre': []}

    for departamento in departamentos:
        df_departamento = fila_max_repeticiones[fila_max_repeticiones['Departamento'] == departamento]
        data_dict['Mujer'].append(df_departamento[df_departamento['Sexo'] == 'Mujer']['Donantes'].iloc[0])
        data_dict['Hombre'].append(df_departamento[df_departamento['Sexo'] == 'Hombre']['Donantes'].iloc[0])
    chart_data = pd.DataFrame(data_dict)
    st.bar_chart(chart_data.set_index('Departamento'))
    st.write("Durante el año 2023, varias personas, entre hombres y mujeres, aceptaron donar sus órganos por todo el país.")
    nacional3 = chart_data_2023[(chart_data_2023['Donacion'] == "Si acepta donar") & (chart_data_2023['Residencia'] == "Nacional")]
    conteo_sexo = nacional3.groupby(['Departamento', 'Sexo']).size().unstack(fill_value=0).reset_index()
    conteo_sexo.columns.name = None
    conteo_sexo = conteo_sexo.rename(columns={'Mujer': 'Mujeres', 'Hombre': 'Hombres'}) 
    st.write(conteo_sexo) 
    st.caption("Este gráfico no incluye los datos del cuarto trimestre del 2023.")

with pestaña3:
    st.title("Condición de donante de órganos a nivel internacional")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.button(" 2022", type="secondary")
            chart_data_2022 = pd.concat([df5_1 , df5_2, df6, df7, df8], ignore_index=True)
            filtered_df_2022 = chart_data_2022[(chart_data_2022['Edad'] > 17) & (chart_data_2022['Edad'] < 81)]
            nacional = filtered_df_2022[(filtered_df_2022['Donacion'] == 'Si acepta donar') & (filtered_df_2022['Residencia'] == 'Extranjero')]
            repeticiones_por_fila = nacional.groupby(['Continente', 'Sexo']).size().reset_index(name='Donantes')
            fila_max_repeticiones = repeticiones_por_fila.loc[repeticiones_por_fila.groupby(['Continente', 'Sexo'])['Donantes'].idxmax()]
            continentes = fila_max_repeticiones['Continente'].unique()
            data_dict = {'Continente': continentes, 'Mujer': [], 'Hombre': []}

            for continente in continentes:
                df_departamento = fila_max_repeticiones[fila_max_repeticiones['Continente'] == continente]
                data_dict['Mujer'].append(df_departamento[df_departamento['Sexo'] == 'Mujer']['Donantes'].iloc[0])
                data_dict['Hombre'].append(df_departamento[df_departamento['Sexo'] == 'Hombre']['Donantes'].iloc[0])
            chart_data = pd.DataFrame(data_dict)
            st.bar_chart(chart_data.set_index('Continente'))
            st.write("Durante 2022, varias personas, entre hombres y mujeres, aceptaron donar sus órganos por todo el mundo.")
            nacional = chart_data_2022[(chart_data_2022['Donacion'] == "Si acepta donar") & (chart_data_2022['Residencia'] == "Extranjero")]
            conteo_sexo = nacional.groupby(['Continente', 'Sexo']).size().unstack(fill_value=0).reset_index()
            conteo_sexo.columns.name = None
            conteo_sexo = conteo_sexo.rename(columns={'Mujer': 'Mujeres', 'Hombre': 'Hombres'}) 
            st.write(conteo_sexo)

        with right_column:
            st.button(" 2023", type="secondary")
            chart_data_2023 = pd.concat([df1, df2, df3,df4 ], ignore_index=True)
            filtered_df_2023 = chart_data_2023[(chart_data_2023['Edad'] > 17) & (chart_data_2023['Edad'] < 81)]
            nacional = filtered_df_2023[(filtered_df_2023['Donacion'] == 'Si acepta donar') & (filtered_df_2023['Residencia'] == 'Extranjero')]
            repeticiones_por_fila = nacional.groupby(['Continente', 'Sexo']).size().reset_index(name='Donantes')
            fila_max_repeticiones = repeticiones_por_fila.loc[repeticiones_por_fila.groupby(['Continente', 'Sexo'])['Donantes'].idxmax()]
            continentes = fila_max_repeticiones['Continente'].unique()
            data_dict = {'Continente': continentes, 'Mujer': [], 'Hombre': []}

            for continente in continentes:
                df_departamento = fila_max_repeticiones[fila_max_repeticiones['Continente'] == continente]
                data_dict['Mujer'].append(df_departamento[df_departamento['Sexo'] == 'Mujer']['Donantes'].iloc[0])
                data_dict['Hombre'].append(df_departamento[df_departamento['Sexo'] == 'Hombre']['Donantes'].iloc[0])
            chart_data = pd.DataFrame(data_dict)
            st.bar_chart(chart_data.set_index('Continente'))
            st.write("Durante 2023, varias personas, entre hombres y mujeres, aceptaron donar sus órganos por todo el mundo.")
            nacional = chart_data_2023[(chart_data_2023['Donacion'] == "Si acepta donar") & (chart_data_2023['Residencia'] == "Extranjero")]
            conteo_sexo = nacional.groupby(['Continente', 'Sexo']).size().unstack(fill_value=0).reset_index()
            conteo_sexo.columns.name = None
            conteo_sexo = conteo_sexo.rename(columns={'Mujer': 'Mujeres', 'Hombre': 'Hombres'}) 
            st.write(conteo_sexo)
            st.caption("Este gráfico no incluye los datos del cuarto trimestre del 2023.")

with pestaña4:
    st.title("Condición de donante de órganos por departamentos")
    option0 = st.selectbox(
        "Elige un año",
        ("2022", "2023"))
    if option0 == "2022":
        st.subheader(f"Gráfico para 2022")
        chart_data_2022 = pd.concat([df5_1 , df5_2, df6, df7,df8], ignore_index=True)
        filtered_df_2022 = chart_data_2022[(chart_data_2022['Edad'] > 17) & (chart_data_2022['Edad'] < 81)]
        nacional_2022 = filtered_df_2022[(filtered_df_2022['Donacion'] == "Si acepta donar") & (filtered_df_2022['Residencia'] == "Nacional")]
        total_donantes_nacionales = nacional_2022.shape[0]
        chart_data_nacional_2022 = nacional_2022.groupby(['Departamento']).size().reset_index(name='Donantes')
        chart_data_nacional_2022['Porcentaje'] = (chart_data_nacional_2022['Donantes'] / total_donantes_nacionales) * 100
        chart_data_nacional_2022['Porcentaje'] = chart_data_nacional_2022['Porcentaje'].round(2)
        st.bar_chart(chart_data_nacional_2022.set_index('Departamento')['Porcentaje'])
        st.write(chart_data_nacional_2022[['Departamento', 'Donantes','Porcentaje']])

        st.write("El gráfico muestra la cantidad de personas que aceptaron donar sus órganos durante el año 2022.")
    elif option0 == "2023":
        st.subheader(f"Gráfico para 2023")
        chart_data_2023 = pd.concat([df1, df2, df3, df4], ignore_index=True)
        filtered_df_2023 = chart_data_2023[(chart_data_2023['Edad'] > 17) & (chart_data_2023['Edad'] < 81)]
        nacional_2023 = filtered_df_2023[(filtered_df_2023['Donacion'] == "Si acepta donar") & (filtered_df_2023['Residencia'] == "Nacional")]
        total_donantes_nacionales = nacional_2023.shape[0]
        chart_data_nacional_2023 = nacional_2023.groupby(['Departamento']).size().reset_index(name='Donantes')
        chart_data_nacional_2023['Porcentaje'] = (chart_data_nacional_2023['Donantes'] / total_donantes_nacionales) * 100
        chart_data_nacional_2023['Porcentaje'] = chart_data_nacional_2023['Porcentaje'].round(2)
        st.bar_chart(chart_data_nacional_2023.set_index('Departamento')['Porcentaje'])
        st.write(chart_data_nacional_2023[['Departamento', 'Donantes','Porcentaje']])
        st.caption("Los datos de este gráfico no están actualizados a la fecha actual.")
        st.write("")
        st.write("El gráfico muestra la cantidad de personas que aceptaron donar sus órganos durante el año 2023.")

with pestaña5:
    st.title("Condición de donante de órganos por países")
    option3 = st.selectbox(
        "Elige un continente",
        ("África", "América", "Asia", "Europa", "Oceanía"))
    option4 = st.selectbox(
        "Elige un año",
        (" 2022", "2023"))
    if option4 == "2023":
        chart_data_2023 = pd.concat([df1, df2, df3, df4], ignore_index=True)
        nacional = chart_data_2023[(chart_data_2023['Donacion'] == "Si acepta donar") & (chart_data_2023['Residencia'] == "Extranjero")]
        filtered_data = nacional[nacional['Continente'] == option3]
        total_donantes = filtered_data.shape[0]
        chart_data_nacional = filtered_data.groupby(['Pais']).size().reset_index(name='Donantes')
        chart_data_nacional['Porcentaje'] = (chart_data_nacional['Donantes'] / total_donantes) * 100
        chart_data_nacional['Porcentaje'] = chart_data_nacional['Porcentaje'].round(2)
        st.bar_chart(chart_data_nacional.set_index('Pais')['Porcentaje'])
        st.write(chart_data_nacional[['Pais','Porcentaje']])
    else:
        chart_data_2022 = pd.concat([df5_1 , df5_2, df6, df7,df8], ignore_index=True)
        nacional = filtered_df_2022[(filtered_df_2022['Donacion'] == "Si acepta donar") & (filtered_df_2022['Residencia'] == "Extranjero")]
        filtered_data = nacional[nacional['Continente'] == option3]
        total_donantes = filtered_data.shape[0]
        chart_data_nacional = filtered_data.groupby(['Pais']).size().reset_index(name='Donantes')
        chart_data_nacional['Porcentaje'] = (chart_data_nacional['Donantes'] / total_donantes) * 100
        chart_data_nacional['Porcentaje'] = chart_data_nacional['Porcentaje'].round(2)
        st.bar_chart(chart_data_nacional.set_index('Pais')['Porcentaje'])
        st.write(chart_data_nacional[['Pais','Porcentaje']])

with pestaña6:
    st.title("Sobre nosotras")
    st.write("Brigitte Bernal Belisario")
    st.write("Milagros Soledad Acevedo Valer")
    st.write("Nardy Liz Condori Mamani")
    st.write("Melissa Quispe Baldeon")
    st.write("Jimena Natalia Vega Sanchez")

st.link_button("Para más información de click aquí", "https://www.datosabiertos.gob.pe/dataset/reniec-poblaci%C3%B3n-identificada-con-dni-de-mayor-de-edad-por-condici%C3%B3n-de-donante-de-%C3%B3rganos")
