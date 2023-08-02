# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import date, datetime

class FatturazioneConfigComunicazioniTipo(models.Model):

    _name = "aeegsi_energia_bolletta.conf_comunicazioni_tipo"

    tipo = fields.Char(string="Tipo", required=True)
    descrizione = fields.Char(string="Descrizione", required=True)

    @api.one
    def name_get(self):
        return self.id, self.descrizione
