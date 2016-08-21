# coding=utf-8

import csv

# probabilidad de supervivencia:
# niños max prioridad (age <= 9), mujeres segunda prioridad, hombres menos prioridad
# más caro el ticket => más chances de sobrevivir
# pega en el frente del barco => cabinas mas cerca de A más probable que no sobrevivan (este dato no está tan presente en el archivo)
# --> ponderar esto o tomar maximo (por ahora maximo)

EDAD_MINIMA_PARA_CONSIDERAR_NINIO = 9
PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_NINIO = 0.8
PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_ADULTO = 0.4
PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_HOMBRE = 0.3
PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_MUJER = 0.7
PRECIO_MEDIO_ASUMIDO = 700
PROBABILIDAD_DE_SUPERVIVENCIA_POR_TICKET_BARATO = 0.3
PROBABILIDAD_DE_SUPERVIVENCIA_POR_TICKET_CARO = 0.7
CABINA_DE_LA_MITAD = 'H'
PROBABILIDAD_DE_SUPERVIVENCIA_POR_ESTAR_CERCA_DEL_CHOQUE = 0.3
PROBABILIDAD_DE_SUPERVIVENCIA_POR_ESTAR_LEJOS_DEL_CHOQUE = 0.6
PROBABILIDAD_MINIMA_PARA_CONSIDERAR_ALGUIEN_COMO_SUPERVIVIENTE = 0.7


def calcular_probabilidad_por_edad(edad, probabilidades_de_supervivencia):
    if edad is not None:
        if edad <= EDAD_MINIMA_PARA_CONSIDERAR_NINIO:
            probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_NINIO)
        else:
            probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_ADULTO)


def calcular_probabilidad_por_sexo(sexo, probabilidades_de_supervivencia):
    if sexo == 'male':
        probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_HOMBRE)
    else:
        probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_SER_MUJER)


def calcular_probabilidad_por_precio_de_ticket(precio_del_ticket, probabilidades_de_supervivencia):
    if precio_del_ticket:
        if precio_del_ticket <= PRECIO_MEDIO_ASUMIDO:
            probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_TICKET_BARATO)
        else:
            probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_TICKET_CARO)


def calcular_probabilidad_por_cabina(cabina, probabilidades_de_supervivencia):
    if cabina:
        if ord(cabina[0]) < ord(CABINA_DE_LA_MITAD):
            probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_ESTAR_CERCA_DEL_CHOQUE)
        else:
            probabilidades_de_supervivencia.append(PROBABILIDAD_DE_SUPERVIVENCIA_POR_ESTAR_LEJOS_DEL_CHOQUE)


def estimar_supervivencia_para(nombre_archivo):
    with open(nombre_archivo, 'rb') as csvfile:
        d_reader = csv.DictReader(csvfile)

        cantidad_total = 0
        cantidad_real_de_sobrevivientes = 0
        cantidad_estimada_de_sobrevivientes = 0
        cantidad_de_aciertos = 0
        for line in d_reader:
            supervivencia_real = int(line['survived'])
            edad = float(line['age']) if line['age'] else None
            sexo = line['sex']
            precio_del_ticket = float(line['fare']) if line['fare'] else None
            cabina = line.get('cabin', None)

            cantidad_total += 1
            cantidad_real_de_sobrevivientes += supervivencia_real

            probabilidades_de_supervivencia = []
            calcular_probabilidad_por_edad(edad, probabilidades_de_supervivencia)
            calcular_probabilidad_por_sexo(sexo, probabilidades_de_supervivencia)
            calcular_probabilidad_por_precio_de_ticket(precio_del_ticket, probabilidades_de_supervivencia)
            calcular_probabilidad_por_cabina(cabina, probabilidades_de_supervivencia)

            probabilidad_de_supervivencia = max(probabilidades_de_supervivencia)  # bastante choto
            probabilidad_suficiente_de_supervivencia = probabilidad_de_supervivencia >= PROBABILIDAD_MINIMA_PARA_CONSIDERAR_ALGUIEN_COMO_SUPERVIVIENTE

            if probabilidad_suficiente_de_supervivencia:
                cantidad_estimada_de_sobrevivientes += 1
                if supervivencia_real == 1:
                    cantidad_de_aciertos += 1
            else:
                if supervivencia_real == 0:
                    cantidad_de_aciertos += 1

        cantidad_real_de_fallecidos = cantidad_total - cantidad_real_de_sobrevivientes

        print 'Cantidad total de personas: %s' % cantidad_total
        print 'Cantidad real de sobrevivientes: %s' % cantidad_real_de_sobrevivientes
        print 'Cantidad real de fallecidos: %s' % cantidad_real_de_fallecidos
        print 'Cantidad estimada de sobrevivientes: %s' % cantidad_estimada_de_sobrevivientes
        print 'Cantidad estimada de fallecidos: %s' % (cantidad_total - cantidad_estimada_de_sobrevivientes)
        print 'Cantidad de aciertos: %s de %s (%.2f%%)' % (cantidad_de_aciertos, cantidad_total,
                                                           float(cantidad_de_aciertos) * 100 / cantidad_total)

if __name__ == '__main__':
    estimar_supervivencia_para('titanic-train.csv')
