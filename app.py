import configparser
import os
import threading
import time
from src.rotinas import log, limpaLogTH
from src.TeamsInt import EnviaComunicado
import src.API as API
import datetime
import src.Servico as Servico
import asyncio
from src.estatisticas import disk_percent

versao = '1.2.5'

# cfg = ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
# cfg.read_file(open(os.path.join(os.path.dirname(__file__),"config.ini")))

try:
    # cfg.read_file(open(os.path.join(os.path.dirname(__file__),"config.ini")))
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = configparser.ConfigParser()
        cfg.read_file(f)
except Exception as ex:
    log('erro', f'[CFG] {ex}')
# Default
host = cfg.get('TELNET','URL')
listaURL = host.split(',')
delay = cfg.getint('DEFAULT','DELAY')
timeout = cfg.getint('DEFAULT','TIMEOUT')
debug = cfg.getboolean('DEFAULT','DEBUG')
local = cfg.get('DEFAULT','LOCALIDADE')
# Serviços
srv = cfg.get('SERVICO','SERVICOS')
servicos = srv.split(',')
iniciaSrv = cfg.getboolean('SERVICO','INICIA_SERVICO')
direct = cfg.getboolean('SERVICO','DIRECT')
# Comunicação
api = cfg.get('COM','API')
apis = api.split(',')
urlTeams = cfg.get('COM','URL')
titulo = f'Aviso automatizado - {local}'
canais = cfg.get('COM','CANAL')
canaisLs = [int(canal) for canal in canais.split(',')]
key = cfg.get('COM','KEY')
#ESPACO EM DISCO
discos = cfg.get('ESTATISTICAS','DISCOS').split(',')
tol = cfg.get('ESTATISTICAS','TOLERANCIA')
tolerancia = [int(percent) for percent in tol.split(',')]

def com(mensagem):
    try:
        # resposta = ""
        # Obter a data e hora atuais
        data_hora_atual = datetime.datetime.now()
        data_formatada = data_hora_atual.strftime("%d de %B de %Y")
        hora_formatada = data_hora_atual.strftime("%H:%M")
        # Mensagem da Dona Odete com um marcador de posição para o aviso
        recado = f"""
Olá, meus amores!  
   
Aqui é a vovó Odete, passando para avisar que identificamos um probleminha em nossos servidores.  
   
**Detalhes do ocorrido:**  
- **Data:** {data_formatada}  
- **Horário:** às {hora_formatada}  
- {mensagem}  
   
Se precisarem de alguma coisa, é só falar com a vovó aqui!  
   
Com muito carinho,  
**Vovó Odete**
        """
         #Rota de comunicação

        if api: #Se possuir url de API
            i = 0
            while (i <= len(apis)):
                for canal in canaisLs:
                    payload = {
                        "titulo": titulo,
                        "msg": recado,
                        "canal": int(canal),
                        "key": key
                    }
                    resposta = API.send_teams_message(payload, apis[i])
                    if resposta != 'true':#Se nao comunicou tenta o proximo
                        log('erro', resposta)
                        if len(apis) == 1:
                            i = len(apis) + 1
                            break
                        elif i >= len(apis): # Se ultima url da lista
                            i = len(apis) + 1
                            break
                        else: #Se nao, tenta proximo
                            i = i+1
                            delay(5)
                    else: #Se comunicou encerra loop
                        i = len(apis) + 1
                        break

        else:#Padrão para teams
            if urlTeams:
                ret = EnviaComunicado(urlTeams, recado, titulo)
                if ret:
                    log('erro', f'[COMUNICACAO] - {ret}')
            else:
                print(f'[COMUNICACAO] - Local: {local} {mensagem}')
    except Exception as ex:
        log('erro', f'[COMUNICACAO] - {ex}')
        print(f'[COMUNICACAO] - {ex}')

def start_telnet_thread():
    loop = asyncio.new_event_loop()  # Cria um novo loop de eventos
    asyncio.set_event_loop(loop)  # Define como o loop da thread
    loop.run_until_complete(thread_telnet())  # Executa a corrotina

# THREADS
async def thread_telnet():
    log('info', 'Iniciando TH Telnet')
    print("Iniciando TH Telnet")
    hosts = {}
    while True:
        try:
            for url in listaURL:
                if url:
                    ip, porta, nome = url.strip().split(":")
                    testeResult = await Telnet.testar_conexao(ip, porta, nome, debug)
                    if testeResult:
                        if nome not in hosts:
                            hosts[nome] = 0
                            print(testeResult)
                            log('erro', testeResult)
                            com(testeResult)
                        else:
                            if hosts[nome] == 1:#Se estado anterior OK
                                hosts[nome] = 0
                                print(testeResult)
                                log('erro', testeResult)
                                com(testeResult)
                    else:
                        if nome not in hosts:
                            hosts[nome] = 1
                        else:
                            if hosts[nome] == 0:#Aviso de reestabelecimento
                                hosts[nome] = 1
                                log('info', f'O host {nome} ({ip}:{porta}) voltou a responder!')
                                print(f'O host {nome} ({ip}:{porta}) voltou a responder!')
                                com(f'O host {nome} ({ip}:{porta}) voltou a responder!')
                        if debug:
                            print(f'O host {nome} está respondendo corretamente')
                            log('info', f'O host {nome} está respondendo corretamente')

            if debug:
                print(f'[TELNET_TH] Aguardando para proxima execução: {delay} minutos')
            await asyncio.sleep(delay * 60)
            # time.sleep(delay*60)
        except Exception as ex:
            log('erro', f'[TELNET_TH] Erro na execução do loop: {ex}')

