# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from decimal import *

class ServizioDettaglioEnergia(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_dettaglio"

    def creaDettaglioEnergia(self, listaOggettiServizioElaboratoEnergia):

        listaServiziDettaglio = []

        perditaKwhF1 = 0
        perditaKwhF2 = 0
        perditaKwhF3 = 0

        totaleImponibile = 0
        corrispettivoUnitarioMonoFascia = 0
        totaleImponibileF1 = 0
        totaleImponibileF2 = 0
        totaleImponibileF3 = 0
        totaleImponibilePerditaF1 = 0
        totaleImponibilePerditaF2 = 0
        totaleImponibilePerditaF3 = 0
        dizionarioServizioDettaglio = {}
        dictPerditeF1 = {}
        dictPerditeF2 = {}
        dictPerditeF3 = {}
        dictImponibilePerditeF1 = {}
        dictImponibilePerditeF2 = {}
        dictImponibilePerditeF3 = {}

        dictDispaccAttuale = {}
        dictDispaccPrecedente = {}


        for servizioElaborato in listaOggettiServizioElaboratoEnergia:
            # Devo prima ciclare le perdite perché sono elementi che vengono dopo, nella lista,
            # ma i cui valori devo utilizzare subito nel conteggio dell''energia divisa per fasce

            if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'a':

                chiaveQuantita = 'quantita_'+servizioElaborato.periodo_dal
                chiaveCorrUnitario = 'corr_'+servizioElaborato.periodo_dal
                chiaveImponibile = 'imponibile_'+servizioElaborato.periodo_dal

                if servizioElaborato.categoria_elaborato_id.etichetta == 'PERF1':
                    dictPerditeF1[chiaveQuantita] = servizioElaborato.quantita
                    dictImponibilePerditeF1[chiaveImponibile] = servizioElaborato.imponibile
                    totaleImponibilePerditaF1 += servizioElaborato.imponibile
                    perditaKwhF1+= servizioElaborato.quantita


                elif servizioElaborato.categoria_elaborato_id.etichetta == 'PERF2':
                    dictPerditeF2[chiaveQuantita] = servizioElaborato.quantita
                    dictImponibilePerditeF2[chiaveImponibile] = servizioElaborato.imponibile
                    totaleImponibilePerditaF2 += servizioElaborato.imponibile
                    perditaKwhF2+= servizioElaborato.quantita

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'PERF3':
                    dictPerditeF3[chiaveQuantita] = servizioElaborato.quantita
                    dictImponibilePerditeF3[chiaveImponibile] = servizioElaborato.imponibile
                    totaleImponibilePerditaF3 += servizioElaborato.imponibile
                    perditaKwhF3+= servizioElaborato.quantita

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'SALV' or \
                    servizioElaborato.categoria_elaborato_id.etichetta == 'TERNA' or \
                    servizioElaborato.categoria_elaborato_id.etichetta == 'DCP' or \
                    servizioElaborato.categoria_elaborato_id.etichetta == 'IC' or \
                    servizioElaborato.categoria_elaborato_id.etichetta == 'AR':

                    # if dictDispaccAttuale.has_key(chiaveCorrUnitario):
                    #     dictDispaccAttuale[chiaveCorrUnitario] = dictDispaccAttuale[chiaveCorrUnitario]  + servizioElaborato.corrispettivo_unitario
                    # else: dictDispaccAttuale[chiaveCorrUnitario]  = servizioElaborato.corrispettivo_unitario

                    if dictDispaccAttuale.has_key(chiaveImponibile):
                        dictDispaccAttuale[chiaveImponibile] = dictDispaccAttuale[chiaveImponibile]  + servizioElaborato.imponibile
                    else: dictDispaccAttuale[chiaveImponibile]  = servizioElaborato.imponibile

                    # La quantità invece non si somma
                    dictDispaccAttuale[chiaveQuantita] = servizioElaborato.quantita

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'EO' or \
                    servizioElaborato.categoria_elaborato_id.etichetta == 'SIC':

                    # if dictDispaccPrecedente.has_key(chiaveCorrUnitario):
                    #     dictDispaccPrecedente[chiaveCorrUnitario] = dictDispaccPrecedente[chiaveCorrUnitario]  + servizioElaborato.corrispettivo_unitario
                    # else: dictDispaccPrecedente[chiaveCorrUnitario]  = servizioElaborato.corrispettivo_unitario

                    if dictDispaccPrecedente.has_key(chiaveImponibile):
                        dictDispaccPrecedente[chiaveImponibile] = dictDispaccPrecedente[chiaveImponibile]  + servizioElaborato.imponibile
                    else: dictDispaccPrecedente[chiaveImponibile]  = servizioElaborato.imponibile

                    # La quantità invece non si somma
                    dictDispaccPrecedente[chiaveQuantita] = servizioElaborato.quantita


        for servizioElaborato in listaOggettiServizioElaboratoEnergia:
            if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'a':
                chiaveQuantita = 'quantita_'+servizioElaborato.periodo_dal
                chiaveCorrUnitario = 'corr_'+servizioElaborato.periodo_dal
                chiaveImponibile = 'imponibile_'+servizioElaborato.periodo_dal

                if servizioElaborato.categoria_elaborato_id.etichetta == 'QF' or servizioElaborato.categoria_elaborato_id.etichetta == 'QPF' :
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota fissa vendita'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        totaleImponibile += servizioElaborato.imponibile

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'QPF':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota fissa placet'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        totaleImponibile += servizioElaborato.imponibile

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'F1':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia vendita fascia f1'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id
                        # Qua impostiamo il corrispettivo monofascia perché il prezzo é unico e compare nella riga che raggruppa l'energia
                        corrispettivoUnitarioMonoFascia = servizioElaborato.corrispettivo_unitario
                        # totaleImponibileF1 += servizioElaborato.imponibile
                        # consumoKwhF1 += servizioElaborato.quantita

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al

                        #Modifiche in seguito alla PLACET : ora le perdite possono non esserci, e devo controllare
                        if dictPerditeF1.has_key(chiaveQuantita):
                            dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita + dictPerditeF1[chiaveQuantita]
                        else:
                            dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita

                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        if dictImponibilePerditeF1.has_key(chiaveImponibile):
                            dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile + dictImponibilePerditeF1[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'F2':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia vendita fascia f2'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        # totaleImponibileF2 += servizioElaborato.imponibile
                        # consumoKwhF2 += servizioElaborato.quantita

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al

                        #Modifiche in seguito alla PLACET : ora le perdite possono non esserci, e devo controllare
                        if dictPerditeF2.has_key(chiaveQuantita):
                            dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita + dictPerditeF2[chiaveQuantita]
                        else:
                            dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita

                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario

                        if dictImponibilePerditeF2.has_key(chiaveImponibile):
                            dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile + dictImponibilePerditeF2[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'F3':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia vendita fascia f3'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        # totaleImponibileF3 += servizioElaborato.imponibile
                        # consumoKwhF3 += servizioElaborato.quantita

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al

                        #Modifiche in seguito alla PLACET : ora le perdite possono non esserci, e devo controllare
                        if dictPerditeF3.has_key(chiaveQuantita):
                            dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita + dictPerditeF3[chiaveQuantita]
                        else:
                            dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita

                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario

                        if dictImponibilePerditeF3.has_key(chiaveImponibile):
                            dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile + dictImponibilePerditeF3[chiaveImponibile]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                # Per ora questo componente Dettaglio lo usa solo Switch Power
                elif servizioElaborato.categoria_elaborato_id.etichetta == 'CSO':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia vendita Sbilanciamento'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                # Per ora questo componente Dettaglio lo usa solo Switch Power
                elif servizioElaborato.categoria_elaborato_id.etichetta == 'PCV':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia vendita PCV'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                # Per ora questo componente Dettaglio lo usa solo Ener.Med
                elif servizioElaborato.categoria_elaborato_id.etichetta == 'QVCV':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota Variabile Commercializzazione e Vendita'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)


                elif servizioElaborato.categoria_elaborato_id.etichetta == 'AGM':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota fissa dispacciamento'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = 1
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'SALV':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia dispacciamento'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = dictDispaccAttuale['quantita_'+servizioElaborato.periodo_dal]
                        if Decimal(dictDispaccAttuale['quantita_'+servizioElaborato.periodo_dal]) == 0:
                            dizionarioServizioDettaglio['corrispettivo_unitario'] = 0
                        else:
                            dizionarioServizioDettaglio['corrispettivo_unitario'] = Decimal(dictDispaccAttuale['imponibile_'+servizioElaborato.periodo_dal]) / Decimal(dictDispaccAttuale['quantita_'+servizioElaborato.periodo_dal])
                        dizionarioServizioDettaglio['imponibile'] = Decimal(dictDispaccAttuale['imponibile_'+servizioElaborato.periodo_dal]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif servizioElaborato.categoria_elaborato_id.etichetta == 'EO':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia dispacciamento (Eolico e Sicurezza)'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = dictDispaccPrecedente['quantita_'+servizioElaborato.periodo_dal]
                        if Decimal(dictDispaccPrecedente['quantita_'+servizioElaborato.periodo_dal]) == 0:
                            dizionarioServizioDettaglio['corrispettivo_unitario'] = 0
                        else:
                            dizionarioServizioDettaglio['corrispettivo_unitario'] = Decimal(dictDispaccPrecedente['imponibile_'+servizioElaborato.periodo_dal]) / Decimal(dictDispaccPrecedente['quantita_'+servizioElaborato.periodo_dal])
                        dizionarioServizioDettaglio['imponibile'] = Decimal(dictDispaccPrecedente['imponibile_'+servizioElaborato.periodo_dal]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

                elif  servizioElaborato.categoria_elaborato_id.etichetta == 'CS':
                    sottoCategoria = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Quota energia sbilanciamento'),('categoria_id.lettera', '=', 'a')])

                    if len(sottoCategoria) == 1:
                        sottoCategoriaId = sottoCategoria[0].id

                        dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaId
                        dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id
                        dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                        dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                        dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                        dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                        dizionarioServizioDettaglio['imponibile'] = Decimal(servizioElaborato.imponibile).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                        servizioDettaglio = super(ServizioDettaglioEnergia,self).create(dizionarioServizioDettaglio)
                        listaServiziDettaglio.append(servizioDettaglio)

        return listaServiziDettaglio
