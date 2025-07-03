import datetime
import time
from src.rotinas import log
import os
import psutil

def verificaServico(servico, inicia, direct, debug): #Verifica status do serviço
    retorno = ''
    try:
        service = psutil.win_service_get(servico)
        psutil.win_service_iter()

        if service:
            service = service.as_dict()
            if service['status'] == 'stopped':
                log('erro', f"{service['display_name']} - O serviço não está em execução")
                retorno = f"[SERVICO] [{service['display_name']}] - O serviço não está em execução"
                print(f"[SERVICO] [{service['display_name']}] - O serviço não está em execução")
                if(inicia): #Caso habilitado, tenta iniciar o serviço
                    log('info', f"Iniciando serviço {service['name']}")
                    
                    if direct:
                        os.system(f'NET START "{servico}"' )
                    else:
                        os.system(f"NET START {service['name']}") #Inicia serviço
                        
                    time.sleep(20)

                    #Verifica status serviço
                    service = psutil.win_service_get(servico)
                    psutil.win_service_iter()
                    service = service.as_dict()

                    if service and service['status'] == 'running': #SERVIÇO HABILITADO COM EXITO
                        log('info', f"[SERVICO] [{service['display_name']}] - O serviço parou mas foi iniciado com sucesso!")
                        print(f"[SERVICO] [{service['display_name']}] - O serviço parou mas foi iniciado com sucesso!")
                        retorno = f"[SERVICO] [{service['display_name']}] - O serviço parou mas foi iniciado com sucesso!"
                    else: #FALHA AO HABILITAR SERVIÇO
                        log('erro', f"[SERVICO] [{service['display_name']}] - O serviço parou e não pode ser reiniciado!")
                        print(f"[SERVICO] [{service['display_name']}] - O serviço parou e não pode ser reiniciado!")
                        retorno = f"[SERVICO] [{service['display_name']}] - O serviço parou e não pode ser reiniciado!"
            else:
                retorno = ''
                if debug:
                    log('info', f"Serviço {service['display_name']} está em {service['status']}")
                    print(f"Serviço {service['display_name']} está em {service['status']}")
                
        else:
            log('erro', f"[SERVICO] O serviço {servico} não pode ser verificado")
            print(f"[SERVICO] O serviço {servico} não pode ser verificado")
            retorno = f"[SERVICO] O serviço {servico} não pode ser verificado"
                            
    except Exception as ex:
        log('erro', f"[SERVICO] - Falha ao processar o serviço {servico}: {ex}")
        # logger.error(f"Falha ao iniciar o serviço: {ex}")
        print(str(f"[SERVICO] - Falha ao processar o serviço {servico}: {ex}"))
        retorno = f"[SERVICO] - Falha ao processar o serviço {servico}: {ex}"

    return retorno
