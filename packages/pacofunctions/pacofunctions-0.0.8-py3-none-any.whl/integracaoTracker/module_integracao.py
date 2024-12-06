# This is a sample Python script.
from utilFunctions.module import list_emails, config

import utils
from utils import relabel_cancelled_xml_emails, files_to_process, get_nf_info, check_if_nota_exists


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# todo
# skip notas that we cannot process instead of crashing the program
# retrieve all xmls attached from an email and process them all (ability to process emails with several xmls)

def get_notas() -> list:
    xml_to_process: list = list_emails(label_id=config.labels_xml_processar, user="me", q=f"-correcao -correção")
    reversas_to_process: list = list_emails(label_id=config.label_devolucoes_processar, user="me", q=" from:(*@mail.pipefy.com)")
    notas_to_process = xml_to_process + reversas_to_process
    return xml_to_process, reversas_to_process


def main():
    # Remove cancelled NF's from processing line:
    relabel_cancelled_xml_emails()
    notas = get_notas()
    for nota in notas:
        payload, nfe_number, danfe = get_nf_info(email_da_nota=nota)
        nota_exists = check_if_nota_exists(nfe=nfe_number, danfe=danfe)

        if not nota_exists and payload is not None:
            utils.recebe_notas_json(nota, id_servico=..., encomendas=payload)
        else:
            pass


if __name__ == '__main__':

    main()
    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
