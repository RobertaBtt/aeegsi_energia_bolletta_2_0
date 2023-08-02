# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class TipoUnitaMisura(models.Model):

    _name = "aeegsi_energia_bolletta.tipo_unita_misura"

    descrizione = fields.Char(string="Descrizione Unita misura", required=True)

    @api.one
    def name_get(self):
        return self.id, self.descrizione


