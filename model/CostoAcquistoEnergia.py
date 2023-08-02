# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class CostoAcquistoEnergia(models.Model):

    _name = "aeegsi_energia_bolletta.costo_acquisto_energia"

    tipologia_prezzo_id = fields.Many2one('aeegsi_energia_bolletta.tipologia_prezzo_energia', "Tipologia Prezzo applicato")

    F0 = fields.Float(string="Prezzo F0", digits=(1, 6)) #Sarebbe fascia unica per i contatori che non consentono le fasce
    F1 = fields.Float(string="Prezzo F1", digits=(1, 6))
    F2 = fields.Float(string="Prezzo F2", digits=(1, 6))
    F3 = fields.Float(string="Prezzo F3", digits=(1, 6))
    peak = fields.Float(string="Prezzo di picco (peak)", digits=(1, 6))
    off_peak = fields.Float(string="Prezzo fuori picco (off-peak)", digits=(1, 6))
    mese = fields.Integer(string="Mese di applicazione del prezzo")
    anno = fields.Integer(string="Anno di applicazione del prezzo")
