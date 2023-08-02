# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import timedelta, date
from decimal import *

from ..servizio_elaborato import SupportoServizioElaborato

class ServizioElaborato(models.Model):

    _name = "aeegsi_energia_bolletta.servizio_elaborato"

    categoria_elaborato_id = fields.Many2one('aeegsi_energia_bolletta.categoria_elaborato', "Categoria Elaborato", required = True)
    bolletta_id = fields.Many2one('aeegsi_energia.bolletta', "Bolletta", ondelete="cascade" )
    tipo_unita_misura_id = fields.Many2one('aeegsi_energia_bolletta.tipo_unita_misura', "Unita di misura", required=True)
    periodo_dal = fields.Date(string="Periodo dal", required = True)
    periodo_al = fields.Date(string="Periodo al", required = True)
    quantita = fields.Float(string="Quantità", required = True, default = 0, digits=(6,7))
    corrispettivo_unitario = fields.Float(string="Corrispettivo unitario", required=True, default=0, digits=(2,7))
    imponibile = fields.Float(string="Imponibile", required=True, default=0, digits=(6,7))
    iva_compresa = fields.Boolean(string="Esente Iva", compute='_iva_compresa')
    iva = fields.Float(string="Iva", digits=(2,2))

    @api.one
    @api.depends('categoria_elaborato_id')
    def _iva_compresa(self):

        if not isinstance(self.id, models.NewId):
            self.iva_compresa = self.categoria_elaborato_id.iva_compresa
        else:
            self.iva_compresa = True
