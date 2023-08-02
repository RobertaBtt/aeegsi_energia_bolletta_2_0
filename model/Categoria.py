# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class Categoria(models.Model):

    _name = "aeegsi_energia_bolletta.categoria"

    lettera = fields.Char(string="Lettera", required=True, size=2)
    descrizione = fields.Char(string="Descrizione Categoria", required=True)
    obbligatorio = fields.Boolean(string="Servizio obbligatorio Si/No")

    _sql_constraints = [('lettera_unique', 'unique(lettera)','Lettera già presente per questa categoria')]


    @api.one
    def name_get(self):
        return self.id, "(" + self.lettera + ")" + self.descrizione