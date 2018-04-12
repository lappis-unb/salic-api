import re

from pycpfcnpj.cpfcnpj import validate as validate_cpf


def cgccpf_mask(cgccpf):
    """
    Create a CPF mask for valid CPFs.
    """
    if not cgccpf:
        return ''
    try:
        if validate_cpf(cgccpf):
            cgccpf = '***' + cgccpf[3:9] + '**'
    except:
        pass
    return cgccpf


def sanitize(value):
    """
    Remove unwanted whitespace from string.
    """
    if value is None:
        return ''
    return re.sub('\s+', ' ', value).strip()