def thread_servico():
    log('info', 'Iniciando TH Serviços')
    print("Iniciando TH Serviços")
    servMem = {}
    while True:
        try:
            for serv in servicos:
                retorno = Servico.verificaServico(serv.strip(),iniciaSrv,direct, debug)
                if retorno:#Se houve indisponibilidade
                    if serv not in servMem:#Se não existe estado anterior
                        log('erro', retorno)
                        print(retorno)
                        servMem[serv] = 0
                        com(retorno)#Envia mensagem de erro
                    else:
                        if servMem[serv] == 1:#Se estado anterior OK
                            log('erro', retorno)
                            print(retorno)
                            servMem[serv] = 0
                            com(retorno)#Envia mensagem de erro
                else:#Se não houve indisponibilidade
                    if serv not in servMem:
                        servMem[serv] = 1
                    else:
                        if servMem[serv] == 0:#Aviso de reestabelecimento
                            servMem[serv] = 1
                            log('info', f'[SERVICO] - Serviço: {serv}, voltou a funcionar!')
                            print(f'[SERVICO] - Serviço: {serv}, voltou a funcionar!')
                            com(f'O Serviço {serv} voltou a funcionar!')
                    # if debug:
                    #     log('info', f'[SERVICO] - Serviço: {serv}, funcionando corretamente')
                    #     print(f'[SERVICO] - Serviço: {serv}, funcionando corretamente')
                    # servMem[serv] = 1
            if debug:
                print(f'[SERVICO_TH] Aguardando para proxima execução: {delay} minutos')
            
        except Exception as ex:
            print(f'[SERVICO_TH] Erro na execução do loop: {ex}')
            log('erro', f'[SERVICO_TH] Erro na execução do loop: {ex}')
        time.sleep(delay*60)

def thread_estatisticas():
    log('info', 'Iniciando TH Estatisticas')
    print("Iniciando TH Estatisticas")
    mem_Percent = {}
    while True:
        try:
            for disco in discos:
                for i, percent_tol in enumerate(tolerancia):
                    percent = int(disk_percent(disco.strip()))
                    if(percent_tol < percent):
                        

                        if disco not in mem_Percent: # Se não há valor anterior OU percent MAIOR que armazenado
                            mem_Percent[disco] = percent  # Atualiza com o novo valor e comunica
                            com(f'[DISCO] - Disco {disco} atingiu a porcentagem de {percent}% de uso!')
                        elif int(mem_Percent[disco]) >= percent: #Não comunica
                            mem_Percent[disco] = percent

                        elif int(mem_Percent[disco]) < percent:
                            mem_Percent[disco] = percent  # Atualiza com o novo valor
                            com(f'[DISCO] - Disco {disco} atingiu a porcentagem de {percent}% de uso!')

                        # t_atual = int(tolerancia[i])
                        # ultimo_t = int(tolerancia[-1])
                        # t_mais_um = tolerancia[i+1]

                        if int(tolerancia[i]) == int(tolerancia[-1]):
                            print(f'[DISCO] - Disco {disco} atingiu a porcentagem de {percent}% de uso!')
                            log('erro', f'[DISCO] - Disco {disco} atingiu a porcentagem de {percent}% de uso!')
                        elif int(tolerancia[i+1]) >= int(percent):
                            print(f'[DISCO] - Disco {disco} atingiu a porcentagem de {percent}% de uso!')
                            log('erro', f'[DISCO] - Disco {disco} atingiu a porcentagem de {percent}% de uso!')

        except Exception as ex:
            print(f'[ESTATISTICAS_TH] Erro na execução do loop: {ex}')
            log('erro', f'[ESTATISTICAS_TH] Erro na execução do loop: {ex}')

        if debug:
                print(f'[ESTATISTICAS_TH] Aguardando para proxima execução: {delay} minutos')
        time.sleep(delay*60)

logTH = threading.Thread(target=limpaLogTH, args=())
telnetTH = threading.Thread(target=start_telnet_thread, args=())
servTH = threading.Thread(target=thread_servico, args=())
estatTH = threading.Thread(target=thread_estatisticas, args=())
# ldapTH =  threading.Thread(target=thread_LDAP, args=())
log('info', f"Iniciando aplicação Versão: {versao}")
print(f"Iniciando aplicação Versão: {versao}")

try:
    logTH.start() #limpeza de log
    if len(listaURL) >= 1:
        import src.Telnet as Telnet
        telnetTH.start() #Testes Via Telnet
    if srv:
        servTH.start()
    if len(discos) >= 1:
        estatTH.start()

    
except(KeyboardInterrupt):
    telnetTH.terminate()
    logTH.terminate()
    estatTH.terminate()
    log('info', 'Finalizando aplicação')
    print("Saindo...")
    quit()
except Exception as ex:
    print(f'Erro na execução do loop: {ex}')
    log('erro', f'Erro na execução do loop: {ex}')