import pandas as pd
from datetime import datetime, timedelta
import re
import math

def obtener_informacion_completa(row, df_sepomex, df_coneval, df_ginequito):
    # Obtener el valor de CP o H en df_cuestionarios
    valor_a_buscar = row['C.P.']

    # Buscar valor_a_buscar en df_sepomex['CP.ASENTAMIENTO']
    # Obtiene el código postal de la paciente desde el cuestionario de riesgo y luego lo busca en la base de datos de SEPOMEX
    # Posterior a esto el código busca el valor obtenido en el municipio de busqueda y lo compara con todo el archivo hasta que encuentra
    # el valor con el que coincide y regresa el tipo de zona de asentamiento que es el municipio

    municipiobusqueda = 'Municipio no encontrado'
    asentamiento = 'Asentamiento no encontrado'
    for index, sepomex_row in df_sepomex.iterrows():

        if sepomex_row['CP.ASENTAMIENTO'] == 'S/R':
            poblacionmun = 'not-found'
            rangopobreza = 'not-found'
        else:
            cpas = int(sepomex_row['CP.ASENTAMIENTO'])
            strcpas = str(cpas)
            municipiobusqueda = sepomex_row['MUNICIPIO']

            if sepomex_row['ZONA.ASENTAMIENTO'] == 'Rural':
                asentamiento = 'rural'
            elif sepomex_row['ZONA.ASENTAMIENTO'] == 'Urbano':
                asentamiento = 'urban'

            if strcpas == valor_a_buscar:
                municipiobusqueda = sepomex_row['MUNICIPIO']
                break

    # Buscar municipiobusqueda en df_coneval['MUNICIPIO']
    # Rangos de pobreza Coneval
    # Compara el valor obtenido en la base de datos de sepomex y ahora busca el municipio obtenido en la base de datos de coneval
    # Posterior a esto el código encuentra el rango de pobreza que tiene el municipio de la paciente y realiza la conparación de los rangos para obtener el rango
    poblacionmun = 'not-found'
    rangopobreza = 'not-found'
    for index, coneval_row in df_coneval.iterrows():

        if str(coneval_row['MUNICIPIO']) == municipiobusqueda:
            poblacionmun = str(coneval_row['POBLACION.ITER'])
            rang = str(coneval_row['RANGO.POBREZA'])
            # Asignar rango según la condición especificada
            if  rang == '[0, 20)' or rang == '[ 0, 20)' :
                rangopobreza = 'very low'
            elif rang == '[20, 40)' or rang == '[ 20, 40)' :
                rangopobreza = 'low'
            elif rang == '[40, 60)' or rang == '[ 40, 60)'  :
                rangopobreza = 'middle'
            elif rang == '[60, 80)' or rang == '[ 60, 80)'  :
                rangopobreza = 'high'
            elif rang == '[80, 100)' or rang == '[ 80, 100)' :
                rangopobreza = 'very high'

            break


    # Calculo fecha de nacimiento
    # Para la obtencion de la fecha de nacimiento el código realiza la obtencion de la fecha de nacimiento con la fecha de toma
    # se utilizan las libreria datetime y quita la hora en el campo de fecha de toma y realiza la comparacion para obtener la edad en la cual se le realizo la toma a la paciente
    #
    if row['FECHA_NAC'] == 'S/R':
        edad = 'not-ans'
    else:
        # Supongamos que row['FECHA_NAC'] es una cadena en el formato '02/05/1968'
        fecha_nacimiento_str = row['FECHA_NAC']
        # Convertir la cadena a un objeto datetime
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%d/%m/%Y')
        # Obtener la fecha actual
        fecha_toma_str = row['FECHA_HORA_TOMA'].split()[0]  # Obtener la parte de la fecha, ignorando la hora
        fecha_actual = datetime.strptime(fecha_toma_str, '%d/%m/%Y')
        # Calcular la diferencia de tiempo entre la fecha actual y la fecha de nacimiento
        edad = fecha_actual.year - fecha_nacimiento.year - (
                (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    # Calcular el bmi
    # Realiza el calculo del indice de masa corporan en float y lo redondea a 4 decimales
    #
    #
    if row['TALLA'] == 'S/R' or row['PESO'] == 'S/R':
        bmi = 'not-computable'
    else:
        talla = row['TALLA']
        tallai = float(talla)
        peso = float(row['PESO'])
        bmi = round(peso / (tallai ** 2), 4)

    # Calcular los campos relacionados con el campo fumar
    #
    #
    #
    valor_fuma = row['CANTIDAD_CIGARRILLOS']
    if valor_fuma == 'S/R':
        frecfum = 'not-ans'
    else:
        if isinstance(valor_fuma, str):
            match = re.match(r'(\d+)\s*A\s*(\d+)', valor_fuma)

            if match:
                # Obtener los dos números del rango
                num1, num2 = map(int, match.groups())

                # Calcular el promedio y redondear hacia arriba
                resultado = math.ceil((num1 + num2) / 2)

            else:
                # Si solo hay un número, convertirlo a entero
                resultado = int(valor_fuma)

        else:
            # Manejar el caso en que valor_fuma no es una cadena
            resultado = None  # O cualquier otro manejo que desees hacer

    if row['FUMA '] == 1:
        fumador = "yes"
        frecfum = ""
        if row['FRECUENCIA_FUMA'] == 'DIARIAMENTE':
            frecfum = resultado * 7

        elif row['FRECUENCIA_FUMA'] == 'ANUALMENTE':
            frecfum = resultado * 1
        elif row['FRECUENCIA_FUMA'] == 'SEMANALMENTE':
            resultado = int(resultado)
            frecfum = math.ceil(resultado)
        elif row['FRECUENCIA_FUMA'] == 'S/R':
            resultado = int(resultado)
            frecfum = math.ceil(resultado)
        elif row['FRECUENCIA_FUMA'] == 'MENSUALMENTE':
            # Asegurarse de que resultado sea un entero antes de operar con él
            resultado = int(resultado)
            frecfum = math.ceil(resultado / 4)
    elif row['FUMA '] == 2:
        fumador = "no"
        frecfum = 'not-computable'
    else:
        fumador = "not-ans"
        cantidadfum = "not-ans"
        frecfum = "not-ans"

    # Calcular el
    #
    #
    #
    if row['MENARCA'] == 'S/R':
        edadM = 'not-ans'
    else:
        menarca_str = row['MENARCA']

        # Utilizar expresiones regulares para extraer la edad como número
        edad_match = re.search(r'(\d+)', menarca_str)

        # Verificar si se encontró una coincidencia y obtener el valor
        edadM = int(edad_match.group(1)) if edad_match else 0  # Puedes asignar un valor predeterminado si no se encuentra la edad

    if row['INICIO_VIDA_SEXUAL '] == 'S/R':
        edadS = 'not-ans'
        edadSince = 'not-ans'
    else:
        sexual_str = row['INICIO_VIDA_SEXUAL ']
        # Utilizar expresiones regulares para extraer la edad como número
        edad_match = re.search(r'(\d+)', sexual_str)

        # Verificar si se encontró una coincidencia y obtener el valor
        edadS = int(edad_match.group(
            1)) if edad_match else 0  # Puedes asignar un valor predeterminado si no se encuentra la edad
        edadSince = edadS - edadM

    if row['NUM_PAREJAS_SEXUALES'] == '1':
        parejas = 1
    elif row['NUM_PAREJAS_SEXUALES'] == '2':
        parejas = 2
    elif row['NUM_PAREJAS_SEXUALES'] == '3':
        parejas = 3
    elif row['NUM_PAREJAS_SEXUALES'] == '4':
        parejas = 4
    else:
        parejas = 'none'


    if row['FECHA_HORA_TOMA'] == 'S/R':
        fechaup = 'not-ans'
        fechaap = 'not-ans'
        fechaac = 'not-ans'
        fechauc = 'not-ans'
    else:
        fecha_toma_str = row['FECHA_HORA_TOMA'].split()[0]  # Obtener la parte de la fecha, ignorando la hora
        fecha_toma = datetime.strptime(fecha_toma_str, '%d/%m/%Y')
        if row['FECHA_ULTIMO_PAPANICOLAOU'] == 'S/R':
            fechaup = 'not-ans'
            fechaap = 'not-ans'
        elif row['FECHA_ULTIMO_PAPANICOLAOU'] == 'NUNCA':
            fechaup = 'never'
            fechaap = 'never'
        elif len(row['FECHA_ULTIMO_PAPANICOLAOU']) == 4:
            intpap = int(row['FECHA_ULTIMO_PAPANICOLAOU'])
            fechaap = fecha_toma.year - intpap
            fechaup = intpap
        else:
            cadena2 = row['FECHA_ULTIMO_PAPANICOLAOU']
            partes_cadena2 = cadena2.split()
            cantidad_cadena2 = int(partes_cadena2[1])  # Convertir a entero
            unidad_cadena2 = partes_cadena2[2]  # Obtener la unidad (años o meses)
            if unidad_cadena2 == 'AÑOS':
                fechaup = fecha_toma.year - cantidad_cadena2
                fechaap = cantidad_cadena2
            else:
                # Calcular una nueva fecha que esté 15 meses atrás
                nueva_fecha = fecha_toma - timedelta(
                    days=cantidad_cadena2 * 30)  # Asumiendo que un mes tiene aproximadamente 30 días
                fechaupm = fecha_toma.year - nueva_fecha.year
                fechaup = fecha_toma.year - fechaupm
                fechaap = fechaupm


        if row['FECHA_ULTIMA_COLPOSCOPIA'] == 'S/R':
            fechauc = 'not-ans'
            fechaac = 'not-ans'
        elif row['FECHA_ULTIMA_COLPOSCOPIA'] == 'NUNCA':
            fechauc = 'never'
            fechaac = 'never'

        elif len(row['FECHA_ULTIMA_COLPOSCOPIA']) == 4:
            intpap = int(row['FECHA_ULTIMA_COLPOSCOPIA'])

            fechaac = fecha_toma.year - intpap

            fechauc = intpap
        else:
            cadena2 = row['FECHA_ULTIMA_COLPOSCOPIA']
            partes_cadena2 = cadena2.split()
            cantidad_cadena2 = int(partes_cadena2[1])  # Convertir a entero
            unidad_cadena2 = partes_cadena2[2]  # Obtener la unidad (años o meses)
            if unidad_cadena2 == 'AÑOS':
                fechauc = fecha_toma.year - cantidad_cadena2
                fechaac = cantidad_cadena2
            else:
                # Calcular una nueva fecha que esté 15 meses atrás
                nueva_fecha = fecha_toma - timedelta(
                    days=cantidad_cadena2 * 30)  # Asumiendo que un mes tiene aproximadamente 30 días
                fechaac = fecha_toma.year - nueva_fecha.year
                fechauc = fecha_toma.year - fechaac

    # Calcular el
    #
    #
    #
    # Diccionario de traduccionesmpf
    traduccionesmpf = {
        'SALPINGOCLASIA': 'tubal occlusion',
        'CONDON': 'condom',
        'ANTICONCEPTIVOS ORALES': 'oral',
        'VASECTOMIA ESPOSO': 'vasectomy(partner)',
        'COITO INTERRUMPIDO': 'coitus interruptus',
        'PARCHE ANTICONCEPTIVO': 'patch',
        'INYECCION ANTICONCEPTIVA (CYCLOFEMINA)': 'injection',
        'DIU (MIRENA)': 'diu mirena',
        'DIU (COBRE)': 'diu copper',
        'DIU': 'diu',
        'CIRUGIA': 'surgery',
        'ANTICONCEPTIVOS ORALES (PASTILLA DIA DESPUES)': 'oral',
        # Agrega más traduccionesmpf según sea necesario
    }

    # Inicializa la variable mpf
    mpf = ""

    # Obtén las observaciones del método de planificación familiar
    observaciones = row['OBSERVACIONES_METODO_PLANIFICACION_FAMILIAR']

    # Convierte las observaciones a inglés y minúsculas usando el diccionario de traduccionesmpf
    observaciones_ingles = [traduccionesmpf.get(obs, obs) for obs in observaciones.split(" | ")]

    # Combina las observaciones traducidas en una cadena separada por " | "
    observaciones_ingles_str = " | ".join(observaciones_ingles)

    if row['OBSERVACIONES_METODO_PLANIFICACION_FAMILIAR'] == 'S/R':
        if row['METODO_PLANIFICACION_FAMILIAR'] == 'S/R':
            mpf = 'not-ans'
        elif len(row['METODO_PLANIFICACION_FAMILIAR']) >= 2:
            # Dividir la cadena usando el carácter "|"
            partes = row['METODO_PLANIFICACION_FAMILIAR'].split(" | ")
            variable1 = partes[0]
            if variable1 == '1':
                mpf1 = "coitus interruptus"
            elif variable1 == '2':
                mpf1 = "condom"
            elif variable1 == '3':
                mpf1 = "hormonal"
            elif variable1 == '4':
                mpf1 = "DIU"
            elif variable1 == '5':
                mpf1 = "other"
            variable2 = partes[1]
            if variable2 == '1':
                mpf2 = "coitus interruptus"
            elif variable2 == '2':
                mpf2 = "condom"
            elif variable2 == '3':
                mpf2 = "hormonal"
            elif variable2 == '4':
                mpf2 = "DIU"
            elif variable2 == '5':
                mpf2 = "other"

            mpf = mpf1 + " | " + mpf2
        else:
            if row['METODO_PLANIFICACION_FAMILIAR'] == '1':
                mpf = "coitus interruptus"
            elif row['METODO_PLANIFICACION_FAMILIAR'] == '2':
                mpf = "condom"
            elif row['METODO_PLANIFICACION_FAMILIAR'] == '3':
                mpf = "hormonal"
            elif row['METODO_PLANIFICACION_FAMILIAR'] == '4':
                mpf = "DIU"
            elif row['METODO_PLANIFICACION_FAMILIAR'] == '5':
                mpf = "other"
            else:
                mpf = "error"
    else:
        mpf = observaciones_ingles_str

    if row['ABORTO'] == 'S/R':
        at = 'not-ans'
        abn = 'not-ans'
    if row['ABORTO'] == '4':
        at = 'none'
        abn = 0
    else:
        # Dividir la cadena usando el carácter "|"
        partes = row['ABORTO'].split(" | ")

        translation_dict = {
            '1': 'curettage',
            '2': 'induced',
            '3': 'spontaneous',
            '4': 'none',
            '5 (EMBARAZO ECTOPICO)': 'ectopic'
        }

        abn = len(partes)
        at_values = [translation_dict.get(part, 'Ninguno') for part in partes]
        at = " | ".join(at_values)

    if row['PARTO'] == 'S/R':
        pn = 'not-ans'
    else:
        pn = int(row['PARTO'])

    if row['CESÁREA'] == 'S/R':
        cn = 'not-ans'
    else:
        cn = int(row['CESÁREA'])

    id_gineq = row['ID_GINEQ']

    # Filtrar df_ginequito para obtener solo la fila que cumple con la condición
    fila_ginequito = df_ginequito[df_ginequito['ID.GINEQ'] == id_gineq]

    # Acceder a los campos específicos de la fila obtenida
    if not fila_ginequito.empty:
        # PREVENTIX
        vptx = fila_ginequito['PREVENTIX'].values[0]
        valorpreventix = {
            'POSITIVO': 'positive',
            'negativo': 'NEGATIVO'
        }.get(vptx, 'not-biopsied')

        # p16
        vp16 = fila_ginequito['p16'].values[0]
        valorp16 = {
            'POSITIVO': 'positive',
            'NEGATIVO': 'negative',
            'NO-REALIZADO': 'not biopsied'
        }.get(vp16, 'na')

        # VPH2
        vphv = fila_ginequito['VPH2'].values[0]
        vph = {
            'POSITIVO': 'positive',
            'NEGATIVO': 'negative',
            's/r': 'not biopsied'
        }.get(vphv, 'na')

        # HPV.PCR.GENOTYPE
        genvph = fila_ginequito['HPV.PCR.GENOTYPE'].values[0]
        hpvgen = {
            'HPV-POOL': 'hpv-pool',
            'HPV-18': 'hpv-18',
            'HPV-16': 'hpv-16'
        }.get(genvph, 'none')

        # COLP.PERF
        colpperf = fila_ginequito['COLP.PERF'].values[0]
        valorcolpos = {
            'ADECUADA': 'adequate',
            'NO ADECUADA': 'inadequate',
            'NA': 'not-biopsied'
        }.get(colpperf, 'na')

        # COLP.CVXCN
        colpcv = fila_ginequito['COLP.CVXCN'].values[0]
        valorcolpcv = {
            'ATROFICO': 'atrophy',
            'HIPERTROFICO': 'hypertrophy',
            'EUTROFICO': 'eutrophy',
            'NA': 'none'
        }.get(colpcv, 'none')

        # COLP.TZ
        colptz = fila_ginequito['COLP.TZ'].values[0]
        valorcopltz = {
            'T1': 't1',
            'T2': 't2',
            'T3': 't3',
            'NORMAL': 'normal'
        }.get(colptz, 'none')

        # COLP.AWA.SURF
        colpawasurf = fila_ginequito['COLP.AWA.SURF'].values[0]
        valorcoplawasurf = {
            'LISA': 'smooth',
            'MACROPAPILAR': 'micropapillar',
            'MOSAICO FINO': 'fine mosaic',
            'MOSAICO GRUESO': 'coarse mosaic',
            'PUNTILLEO GRUESO': 'coarse punctation',
            'PUNTILLEO FINO': 'fine punctation'
        }.get(colpawasurf, 'na')

        # COLP.AWA
        valorcoplawa = ""

        # COLP.AWA.BOR
        colpawabor = fila_ginequito['COLP.AWA.BOR'].values[0]
        valorcoplawabor = {
            'DEFINIDOS': 'defined',
            'SIN RELIEVE': 'wo-ridge',
            'DIFUSOS': 'undefined',
            'CON RELIEVE': 'ridge'
        }.get(colpawabor, 'none')

        # Obtener el valor de ACETOWHITE.EPITHELIUM
        acetowhite = fila_ginequito['ACETOWHITE.EPITHELIUM'].values[0]
        acetowhitevalue = 'defined' if acetowhite == 'BLANCO FINO' else 'wo-ridge' if acetowhite == 'BLANCO GRUESO' else 'undefined' if acetowhite == 'ACETOFUGAZ' else 'none'

        # Obtener el valor de COLP.SCHIL
        schill = fila_ginequito['COLP.SCHIL'].values[0]
        schillvalue = 'positive' if schill in {'BLANCO FINO', 'BLANCO GRUESO', 'ACETOFUGAZ'} else 'negative'

        # Obtener el valor de BIOPSIED
        biopsed = fila_ginequito['BIOPSIED'].values[0]
        valorbiosed = 'biopsied' if biopsed == 'SI' else 'not biopsied' if biopsed == 'NO' else 'not-biopsied'

        # Obtener el valor de COLP.PERF
        colpperf = fila_ginequito['COLP.PERF'].values[0]
        valorcolpperf = 'adequate' if colpperf == 'ADECUADA' else 'inadequate' if colpperf == 'NO ADECUADA' else 'na' if colpperf == 'NA' else 'na'

        # Obtener los valores de la columna
        lbcdx = fila_ginequito['LBC.DX'].values[0]

        # Comprobar si lbcdx es una cadena antes de intentar dividirla
        if isinstance(lbcdx, str):
            # Mapeo de opciones
            mapeo_opciones = {
                'ALTERACIONES INFLAMATORIAS LEVES': 'mild inflammation',
                'ALTERACIONES INFLAMATORIAS MODERADAS': 'moderate inflammation',
                'ALTERACIONES INFLAMATORIAS SEVERAS': 'severe inflammation',
                'ATIPIA DE CELULAS ESCAMOSAS (ASC-US) DE SIGNIFICADO INCIERTO': 'asc-us',
                'LESION INTRAEPITELIAL ESCAMOSA DE BAJO GRADO (DISPLASIA LEVE)': 'lsil',
                'LIBG (NIC-1)': 'lsil',
                'CAMBIO DE LA FLORA VAGINAL POR FLORA COCO-BACILAR': 'bacterial vaginosis',
                'VAGINOSIS BACTERIANA': 'bacterial vaginosis',
                'IMAGEN DE ATROFIA CELULAR': 'cellular atrophy',
                'METAPLASIA ESCAMOSA': 'squamous metaplasia',
                'ATROFIA CELULAR': 'cellular atrophy',
                'CAMBIOS CITOPATICOS SUGESTIVOS DE INFECCION POR VIRUS DEL PAPILOMA HUMANO': 'suggestive hpv cellular change',
                'CAMBIOS CITOPATICOS POR VPH': 'suggestive hpv cellular change',
                'CAMBIO DE LA FLORA VAGINAL SUGESTIVO DE VAGINOSIS BACTERIANA': 'bacterial vaginosis'
            }

            # Dividir la cadena usando el carácter "|"
            lbcdx_opciones = lbcdx.split(" | ")

            # Iterar sobre cada opción y asignar el valor correspondiente
            valoreslbcdx = [mapeo_opciones.get(opcion.upper(), opcion) for opcion in lbcdx_opciones]

            # Comprobar si el arreglo está vacío y asignar 'not-biopsied' en ese caso
            if not valoreslbcdx:
                valoreslbcdx = 'not-biopsied'
            else:
                # Concatenar los valores en una cadena separada por " | "
                valoreslbcdx = " | ".join(valoreslbcdx)
        else:
            valoreslbcdx = 'not-biopsied'

        # Diccionario de traducciones para colpofind_opciones
        traducciones_colpofind = {
            'ALTERACIONES INFLAMATORIAS': 'inflammation',
            'ATROFIA SEVERA': 'severe atrophy',
            'ATROFIA': 'atrophy',
            'ATROFIA VAGINAL': 'atrophy',
            'ATROFIA VAGINAL MODERADA': 'moderate atrophy',
            'ATROFIA VAGINAL SEVERA': 'severe atrophy',
            'CONDILOMATOSIS': 'condylomatosis',
            'PROBABLE NIC-1': 'probable cin-1',
            'NIC-1 EN ENDOCERVIX': 'cin-1 endocervix',
            'POSIBLE NIC-1 EN ENDOCERVIX': 'probable cin-1 endocervix',
            'DESCARTAR NIC-1': 'discard cin-1',
            'NIC 1': 'cin-1',
            'LIAG': 'hsil',
            'LESION ACETOBLANCA DE 6 MM': 'acetowhite lesion',
            'QUISTE DE NABOTH': 'nabothian cyst',
            'LIQUEN ESCLEROSO': 'lichen sclerosus',
            'LIQUEN PLANO': 'lichen flat',
            'PROBABLE LIQUEN ESCLEROSO': 'probable lichen sclerosus',
            'LIQUEN ESCAMOSO': 'lichen squamous',
            'LIBG (NIC-1)': 'lsil',
            'LIAG (NIC-2)': 'cin-2',
            'METAPLASIA ESCAMOSA': 'squamous metaplasia',
            'POLIPO CERVICAL': 'polyp',
            'POLIPO': 'polyp',
            'SIN ALTERACIONES': 'neg-for-sil-malign',
            'EVERSION GLANDULAR': 'glandular eversion',
            'CAMBIOS CITOPATICOS POR VPH': 'cytopathic changes due to hpv',
            'ATROFIA SEVERA (PACIENTE CON HISTERECTOMIA)': 'severe atrophy hysterectomy',
            'MOLUSCO CONTAGIOSO': 'molluscum contagiosum',
            'NINGUNA': 'none',
            'VAGINITIS': 'vaginitis',
        }

        # Obtener los valores de la columna COLP.OFIND
        colpofind = fila_ginequito['COLP.OFIND'].values[0]

        # Inicializar una lista para almacenar los resultados
        valores_colpofind = []

        # Comprobar si colpofind es una cadena antes de intentar dividirla
        if isinstance(colpofind, str):
            # Dividir la cadena usando el carácter "|"
            colpofind_opciones = colpofind.split(" | ")

            # Iterar sobre cada opción y asignar el valor correspondiente
            for opcion in colpofind_opciones:
                opcion_mayusculas = opcion.upper()
                # Utilizar el diccionario para obtener la traducción o 'none' si no hay traducción
                valores_colpofind.append(traducciones_colpofind.get(opcion_mayusculas, opcion))

        # Comprobar si la lista está vacía y asignar 'not-biopsied' en ese caso
        if not valores_colpofind:
            valores_colpofind = 'not-biopsied'
        else:
            # Concatenar los valores en una cadena separada por " | "
            valores_colpofind = " | ".join(valores_colpofind)


        colpdxfile = fila_ginequito['COLP.DX'].values[0]

        # Inicializar una lista para almacenar los resultados
        colpdx = []

        # Comprobar si colpofind es una cadena antes de intentar dividirla
        if isinstance(colpdxfile, str):
            # Dividir la cadena usando el carácter "|"
            colpofind_opciones = colpdxfile.split(" | ")

            # Iterar sobre cada opción y asignar el valor correspondiente
            for opcion in colpofind_opciones:
                opcion_mayusculas = opcion.upper()
                # Utilizar el diccionario para obtener la traducción o 'none' si no hay traducción
                colpdx.append(traducciones_colpofind.get(opcion_mayusculas, opcion))

        # Comprobar si la lista está vacía y asignar 'not-biopsied' en ese caso
        if not colpdx:
            colpdx = 'not-biopsied'
        else:
            # Concatenar los valores en una cadena separada por " | "
            colpdx = " | ".join(colpdx)



        valorhistdx = []
        hist = fila_ginequito['HISTOPATH.DX'].values[0]

        # Comprobar si hist es una cadena antes de intentar dividirla
        if isinstance(hist, str):
            # Dividir la cadena usando el carácter "|"
            hist_opciones = hist.split(" | ")

            # Mapeo de opciones a traducciones en inglés
            opciones_mapping = {
                'CAMBIOS CITOPATICOS POR VPH': 'cytopathic changes associated with human papillomavirus',
                'LIBG (NIC-1)': 'lsil',
                'NEGATIVO PARA MALIGNIDAD': 'negative for malignancy',
                'ENDOCERVICITIS AGUDA': 'acute endocervicitis',
                'METAPLASIA ESCAMOSA MADURA': 'mature squamous metaplasia',
                'NA': 'not available',
                'CERVICITIS CRONICA': 'chronic cervicitis',
                'METAPLASIA ESCAMOSA INMADURA': 'immature squamous metaplasia',
                'EXTENSION GLANDULAR': 'glandular extension',
                'CONGESTION VASCULAR': 'vascular congestion',
                'LIEBG (NIC-1)': 'lsil',
                'POLIPO ENDOCERVICAL': 'endocervical polyp',
                'ENDOCERVICITIS PAPILAR': 'papillary endocervicitis',
                'ATROFIA': 'atrophy',
                'PERMEACION VASCULAR': 'vascular permeation',
                'CAMBIOS REACTIVOS': 'reactive changes',
                'FONDO MUCOIDE': 'mucoid background',
                'ADENOCARCINOMA ENDOCERVICAL (G2)': 'endocervical adenocarcinoma (G2)',
                'PATRON DE INVASION B': 'invasion pattern B'
            }

            # Iterar sobre cada opción y asignar el valor correspondiente
            valorhistdx = [opciones_mapping.get(opcion, 'none') for opcion in hist_opciones]

        # Comprobar si el arreglo está vacío y asignar 'na' en ese caso
        valorhistdx = " | ".join(valorhistdx) if valorhistdx else 'not-biopsied'

        # Obtener los valores de las columnas
        columnas = [
            'LBC.Tvaginalis',
            'LBC.Candida.spp',
            'LBC.BACTERIAL.VAGINOSIS',
            'LBC.Actinomyces.spp',
            'LBC.HERPES.VIRUX',
            'LBC.INFLAMMATION',
            'LBC.RADIATION.CELLULAR.CHANGES',
            'LBC.IUD.CELLULAR.CHANGES',
            'LBC.ATROPHY',
            'LBC.ASC-US',
            'LBC.ASC-H',
            'LBC.HPV.CELLULAR.CHANGES',
            'LBC.LSIL',
            'LBC.HSIL',
            'LBC.SQUAMOUS.CELL.CARCINOMA',
            'LBC.POSTMENOPAUSAL.BENIGN.ENDOMETRIAL.CELLS',
            'LBC.AGUS',
            'LBC.ENDOCERVICAL.ADENOCARCINOMA',
            'LBC.ENDOMETRIAL.ADENOCARCINOMA',
            'LBC.UNKNOWNPRIMARYSITE.ADENOCARCINOMA'
        ]

        # Crear el arreglo LBCOFIND
        LBCOFIND = []

        # Verificar si cada variable contiene las palabras clave
        for columna in columnas:
            valor = fila_ginequito[columna].values[0]
            if pd.notna(valor) and ('PRESENTES' in valor or 'presentes' in valor.lower()):
                LBCOFIND.append(columna.split('.')[-1].lower())

        # Utilizar el arreglo resultante
        LBCOFIND_resultado = " | ".join(LBCOFIND) if LBCOFIND else 'none'

        valorcopschil = ""



        # Inicializamos el arreglo para almacenar los valores encontrados en ambos arreglos
        lbcres = []
        # Iteramos sobre valoreslbcdx
        lbcres.extend(valoreslbcdx.split(" | "))
        # Iteramos sobre LBCOFIND_resultado
        lbcres.extend(LBCOFIND_resultado.split(" | "))
        # Convertimos lbcres a un conjunto para eliminar duplicados
        lbcres = set(lbcres)
        # Definimos los valores positivos a buscar
        valoreslbcPos = {'nic-1', 'nic-2', 'nic-3', 'nic-3 carcinoma in situ', 'microinvasive/invasive carcinoma',
                         'adenocarcinoma', 'unespecified malignancy', 'asc-us', 'asc-h', 'acis', 'agus', 'agc', 'lsil',
                         'hsil','asc-us of uncertain significance',
                          'asc-h of uncertain significance, cannot rule out high-grade lesion',
                          'atypical glandular cells of undetermined significance', 'asc-us', 'asc-us', 'asc-h', 'agus',
                          'lsil (nic-1)', 'hsil', 'dysplasia', 'mild dysplasia (nic-1)', 'moderate dysplasia (nic-2)',
                          'severe dysplasia (nic-3)', 'carcinoma', 'carcinoma in situ (nic-3)', 'cancer',
                          'microinvasive cancer', 'invasive cancer', 'adenocarcinoma',
                          'not otherwise specified malignancy', 'probable nic', 'probable dysplasia',
                          'probable carcinoma', 'probable adenocarcinoma', 'probable malignancy', 'discard nic',
                          'discard dysplasia', 'discard carcinoma', 'discard adenocarcinoma', 'discard malignancy'}


        # Comparamos los conjuntos
        if lbcres.intersection(valoreslbcPos):
            resultadolbcpos = "positive"
        else:
            resultadolbcpos = "negative"


        # Inicializamos el arreglo para almacenar los valores encontrados en ambos arreglos
        colpres = []
        # Iteramos sobre valoreslbcdx
        colpres.extend(valores_colpofind.split(" | "))
        colpres.extend(colpdx.split(" | "))
        # Iteramos sobre LBCOFIND_resultado
        #colpres.extend(valorcopothers.split(" | "))
        # Convertimos lbcres a un conjunto para eliminar duplicados
        colpres = set(colpres)
        # Definimos los valores positivos a buscar

        valorescolpPos = ['lsil (nic-1)', 'hsil', 'hsil (nic-2)', 'hsil (nic-3)', 'probable nic-1',
                          'probable nic-1 in endocervix', 'probable lsil (nic-1)', 'discard nic-1', 'discard nic',
                          'mild dysplasia (nic-1)', 'moderate dysplasia (nic-2)', 'severe dysplasia (nic-3)',
                          'carcinoma', 'carcinoma in situ (nic-3)', 'neoplasia', 'invasive neoplasia',
                          'intraepithelial lesion', 'squamous intraepithelial lesion','nic-1','nic-2','nic-3',
                          'nic-3 carcinoma in situ','invasive carcinoma','lsil','hsil','cin-2','discard cin','cin-1 endocervix','discard cin-1','probable cin-1 endocervix','probable cin-1','squamous metaplasia']

        # Comparamos los conjuntos
        if colpres.intersection(valorescolpPos):
            resultadocolps = "positive"
        else:
            resultadocolps = "negative"

        # Inicializamos el arreglo para almacenar los valores encontrados en ambos arreglos
        histres = []
        # Iteramos sobre LBCOFIND_resultado
        histres.extend(valorhistdx.split(" | "))
        # Convertimos lbcres a un conjunto para eliminar duplicados
        histres = set(histres)
        # Definimos los valores positivos a buscar
        valoreshistposdx = ['lsil','hsil','nic-1','nic-2','nic-3','mild dysplasia','moderate dysplasia','severe dysplasia',
                            'carcinoma in situ','carcinoma','cervical cancer','microinvasive carcinoma','invasive carcinoma',
                            'adenocarcinoma','endocervical adenocarcinoma','endometrial adenocarcinoma','unespecified malignancy',
                            'mature squamous metaplasia','immature squamous metaplasia','CIN 1','high-grade squamous intraepithelial lesion',
                            'low-grade squamous intraepithelial lesion','mild dysplasia','mature squamous metaplasia','immature squamous metaplasia',
                            'lsil (nic-1)', 'lsil (nic-1)', 'hsil', 'hsil', 'hsil (nic-2)', 'hsil (nic-3)',
                            'adenocarcinoma', 'endocervical adenocarcinoma', 'mild dysplasia (nic-1)',
                            'moderate dysplasia (nic-2)', 'severe dysplasia (nic-3)', 'carcinoma',
                            'carcinoma in situ (nic-3)', 'microinvasive cancer', 'invasive cancer', 'sarcoma',
                            'sarcoma and other tumors', 'unspecified malignancy'
                            ]



        # Comparamos los conjuntos
        if histres.intersection(valoreshistposdx):
            resultadohistpos = "positive"
        else:
            resultadohistpos = "negative"





        iddev = fila_ginequito['ID.DEVELLAB'].values[0]



    else:
        print(f"No se encontró información para ID.GINEQ: {id_gineq}")


    # Crear un diccionario con la información completa
    paciente_completo = {
            'ID': iddev,
            'AGE': edad,
            'BMI': bmi,
            'PREVENTIX': valorpreventix,
            'LBC': resultadolbcpos,
            'HPV.PCR': vph,
            'COLP': resultadocolps,
            'HISTOPATH': resultadohistpos,
            'p16': valorp16,
            'LBC.DX': valoreslbcdx,
            'LBC.OFIND': LBCOFIND_resultado,
            'HPV.PCR.GENOTYPE': hpvgen,
            'COLP.PERF': valorcolpperf,
            'COLP.CVXCN': valorcolpcv,
            'COLP.TZ': valorcopltz,
            'COLP.AWA.SURF': valorcoplawasurf,
            'COLP.AWA.BOR': valorcoplawabor,
            'COLP.SCHIL': schillvalue,
            'COLP.OFIND': valores_colpofind,
            'COLP.DX': colpdx,
            'BIOPSIED': valorbiosed,
            'HISTOPATH.DX': valorhistdx,
            'SMOKE': fumador,
            'SMOKE.QTY.WEEK': frecfum,
            'MENARCH': edadM,
            'AGE.SEX.DEBUT': edadS,
            'YEARS.SINCE.MENAR.TO.SEXDEBUT': edadSince,
            'NO.SEX.PARTN': parejas,
            'YEAR.OF.LAST.CITOL': fechaup,
            'YEARS.SINCE.LAST.CITOL': fechaap,
            'YEAR.OF.LAST.COLP': fechauc,
            'YEARS.SINCE.LAST.COLP': fechaac,
            'CONTRACEP.METH': mpf,
            'ABORT.TYPE': at,
            'ABORT.NUM': abn,
            'VAG.DEL': pn,
            'C.SECTION': cn,
            'AREA.TYPE': asentamiento,
            'TOWN.POV.LEVEL': rangopobreza
    }

    #     'COLP.CELLATR': row['COLP.CELLATR'],
    #     'COLP.INFCELCHAN': row['COLP.INFCELCHAN'],

    return paciente_completo

# Cargar los datos de los archivos CSV
df_cuestionarios = pd.read_csv('Cuestionarios-Ginequito-20231109.csv')
df_sepomex = pd.read_csv('CP-NL-SEPOMEX-2023.csv')
df_coneval = pd.read_csv('Rangos-pobreza-municipios-CONEVAL-2020.csv')
df_ginequito = pd.read_csv('GinequitoFinal.csv')

# Crear la lista para almacenar los resultados
pacientes_completa = []

# Recorrer cada fila en df_cuestionarios
for index, row in df_cuestionarios.iterrows():
    # Obtener la información completa y agregarla a la lista
    paciente_completo = obtener_informacion_completa(row, df_sepomex, df_coneval, df_ginequito)
    pacientes_completa.append(paciente_completo)

# Crear un DataFrame a partir de la lista completa
df_pacientes_completa = pd.DataFrame(pacientes_completa)

# Exportar el DataFrame a un archivo CSV
df_pacientes_completa.to_csv('CC-screen-women-NL.csv', index=False)
