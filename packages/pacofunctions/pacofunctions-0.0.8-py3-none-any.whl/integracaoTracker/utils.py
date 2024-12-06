import ast
import json
import pathlib
import re

import requests
import xmltodict
from utilFunctions.module import get_email_content, modify_label, list_emails, get_attachments, config


def relabel_cancelled_xml_emails() -> None:
    """Changes the label of emails which xmls have been already cancelled."""
    # find canceled xmls:
    canceled_email_ids: list = list_emails(label_id=config.labels_xml_processar, user="me", q="Cancelamento")

    # find canceled xmls nf-e number and modify email labels:
    if canceled_email_ids is not None:
        for email in canceled_email_ids:
            subject, _, _ = get_email_content(email["id"])
            nf_number = re.search(r"(?<=-\s)\d+$", subject).group(0)
            # find emails relating to this nf-e number:
            emails_to_treat = list_emails(label_id=config.labels_xml_processar, user="me", q=f"{nf_number}")
            if emails_to_treat is not None:
                for email_to_treat in emails_to_treat:
                    modify_label(msg_id=email_to_treat["id"], label_id_remove=[config.labels_xml_processar, "INBOX", "UNREAD"],
                                 label_id_add=[config.label_xml_cancelado])

def files_to_process() -> list:
    """Get CSV files to process from specified folder"""
    return [file for file in pathlib.Path(config.csv_path).glob(f"*.csv")] + []

def process_pdf(pdf_content):
    ...

