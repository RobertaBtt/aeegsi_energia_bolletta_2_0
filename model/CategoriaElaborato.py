# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
import requests

class CategoriaElaborato(models.Model):

    _name = "aeegsi_energia_bolletta.categoria_elaborato"

    etichetta = fields.Char(string="Etichetta categoria elaborato", required=True)
    descrizione = fields.Char(string="Descrizione categoria elaborato", required=True)
    categoria_id = fields.Many2one('aeegsi_energia_bolletta.categoria', "Categoria", required=True)
    tipo_componente_id = fields.Many2one('aeegsi_energia_bolletta.tipo_componente', "Tipo Componente", required=True)
    tipo_unita_di_misura_id = fields.Many2one('aeegsi_energia_bolletta.tipo_unita_misura', "Unità di misura", required=True)
    iva_compresa = fields.Boolean(string="IVA compresa si/no", default=False)

    # SQL constraints
    _sql_constraints = [('etichetta_categoria_id_unique', 'unique(etichetta,categoria_id)','Etichetta già presente per questa categoria')]

    @api.one
    def name_get(self):
        return self.id, self.categoria_id.lettera + " " + self.etichetta + "(" + self.descrizione + ")"