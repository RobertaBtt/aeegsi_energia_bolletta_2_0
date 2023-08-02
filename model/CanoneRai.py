# -*- coding: utf-8 -*-

from openerp.tools.translate import _
from openerp import models, fields, api


class CanoneRai(models.Model):

    _name = "aeegsi_energia_bolletta.canone_rai"

    canone = fields.Float(string="Totale Canone (€)", required=True)
    n_mesi = fields.Integer(string = "Numero di mesi", required = True, digits=2)
    creata_il = fields.Date(string="Valore impostato il: ", required=True)
    data_inizio = fields.Date(string="Mese inizio: ", required=True)
    data_fine = fields.Date(string="Mese fine: ", required=True)
    attivo = fields.Boolean(string="Attivo Si/No", default=True)

    _order = 'creata_il desc'

    @api.one
    def name_get(self):
        return self.id, self.creata_il
