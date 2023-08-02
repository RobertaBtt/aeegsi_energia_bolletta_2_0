# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class TipoMercato(models.Model):

    _name = "aeegsi_energia_bolletta.tipo_mercato"

    descrizione = fields.Char(string="Descrizione Mercato", required=True)
