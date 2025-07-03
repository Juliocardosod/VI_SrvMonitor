import telnetlib3
from src.rotinas import log

async def testar_conexao(ip_entrada, port, nome, debug):
    try:
        partes = ip_entrada.split("/", 1)
        ip = partes[0]  # Primeiro elemento será sempre o IP
        rota = f"/{partes[1]}" if len(partes) > 1 else "/"  # Se existir rota, adi

        reader, writer = await telnetlib3.open_connection(ip, port)

        resposta = "" #Conexão Telnet estabelecida com sucesso."

        writer.close()
        if debug:
            print(f"Conexão estabelecida com sucesso na API {nome} - ({ip}:{port})")
            log('info', f"Conexão estabelecida com sucesso na API {nome} - ({ip}:{port})")
        return resposta 
    except Exception as e:
        log('erro', f'[API] [{nome} {ip}:{port}] - {e}')
        print(f'[API] [{nome} {ip}:{port}] - {e}')
        return f'[API] [{nome} {ip}:{port}] - {e}'
