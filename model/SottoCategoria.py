# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'


from openerp import models, fields, api

class SottoCategoria(models.Model):

    _name = "aeegsi_energia_bolletta.sotto_categoria"

    descrizione = fields.Char(string="Descrizione Sotto Categoria", required=True)
    categoria_id = fields.Many2one('aeegsi_energia_bolletta.categoria', "Categoria", required=True) # Categoria di riferimento

    _sql_constraints = [('descrizione_categoria_unique', 'unique(descrizione, categoria_id)','Descrizione già presente per questa categoria')]

    @api.one
    def name_get(self):
        return self.id, self.categoria_id.lettera + " " + self.descrizione

