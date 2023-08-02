# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

import operator
from datetime import date, datetime

class SupportoServizioElaborato:

    @staticmethod
    def trovaValore(valoreEnv, tipoComponente, codiceComponente, dizionarioContratto, consumoAnnuoPresunto = None, dataInizioValidita = None, dataFineValidita = None, \
                    valoreMinimoColonna=None, valoreMassimoColonna = None, datePrecise = False):

        ops = { "<": operator.lt,
                "<=": operator.le,
                "=": operator.eq,
                ">": operator.gt,
                ">=": operator.ge
            }

        dominioRicercaValore = []
        uso = None
        tensione = None
        valoreTrovato = None
        dictValore = {}
        potenza_contrattuale = None
        potenza_disponibile = None

        dominioRicercaValore.append(('tabella_id.componente_id.tipo_componente_id.tipo', '=', tipoComponente))
        dominioRicercaValore.append(('tabella_id.componente_id.codice', '=', codiceComponente))

        if dizionarioContratto is not None:
            if dizionarioContratto.has_key('uso'):
                uso = dizionarioContratto['uso']
                dominioRicercaValore.append(('riga_id.tipo_uso_id.etichetta', '=', uso))
            if dizionarioContratto.has_key('tensione'):
                tensione = dizionarioContratto['tensione']
                dominioRicercaValore.append(('riga_id.tipo_tensione_id.etichetta', '=', tensione))
            if dizionarioContratto.has_key('potenza_contrattuale'):
                potenza_contrattuale = dizionarioContratto['potenza_contrattuale']
            if dizionarioContratto.has_key('potenza_disponibile'):
                potenza_disponibile = dizionarioContratto['potenza_disponibile']

        if (dataInizioValidita is not None or dataFineValidita is not None) and datePrecise:
            if dataInizioValidita is not None:
                dominioRicercaValore.append(('data_inizio_validita', '=', dataInizioValidita))
            if dataFineValidita is not None:
                dominioRicercaValore.append(('data_fine_validita', '=', dataFineValidita))


        if valoreMinimoColonna is not None:
            dominioRicercaValore.append(('regola_colonna_id.valore_minimo', '=', valoreMinimoColonna))

        if valoreMassimoColonna is not None:
            dominioRicercaValore.append(('regola_colonna_id.valore_massimo', '=', valoreMassimoColonna))


        valore_list = valoreEnv.search(dominioRicercaValore)
        idTrovati = []

        if (dataInizioValidita is not None or dataFineValidita is not None) and datePrecise == False:

            for val in valore_list:

                if dataInizioValidita is not None:
                    if not (isinstance(dataInizioValidita, date)):
                        dataInizioValidita = datetime.strptime(dataInizioValidita, '%Y-%m-%d').date()

                    if dataInizioValidita >= datetime.strptime(val.data_inizio_validita, '%Y-%m-%d').date():

                        if dataFineValidita is not None:

                            if not (isinstance(dataFineValidita, date)):
                                dataFineValidita = datetime.strptime(dataFineValidita, '%Y-%m-%d').date()

                            if dataFineValidita <= datetime.strptime(val.data_fine_validita, '%Y-%m-%d').date():
                                idTrovati.append(val.id)

        if len(idTrovati) > 0:
            valore_list = valoreEnv.search([('id', 'in', idTrovati)])


                    #dominioRicercaValore.append( (('data_fine_validita', '>=', dataFineValidita[:10]), '&', ('data_inizio_validita', '<=', dataInizioValidita[:10])))
                    # elif dataInizioValidita is None and dataFineValidita is not None and datePrecise == False:
                    #     dominioRicercaValore.append( ('data_fine_validita', '>=', dataFineValidita[:10]))
                    #
                    # elif dataInizioValidita is not None and dataFineValidita is None and datePrecise == False:
                    #     dominioRicercaValore.append( ('data_inizio_validita', '<=', dataInizioValidita[:10]))



        for val in valore_list:
            if val.riga_id.consumo_annuo_limite_inferiore is not False and val.riga_id.consumo_annuo_limite_superiore is False:
                # Confronto solo con il limite inferiore
                if ops[ (val.riga_id.operatore_consumo_annuo_limite_inferiore).encode('utf-8')] (consumoAnnuoPresunto, int(val.riga_id.consumo_annuo_limite_inferiore)):
                    # Ho trovato corrispondenza con il consumo annuale
                    if val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )) \
                            and ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is False:
                        if val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )) \
                                and ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is False:
                            return val

            elif val.riga_id.consumo_annuo_limite_superiore is not False and val.riga_id.consumo_annuo_limite_inferiore is False:
                # Confronto solo con il limite superiore
                if ops[ (val.riga_id.operatore_consumo_annuo_limite_superiore).encode('utf-8')] (consumoAnnuoPresunto, int(val.riga_id.consumo_annuo_limite_superiore )):
                    # Trovata corrispondenza con il consumo annuale
                    if val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )) \
                            and ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
            elif val.riga_id.consumo_annuo_limite_superiore is not False and val.riga_id.consumo_annuo_limite_inferiore is not False:
                    # Confronto entrambi i valori
                if ops[ (val.riga_id.operatore_consumo_annuo_limite_superiore).encode('utf-8')] (consumoAnnuoPresunto, int(val.riga_id.consumo_annuo_limite_superiore )) \
                    and ops[ (val.riga_id.operatore_consumo_annuo_limite_inferiore).encode('utf-8')] (consumoAnnuoPresunto, int(val.riga_id.consumo_annuo_limite_inferiore )):
                    # Trovata corrispondenza con il consumo annuale
                    if val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )) \
                            and ops[ str(val.riga_id.operatore_potenza_impegnata_limite_inferiore)] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza impegnata  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is False:
                        # non dovrebbe più esserci niente da verificare
                        return val
            elif val.riga_id.consumo_annuo_limite_inferiore is  False and val.riga_id.consumo_annuo_limite_superiore is False:
                if val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is False:
                    if ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                        if val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )) \
                                and ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is False:
                            return val

                elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                    if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )):

                        if val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                            if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )) \
                                and ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                return val
                        elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is False:
                            return val

                elif val.riga_id.potenza_impegnata_limite_inferiore is not False and val.riga_id.potenza_impegnata_limite_superiore is not False:
                    if ops[ (val.riga_id.operatore_potenza_impegnata_limite_superiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_superiore )) \
                        and ops[ (val.riga_id.operatore_potenza_impegnata_limite_inferiore).encode('utf-8')] (float(potenza_contrattuale), float(val.riga_id.potenza_impegnata_limite_inferiore )):
                            if val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is False:
                                if ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                    # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                    return val
                            elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                                if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )):
                                    # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                    return val
                            elif val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                                if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )) \
                                    and ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                                    # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                                    return val
                            elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is False:
                                return val
                elif val.riga_id.potenza_impegnata_limite_inferiore is False and val.riga_id.potenza_impegnata_limite_superiore is False:
                    if val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is False:
                        if ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )):
                            # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_disponibile_limite_inferiore is not False and val.riga_id.potenza_disponibile_limite_superiore is not False:
                        if ops[ (val.riga_id.operatore_potenza_disponibile_limite_superiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_superiore )) \
                            and ops[ (val.riga_id.operatore_potenza_disponibile_limite_inferiore).encode('utf-8')] (float(potenza_disponibile), float(val.riga_id.potenza_disponibile_limite_inferiore )):
                            # Trovata corrispondenza anche con la potenza disponibile  - PER ORA MI FERMO E PRENDO IL VALORE
                            return val
                    elif val.riga_id.potenza_disponibile_limite_inferiore is False and val.riga_id.potenza_disponibile_limite_superiore is False:
                        return val

        return None


