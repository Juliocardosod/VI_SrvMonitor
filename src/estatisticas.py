import shutil
from psutil._common import bytes2human

def disk_percent(path):
    nt = shutil.disk_usage(path)
    total = 0
    usado = 0
    for name in nt._fields:
        value = getattr(nt, name)
        if name == 'total':
            total = int(value)
        if name == 'used':
            usado = int(value)
    percent =int((usado*100)/total)
    return(percent)

def pprint_memory(nt): #Captura de estatísticas de memória
    ls = []
    global memoria
    for name in nt._fields:
        # parei aqui valores em bytes        
        value = getattr(nt, name)
        if name == 'percent':
            memoria = float(value)
        if name != 'percent':
            value = bytes2human(value)
        else:
            value = f'{value}%'    
        val = str('%-0s : %0s' % (name.capitalize(), value))
        ls.insert(1, val)
    
    del ls[2]
    del ls[3]
    lm = ' . '.join(ls)
    return (lm)
