# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

VOLTAGES = [
    ('BT', 'Bassa Tensione'),
    ('MT', 'Media Tensione'),
    ('AT', 'Alta Tensione'),
    ('AAT', 'Altissima Tensione')
]



USE = [
    ('D', 'Domestico residente'),
    ('NR', 'Domestico non residente'),
    ('A', 'Altri usi'),
    ('IP', 'Illuminazione Pubblica')
]
IVA_SOURCE=[
    ('IvaCustom', 'Custom'),
    ('IvaContratto', 'Da Contratto')
]

class ConfigurazioneAltrePartite(models.Model):

    _name = "aeegsi_energia_bolletta.conf_altre_partite"

    descrizione = fields.Text(string="Descrizione Impostazione", required=True)

    #Valore é il numero che imposto in altre Partite
    valore = fields.Float(string = "Valore")

    cat_elaborato_id = fields.Many2one('aeegsi_energia_bolletta.categoria_elaborato', "Categoria (Elaborato)", required=True)
    provenienza_iva=fields.Selection(IVA_SOURCE, string="Provenienza IVA")
    #Iva = l'iva del valore, se non viene dal contratto
    iva = fields.Float(string="Iva", digits=(2,2))

    #Valori che utilizzo per la ricerca
    tipo_tensione = fields.Selection(VOLTAGES, string="Tipo di tensione")
    use = fields.Selection(USE, string="Tipo di Uso")

    creata_il = fields.Date(string="Data creazione Configurazione", required=True)
    _order = 'creata_il desc'


    @api.one
    def name_get(self):
        return self.id, self.descrizione

    @api.model
    def get_by_category(self, category_id, tipo_tensione = None, use=None ):
        """

        :param category_id:
        :param tipo_tensione:
        :param use:
        :return: oggetto intero
        """

        recordConAltrePartite = None

        if tipo_tensione is not None and use is not None:
            recordConAltrePartite = self.env['aeegsi_energia_bolletta.conf_altre_partite'].search([
                ('cat_elaborato_id', '=', category_id),
                ('tipo_tensione', '=', tipo_tensione),
                ('use', '=', use)], limit = 1)
        elif tipo_tensione is None and use is None:
            recordConAltrePartite = self.env['aeegsi_energia_bolletta.conf_altre_partite'].search([(
            'cat_elaborato_id', '=', category_id,

            )], limit = 1)

        return recordConAltrePartite