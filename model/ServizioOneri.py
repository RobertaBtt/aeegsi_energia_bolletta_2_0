# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import datetime
from decimal import *

class ServizioOneri(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio"

    def creaServizioOneri(self, listaOggettiServizioDettaglioOneri):

        print "Crea Servizio Oneri"

        listaServizi = []
        dizionarioServizio = {}
        totaleImponibileServizioC = 0
        totaleQuantitaServizioC = 0
        listaDateString = set()
        listaDateObj = []

        categoria_id = self.env['aeegsi_energia_bolletta.categoria'].search([('lettera', '=', 'c')]).id
        tipo_unita_misura_id = self.env['aeegsi_energia_bolletta.tipo_unita_misura'].search([ ('descrizione', '=', 'Misto') ]).id

        for servizioDettaglio in listaOggettiServizioDettaglioOneri:
            if servizioDettaglio.sotto_categoria_id.categoria_id.lettera == 'c':
                if servizioDettaglio.sotto_categoria_id.descrizione != 'Totale C':
                    listaDateString.add(servizioDettaglio.periodo_dal)
                    listaDateString.add(servizioDettaglio.periodo_al)

                    totaleImponibileServizioC = totaleImponibileServizioC + servizioDettaglio.imponibile

                elif servizioDettaglio.sotto_categoria_id.descrizione == 'Totale C':
                    totaleQuantitaServizioC = totaleQuantitaServizioC + servizioDettaglio.quantita

        for data in listaDateString:
            listaDateObj.append(datetime.strptime(data, '%Y-%m-%d').date())

        listaDateObj.sort()

        if len(listaDateObj) >0:
            dizionarioServizio['categoria_id'] = categoria_id
            dizionarioServizio['periodo_dal'] = listaDateObj[0]
            dizionarioServizio['periodo_al'] = listaDateObj[len(listaDateString)-1]
            dizionarioServizio['unita_misura_id'] = tipo_unita_misura_id
            dizionarioServizio['quantita'] = totaleQuantitaServizioC

            if totaleQuantitaServizioC > 0:
                corrUnitario = totaleImponibileServizioC / totaleQuantitaServizioC
            else:
                corrUnitario = 0
            dizionarioServizio['corrispettivo_unitario'] = corrUnitario

            dizionarioServizio['imponibile'] = Decimal(totaleImponibileServizioC).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

            servizio = super(ServizioOneri,self).create(dizionarioServizio)
        else:
            raise models.except_orm('Attenzione', 'Il Servizio Oneri non é stato creato a causa della mancanza di date. Controllare che ci siano i valori')
        return servizio

