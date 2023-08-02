# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import timedelta, date, datetime
from decimal import *
import re

from ..servizio_elaborato import SupportoServizioElaborato

class ServizioElaboratoEnergia(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_elaborato"

    def creaElaboratoEnergia(self, dizionarioContratto, listaDictConsumoPeriodi, listaDictConsumoPeriodiPrecedente):

        listaOggettiCreati = []

        listaOggettiCreati.extend( self.creaQF(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaPQF(listaDictConsumoPeriodi, dizionarioContratto)) #Nuova Placet Quota Fissa
        listaOggettiCreati.extend( self.creaF1(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaF2(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaF3(listaDictConsumoPeriodi, dizionarioContratto))

        # Solo se la tariffa non é placet, metto questo componente
        if dizionarioContratto['descrizione_offerta'].find("Placet") < 0:
            listaOggettiCreati.extend( self.creaPERF1(listaDictConsumoPeriodi, dizionarioContratto))
            listaOggettiCreati.extend( self.creaPERF2(listaDictConsumoPeriodi, dizionarioContratto))
            listaOggettiCreati.extend( self.creaPERF3(listaDictConsumoPeriodi, dizionarioContratto))

        # questi due servizi potrebbero essere nulli, fin'ora li ha solo Switch Power
        listaOggettiCreati.extend( self.creaSbilanciamentoOfferta(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaPCVOfferta(listaDictConsumoPeriodi, dizionarioContratto))

        # Questo servizio lo ha enermed
        listaOggettiCreati.extend( self.creaQVCV(listaDictConsumoPeriodi, dizionarioContratto))

        listaOggettiCreati.extend( self.creaSIC(listaDictConsumoPeriodi,listaDictConsumoPeriodiPrecedente, dizionarioContratto))
        listaOggettiCreati.extend( self.creaEO(listaDictConsumoPeriodi,listaDictConsumoPeriodiPrecedente, dizionarioContratto))
        listaOggettiCreati.extend( self.creaSALV(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaTERNA(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaDCP(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaIC(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaAR(listaDictConsumoPeriodi, dizionarioContratto))
        listaOggettiCreati.extend( self.creaAGM(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaCS(listaDictConsumoPeriodi, dizionarioContratto))

        ultimaLista = self.creaA(listaOggettiCreati, dizionarioContratto)
        listaOggettiCreati.extend(ultimaLista)

        return listaOggettiCreati


    def creaQF(self, listaDictConsumoPeriodi, dizionarioContratto):
        """ Creazione della Quota Fissa Energia
        :param listaDictConsumoPeriodi: dizionario dei consumi
        :return: l'oggetto creato oppure None
        """

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'QF')])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('quotaFissaEnergia'):

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['quotaFissaEnergia']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['quotaFissaEnergia']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaPQF(self, listaDictConsumoPeriodi, dizionarioContratto):
        """ Creazione della Quota Fissa Energia
        :param listaDictConsumoPeriodi: dizionario dei consumi
        :return: l'oggetto creato oppure None
        """

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'QPF')])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('quotaFissaPlacet') and dictConsumoPeriodo['quotaFissaPlacet'] is not None:

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['quotaFissaPlacet']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['quotaFissaPlacet']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaF1(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'F1')
        ])

        if len(categoriaElaboratoList) == 1:

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F1') \
                            and dictConsumoPeriodo.has_key('prezzo_F1'):

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1']
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['prezzo_F1']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['prezzo_F1'] * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']
                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato



    def creaF2(self, listaDictConsumoPeriodi, dizionarioContratto):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'F2')
        ])

        if len(categoriaElaboratoList) == 1:

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F2') \
                            and dictConsumoPeriodo.has_key('prezzo_F2'):

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F2']
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['prezzo_F2']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['prezzo_F2'] * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaF3(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'F3')
        ])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F3') \
                            and dictConsumoPeriodo.has_key('prezzo_F3'):

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F3']
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['prezzo_F3']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['prezzo_F3'] * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaPERF1(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'PERF1')
        ])

        if len(categoriaElaboratoList) == 1:

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('perdita_F1') \
                            and dictConsumoPeriodo.has_key('prezzo_F1'):

                        kwhPerdita = dictConsumoPeriodo['perdita_F1']
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = kwhPerdita
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['prezzo_F1']
                        dizionarioServizioElaborato['imponibile'] = Decimal(kwhPerdita * dictConsumoPeriodo['prezzo_F1']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaPERF2(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'PERF2')
        ])

        if len(categoriaElaboratoList) == 1:

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('perdita_F2') \
                            and dictConsumoPeriodo.has_key('prezzo_F2'):

                        kwhPerdita = dictConsumoPeriodo['perdita_F2']
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = kwhPerdita
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['prezzo_F2']
                        dizionarioServizioElaborato['imponibile'] = Decimal(kwhPerdita * dictConsumoPeriodo['prezzo_F2']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaPERF3(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'PERF3')
        ])

        if len(categoriaElaboratoList) == 1:

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('perdita_F3') \
                            and dictConsumoPeriodo.has_key('prezzo_F3'):

                        kwhPerdita = dictConsumoPeriodo['perdita_F3']
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = kwhPerdita
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['prezzo_F3']
                        dizionarioServizioElaborato['imponibile'] = Decimal(kwhPerdita * dictConsumoPeriodo['prezzo_F3']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaSIC(self, listaDictConsumoPeriodi, listaDictConsumoPeriodiPrecedente, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'a'), ('etichetta', '=', 'SIC') ])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "SIC"

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:

                    date4 = date(day=1, month=dictConsumoPeriodo['mese_calcolo'], year=dictConsumoPeriodo['anno_calcolo']) - timedelta(days=1) # 30 ottobre
                    date3 = date(day=1, month=date4.month, year=date4.year) - timedelta(days=1) # 30 settembre
                    date2 = date(day=1, month=date3.month, year=date3.year) - timedelta(days=1) # 31 agosto

                    dataInizioValidita1 = date(day=1, month=date2.month, year=date2.year)
                    dataFineValidita1 = date(day=date2.day, month=date2.month, year=date2.year)

                    # l'ultimo True vuol dire che le date sono precise !!!
                    valoreTrovato1 = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(valoreEnv, tipoComponente,
                                codiceComponente, None, None, dataInizioValidita1, dataFineValidita1, None, None, True)

                    dataInizioValidita2 = date(day=1, month=date3.month, year=date3.year)
                    dataFineValidita2 = date(day=date3.day, month=date3.month, year=date3.year)

                    # l'ultimo True vuol dire che le date sono precise !!!
                    valoreTrovato2 = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(valoreEnv, tipoComponente,
                                codiceComponente, None, None, dataInizioValidita2, dataFineValidita2, None, None, True)


                if listaDictConsumoPeriodiPrecedente is not None:
                    if len(listaDictConsumoPeriodiPrecedente) == 1:
                        for dictConsumoPeriodoPrecedente in listaDictConsumoPeriodiPrecedente:

                            if dictConsumoPeriodoPrecedente.has_key('dal') and dictConsumoPeriodoPrecedente.has_key('al') \
                                    and dictConsumoPeriodoPrecedente.has_key('kWh_F1') \
                                    and dictConsumoPeriodoPrecedente.has_key('kWh_F2') \
                                    and dictConsumoPeriodoPrecedente.has_key('kWh_F3'):

                                quantitaTotaleKwhConsumoPrecedente = dictConsumoPeriodoPrecedente['kWh_F1'] + dictConsumoPeriodoPrecedente['kWh_F2'] + \
                                         dictConsumoPeriodoPrecedente['kWh_F3'] + dictConsumoPeriodoPrecedente['perdita_F1'] + \
                                         dictConsumoPeriodoPrecedente['perdita_F2'] + dictConsumoPeriodoPrecedente['perdita_F3']

                                dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                                dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                                dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumoPrecedente
                                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodoPrecedente['dal']
                                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodoPrecedente['al']

                                if valoreTrovato2 is not None:
                                    dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro)
                                    dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro) * quantitaTotaleKwhConsumoPrecedente).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                    dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                                listaServiziElaborato.append(servizioElaborato)


                    elif len(listaDictConsumoPeriodiPrecedente) > 1:
                        for dictConsumoPeriodoPrecedente in listaDictConsumoPeriodiPrecedente:
                            if dictConsumoPeriodoPrecedente.has_key('dal') and dictConsumoPeriodoPrecedente.has_key('al') \
                                        and dictConsumoPeriodoPrecedente.has_key('kWh_F1') \
                                        and dictConsumoPeriodoPrecedente.has_key('kWh_F2') \
                                        and dictConsumoPeriodoPrecedente.has_key('kWh_F3'):

                                    quantitaTotaleKwhConsumoPrecedente = dictConsumoPeriodoPrecedente['kWh_F1'] + dictConsumoPeriodoPrecedente['kWh_F2'] + \
                                             dictConsumoPeriodoPrecedente['kWh_F3'] + dictConsumoPeriodoPrecedente['perdita_F1'] + \
                                             dictConsumoPeriodoPrecedente['perdita_F2'] + dictConsumoPeriodoPrecedente['perdita_F3']

                                    dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                                    dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                                    dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumoPrecedente
                                    dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodoPrecedente['dal']
                                    dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodoPrecedente['al']

                                    if dictConsumoPeriodoPrecedente['periodo_n'] == 1:
                                        if valoreTrovato1 is not None:
                                            dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato1.valore/float(valoreTrovato1.tipo_valore_euro)
                                            dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato1.valore/float(valoreTrovato1.tipo_valore_euro) * quantitaTotaleKwhConsumoPrecedente).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                    elif dictConsumoPeriodoPrecedente['periodo_n'] == 2:
                                        if valoreTrovato2 is not None:
                                            dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro)
                                            dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro) * quantitaTotaleKwhConsumoPrecedente).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                    servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                                    listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaEO(self,  listaDictConsumoPeriodi, listaDictConsumoPeriodiPrecedente, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'EO') ])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "EO"

            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:

                    date4 = date(day=1, month=dictConsumoPeriodo['mese_calcolo'], year=dictConsumoPeriodo['anno_calcolo']) - timedelta(days=1) # 30 ottobre
                    date3 = date(day=1, month=date4.month, year=date4.year) - timedelta(days=1) # 30 settembre
                    date2 = date(day=1, month=date3.month, year=date3.year) - timedelta(days=1) # 31 agosto

                    dataInizioValidita1 = date(day=1, month=date2.month, year=date2.year)
                    dataFineValidita1 = date(day=date2.day, month=date2.month, year=date2.year)

                    # l'ultimo True vuol dire che le date sono precise !!!
                    valoreTrovato1 = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(valoreEnv, tipoComponente,
                             codiceComponente, None, None, dataInizioValidita1, dataFineValidita1, None, None, True)

                    dataInizioValidita2 = date(day=1, month=date3.month, year=date3.year)
                    dataFineValidita2 = date(day=date3.day, month=date3.month, year=date3.year)

                    # l'ultimo True vuol dire che le date sono precise !!!
                    valoreTrovato2 = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(valoreEnv, tipoComponente,
                            codiceComponente, None, None, dataInizioValidita2, dataFineValidita2, None, None, True)


                if listaDictConsumoPeriodiPrecedente is not None:

                    if len(listaDictConsumoPeriodiPrecedente) == 1:
                        for dictConsumoPeriodoPrecedente in listaDictConsumoPeriodiPrecedente:

                            if dictConsumoPeriodoPrecedente.has_key('dal') and dictConsumoPeriodoPrecedente.has_key('al') \
                                    and dictConsumoPeriodoPrecedente.has_key('kWh_F1') \
                                    and dictConsumoPeriodoPrecedente.has_key('kWh_F2') \
                                    and dictConsumoPeriodoPrecedente.has_key('kWh_F3'):

                                quantitaTotaleKwhConsumoPrecedente = dictConsumoPeriodoPrecedente['kWh_F1'] + dictConsumoPeriodoPrecedente['kWh_F2'] + dictConsumoPeriodoPrecedente['kWh_F3'] + \
                                    dictConsumoPeriodoPrecedente['perdita_F1'] + dictConsumoPeriodoPrecedente['perdita_F2'] + dictConsumoPeriodoPrecedente['perdita_F3']

                                dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                                dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                                dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumoPrecedente
                                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodoPrecedente['dal']
                                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodoPrecedente['al']

                                if valoreTrovato2 is not None:
                                    dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro)
                                    dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro) * quantitaTotaleKwhConsumoPrecedente).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                    dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                                listaServiziElaborato.append(servizioElaborato)

                    elif len(listaDictConsumoPeriodiPrecedente) > 1:
                        for dictConsumoPeriodoPrecedente in listaDictConsumoPeriodiPrecedente:
                            if dictConsumoPeriodoPrecedente.has_key('dal') and dictConsumoPeriodoPrecedente.has_key('al') \
                                        and dictConsumoPeriodoPrecedente.has_key('kWh_F1') \
                                        and dictConsumoPeriodoPrecedente.has_key('kWh_F2') \
                                        and dictConsumoPeriodoPrecedente.has_key('kWh_F3'):

                                    quantitaTotaleKwhConsumoPrecedente = dictConsumoPeriodoPrecedente['kWh_F1'] + dictConsumoPeriodoPrecedente['kWh_F2'] + \
                                             dictConsumoPeriodoPrecedente['kWh_F3'] + dictConsumoPeriodoPrecedente['perdita_F1'] + \
                                             dictConsumoPeriodoPrecedente['perdita_F2'] + dictConsumoPeriodoPrecedente['perdita_F3']

                                    dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                                    dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                                    dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumoPrecedente
                                    dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodoPrecedente['dal']
                                    dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodoPrecedente['al']

                                    if dictConsumoPeriodoPrecedente['periodo_n'] == 1:
                                        if valoreTrovato1 is not None:
                                            dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato1.valore/float(valoreTrovato1.tipo_valore_euro)
                                            dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato1.valore/float(valoreTrovato1.tipo_valore_euro) * quantitaTotaleKwhConsumoPrecedente).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                    elif dictConsumoPeriodoPrecedente['periodo_n'] == 2:
                                        if valoreTrovato2 is not None:
                                            dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro)
                                            dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato2.valore/float(valoreTrovato2.tipo_valore_euro) * quantitaTotaleKwhConsumoPrecedente).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                    servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                                    listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaSALV(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'SALV')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "SALV"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') \
                        and dictConsumoPeriodo.has_key('kWh_F2') \
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                        dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                    dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(
                        valoreEnv, tipoComponente, codiceComponente, None, None, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaTERNA(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'TERNA') ])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "TERNA"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') \
                        and dictConsumoPeriodo.has_key('kWh_F2') \
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                        dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                    dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(
                        valoreEnv, tipoComponente, codiceComponente, None, None, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaDCP(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'DCP')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "DCP"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') \
                        and dictConsumoPeriodo.has_key('kWh_F2') \
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                        dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                    dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(
                        valoreEnv, tipoComponente, codiceComponente, None, None, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaIC(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'a'),('etichetta', '=', 'IC')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "IC"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') \
                        and dictConsumoPeriodo.has_key('kWh_F2') \
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                        dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                    dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(
                        valoreEnv, tipoComponente, codiceComponente, None, None, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    # Costo approvvigionamento risorse
    def creaAR(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'a'), ('etichetta', '=', 'AR')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "AR"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') \
                        and dictConsumoPeriodo.has_key('kWh_F2') \
                        and dictConsumoPeriodo.has_key('kWh_F3'):
                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                        dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(
                        valoreEnv, tipoComponente, codiceComponente, None, None, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = (valoreTrovato.valore)/ float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaAGM(self, dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'a'), ('etichetta', '=', 'AGM')])
        valoreEnv = self.env['aeegsi_energia.valore']

        # solo per questo tipo di valore ci vuole un dizionario specifico
        # perché contiene solo l'uso e la potenza disponibile

        dizionarioContrattoCustom = {}
        if dizionarioContratto.has_key('tensione'):
            dizionarioContrattoCustom ['tensione'] = dizionarioContratto['tensione']
        if dizionarioContratto.has_key('potenza_disponibile'):
            dizionarioContrattoCustom ['potenza_disponibile'] = dizionarioContratto['potenza_disponibile']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "AGM"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al'):

                    dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore(
                        valoreEnv, tipoComponente, codiceComponente, dizionarioContrattoCustom, None, dataInizioValidita, None, None, None, True)


                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    # Costo Sbilanciamento
    def creaCS(self,  listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'CS')
        ])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F1') \
                            and dictConsumoPeriodo.has_key('kWh_F2') \
                            and dictConsumoPeriodo.has_key('kWh_F3'):

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                            dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['costoSbilanciamento']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['costoSbilanciamento'] * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaSbilanciamentoOfferta(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'CSO')
        ])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F1') \
                            and dictConsumoPeriodo.has_key('kWh_F2') \
                            and dictConsumoPeriodo.has_key('kWh_F3') \
                            and dictConsumoPeriodo.has_key('costoSbilanciamentoOfferta') :

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                            dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['costoSbilanciamentoOfferta']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['costoSbilanciamentoOfferta'] * \
                                                                    quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    #Usato solo da switch power
    def creaPCVOfferta(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'PCV')
        ])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F1') \
                            and dictConsumoPeriodo.has_key('kWh_F2') \
                            and dictConsumoPeriodo.has_key('kWh_F3') \
                            and dictConsumoPeriodo.has_key('pcvOfferta') :

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                            dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['pcvOfferta']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['pcvOfferta'] * \
                                                                    quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    # usato solo da enermed
    def creaQVCV(self, listaDictConsumoPeriodi, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'a'),
            ('etichetta', '=', 'QVCV')
        ])

        if len(categoriaElaboratoList) == 1:
            if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                            and dictConsumoPeriodo.has_key('kWh_F1') \
                            and dictConsumoPeriodo.has_key('kWh_F2') \
                            and dictConsumoPeriodo.has_key('kWh_F3') \
                            and dictConsumoPeriodo.has_key('quotaVariabileEnergia') :

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3'] + \
                            dictConsumoPeriodo['perdita_F1'] + dictConsumoPeriodo['perdita_F2'] + dictConsumoPeriodo['perdita_F3']

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = dictConsumoPeriodo['quotaVariabileEnergia']
                        dizionarioServizioElaborato['imponibile'] = Decimal(dictConsumoPeriodo['quotaVariabileEnergia'] * \
                                                                    quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaA(self, listaOggettiServizioElaborato, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []


        listaDateString = set()
        listaDateObj = []
        totaleImponibileServizioA = 0
        totaleQuantitaServizioA = 0

        # numeroPeriodi = len(listaDictConsumoPeriodi)
        # periodoInizioServizio = None
        # periodoFineServizio = None

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'a'),  ('etichetta', '=', 'A')])

        # # Riunisco i periodi
        # if numeroPeriodi >1:
        #     for dictConsumoPeriodo in listaDictConsumoPeriodi:
        #         if dictConsumoPeriodo.has_key('periodo_n'):
        #             if dictConsumoPeriodo['periodo_n'] == 1:
        #                 if dictConsumoPeriodo.has_key('dal'):
        #                     periodoInizioServizio = dictConsumoPeriodo['dal']
        #             elif dictConsumoPeriodo['periodo_n'] == numeroPeriodi:
        #                 if dictConsumoPeriodo.has_key('al'):
        #                     periodoFineServizio = dictConsumoPeriodo['al']
        # elif numeroPeriodi == 1:
        #     periodoInizioServizio = listaDictConsumoPeriodi[0]['dal']
        #     periodoFineServizio = listaDictConsumoPeriodi[0]['al']


        if len(listaOggettiServizioElaborato) !=0 and  len(categoriaElaboratoList) == 1:
            for servizioElaborato in listaOggettiServizioElaborato:
                listaDateString.add(servizioElaborato.periodo_dal)
                listaDateString.add(servizioElaborato.periodo_al)

                totaleImponibileServizioA += servizioElaborato.imponibile

                # Solo con uno qualsiasi delle etichette di tipo variabile,
                # salvo la quantita. Sarebbe stata la stessa cosa prendere un altro servizio di tipo variabile C
                if servizioElaborato.categoria_elaborato_id.etichetta == "F1" \
                    or servizioElaborato.categoria_elaborato_id.etichetta == "F2" \
                    or servizioElaborato.categoria_elaborato_id.etichetta == "F3":

                    totaleQuantitaServizioA += servizioElaborato.quantita

            for data in listaDateString:
                listaDateObj.append(datetime.strptime(data, '%Y-%m-%d').date())

            listaDateObj.sort()

            dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
            dizionarioServizioElaborato['periodo_dal'] = listaDateObj[0]
            dizionarioServizioElaborato['periodo_al'] = listaDateObj[len(listaDateString)-1]
            dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
            dizionarioServizioElaborato['quantita'] = totaleQuantitaServizioA

            if totaleQuantitaServizioA > 0:
                corrUnitario = totaleImponibileServizioA / totaleQuantitaServizioA
            else:
                corrUnitario = 0
            dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitario

            dizionarioServizioElaborato['imponibile'] = Decimal(totaleImponibileServizioA).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

            servizioElaborato = super(ServizioElaboratoEnergia,self).create(dizionarioServizioElaborato)
            listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


