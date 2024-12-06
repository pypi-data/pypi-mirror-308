import json
import os

import geopandas as gpd
import requests

project_root = os.path.dirname(os.path.abspath(__file__))
drive_path = os.path.join(project_root, 'Google APIs', 'token_drive.json')
gmail_path = os.path.join(project_root, 'Google APIs', 'token_gmail.json')
sheets_path = os.path.join(project_root, 'Google APIs', 'token_sheets.json')
rodizio_polygon = gpd.read_file(os.path.join(project_root, 'data', 'shapesMiniAnel.shp'))

# fretes_db_path = os.path.join(project_root, 'Google APIs', 'fretes.db')

# Tracker
tokens = {
    "DEMAK COMERCIO, IMPORTACAO E EXPORTACAO LTDA.": {
        "code": 248302,
        "token": ""
    },
    "SG COMERCIO, IMPORTACAO E EXPORTACAO LTDA": {
        "code": 248683,
        "token": "620a874d-2ff8-4b92-9975-bcbfc3cbf2b8"
    },
    "homolog": {
        "code": "",
        "token": "11f816b7-eda3-4082-b202-c5a745c6cc1f"
    }
}

# Mapbox
mapbox_api_key = 'pk.eyJ1IjoiYW5kcmVmcmVpcmUiLCJhIjoiY2xtbTU1YjNhMGd3YTJybzJtdWluazM1biJ9.TEiRVhtnLzbqDINuHxhANQ'

# Correios
contrato_correio = "0078278236"


def token_correios() -> str:
    url = "https://api.correios.com.br/token/v1/autentica/cartaopostagem"

    payload = json.dumps({
        "numero": "0078278236"  # contrato_correio
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic NTE4Mjg4MTcwMDAxOTM6aE1oZ1l0VUpuQXAzT0NJVWpjTUI0SE53Q3h3T0JndmJaeDdtSEtQaA==',
        'Cookie': 'LBprdExt1=684195850.47873.0000'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return 'Bearer ' + response.json()['token']


# Google APIs
google_api_key: str = 'AIzaSyD-uw7IJhb5EKwibQXtAaUZ9GIFUzco6Vo'

drive_scopes = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
gmail_scopes = ["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/gmail.labels", "https://mail.google.com/",
                "https://www.googleapis.com/auth/spreadsheets"]
sheets_scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Integração Tracker
label_xml_cancelado = 'Label_6704754831970529690'
labels_xml_processar = 'Label_2975458266223650493'
label_xml_processado = 'Label_5715990699177054782'
label_xml_process_failed = 'Label_1239472781903625775'
label_devolucoes_processada = 'Label_9078542780954941257'
label_devolucoes_processar = 'Label_1823716647724364570'
label_devolucoes_manual = 'Label_8501872872577166508'
csv_path = r"P:\My Drive\Areas\Routing\csvs to upload"
siglas_estados = r"\b(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b"
cidades_possiveis = r"\b(Barueri|Carapicuiba|Cotia|Diadema|Embu das Artes|Guarulhos|Itapecerica da Serra|Itapevi|Itaquaquecetuba|" \
                    r"Jandira|Maua|Osasco|Santana de Parnaiba|Santo Andre|Sao Bernardo do Campo|Sao Caetano do Sul|" \
                    r"Sao Paulo|Taboao da Serra)\b"
products = {
    'Demak':
        {
            '1':  # Tipo de operação - 1 = Entrega
                {
                    'codigo': 1677,
                    'descricao': 'Demak Entrega',
                    'servico': 'Entrega'
                },
            '4':  # Tipo de operação - 4 = Reversa
                {
                    'codigo': 1678,
                    'descricao': 'Demak Reversa',
                    'servico': 'Reversa',
                }
        },
    'Mecanizou':
        {
            '1':  # Tipo de operação - 1 = Entrega
                {
                    'codigo': 1829,
                    'descricao': 'Mecanizou Agendadas - Reversa - Óleo',
                    'servico': 'Reversa'
                },
            '4':
                {
                    'codigo': 1832,
                    'descricao': 'Mecanizou Agendadas - Reversa - Óleo',
                    'servico': 'Reversa'
                }
        },
    'CAML':
        {
            '1':
                {
                    'codigo': 1851,
                    'descricao': 'CAML - Revista',
                    'servico': 'Entrega'
                }
        }
}

agrupadores = {
    '21437818000146': 'Demak',
    '24552989000104': 'Demak',
    '52093450000170': 'Demak',
    '30686469000197': 'Demak',
    '55961703000178': 'Demak',
    '37199406000155': 'Mecanizou',
    '02985369000126': 'Mecanizou',
    '00846804000106': 'Mecanizou',
    '13396258000109': 'Mecanizou',
    '08373156000634': 'Mecanizou',
    '58279696000117': 'Mecanizou',
    '60892858000300': 'Mecanizou',
    '32554486000104': 'Mecanizou',
    '37867804000100': 'Mecanizou',
    '60522190000139': 'Mecanizou',
    '10619557000240': 'Mecanizou',
    '55847057000112': 'Mecanizou',
    '60782778000121': 'CAML'
}

