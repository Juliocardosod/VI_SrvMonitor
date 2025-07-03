import pymsteams

def EnviaComunicado(url, mensagem, titulo):
    retorno = ''
    myTeamsMessage = pymsteams.connectorcard(url)
    myTeamsMessage.title(titulo)
    myTeamsMessage.text(mensagem)
    try:
        myTeamsMessage.send()
        codResp = myTeamsMessage.last_http_response.status_code
        if codResp != 200:
            retorno = f"Erro ao enviar mensagem, COD {codResp}"
    except Exception as ex:
        retorno = ex
    return retorno