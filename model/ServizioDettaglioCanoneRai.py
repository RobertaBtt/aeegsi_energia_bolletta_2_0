# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

class ServizioDettaglioCanoneRai(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_dettaglio"

    def creaDettaglioCanoneRai(self, listaOggettiServizioElaboratoCanoneRai):

        print "Crea Servizio Dettaglio Canone Rai"

        dizionarioServizioDettaglio = {}
        listaServiziDettaglio = []

        for servizioElaborato in listaOggettiServizioElaboratoCanoneRai:

            # Attenzione ! Si sta presupponendo che la riga con lettera h compaia una sola volta !
            if servizioElaborato.categoria_elaborato_id.categoria_id.lettera == 'h':

                sottoCategoriaCanoneRai = self.env['aeegsi_energia_bolletta.sotto_categoria'].search([('descrizione', '=', 'Canone di Abbonamento alla Televisione per uso privato'),('categoria_id.lettera', '=', 'h')]).id

                dizionarioServizioDettaglio['periodo_dal'] = servizioElaborato.periodo_dal
                dizionarioServizioDettaglio['periodo_al'] = servizioElaborato.periodo_al
                dizionarioServizioDettaglio['tipo_unita_misura_id'] = servizioElaborato.tipo_unita_misura_id.id


                dizionarioServizioDettaglio['sotto_categoria_id'] = sottoCategoriaCanoneRai
                dizionarioServizioDettaglio['quantita'] = servizioElaborato.quantita
                dizionarioServizioDettaglio['corrispettivo_unitario'] = servizioElaborato.corrispettivo_unitario
                dizionarioServizioDettaglio['imponibile'] = servizioElaborato.imponibile
                dizionarioServizioDettaglio['iva'] = servizioElaborato.iva

                servizioDettaglio = super(ServizioDettaglioCanoneRai,self).create(dizionarioServizioDettaglio)
                listaServiziDettaglio.append(servizioDettaglio)

        return  listaServiziDettaglio

