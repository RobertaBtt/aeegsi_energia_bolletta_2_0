# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class ServizioDettaglio(models.Model):

    _name = "aeegsi_energia_bolletta.servizio_dettaglio"

    sotto_categoria_id = fields.Many2one('aeegsi_energia_bolletta.sotto_categoria', "Sotto Categoria", required = True)
    bolletta_id = fields.Many2one('aeegsi_energia.bolletta', "Bolletta", ondelete="cascade")
    tipo_unita_misura_id = fields.Many2one('aeegsi_energia_bolletta.tipo_unita_misura', "Unita di misura", required=True)
    periodo_dal = fields.Date(string="Periodo dal", required = True)
    periodo_al = fields.Date(string="Periodo al", required = True)
    quantita = fields.Float(string="Quantità", required = True, default = 0, digits=(6,7))
    corrispettivo_unitario = fields.Float(string="Corrispettivo unitario", required=True, default=0, digits=(2,7))
    imponibile = fields.Float(string="Imponibile", required=True, default=0, digits=(6,7))
    iva_compresa = fields.Boolean(string="IVA compresa si/no", default=True)
    iva = fields.Float(string="Iva", digits=(2,2))

    @api.one
    def name_get(self):
        return self.id, self.sotto_categoria_id.descrizione

    # # SQL constraints
    # _sql_constraints = [('bolletta_sottocategoria_unique', 'unique(bolletta_id,sotto_categoria_id)','Servizio di dettaglio già raggruppato')]

