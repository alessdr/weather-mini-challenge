def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def formatar_string_dias(lista):
    dias_quarda_chuva = ','.join(lista)
    return rreplace(dias_quarda_chuva, ',', ' e ', 1)
