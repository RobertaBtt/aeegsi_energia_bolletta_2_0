# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import datetime
from decimal import *

class ServizioTrasporto(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio"

    def creaServizioTrasporto(self, listaOggettiServizioDettaglioTrasporto):

        # if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'b' and servizioElaborato.categoria_elaborato_id.etichetta =='B'
        print "Crea Servizio Trasporto"

        listaServizi = []
        dizionarioServizio = {}
        totaleImponibileServizioB = 0
        totaleQuantitaServizioB = 0
        listaDateString = set()
        listaDateObj = []

        categoria_id = self.env['aeegsi_energia_bolletta.categoria'].search([('lettera', '=', 'b')]).id
        tipo_unita_misura_id = self.env['aeegsi_energia_bolletta.tipo_unita_misura'].search([ ('descrizione', '=', 'Misto') ]).id


        for servizioDettaglio in listaOggettiServizioDettaglioTrasporto:

            if servizioDettaglio.sotto_categoria_id.categoria_id.lettera == 'b' :
                if servizioDettaglio.sotto_categoria_id.descrizione != 'Totale B':

                    listaDateString.add(servizioDettaglio.periodo_dal)
                    listaDateString.add(servizioDettaglio.periodo_al)

                    totaleImponibileServizioB = totaleImponibileServizioB + servizioDettaglio.imponibile


                elif servizioDettaglio.sotto_categoria_id.descrizione == 'Totale B':
                    totaleQuantitaServizioB = totaleQuantitaServizioB + servizioDettaglio.quantita


        for data in listaDateString:
            listaDateObj.append(datetime.strptime(data, '%Y-%m-%d').date())

        listaDateObj.sort()

        if len(listaDateObj) >0:
            dizionarioServizio['categoria_id'] = categoria_id
            dizionarioServizio['periodo_dal'] = listaDateObj[0]
            dizionarioServizio['periodo_al'] = listaDateObj[len(listaDateString)-1]
            dizionarioServizio['unita_misura_id'] = tipo_unita_misura_id
            dizionarioServizio['quantita'] = totaleQuantitaServizioB

            if totaleQuantitaServizioB > 0:
                corrUnitario = totaleImponibileServizioB / totaleQuantitaServizioB
            else:
                corrUnitario = 0
            dizionarioServizio['corrispettivo_unitario'] = corrUnitario


            dizionarioServizio['imponibile'] = Decimal(totaleImponibileServizioB).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

            servizio = super(ServizioTrasporto,self).create(dizionarioServizio)

        return servizio
