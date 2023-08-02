# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class PercentualePerdite(models.Model):

    _name = "aeegsi_energia_bolletta.percentuale_perdite"

    descrizione = fields.Char(string="Descrizione Sconto", required=True)
    valore = fields.Float(string = "Valore", required=True)
    categoria_id = fields.Many2one('aeegsi_energia_bolletta.categoria_sconto', "Categoria Sconto") # Categoria Sconto
    applica_su = fields.Many2one('aeegsi_energia_bolletta.sotto_categoria', "Applica su sotto Categoria") # Sotto categoria di riferimento
    applica_su_orario_inizio = fields.Date(string="Inizio orario Sconto")
    applica_su_orario_fine = fields.Date(string="Fine orario Sconto")
    data_inizio_validita = fields.Date(string="Inizio validità Sconto")
    data_fine_validita = fields.Date(string="Fine validità Sconto")
    attivo = fields.Boolean(string="Sconto attivo Si/No")
