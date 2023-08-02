# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class Sconto(models.Model):

    _name = "aeegsi_energia_bolletta.sconto"

    descrizione = fields.Text(string="Descrizione Sconto", required=True)
    valore = fields.Float(string = "Valore")
    categoria_id = fields.Many2one('aeegsi_energia_bolletta.categoria_sconto', "Tipo sconto")
    cat_elaborato_id = fields.Many2one('aeegsi_energia_bolletta.categoria_elaborato', "Riga Elaborato Bolletta", required=True)

    @api.one
    def name_get(self):
        return self.id, self.descrizione


    @api.model
    def create(self, vals):


        if not vals['valore'] and vals['cat_elaborato_id']:

            categElaboratoObj = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search( [ ('id', '=', vals['cat_elaborato_id']) ])
            if categElaboratoObj:
                if categElaboratoObj.etichetta == 'SCKWH' or categElaboratoObj.etichetta=='SCPERC':
                    raise models.except_orm('Error', 'Per questa tipologia di sconto (%s) e\' necessario inserire un valore. '
                                                     'Puoi personalizzarlo in seguito nella scheda \'Sconti\' del contratto' %(categElaboratoObj.descrizione))

        sconto = super(Sconto, self).create(vals)
        return sconto

    @api.multi
    def write(self, vals):


        if vals.has_key('valore'):
            if vals['valore'] == 0:
                categElaboratoObj = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search( [ ('id', '=', vals['cat_elaborato_id']) ])
                if categElaboratoObj:
                    if categElaboratoObj.etichetta == 'SCKWH' or categElaboratoObj.etichetta=='SCPERC':
                        raise models.except_orm('Error', 'Per questa tipologia di sconto (%s) e\' necessario inserire un valore. '
                                                     'Puoi personalizzarlo in seguito nella scheda \'Sconti\' del contratto' %(categElaboratoObj.descrizione))

        else:
            if self.valore == 0:
                if vals.has_key('cat_elaborato_id'):
                    categElaboratoObj = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search( [ ('id', '=', vals['cat_elaborato_id']) ])
                else:
                    categElaboratoObj = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search( [ ('id', '=', self.cat_elaborato_id.id) ])
                if categElaboratoObj:
                    if categElaboratoObj.etichetta == 'SCKWH' or categElaboratoObj.etichetta=='SCPERC':
                        raise models.except_orm('Error', 'Per questa tipologia di sconto (%s) e\' necessario inserire un valore. '
                                                     'Puoi personalizzarlo in seguito nella scheda \'Sconti\' del contratto' %(categElaboratoObj.descrizione))


        sconto = super(Sconto, self).write(vals)
        return sconto