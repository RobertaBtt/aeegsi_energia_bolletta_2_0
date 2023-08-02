# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class CategoriaSconto(models.Model):

    _name = "aeegsi_energia_bolletta.categoria_sconto"

    etichetta = fields.Char(string="Etichetta", required=True)
    descrizione = fields.Char(string="Descrizione Sconto", required=True)

    @api.one
    def name_get(self):
        return self.id, self.descrizione