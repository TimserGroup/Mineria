import pandas as pd
from datetime import datetime, timedelta
import re

def obtener_informacion_completa(row, df_sepomex, df_coneval, df_ginequito):
    # Obtener el valor de CP o H en df_cuestionarios
    valor_a_buscar = row['C.P.'] if 'C.P.' in row else row['H']



    # Buscar valor_a_buscar en df_sepomex['CP.ASENTAMIENTO']
    municipiobusqueda = 'Municipio no encontrado'
    asentamiento = 'Asentamiento no encontrado'
    for index, sepomex_row in df_sepomex.iterrows():
        #print(sepomex_row['CP.ASENTAMIENTO'])

        if sepomex_row['CP.ASENTAMIENTO'] == 'S/R':
            poblacionmun = 'No encontrado'
            rangopobreza = 'No encontrado'
        else:
            cpas = int(sepomex_row['CP.ASENTAMIENTO'])
            strcpas = str(cpas)
            municipiobusqueda = sepomex_row['MUNICIPIO']
            asentamiento = sepomex_row['ZONA.ASENTAMIENTO']

            if strcpas == valor_a_buscar:
                municipiobusqueda = sepomex_row['MUNICIPIO']
                break

    # Buscar municipiobusqueda en df_coneval['MUNICIPIO']
    poblacionmun = 'No encontrado'
    rangopobreza = 'No encontrado'
    for index, coneval_row in df_coneval.iterrows():

        if str(coneval_row['MUNICIPIO']) == municipiobusqueda:
            poblacionmun = str(coneval_row['POBLACION.ITER'])
            rang = str(coneval_row['RANGO.POBREZA'])
            #print("rang "+rang)
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







    if row['FECHA_NAC'] == 'S/R':
        edad = 'S/R'
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
    if row['TALLA'] == 'S/R' or row['PESO'] == 'S/R':
        bmi = 'No calc'
    else:
        talla = row['TALLA']
        tallai = float(talla)
        peso = float(row['PESO'])
        bmi = peso / (tallai ** 2)




    if row['FUMA'] == '1':
        fumador = "Yes"
        frecfum =  row['CANTIDAD_CIGARRILLOS'] +" "+ row['FRECUENCIA_FUMA']
    else:
        fumador = "No"
        cantidadfum ="N/A"
        frecfum = "N/A"
        
    if row['MENARCA'] == 'S/R':
        edadM = 'S/R'
    else:
        menarca_str = row['MENARCA']

        # Utilizar expresiones regulares para extraer la edad como número
        edad_match = re.search(r'(\d+)', menarca_str)

        # Verificar si se encontró una coincidencia y obtener el valor
        edadM = int(edad_match.group(1)) if edad_match else 0  # Puedes asignar un valor predeterminado si no se encuentra la edad

    if row['INICIO_VIDA_SEXUAL'] == 'S/R':
        edadS = 'S/R'
        edadSince = 'S/R'
    else:
        sexual_str = row['INICIO_VIDA_SEXUAL']
        #print(sexual_str)
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
        parejas = 'na'


    if row['FECHA_HORA_TOMA'] == 'S/R':
        fechaup = 'na'
        fechaap = 'na'
        fechaac = 'na'
        fechauc = 'na'
    else:
        fecha_toma_str = row['FECHA_HORA_TOMA'].split()[0]  # Obtener la parte de la fecha, ignorando la hora
        fecha_toma = datetime.strptime(fecha_toma_str, '%d/%m/%Y')
        if row['FECHA_ULTIMO_PAPANICOLAOU'] == 'S/R' or row['FECHA_ULTIMO_PAPANICOLAOU'] == 'NUNCA':
            fechaup = 'na'
            fechaap = 'na'
        elif len(row['FECHA_ULTIMO_PAPANICOLAOU']) == 4:
            intpap = int(row['FECHA_ULTIMO_PAPANICOLAOU'])
            fechaap = fecha_toma.year - intpap
            fechaup = intpap
        else:
            # print(row['FECHA_ULTIMO_PAPANICOLAOU'])
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


        if row['FECHA_ULTIMA_COLPOSCOPIA'] == 'S/R' or row['FECHA_ULTIMA_COLPOSCOPIA'] == 'NUNCA':
            fechauc = 'na'
            fechaac = 'na'
        elif len(row['FECHA_ULTIMA_COLPOSCOPIA']) == 4:
            intpap = int(row['FECHA_ULTIMA_COLPOSCOPIA'])

            fechaac = fecha_toma.year - intpap

            fechauc = intpap
        else:
            # print(row['FECHA_ULTIMA_COLPOSCOPIA'])
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

    if row['METODO_PLANIFICACION_FAMILIAR'] == 'S/R':
        #print("S/R")
        mpf = 'na'
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
            mpf= "error"

    # if row['METODO_PLANIFICACION_FAMILIAR'] == 'S/R':
    #     print()
    # row['ABORTO']



    if row['ABORTO'] == 'S/R':
        #print("S/R")
        at = 'na'
        abn = 'na'
    else:
        # Dividir la cadena usando el carácter "|"
        partes = row['ABORTO'].split(" | ")

        if len(partes) >= 3:
            variable1 = partes[0]
            if variable1 == '1':
                at1 = "Legrado"
            elif variable1 == '2':
                at1 = "Inducido"
            elif variable1 == '3':
                at1 = "Espontaneo"
            elif variable1 == '4':
                at1 = "Ninguno"
            elif variable1 == '5 (EMBARAZO ECTOPICO)':
                at1 = "Embarazo ectopico"

            variable2 = partes[1]
            if variable2 == '1':
                at2 = "Legrado"
            elif variable2 == '2':
                at2 = "Inducido"
            elif variable2 == '3':
                at2 = "Espontaneo"
            elif variable2 == '4':
                at2 = "Ninguno"
            elif variable2 == '5 (EMBARAZO ECTOPICO)':
                at2 = "Embarazo ectopico"

            variable3 = partes[2]
            if variable3 == '1':
                at3 = "Legrado"
            elif variable3 == '2':
                at3 = "Inducido"
            elif variable3 == '3':
                at3 = "Espontaneo"
            elif variable3 == '4':
                at3 = "Ninguno"
            elif variable3 == '5 (EMBARAZO ECTOPICO)':
                at3 = "Embarazo ectopico"

            at = at1 + " | " + at2 + " | " + at3
            abn = len(partes)
        elif len(partes) == 2:
            # Manejar el caso en el que solo hay dos partes
            variable1 = partes[0]
            if variable1 == '1':
                at1 = "Legrado"
            elif variable1 == '2':
                at1 = "Inducido"
            elif variable1 == '3':
                at1 = "Espontaneo"
            elif variable1 == '4':
                at1 = "Ninguno"
            elif variable1 == '5 (EMBARAZO ECTOPICO)':
                at1 = "Embarazo ectopico"

            variable2 = partes[1]
            if variable2 == '1':
                at2 = "Legrado"
            elif variable2 == '2':
                at2 = "Inducido"
            elif variable2 == '3':
                at2 = "Espontaneo"
            elif variable2 == '4':
                at2 = "Ninguno"
            elif variable2 == '5 (EMBARAZO ECTOPICO)':
                at2 = "Embarazo ectopico"

            at = at1 + " | " + at2
            abn = len(partes)
        else:
            # Manejar el caso en el que hay menos de dos partes
            variable1 = partes[0] if len(partes) >= 1 else 'Ninguno'
            if variable1 == '1':
                at1 = "curettage"
                abn = len(partes)
            elif variable1 == '2':
                at1 = "induced"
                abn = len(partes)
            elif variable1 == '3':
                at1 = "spontaneous"
                abn = len(partes)
            elif variable1 == '4':
                at1 = "none"
                abn = 0
            elif variable1 == '5 (EMBARAZO ECTOPICO)':
                at1 = "ectopic pregnancy"
                abn = len(partes)

            at = at1


    if row['PARTO'] == 'S/R':
        pn = 'na'
    else:
        pn = int(row['PARTO'])

    if row['CESÁREA'] == 'S/R':
        cn = 'na'
    else:
        cn = int(row['CESÁREA'])




    id_gineq = row['ID_GINEQ']

    # Filtrar df_ginequito para obtener solo la fila que cumple con la condición
    fila_ginequito = df_ginequito[df_ginequito['ID_GINEQ'] == id_gineq]

    # Acceder a los campos específicos de la fila obtenida
    if not fila_ginequito.empty:
        valorpreventix = ""
        valorp16 = ""
        vph = ""
        vptx = fila_ginequito['preventix'].values[0]
        if vptx == 'positivo':
            valorpreventix = 'positive'
        elif vptx == 'negativo':
            valorpreventix = 'negative'
        else:
            valorpreventix = 'na'


        vp16 = fila_ginequito['p16'].values[0]
        if vptx == 'positivo':
            valorp16 = 'positive'
        elif vp16 == 'negativo':
            valorp16 = 'negative'
        elif vp16 == 'nr':
            valorp16 = 'not biopsed'
        else:
            valorp16 = 'na'

        vphv = fila_ginequito['vph2'].values[0]
        if vphv == 'positivo':
            vph = 'positive'
        elif vphv == 'negativo':
            vph = 'negative'
        elif vp16 == 's/r':
            vph = 'na'
        else:
            vph = 'na'

        hpvgen = ""
        genvph = fila_ginequito['HPV.PCR.GENOTYPE'].values[0]
        if genvph == 'pool':
            hpvgen = 'hpv-pool'
        elif genvph == '18':
            hpvgen = 'hpv-18'
        elif genvph == '16':
            hpvgen = 'hpv-16'
        else:
            hpvgen ='na'

        valorcolpos = ""
        colpperf = fila_ginequito['COLP.PERF'].values[0]
        if colpperf == 'adecuada':
            valorcolpos = 'adequate'
        elif colpperf == 'no adecuada':
            valorcolpos = 'inadequate'
        elif colpperf == 'na':
            valorcolpos = 'na'
        else:
            valorcolpos = 'na'

        valorcolpcv = ""
        colpcv = fila_ginequito['COLP.CVXCN'].values[0]
        if colpcv == 'atrofico':
            valorcolpcv = 'atrophy'
        elif colpcv == 'hipertrofico':
            valorcolpcv = 'hypertrophy'
        elif colpcv == 'eutrofico':
            valorcolpcv = 'eutrophy'
        elif colpcv == 'no aplica':
            valorcolpcv = 'na'
        else:
            valorcolpcv = 'na'

        valorcopltz = ""
        colptz = fila_ginequito['COLP.TZ'].values[0]
        if colptz == '1':
            valorcopltz = 't1'
        elif colptz == '2':
            valorcopltz = 't2'
        elif colptz == '3':
            valorcopltz = 't3'
        elif colptz == 'normal':
            valorcopltz = 'normal'
        else:
            valorcopltz = 'na'


        valorcoplawasurf = ""
        colpawasurf = fila_ginequito['COLP.AWA.SURF'].values[0]
        if colpawasurf == 'lisa':
            valorcoplawasurf = 'smooth'
        elif colpawasurf == 'macropapilar':
            valorcoplawasurf = 'micropapillar'
        elif colpawasurf == 'mosaico fino':
            valorcoplawasurf = 'fine mosaic'
        elif colpawasurf == 'mosaico grueso':
            valorcoplawasurf = 'coarse mosaic'
        elif colpawasurf == 'puntilleo grueso':
            valorcoplawasurf = 'coarse punctation'
        elif colpawasurf == 'puntilleo fino':
            valorcoplawasurf = 'fine punctation'
        else:
            valorcoplawasurf = 'na'


        valorcoplawa = ""
        # colpawa = fila_ginequito['COLP.AWA'].values[0]
        # if colpawa == 'lisa':
        #     valorcoplawa = 'absent'
        # elif colpawa == 'macropapilar':
        #     valorcoplawa = 'fine'
        # elif colpawa == 'mosaico fino':
        #     valorcoplawa = 'coarse'
        # elif colpawa == 'mosaico grueso':
        #     valorcoplawa = 'rawa'
        #
        # else:
        #     valorcoplawa = 'na'

        valorcoplawabor = ""
        colpawabor = fila_ginequito['COLP.AWA.BOR'].values[0]
        if colpawabor == 'definidos':
            valorcoplawabor = 'defined'
        elif colpawabor == 'sin relieve':
            valorcoplawabor = 'wo-ridge'
        elif colpawabor == 'difusos':
            valorcoplawabor = 'undefined'
        elif colpawabor == 'con relieve':
            valorcoplawabor = 'ridge'
        else:
            valorcoplawabor = 'na'

        valorbiosed = ""
        biopsed = fila_ginequito['BIOPSIED'].values[0]
        if biopsed == 'si':
            valorbiosed = 'no'
        elif biopsed == 'no':
            valorbiosed = 'yes'
        else:
            valorbiosed = 'na'

        valorcolpperf = ""
        colpperf = fila_ginequito['COLP.PERF'].values[0]
        if colpperf == 'adecuada':
            valorcolpperf = 'adequate'
        elif colpperf == 'no adecuada':
            valorcolpperf = 'inadequate'
        elif colpperf == 'na':
            valorcolpperf = 'na'
        else:
            valorcolpperf = 'na'

        valoreslbcdx = []
        lbcdx = fila_ginequito['LBC.DX'].values[0]

        # Comprobar si lbcdx es una cadena antes de intentar dividirla
        if isinstance(lbcdx, str):
            # Dividir la cadena usando el carácter "|"
            lbcdx_opciones = lbcdx.split(" | ")

            # Iterar sobre cada opción y asignar el valor correspondiente
            for opcion in lbcdx_opciones:
                if opcion == 'alteraciones inflamatorias leves':
                    valoreslbcdx.append('mild inflammation')
                elif opcion == 'alteraciones inflamatorias moderadas':
                    valoreslbcdx.append('moderate inflammation')
                elif opcion == 'alteraciones inflamatorias severas':
                    valoreslbcdx.append('severe inflammation')
                elif opcion == 'atipia de celulas escamosas (asc-us) de significado incierto':
                    valoreslbcdx.append('asc-us')
                elif opcion == 'lesion intraepitelial escamosa de bajo grado (displasia leve)':
                    valoreslbcdx.append('lsil')
                elif opcion == 'cambio de la flora vaginal por flora coco-bacilar':
                    valoreslbcdx.append('bacterial vaginosis')
                elif opcion == 'imagen de atrofia celular':
                    valoreslbcdx.append('cellular atrophy')
                elif opcion == 'cambios citopaticos sugestivos de infeccion por virus del papiloma humano':
                    valoreslbcdx.append('suggestive hpv celular change')
                elif opcion == 'cambio de la flora vaginal sugestivo de vaginosis bacteriana':
                    valoreslbcdx.append('bacterial vaginosis')
                else:
                    valoreslbcdx.append('na')

        # Comprobar si el arreglo está vacío y asignar 'na' en ese caso
        if not valoreslbcdx:
            valoreslbcdx = 'na'
        else:
            # Concatenar los valores en una cadena separada por " | "
            valoreslbcdx = " | ".join(valoreslbcdx)



        valorescolpofind = []
        colpofind = fila_ginequito['COLP.OFIND'].values[0]

        # Comprobar si lbcdx es una cadena antes de intentar dividirla
        if isinstance(colpofind, str):
            # Dividir la cadena usando el carácter "|"
            colpofind_opciones = colpofind.split(" | ")

            # Iterar sobre cada opción y asignar el valor correspondiente
            for opcion in colpofind_opciones:
                if opcion == 'alteraciones inflamatorias':
                    valorescolpofind.append('inflamation')
                elif opcion == 'atrofia severa':
                    valorescolpofind.append('severe atrophy')
                elif opcion == 'condilomatosis':
                    valorescolpofind.append('condylomatosis')
                elif opcion == 'descartar nic 1':
                    valorescolpofind.append('probable cin-1')
                elif opcion == 'nic 1':
                    valorescolpofind.append('cin-1')
                elif opcion == 'liag':
                    valorescolpofind.append('hsil')
                elif opcion == 'libg':
                    valorescolpofind.append('lsil')
                elif opcion == 'nic-2':
                    valorescolpofind.append('cin-2')
                elif opcion == 'metaplasia escamosa':
                    valorescolpofind.append('squamous metaplasia')
                elif opcion == 'polipo cervical':
                    valorescolpofind.append('polyp')
                elif opcion == 'sin alteraciones':
                    valorescolpofind.append('none')
                else:
                    valorescolpofind.append('na')

        # Comprobar si el arreglo está vacío y asignar 'na' en ese caso
        if not valorescolpofind:
            valorescolpofind = 'na'
        else:
            # Concatenar los valores en una cadena separada por " | "
            valorescolpofind = " | ".join(valorescolpofind)

        valorcopothers = []
        colpoothers = fila_ginequito['COLP.Others'].values[0]

        # Comprobar si colpoothers es una cadena antes de intentar dividirla
        if isinstance(colpoothers, str):
            # Dividir la cadena usando el carácter "|"
            colpoothers_opciones = colpoothers.split(" | ")


            # Iterar sobre cada opción y asignar el valor correspondiente
            # Iteramos sobre colpoothers_opciones
            for opcion in colpoothers_opciones:
                if opcion == 'atrofia':
                    valorcopothers.append('atrophy')
                elif opcion == 'atrofia severa':
                    valorcopothers.append('severe atrophy')
                elif opcion == 'vaginitis':
                    valorcopothers.append('vaginitis')
                elif opcion == 'atrofia vaginal':
                    valorcopothers.append('vaginal atrophy')
                elif opcion == 'atrofia vaginal moderada':
                    valorcopothers.append('moderate vaginal atrophy')
                elif opcion == 'atrofia vaginal severa':
                    valorcopothers.append('severe vaginal atrophy')
                elif opcion == 'liquen escleroso':
                    valorcopothers.append('lichen sclerosus')
                elif opcion == 'descartar nic':
                    valorcopothers.append('discard cin')
                elif opcion == 'eversion glandular':
                    valorcopothers.append('glandular eversion')
                elif opcion == 'cervicovaginitis':
                    valorcopothers.append('cervicovaginitis')
                elif opcion == 'lesion acetoblanca':
                    valorcopothers.append('acetowhite lesion')
                elif opcion == 'liquen escleroso':
                    valorcopothers.append('lichen sclerosus')
                elif opcion == 'metaplasia escamosa':
                    valorcopothers.append('squamous metaplasia')
                elif opcion == 'molusco contagioso':
                    valorcopothers.append('contagious mollusk')
                elif opcion == 'ninguna':
                    valorcopothers.append('none')
                elif opcion == 'polipo cervical':
                    valorcopothers.append('cervical polyp')
                elif opcion == 'atrofia vaginal':
                    valorcopothers.append('vaginal atrophy')
                elif opcion == 'quiste de naboth':
                    valorcopothers.append('nabothian cyst')
                elif opcion == 'vaginitis':
                    valorcopothers.append('vaginitis')
                else:
                    valorcopothers.append('na')

        # Comprobar si el arreglo está vacío y asignar 'na' en ese caso
        if not valorcopothers:
            valorcopothers = 'na'
        else:
            # Concatenar los valores en una cadena separada por " | "
            valorcopothers = " | ".join(valorcopothers)

        valorcolpdx = valorcopothers + " | " + valorescolpofind

        # Verifica si alguno de los dos valores es 'na' para asignar 'na' a valorcolpdx en ese caso
        if 'na' in valorcopothers or 'na' in valorescolpofind:
            valorcolpdx = 'na'



        valorhistdx = []
        hist = fila_ginequito['HISTOPATH.DX'].values[0]

        # Comprobar si hist es una cadena antes de intentar dividirla
        if isinstance(hist, str):
            # Dividir la cadena usando el carácter "|"
            hist_opciones = hist.split(" | ")

            # Iterar sobre cada opción y asignar el valor correspondiente
            # Iteramos sobre hist_opciones
            for opcion in hist_opciones:
                if opcion == 'atrofia':
                    valorhistdx.append('atrophy')
                elif opcion == 'atrofia severa':
                    valorhistdx.append('severe atrophy')
                elif opcion == 'vaginitis':
                    valorhistdx.append('vaginitis')
                elif opcion == 'atrofia vaginal':
                    valorhistdx.append('vaginal atrophy')
                elif opcion == 'atrofia vaginal moderada':
                    valorhistdx.append('moderate vaginal atrophy')
                elif opcion == 'atrofia vaginal severa':
                    valorhistdx.append('severe vaginal atrophy')
                elif opcion == 'alteraciones inflamatorias leves':
                    valorhistdx.append('mild inflammatory changes')
                elif opcion == 'cambios citopaticos asociados a infeccion por el virus del papiloma humano':
                    valorhistdx.append('cytopathic changes associated with human papillomavirus infection')
                elif opcion == 'cervicitis cronica con hiperplasia microglandular':
                    valorhistdx.append('chronic cervicitis with microglandular hyperplasia')
                elif opcion == 'cervicitis cronica con metaplasia escamosa':
                    valorhistdx.append('chronic cervicitis with squamous metaplasia')
                elif opcion == 'negativo para displasia o malignidad':
                    valorhistdx.append('negative for dysplasia or malignancy')
                elif opcion == 'negativo para lesion o malignidad':
                    valorhistdx.append('negative for lesion or malignancy')
                elif opcion == 'negativo para malignidad':
                    valorhistdx.append('negative for malignancy')
                elif opcion == 'congestion vascular':
                    valorhistdx.append('vascular congestion')
                elif opcion == 'displasia leve':
                    valorhistdx.append('mild dysplasia')
                elif opcion == 'endocervicitis aguda':
                    valorhistdx.append('acute endocervicitis')
                elif opcion == 'extension glandular':
                    valorhistdx.append('glandular extension')
                elif opcion == 'lesion escamosa intraepitelial de bajo grado':
                    valorhistdx.append('low-grade squamous intraepithelial lesion')
                elif opcion == 'lesion intraepitelial escamosa de alto grado':
                    valorhistdx.append('high-grade squamous intraepithelial lesion')
                elif opcion == 'metaplasia escamosa inmadura':
                    valorhistdx.append('immature squamous metaplasia')
                elif opcion == 'metaplasia escamosa madura':
                    valorhistdx.append('mature squamous metaplasia')
                elif opcion == 'neoplasia intraepitelial vaginal de bajo grado (vain 1)':
                    valorhistdx.append('vaginal low-grade intraepithelial neoplasia (VAIN 1)')
                elif opcion == 'nic 1':
                    valorhistdx.append('CIN 1')
                elif opcion == 'polipo de tipo fibroso':
                    valorhistdx.append('fibrous-type polyp')
                elif opcion == 'proceso inflamatorio agudo':
                    valorhistdx.append('acute inflammatory process')
                else:
                    valorhistdx.append('na')

        # Comprobar si el arreglo está vacío y asignar 'na' en ese caso
        if not valorhistdx:
            valorhistdx = 'na'
        else:
            # Concatenar los valores en una cadena separada por " | "
            valorhistdx = " | ".join(valorhistdx)

        # print(valorhistdx)



        # Obtener los valores de las columnas
        tv = fila_ginequito['T.vaginalis'].values[0]
        Candidaspp = fila_ginequito['Candida spp'].values[0]
        bacvag = fila_ginequito['bacterial vaginosis'].values[0]
        acspp = fila_ginequito['Actinomyces spp'].values[0]
        herpesvirux = fila_ginequito['herpes virux'].values[0]

        # Crear el arreglo LBCOFIND
        LBCOFIND = []

        # Verificar si cada variable contiene las palabras clave
        if pd.notna(tv) and ('presente' in tv or 'presentes' in tv.lower()):
            LBCOFIND.append('T.vaginalis')

        if pd.notna(Candidaspp) and ('presente' in Candidaspp or 'presentes' in Candidaspp.lower()):
            LBCOFIND.append('Candida spp')

        if pd.notna(bacvag) and ('presente' in bacvag or 'presentes' in bacvag.lower()):
            LBCOFIND.append('bacterial vaginosis')

        if pd.notna(acspp) and ('presente' in acspp or 'presentes' in acspp.lower()):
            LBCOFIND.append('Actinomyces spp')

        if pd.notna(herpesvirux) and ('presente' in herpesvirux or 'presentes' in herpesvirux.lower()):
            LBCOFIND.append('herpes virux')

        # Utilizar el arreglo resultante
        if len(LBCOFIND) == 0:
            LBCOFIND_resultado = 'na'
        else:
            LBCOFIND_resultado = " | ".join(LBCOFIND)








        valorcopschil = ""
        colpschil = fila_ginequito['COLP.SCHIL'].values[0]
        if colpschil == 'positivo':
            valorcopschil = 'positive'
        elif colpschil == 'negativo':
            valorcopschil = 'negative'
        else:
            valorcopschil = 'na'




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
                         'hsil'}
        # Comparamos los conjuntos
        if lbcres.intersection(valoreslbcPos):
            resultadolbcpos = "positive"
        else:
            resultadolbcpos = "false"


        # Inicializamos el arreglo para almacenar los valores encontrados en ambos arreglos
        colpres = []
        # Iteramos sobre valoreslbcdx
        colpres.extend(valorescolpofind.split(" | "))
        # Iteramos sobre LBCOFIND_resultado
        colpres.extend(valorcopothers.split(" | "))
        # Convertimos lbcres a un conjunto para eliminar duplicados
        colpres = set(colpres)
        # Definimos los valores positivos a buscar
        valorescolpPos = ['nic-1','nic-2','nic-3','nic-3 carcinoma in situ','invasive carcinoma','lsil','hsil','cin-2','discard cin','probable cin-1','squamous metaplasia']
        # Comparamos los conjuntos
        if colpres.intersection(valorescolpPos):
            resultadocolps = "positive"
        else:
            resultadocolps = "false"





        # Inicializamos el arreglo para almacenar los valores encontrados en ambos arreglos
        histres = []

        # Iteramos sobre LBCOFIND_resultado
        histres.extend(valorhistdx.split(" | "))
        # Convertimos lbcres a un conjunto para eliminar duplicados
        histres = set(histres)
        # Definimos los valores positivos a buscar
        valoreshistposdx = ['lsil','hsil','nic-1','nic-2','nic-3','mild dysplasia','moderate dysplasia','severe dysplasia','carcinoma in situ','carcinoma','cervical cancer','microinvasive carcinoma','invasive carcinoma','adenocarcinoma','endocervical adenocarcinoma','endometrial adenocarcinoma','unespecified malignancy','mature squamous metaplasia','immature squamous metaplasia','CIN 1','high-grade squamous intraepithelial lesion','low-grade squamous intraepithelial lesion','mild dysplasia','mature squamous metaplasia','immature squamous metaplasia','vaginal low-grade intraepithelial neoplasia (VAIN 1)']
        # Comparamos los conjuntos
        if histres.intersection(valoreshistposdx):
            resultadohistpos = "positive"
        else:
            resultadohistpos = "false"





    else:
        print(f"No se encontró información para ID_GINEQ: {id_gineq}")





    # Crear un diccionario con la información completa
    paciente_completo = {
            'ID': row['ID_DEVELLAB'],
            'ID': row['ID_GINEQ'],
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
            'COLP.DX': valorcolpdx,
            'COLP.PERF': valorcolpperf,
            'COLP.CVXCN': colpcv,
            'COLP.TZ': valorcopltz,
            'COLP.AWA.SURF': valorcoplawasurf,
            'COLP.AWA.BOR': valorcoplawabor,
            'COLP.SCHIL': valorcopschil,
            'COLP.OFIND': valorescolpofind,
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


    # paciente_completo = {
    #     'ID': row['ID_DEVELLAB'],
    #     'ID': row['ID_GINEQ'],
    #     'AGE': edad,
    #     'BMI': bmi,
    #     'PREVENTIX': valorpreventix,
    #     'LBC': resultadolbcpos,
    #     'HPV.PCR': vph,
    #     'COLP': resultadocolps,
    #     'HISTOPATH': resultadohistpos,
    #     'p16': valorp16,
    #     'LBC.DX': valoreslbcdx,
    #     'LBC.OFIND': LBCOFIND_resultado,
    #     'HPV.PCR.GENOTYPE': hpvgen,
    #     'COLP.DX': valorcolpdx,
    #     'COLP.PERF': valorcolpperf,
    #     'COLP.CVXCN': colpcv,
    #     'COLP.TZ': valorcopltz,
    #     'COLP.AWA.SURF': valorcoplawasurf,
    #     'COLP.AWA.BOR': valorcoplawabor,
    #     'COLP.SCHIL': valorcopschil,
    #     'COLP.OFIND': valorescolpofind,
    #     'COLP.CELLATR': row['COLP.CELLATR'],
    #     'COLP.INFCELCHAN': row['COLP.INFCELCHAN'],
    #     'BIOPSIED': valorbiosed,
    #     'HISTOPATH.DX': valorhistdx,
    #     'SMOKE': fumador,
    #     'SMOKE.QTY.WEEK': frecfum,
    #     'MENARCH': edadM,
    #     'AGE.SEX.DEBUT': edadS,
    #     'YEARS.SINCE.MENAR.TO.SEXDEBUT': edadSince,
    #     'NO.SEX.PARTN': parejas,
    #     'YEAR.OF.LAST.CITOL': fechaup,
    #     'YEARS.SINCE.LAST.CITOL': fechaap,
#         'YEAR.OF.LAST.COLP': fechauc,
#         'YEARS.SINCE.LAST.COLP': fechaac,
    #     'CONTRACEP.METH': mpf,
    #     'ABORT.TYPE': at,
    #     'ABORT.NUM': abn,
    #     'VAG.DEL': pn,
    #     'C.SECTION': cn,
    #     'AREA.TYPE': asentamiento,
    #     'TOWN.POV.LEVEL': rangopobreza
    # }



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
