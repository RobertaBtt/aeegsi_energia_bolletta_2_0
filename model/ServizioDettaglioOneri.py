# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from decimal import *

class ServizioDettaglioOneri(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_dettaglio"

    def creaDettaglioOneri(self, listaOggettiServizioElaboratoOneri):

        print "Crea Servizio Dettaglio Oneri"

        listaServiziDettaglio = []
        dictQuotaFissa = {}
        dictQuotaEnergia1800 = {}
        dictQuotaEnergia2640 = {}
        dictQuotaEnergia2641 = {}
        dictQuotaPotenza = {}


        dizionarioServizioDettaglio = {}


        for servizioElaborato in listaOggettiServizioElaboratoOneri:
            etichetta = servizioElaborato.categoria_elaborato_id.etichetta

            if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'c':
                chiaveQuantita = 'quantita_'+servizioElaborato.periodo_dal
                chiaveCorrUnitario = 'corr_'+servizioElaborato.periodo_dal
                chiaveImponibile = 'imponibile_'+servizioElaborato.periodo_dal

                if etichetta == 'ArimF' or etichetta == 'AsosF' or etichetta == 'A2F' or etichetta == 'A3F'  or etichetta == 'A4F' or etichetta == 'A5F' or \
                    etichetta == 'ASF'  or etichetta == 'AEF' or etichetta == 'UC4F' or etichetta == 'UC7F' or etichetta == 'MCTF':

                    if dictQuotaFissa.has_key(chiaveCorrUnitario):
                        dictQuotaFissa[chiaveCorrUnitario] = dictQuotaFissa[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                    else: dictQuotaFissa[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                    if dictQuotaFissa.has_key(chiaveImponibile):
                        dictQuotaFissa[chiaveImponibile] = dictQuotaFissa[chiaveImponibile] + servizioElaborato.imponibile
                    else: dictQuotaFissa[chiaveImponibile] = servizioElaborato.imponibile

                elif etichetta == 'Arim1800'  or etichetta == 'Asos1800' or etichetta == 'A21800' or etichetta == 'A31800' or etichetta == 'A41800' or etichetta == 'A51800' \
                    or etichetta == 'AS1800' or etichetta == 'AE1800' or etichetta == 'UC41800' or etichetta == 'UC71800' or etichetta == 'MCT1800':

                    dictQuotaEnergia1800[chiaveQuantita] = servizioElaborato.quantita

                    if dictQuotaEnergia1800.has_key(chiaveCorrUnitario):
                        dictQuotaEnergia1800[chiaveCorrUnitario] = dictQuotaEnergia1800[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                    else: dictQuotaEnergia1800[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                    if dictQuotaEnergia1800.has_key(chiaveImponibile):
                        dictQuotaEnergia1800[chiaveImponibile] = dictQuotaEnergia1800[chiaveImponibile] + servizioElaborato.imponibile
                    else: dictQuotaEnergia1800[chiaveImponibile] = servizioElaborato.imponibile

                elif etichetta == 'Arim2640'  or etichetta == 'Asos2640' or etichetta == 'A22640' or etichetta == 'A32640' or etichetta == 'A42640' or etichetta == 'A52640' \
                    or etichetta == 'AS2640' or etichetta == 'AE2640' or etichetta == 'UC42640' or etichetta == 'UC72640' or etichetta == 'MCT2640':

                    dictQuotaEnergia2640[chiaveQuantita] = servizioElaborato.quantita

                    if dictQuotaEnergia2640.has_key(chiaveCorrUnitario):
                        dictQuotaEnergia2640[chiaveCorrUnitario] = dictQuotaEnergia2640[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                    else: dictQuotaEnergia2640[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                    if dictQuotaEnergia2640.has_key(chiaveImponibile):
                        dictQuotaEnergia2640[chiaveImponibile] = dictQuotaEnergia2640[chiaveImponibile] + servizioElaborato.imponibile
                    else: dictQuotaEnergia2640[chiaveImponibile] = servizioElaborato.imponibile

                elif etichetta == 'Arim2641'  or etichetta == 'Asos2641' or etichetta == 'A22641' or etichetta == 'A32641' or etichetta == 'A42641' or etichetta == 'A52641' \
                    or etichetta == 'AS2641' or etichetta == 'AE2641' or etichetta == 'UC42641' or etichetta == 'UC72641' or etichetta == 'MCT2641':

                    dictQuotaEnergia2641[chiaveQuantita] = servizioElaborato.quantita

                    if dictQuotaEnergia2641.has_key(chiaveCorrUnitario):
                        dictQuotaEnergia2641[chiaveCorrUnitario] = dictQuotaEnergia2641[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                    else: dictQuotaEnergia2641[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                    if dictQuotaEnergia2641.has_key(chiaveImponibile):
                        dictQuotaEnergia2641[chiaveImponibile] = dictQuotaEnergia2641[chiaveImponibile] + servizioElaborato.imponibile
                    else: dictQuotaEnergia2641[chiaveImponibile] = servizioElaborato.imponibile

                elif etichetta == 'ArimP' or etichetta == 'AsosP':

                    if dictQuotaPotenza.has_key(chiaveCorrUnitario):
                        dictQuotaPotenza[chiaveCorrUnitario] = dictQuotaPotenza[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                    else: dictQuotaPotenza[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                    if dictQuotaPotenza.has_key(chiaveImponibile):
                        dictQuotaPotenza[chiaveImponibile] = dictQuotaPotenza[chiaveImponibile] + servizioElaborato.imponibile
                    else: dictQuotaPotenza[chiaveImponibile] = servizioElaborato.imponibile


        for servizioElaborato in listaOggettiServizioElaboratoOneri:

            etichetta = servizioElaborato.categoria_elaborato_id.etichetta
            chiaveQuantita = 'quantita_'+servizioElaborato.periodo_dal
            chiaveCorrUnitario = 'corr_'+servizioElaborato.periodo_dal
            chiaveImponibile = 'imponibile_'+servizioElaborato.periodo_dal

            dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
            dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
            dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
            dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

            if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'c':

                # Per fare la quota fissa basta uno solo dei componenti fissi
                # Nella quota fissa la quantità é sempre '1' (un punto di prelievo)
                if etichetta == 'ArimF' or etichetta == "A2F":
                    # Oneri Quota Fissa
                    sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota fissa'),('categoria_id.lettera', '=', 'c')]).id

                    dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                    dizionarioServizioDettaglio['quantita'] = 1
                    dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaFissa[chiaveCorrUnitario]
                    dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaFissa[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                    dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                    servizioDettaglio = super(ServizioDettaglioOneri,self).create(dizionarioServizioDettaglio)
                    listaServiziDettaglio.append(servizioDettaglio)

                elif etichetta == 'Arim1800' or etichetta == "A21800":
                    # Trasporto Quota Energia 1800
                    sottoCategoriaQuotaEnergia1800Id = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui entro 1800kWh'),('categoria_id.lettera', '=', 'c')]).id

                    dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaEnergia1800Id
                    dizionarioServizioDettaglio['quantita'] = dictQuotaEnergia1800[chiaveQuantita]
                    dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaEnergia1800[chiaveCorrUnitario]
                    dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaEnergia1800[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                    dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                    servizioDettaglio = super(ServizioDettaglioOneri,self).create(dizionarioServizioDettaglio)
                    listaServiziDettaglio.append(servizioDettaglio)

                elif etichetta == 'Arim2640' or etichetta == "A22640":
                    # Trasporto Quota Energia 2640
                    sottoCategoriaQuotaEnergia2640Id = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui da 1801 a 2640kWh'),('categoria_id.lettera', '=', 'c')]).id

                    dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaEnergia2640Id
                    dizionarioServizioDettaglio['quantita'] = dictQuotaEnergia2640[chiaveQuantita]
                    dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaEnergia2640[chiaveCorrUnitario]
                    dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaEnergia2640[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                    dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                    servizioDettaglio = super(ServizioDettaglioOneri,self).create(dizionarioServizioDettaglio)
                    listaServiziDettaglio.append(servizioDettaglio)

                elif etichetta == 'Arim2641' or etichetta == "A22641":
                    # Trasporto Quota Energia Oltre 2640
                    sottoCategoriaQuotaEnergia2641Id = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui oltre 2640kWh'),('categoria_id.lettera', '=', 'c')]).id

                    dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaEnergia2641Id
                    dizionarioServizioDettaglio['quantita'] = dictQuotaEnergia2641[chiaveQuantita]
                    dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaEnergia2641[chiaveCorrUnitario]
                    dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaEnergia2641[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                    dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                    servizioDettaglio = super(ServizioDettaglioOneri,self).create(dizionarioServizioDettaglio)
                    listaServiziDettaglio.append(servizioDettaglio)

                elif etichetta == 'ArimP':
                    # Oneri Quota Potenza
                    sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota potenza'),('categoria_id.lettera', '=', 'c')]).id

                    dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                    dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                    dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaPotenza[chiaveCorrUnitario]
                    dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaPotenza[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                    dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                    servizioDettaglio = super(ServizioDettaglioOneri,self).create(dizionarioServizioDettaglio)
                    listaServiziDettaglio.append(servizioDettaglio)

                elif etichetta == 'C':

                    sottoCategoriaTotaleC = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Totale C'),('categoria_id.lettera', '=', 'c')]).id
                    dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaTotaleC
                    dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                    dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                    dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                    dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                    servizioDettaglio = super(ServizioDettaglioOneri,self).create(dizionarioServizioDettaglio)
                    listaServiziDettaglio.append(servizioDettaglio)

        return listaServiziDettaglio

