import pandas as pd
import streamlit as st
from datetime import datetime
import base64
import uuid
import re
import subprocess

# Función para instalar openpyxl si no está instalado
def install_openpyxl():
    try:
        import openpyxl
    except ImportError:
        subprocess.check_call(["python", '-m', 'pip', 'install', 'openpyxl'])

install_openpyxl()

# Función para generar el enlace de descarga
def download_button(object_to_download, download_filename, button_text):
    b64 = base64.b64encode(object_to_download.encode()).decode()
    button_id = str(uuid.uuid4()).replace('-', '')
    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """
    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'
    return dl_link

# Título de la aplicación
st.title("Generador de archivo ICT")

# Subir archivo Excel
uploaded_file = st.file_uploader("Carga tu archivo de Excel", type=['xlsx'])

if uploaded_file:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Mostrar el contenido del archivo
    st.write("Contenido del archivo:")
    st.dataframe(df)

    # Preparar el contenido del archivo .ict
    ict_header = "SourceCashAccount;ReceivingCashAccount;TransactionReference;PaymentSystem;Currency;Amount;SettlementDate;Description;CorporateActionReference;TransactionOnHoldCSD;TransactionOnHoldParticipant\n"
    ict_content = []
    
    for index, row in df.iterrows():
        # Ejemplo de cómo completar las variables, ajustar según sea necesario
        SourceCashAccount = row['Numero']
        ReceivingCashAccount = 'ReceivingAccount'  # Ajustar según sea necesario
        TransactionReference = 'Ref-' + str(index)
        PaymentSystem = 'PaymentSystem'  # Ajustar según sea necesario
        Currency = row['Moneda']
        Amount = 0  # Ajustar según sea necesario
        SettlementDate = datetime.now().strftime('%Y-%m-%d')
        Description = 'Description'  # Ajustar según sea necesario
        CorporateActionReference = 'CorpAct-' + str(index)
        TransactionOnHoldCSD = 'No'
        TransactionOnHoldParticipant = 'No'

        ict_line = f"{SourceCashAccount};{ReceivingCashAccount};{TransactionReference};{PaymentSystem};{Currency};{Amount};{SettlementDate};{Description};{CorporateActionReference};{TransactionOnHoldCSD};{TransactionOnHoldParticipant}\n"
        ict_content.append(ict_line)

    ict_file_content = ict_header + "".join(ict_content)

    # Guardar el archivo .ict
    ict_filename = 'output_file.ict'
    with open(ict_filename, 'w') as f:
        f.write(ict_file_content)

    # Mostrar el enlace de descarga
    download_button_str = download_button(ict_file_content, ict_filename, 'Descargar archivo ICT')
    st.markdown(download_button_str, unsafe_allow_html=True)
