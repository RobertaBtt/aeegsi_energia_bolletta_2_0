# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class Servizio(models.Model):

    _name = "aeegsi_energia_bolletta.servizio"

    bolletta_id = fields.Many2one('aeegsi_energia.bolletta', "Bolletta", ondelete="cascade")
    categoria_id = fields.Many2one('aeegsi_energia_bolletta.categoria', "Categoria", required = True)
    unita_misura_id = fields.Many2one('aeegsi_energia_bolletta.tipo_unita_misura', "Unita di misura", required = True)
    periodo_dal = fields.Date(string="Periodo dal", required = True)
    periodo_al = fields.Date(string="Periodo al", required = True)
    quantita = fields.Float(string="Quantità", required = True, default = 0, digits=(6,7))
    corrispettivo_unitario = fields.Float(string="Corrispettivo unitario", required=True, default=0, digits=(2,7))
    imponibile = fields.Float(string="Imponibile", required=True, default=0, digits=(6,7))