def get_pdf_from_url(pdf_url):
    """Retrieves a PDF file from a URL.

    Args:
        pdf_url: The URL of the PDF file.

    Returns:
        The content of the PDF file as bytes, or None if the request fails.
    """

    response = requests.get(pdf_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error downloading PDF: {response.status_code}")
        return None


def get_nf_info(email_da_nota):
    """Retrieves NF information from email, prioritizing XML attachments."""
    subject, body, attachments = get_email_content(email_da_nota["id"])

    nfe_url = re.search(r"\b(?:https?|http)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]", body, re.IGNORECASE)
    nfe_url = nfe_url.group(0) if nfe_url else None

    data = nfe_numero = danfe = tipo_operacao = None

    if 'xml' in attachments:
        xml_content = get_attachments(attachment_id=attachments['xml']['attachment_id'],
                                      msg_id=email_da_nota["id"],
                                      download=False,
                                      return_filecontent=True)
        data = lower_dict_keys(process_xml(xml_content))
        nfe_numero = data['documento_transportado']['numero']
        danfe = data['documento_transportado']['chave_acesso']
        tipo_operacao = data['ide']['finNFe']

    elif 'pdf' in attachments or nfe_url:
        if nfe_url:
            pdf_content = get_pdf_from_url(nfe_url)
        else:
            pdf_content = get_attachments(attachment_id=attachments['pdf']['attachment_id'],
                                          msg_id=email_da_nota["id"],
                                          download=False,
                                          return_filecontent=True)

        if pdf_content:
            data = process_pdf(pdf_content)
            # TODO: Implement logic to extract nfe_numero, danfe, tipo_operacao from PDF

    return data, nfe_numero, danfe, tipo_operacao

def get_agrupador(cnpj):
    """Retrieves the agrupador string for a given 14-digit code."""
    return config.agrupadores.get(cnpj, None)  #

def get_product_id(cnpj, tipo_operacao):
    cliente = get_agrupador(cnpj)
    product_id = config.products[cliente][tipo_operacao]['codigo']
    return product_id

def authorize_session() -> str:
    token = 'e49e188e-ef13-487d-a176-24419d6b14ba'
    url = f'http://api.track3r.com.br/v2/api/Autenticacao?token={token}'

    response = requests.get(url)
    session_id = ast.literal_eval(response.text)['sessao']

    return session_id

def recebe_notas_json(session_id: str, id_servico: int, encomendas: dict | list[dict], numero_carga: str = None):
    """
    Descricao: Recebe notas via json a serem transportadas.
    Parametros:
        CodigoServico:
            1 = Entrega
            4 = Reversa
            7 = Entrega na Loja
            8 = Lotação
            9 = Retira
        CodigoProduto:
            É o campo no json id_produto que corresponde ao tipo de transporte. Exemplo: Expresso, Economico, etc.
            Os codigos devem ser solicitados a transportadora.
            Cada transportadora tem o seu codigo e produto especifico.

        TipoDocumento (encomendas.documento_transportado.tipo):
            1 = NF-e (Nota Fiscal Eletrônica)
            2 = NFC (Nota Fiscal ao Consumidor)
            3 = Declaração

        TipoPessoa (Destinatário/Loja Remetente):
            F = Pessoa física
            J = Pessoa jurídica

        Informação de dimensões e pesos:
            Altura/Largura/Comprimento são campos são do tipo Double em Metros,
            Pesos os campos são tipo Double em Kg

        pedido_aguardado_faturamento:
            true = Utilizar a API Atualiza dados NFe (/api/AtualizarDadosNFe) para complementar os dados."""

    # Check validity of inputs: ID_servico, documento_tipo
    while True:
        if id_servico not in [1, 4, 7, 8, 9]:
            print(f"Invalid service code - {id_servico}:\n")
            print("Select a valid service codes:")
            id_servico = int(input("\t1 = Entrega\n"
                                   "\t4 = Reversa\n"
                                   "\t7 = Entrega na Loja\n"
                                   "\t8 = Lotação\n"
                                   "\t9 = Retira)"))

        else:
            break

    # Convert dict to list if necessary:
    if isinstance(encomendas, dict):
        encomendas = [encomendas]

    url = "https://api.track3r.com.br/v2/api/GerarEncomendas"

    payload = json.dumps({
        "sessao": session_id,
        "id_servico": id_servico,
        "numero_carga": numero_carga,
        "encomendas": encomendas
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    api_message = json.loads(response.text)
    if not response.status_code == 200:
        [print(f'{key}: {value}\n') for key, value in api_message.items()]

        print(f"{response.status_code=}")
        print(f"{response.text=}")
        print(json.dumps({
            "sessao": session_id,
            "id_servico": id_servico,
            "numero_carga": numero_carga,
            "encomendas": encomendas
        }, indent=4))
    else:
        [print(f"\t{item}") for item in api_message["status"]]

    return api_message

def check_if_nota_exists(cnpj: str, nfe: str=None, serie: str=None, danfe: str=None) -> bool:
    """
    :param nfe: Condicional. Se usar NFe precisa de Serie e nõa precisa de danfe
    :param serie: Condicional. Se usar NFe precisa de Serie e nõa precisa de danfe
    :param cnpj: Obrigatório
    :param danfe: Condicional. Se usar DANFE não NFe precisa de Serie e não precisa de NFE
    :return:
    """
    session_id = authorize_session()
    url = 'https://api.track3r.com.br/v2/Api/RetornaCodigoRastreio'

    if not (cnpj and ((nfe and serie) or danfe)):
        return False

    payload = json.dumps({
        "Token": session_id,
        "notasfiscais": [
            {
                "NrCnpj": cnpj,
                "NotaFiscal": nfe,
                "SerieNota": serie,
                "Pedido": "",
                "ChaveNfe": danfe
            }
        ]
    })
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False

def process_xml(xml: bytes, **kwargs) -> dict:
    xml_dict = xmltodict.parse(xml)
    data = xml_dict["nfeProc"]["NFe"]["infNFe"]

    product_id = kwargs.get('product_id', None)

    if not product_id:
        product_id = get_product_id(cnpj=data['emit']['CNPJ'], tipo_operacao=data['ide']['finNFe'])

    qtde_volumes = int(data['transp']['vol']['qVol'])
    peso_total = float(data['transp']['vol']['pesoL'])

    recebe_notas_json_payload = {
        "id_produto": product_id,
        "numero_pedido": data['compra']['xPed'],
        "nome_marca": '',  # Candidato a usar como TAG
        "numero_rastreio_embarcador": '',  # Candidato a usar como TAG
        "pedido_aguardando_faturamento": False,
        "documento_transportado": {
            "tipo": "1",
            "numero": data['ide']['nNF'],
            "serie": data['ide']['serie'],
            "chave_acesso": xml_dict['protNFe']['infProt']['chNFe'],
            "quantidade_volumes": data['transp']['vol']['qVol'],
            "valor_documento": data['total']['ICMSTot']['vNF'],
            "data_emissao": data['ide']['dhEmi']
        },
        "embarcador": {
            "cnpj": data['emit']['CNPJ'],
            "inscricao_estadual": data['emit']['IE'],
            "razao_social": data['emit']['xNome'],
            "endereco": {
                "cep": data['emit']['enderEmit']['CEP'],
                "bairro": data['emit']['enderEmit']['xBairro'],
                "rua": data['emit']['enderEmit']['xLgr'],
                "numero": data['emit']['enderEmit']['nro'],
                "complemento": data['emit']['enderEmit']['xCpl'],
                "cidade": data['emit']['enderEmit']['xMun'],
                "estado": data['emit']['enderEmit']['UF']
            }
        },
        "tomador": {
            "cnpj": data['emit']['CNPJ'],
            "inscricao_estadual": data['emit']['IE'],
            "razao_social": data['emit']['xNome'],
            "endereco": {
                "cep": data['emit']['enderEmit']['CEP'],
                "bairro": data['emit']['enderEmit']['xBairro'],
                "rua": data['emit']['enderEmit']['xLgr'],
                "numero": data['emit']['enderEmit']['nro'],
                "complemento": data['emit']['enderEmit']['xCpl'],
                "cidade": data['emit']['enderEmit']['xMun'],
                "estado": data['emit']['enderEmit']['UF']
            }
        },
        "destinatario": {
            "tipo_pessoa": "J",
            "cnpj_cpf": data['entrega']['CNPJ'],
            "inscricao_estadual": data['entrega']['IE'],
            "nome": data['entrega']['xNome'],
            "observacoes": "",
            "endereco": {
                "cep": data['entrega']['enderDest']['CEP'],
                "bairro": data['entrega']['enderDest']['xBairro'],
                "rua": data['entrega']['enderDest']['xLgr'],
                "numero": data['entrega']['enderDest']['nro'],
                "complemento": data['entrega']['enderDest']['xCpl'],
                "cidade": data['entrega']['enderDest']['xMun'],
                "estado": data['entrega']['enderDest']['UF']
            }
        },
        "volumes": [
            {
                "codigo_etiqueta": "",
                "altura": 0.00,
                "largura": 0.00,
                "comprimento": 0.00,
                "peso_real": peso_total / qtde_volumes,
                "peso_cubado": 0.00
            }
        ] * qtde_volumes
    }

    return recebe_notas_json_payload

def lower_dict_keys(dictionary: dict) -> dict:
    return {k.lower(): v for k, v in dictionary.items()}

danfe = '35241124552989000104550020001583151544824593'
cnpj = '24.552.989/0001-04'
results = check_if_nota_exists(danfe=danfe)
