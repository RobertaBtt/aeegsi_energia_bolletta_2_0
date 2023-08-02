# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from decimal import *

class ServizioDettaglioTrasporto(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_dettaglio"

    def creaDettaglioTrasporto(self, listaOggettiServizioElaboratoTrasporto):

        print "Crea Servizio Dettaglio Trasporto"

        listaServiziDettaglio = []
        dictQuotaFissa = {}
        dictQuotaPotenza = {}

        dictCorrUnitarioUC3V = {}
        dictCorrUnitarioUC6V = {}
        dictCorrUnitarioCT = {}
        dictCorrUnitarioCMV = {}

        dizionarioServizioDettaglio = {}

        for servizioElaborato in listaOggettiServizioElaboratoTrasporto:
            if servizioElaborato is not None:
                etichetta = servizioElaborato.categoria_elaborato_id.etichetta

                dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'b':

                    chiaveCorrUnitario = 'corr_'+servizioElaborato.periodo_dal
                    chiaveImponibile = 'imponibile_'+servizioElaborato.periodo_dal

                    if etichetta == 'UC3V':
                        dictCorrUnitarioUC3V[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario
                    if etichetta == 'UC6V':
                        dictCorrUnitarioUC6V[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario
                    if etichetta == 'CT':
                        dictCorrUnitarioCT[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario
                    if etichetta == 'CMV':
                        dictCorrUnitarioCMV[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                    if etichetta == 'UC3F' or etichetta == 'UC6F' or etichetta == 'UCF' or etichetta == 'TF' or etichetta == 'CMF' :

                        if dictQuotaFissa.has_key(chiaveCorrUnitario):
                            dictQuotaFissa[chiaveCorrUnitario] = dictQuotaFissa[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                        else: dictQuotaFissa[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                        if dictQuotaFissa.has_key(chiaveImponibile):
                            dictQuotaFissa[chiaveImponibile] = dictQuotaFissa[chiaveImponibile] + servizioElaborato.imponibile
                        else: dictQuotaFissa[chiaveImponibile] = servizioElaborato.imponibile

                    elif etichetta == 'UC6P' or etichetta == 'TP' or etichetta == 'TRASp':

                        if dictQuotaPotenza.has_key(chiaveCorrUnitario):
                            dictQuotaPotenza[chiaveCorrUnitario] = dictQuotaPotenza[chiaveCorrUnitario] + servizioElaborato.corrispettivo_unitario
                        else: dictQuotaPotenza[chiaveCorrUnitario] = servizioElaborato.corrispettivo_unitario

                        if dictQuotaPotenza.has_key(chiaveImponibile):
                            dictQuotaPotenza[chiaveImponibile] = dictQuotaPotenza[chiaveImponibile] + servizioElaborato.imponibile
                        else: dictQuotaPotenza[chiaveImponibile] = servizioElaborato.imponibile

                    elif etichetta == 'PER33':

                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Penali en. Reattiva 33/75% Ea su F1 e F2'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'PER50':

                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Penali en. Reattiva 50/75% Ea su F1 e F2'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'PER75':

                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Penali en. Reattiva oltre 75% Ea su F1 e F2'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

        for servizioElaborato in listaOggettiServizioElaboratoTrasporto:
            if servizioElaborato is not None:

                etichetta = servizioElaborato.categoria_elaborato_id.etichetta
                dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id

                if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'b':

                    chiaveCorrUnitario = 'corr_'+servizioElaborato.periodo_dal
                    chiaveImponibile = 'imponibile_'+servizioElaborato.periodo_dal
                    # Per fare la quota fissa basta uno solo dei componenti fissi
                    # Nella quota fissa la quantità é sempre '1' (un punto di prelievo)
                    if etichetta == 'UC3F':
                        # Trasporto Quota Fissa
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota fissa'),('categoria_id.lettera', '=', 'b')]).id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = 1
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaFissa[chiaveCorrUnitario]
                        dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaFissa[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'UC6P':
                        # Trasporto Quota Potenza
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota potenza'),('categoria_id.lettera', '=', 'b')]).id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = dictQuotaPotenza[chiaveCorrUnitario]
                        dizionarioServizioDettaglio['imponibile'] = Decimal(dictQuotaPotenza[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'TE900':
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui entro 900kWh'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario \
                                                + dictCorrUnitarioCT[chiaveCorrUnitario] + dictCorrUnitarioUC3V[chiaveCorrUnitario] + dictCorrUnitarioUC6V[chiaveCorrUnitario] \
                                                + dictCorrUnitarioCMV [chiaveCorrUnitario]

                        dizionarioServizioDettaglio['imponibile'] = Decimal(dizionarioServizioDettaglio['corrispettivo_unitario'] * dizionarioServizioDettaglio['quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'TE1800':
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui da 901 a 1800kWh'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario \
                                                + dictCorrUnitarioCT[chiaveCorrUnitario] + dictCorrUnitarioUC3V[chiaveCorrUnitario] + dictCorrUnitarioUC6V[chiaveCorrUnitario]\
                                                + dictCorrUnitarioCMV [chiaveCorrUnitario]

                        dizionarioServizioDettaglio['imponibile'] = Decimal(dizionarioServizioDettaglio['corrispettivo_unitario'] * dizionarioServizioDettaglio['quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'TE2640':
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui da 1801 a 2640kWh'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario \
                                                + dictCorrUnitarioCT[chiaveCorrUnitario] + dictCorrUnitarioUC3V[chiaveCorrUnitario] + dictCorrUnitarioUC6V[chiaveCorrUnitario] \
                                                + dictCorrUnitarioCMV [chiaveCorrUnitario]

                        dizionarioServizioDettaglio['imponibile'] = Decimal(dizionarioServizioDettaglio['corrispettivo_unitario'] * dizionarioServizioDettaglio['quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'TE3540':
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui da 2641 a 3540kWh'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario \
                                                + dictCorrUnitarioCT[chiaveCorrUnitario] + dictCorrUnitarioUC3V[chiaveCorrUnitario] + dictCorrUnitarioUC6V[chiaveCorrUnitario]\
                                                + dictCorrUnitarioCMV [chiaveCorrUnitario]

                        dizionarioServizioDettaglio['imponibile'] = Decimal(dizionarioServizioDettaglio['corrispettivo_unitario'] * dizionarioServizioDettaglio['quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'TE4440':
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui da 3541 a 4440kWh'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario \
                                                + dictCorrUnitarioCT[chiaveCorrUnitario] + dictCorrUnitarioUC3V[chiaveCorrUnitario] + dictCorrUnitarioUC6V[chiaveCorrUnitario]\
                                                + dictCorrUnitarioCMV [chiaveCorrUnitario]

                        dizionarioServizioDettaglio['imponibile'] = Decimal(dizionarioServizioDettaglio['corrispettivo_unitario'] * dizionarioServizioDettaglio['quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'TE4441':
                        sottoCategoriaQuotaFissaId = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia: consumi annui oltre 4440kWh'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaQuotaFissaId
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario \
                                                + dictCorrUnitarioCT[chiaveCorrUnitario] + dictCorrUnitarioUC3V[chiaveCorrUnitario] + dictCorrUnitarioUC6V[chiaveCorrUnitario]\
                                                + dictCorrUnitarioCMV [chiaveCorrUnitario]

                        dizionarioServizioDettaglio['imponibile'] = Decimal(dizionarioServizioDettaglio['corrispettivo_unitario'] * dizionarioServizioDettaglio['quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                    elif etichetta == 'B':
                        sottoCategoriaTotaleB = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Totale B'),('categoria_id.lettera', '=', 'b')]).id
                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaTotaleB
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioTrasporto,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

        return listaServiziDettaglio