#TODO sicuramente manca ancora qualcosa ai filtri applicati al valore

    @staticmethod
    def getAcciseDict(use, potenzaContrattuale, kwhMese):

        class RATE:
            PRIVATE = 0.0227
            BUSINESS_NORMAL = 0.0125
            BUSINESS_LOW = 0.0075
            PUBLIC = BUSINESS_NORMAL

        dictAccise = []
        if use == 'dnr':
            dictAccise = {'corrUnitario': RATE.PRIVATE, 'kwh': kwhMese, 'imponibile': kwhMese * RATE.PRIVATE}
            return dictAccise

        elif use == 'ip':
            dictAccise = {'corrUnitario': RATE.PUBLIC, 'kwh': kwhMese, 'imponibile': kwhMese * RATE.PUBLIC}
            return dictAccise

        elif use == 'dr':
            if potenzaContrattuale <= 1.5:
                if kwhMese <= 150:
                    exemption = kwhMese
                else:
                    exemption = max(150 - (kwhMese-150), 0)

            elif 1.5 < potenzaContrattuale <= 3:
                if kwhMese <= 150:
                    exemption = kwhMese
                elif 150 < kwhMese <= 220:
                    exemption = 150
                elif kwhMese > 220:
                    exemption = max(150 - (kwhMese-220), 0)

            elif potenzaContrattuale > 3:
                exemption = 0

            dictAccise = {'corrUnitario': RATE.PRIVATE, 'kwh': (kwhMese - exemption), 'imponibile': (kwhMese - exemption) * RATE.PRIVATE}
            return dictAccise

        elif use == 'au':
            if kwhMese <= 1200000:
                normal_corrUnitario_imponibile = min(kwhMese, 200000)
                low_corrUnitario_imponibile = max(0, kwhMese - 200000)

                dictAccise = {'corrUnitario': RATE.BUSINESS_NORMAL,
                         'kwh': kwhMese,
                         'imponibile': normal_corrUnitario_imponibile * RATE.BUSINESS_NORMAL + low_corrUnitario_imponibile * RATE.BUSINESS_LOW}
                return dictAccise
            else:
                dictAccise = {'corrUnitario': RATE.BUSINESS_NORMAL, 'kwh': kwhMese, 'imponibile': 200000 * RATE.BUSINESS_NORMAL + 4820}
                return dictAccise

        else:
            raise Exception("Contratto con tipo di uso sconosciuto: %s" % use)