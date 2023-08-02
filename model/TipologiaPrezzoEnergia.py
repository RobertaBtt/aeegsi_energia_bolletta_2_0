# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class TipologiaPrezzoEnergia(models.Model):

    _name = "aeegsi_energia_bolletta.tipologia_prezzo_energia"

    etichetta = fields.Char(string="Etichetta Tipologia di Prezzo", required=True)
    descrizione = fields.Char(string="Descrizione Tipologia di Prezzo", required=True)
    durata_in_mesi = fields.Integer(string="Durata in mesi", default=1)

    @api.one
    def name_get(self):
        return self.id, self.descrizione
