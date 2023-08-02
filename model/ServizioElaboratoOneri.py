# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import datetime
from decimal import *
from datetime import timedelta, date, datetime, time

from ..servizio_elaborato import SupportoServizioElaborato

class ServizioElaboratoOneri(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_elaborato"

    def creaElaboratoOneri(self, dizionarioContratto, listaDictConsumoPeriodi):

        listaOggettiCreati = []

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                annoValido = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4])).year

                # Simuliamo di avere una lista, perché i metodi che elaborano
                # le componenti della bolletta, devono avere una lista di periodi,
                # quindi simuliamo di avere una lista di consumi, altrimenti sarebbe stato
                # da cambiare tutta la procedura.

                listaTemp = []
                listaTemp.append(dictConsumoPeriodo)

                if annoValido == 2018:

                    listaOggettiCreati.extend(self.creaComponenti2018(dizionarioContratto, listaTemp))
                else:
                    listaOggettiCreati.extend(self.creaComponentiAnniPrecedenti(dizionarioContratto, listaTemp))

            ultimaLista = self.creaC(listaOggettiCreati, dizionarioContratto)
            listaOggettiCreati.extend(ultimaLista)

        return listaOggettiCreati


    def creaComponenti2018(self, dizionarioContratto, listaDictConsumoPeriodi ):

        listaOggettiCreati = []

        listaOggettiCreati.extend( self.creaArimV(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaArimF(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaArimP(dizionarioContratto, listaDictConsumoPeriodi))

        listaOggettiCreati.extend( self.creaAsosV(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaAsosF(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaAsosP(dizionarioContratto, listaDictConsumoPeriodi))


        return listaOggettiCreati

    def creaComponentiAnniPrecedenti(self, dizionarioContratto, listaDictConsumoPeriodi):

        listaOggettiCreati = []

        listaOggettiCreati.extend( self.creaA2V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA2F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA3V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA3F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA4V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA4F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA5V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaA5F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaASV(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaASF(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaAEV(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaAEF(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC4V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC4F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC7V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC7F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaMCTV(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaMCTF(dizionarioContratto, listaDictConsumoPeriodi))

        return listaOggettiCreati



        #Attenzione: é stato aggiungo un controllo, perché a partire dal 2018 valgono
        # i componenti Arim e Asos, al posto di A2, A3 ecc
        # ma in tutti i mesi precedenti, continuano a valere le vecchie componenti






        ultimaLista = self.creaC(listaOggettiCreati, dizionarioContratto)
        listaOggettiCreati.extend(ultimaLista)

        return listaOggettiCreati


    def creaArimV(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "Arim"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito
                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'Arim1800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal( ( 1800 / 365.0 )*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00


                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'Arim2640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal (( (2640 - 1801) / 365.0) * numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'Arim2641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00


                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaArimF(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'ArimF')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "Arim"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaArimP(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'ArimP')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "potenza"
            codiceComponente = "Arim"

        if dizionarioContratto.has_key('potenza_contrattuale'):
            potenza_contrattuale = dizionarioContratto['potenza_contrattuale']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0 ) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = potenza_contrattuale
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] =  Decimal(corrUnitarioRounded * potenza_contrattuale).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato



    def creaAsosV(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "Asos"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito
                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'Asos1800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal( ( 1800 / 365.0 )*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00


                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'Asos2640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal (( (2640 - 1801) / 365.0) * numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'Asos2641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00


                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaAsosF(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'AsosF')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "Asos"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaAsosP(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'AsosP')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "potenza"
            codiceComponente = "Asos"

        if dizionarioContratto.has_key('potenza_contrattuale'):
            potenza_contrattuale = dizionarioContratto['potenza_contrattuale']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0 ) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = potenza_contrattuale
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] =  Decimal(corrUnitarioRounded * potenza_contrattuale).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato




    def creaA2V(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "A2"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito
                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A21800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal( ( 1800 / 365.0 )*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00


                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A22640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal (( (2640 - 1801) / 365.0) * numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A22641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00


                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaA2F(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'A2F')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "A2"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaA3V(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "A3"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']


        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A31800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 = float(Decimal ((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A32640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal(( (2640 - 1801)/365.0)*numGiorni ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A32641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanenti
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaA4V(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "A4"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']


        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A41800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodo
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A42640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801) / 365.0) *numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A42641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaA5V(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "A5"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodo = 0
                kwhPeriodoRounded = 0


                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A51800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A52640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0) * numGiorni ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'A52641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)
        return listaServiziElaborato

    def creaASV(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "AS"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']


        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)
                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'AS1800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'AS2640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0) * numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'AS2641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaAEV(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "AE"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)
                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'AE1800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'AE2640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0) * numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal ((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'AE2641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)
        return listaServiziElaborato


    def creaUC4V(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "UC4"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']


        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)
                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'UC41800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'UC42640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0)*numGiorni ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)


                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'UC42641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)
        return listaServiziElaborato

    def creaUC7V(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}

        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "UC7"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    numGiorni =  dictConsumoPeriodo['n_giorni']

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'UC71800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'UC72640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0) *numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)


                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'UC72641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)
        return listaServiziElaborato

    def creaMCTV(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        numGiorni = 0

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = []
        tipoComponente = "variabile"
        codiceComponente = "MCT"
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']


        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                quantita1800 = 0
                quantita2640 = 0
                quantita2641 = 0
                kwhPeriodo = 0
                kwhRimanenti  = 0
                kwhPeriodoRounded = 0

                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    # Analisi primo scaglione 1800, che viene sempre riempito

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)
                    numGiorni =  dictConsumoPeriodo['n_giorni']
                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'MCT1800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita1800 =  float(Decimal((1800 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita1800:
                            kwhRimanenti = kwhPeriodo - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo < quantita1800 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhPeriodo == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'MCT2640')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0)*numGiorni ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2641, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'c'), ('etichetta', '=', 'MCT2641')])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)
        return listaServiziElaborato

    def creaA3F(self,  dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'A3F')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "A3"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)
        return listaServiziElaborato

    def creaA4F(self,  dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'A4F')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "A4"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaA5F(self,  dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'A5F')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "A5"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaASF(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'ASF')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "AS"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaAEF(self,  dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'AEF')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "AE"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0)/ float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaUC4F(self,  dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'UC4F')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "UC4"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore /12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaUC7F(self,  dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'UC7F')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "UC7"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaMCTF(self,  dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),('etichetta', '=', 'MCTF')])
        listaServiziElaborato = []
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "MCT"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore /12.0) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaC(self, listaOggettiServizioElaborato, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        listaDateString = set()
        listaDateObj = []

        totaleImponibileServizioC = 0
        totaleQuantitaServizioC = 0

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'c'),  ('etichetta', '=', 'C')])

        if len(listaOggettiServizioElaborato) !=0 and  len(categoriaElaboratoList) == 1:
            for servizioElaborato in listaOggettiServizioElaborato:
                listaDateString.add(servizioElaborato.periodo_dal)
                listaDateString.add(servizioElaborato.periodo_al)

                totaleImponibileServizioC = totaleImponibileServizioC + servizioElaborato.imponibile

                # Solo con uno qualsiasi delle etichette di tipo variabile,
                # salvo la quantita. Sarebbe stata la stessa cosa prendere un altro servizio di tipo variabile C
                if servizioElaborato.categoria_elaborato_id.etichetta == "Arim1800" \
                    or servizioElaborato.categoria_elaborato_id.etichetta == "Arim2640" \
                    or servizioElaborato.categoria_elaborato_id.etichetta == "Arim2641":

                        totaleQuantitaServizioC += servizioElaborato.quantita

            for data in listaDateString:
                listaDateObj.append(datetime.strptime(data, '%Y-%m-%d').date())

            listaDateObj.sort()

            dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
            dizionarioServizioElaborato['periodo_dal'] = listaDateObj[0]
            dizionarioServizioElaborato['periodo_al'] = listaDateObj[len(listaDateString)-1]
            dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
            dizionarioServizioElaborato['quantita'] = totaleQuantitaServizioC
            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

            if totaleQuantitaServizioC > 0:
                corrUnitario = totaleImponibileServizioC / totaleQuantitaServizioC
            else:
                corrUnitario = 0
            dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitario

            dizionarioServizioElaborato['imponibile'] = Decimal(totaleImponibileServizioC).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

            servizioElaborato = super(ServizioElaboratoOneri,self).create(dizionarioServizioElaborato)
            listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

