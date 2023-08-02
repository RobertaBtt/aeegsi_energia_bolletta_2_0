# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'


from openerp import models, fields, api

class TipoComponente(models.Model):

    _name = "aeegsi_energia_bolletta.tipo_componente"

    tipo = fields.Char(string="Tipo", required=True)
    descrizione = fields.Char(string="Descrizione", required=True)

    @api.one
    def name_get(self):
        return self.id, self.tipo
