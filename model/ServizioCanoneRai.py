# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import timedelta, date, datetime, time
from decimal import *

class ServizioCanoneRai(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio"

    def creaServizioCanoneRai(self, listaOggettiServizioDettaglioCanoneRai):

        print "Crea Servizio Canone Rai"
        listaServizi = []

        dizionarioServizio = {}
        totaleImponibileServizioH = 0
        totaleQuantitaServizioH = 0
        listaDateString = set()
        listaDateObj = []
        servizio = None

        categoria_id = self.env['aeegsi_energia_bolletta.categoria'].search([('lettera', '=', 'h')]).id
        tipo_unita_misura_id = self.env['aeegsi_energia_bolletta.tipo_unita_misura'].search([ ('descrizione', '=', 'Misto') ]).id


        for servizioDettaglio in listaOggettiServizioDettaglioCanoneRai:
            # Attenzione ! Si presuppone che la riga con h sia solo una !

            if servizioDettaglio.sotto_categoria_id.categoria_id.lettera == 'h' :

                listaDateString.add(servizioDettaglio.periodo_dal)
                listaDateString.add(servizioDettaglio.periodo_al)

                totaleImponibileServizioH = totaleImponibileServizioH + servizioDettaglio.imponibile
                totaleQuantitaServizioH = totaleQuantitaServizioH + servizioDettaglio.quantita

        for data in listaDateString:
            listaDateObj.append(datetime.strptime(data, '%Y-%m-%d').date())

        dizionarioServizio['categoria_id'] = categoria_id
        dizionarioServizio['unita_misura_id'] = tipo_unita_misura_id

        if len(listaDateString) >0:
            listaDateObj.sort()

            dizionarioServizio['periodo_dal'] = listaDateObj[0]
            dizionarioServizio['periodo_al'] = listaDateObj[len(listaDateString)-1]
            dizionarioServizio['quantita'] = totaleQuantitaServizioH
            dizionarioServizio['corrispettivo_unitario'] = totaleImponibileServizioH / totaleQuantitaServizioH
            dizionarioServizio['imponibile'] = Decimal(totaleImponibileServizioH).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

            servizio = super(ServizioCanoneRai,self).create(dizionarioServizio)

        return servizio