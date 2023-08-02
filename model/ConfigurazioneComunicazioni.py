# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import date, datetime

class FatturazioneConfigComunicazioni(models.Model):

    _name = "aeegsi_energia_bolletta.conf_comunicazioni"

    testo = fields.Html(string="Testo", required=True)
    company_id = fields.Many2one('res.company', "Venditore", default=1)
    creato_il = fields.Date(string="Data creazione", required=True)
    tipo_id = fields.Many2one('aeegsi_energia_bolletta.conf_comunicazioni_tipo', "Tipo Comunicazione")

    _order = 'creato_il desc'

    @api.one
    def name_get(self):
        return self.id, self.creato_il
