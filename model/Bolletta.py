# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api

#from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
#from psycopg2.extensions import   ISOLATION_LEVEL_AUTOCOMMIT
#from psycopg2.extensions import   ISOLATION_LEVEL_SERIALIZABLE
#from psycopg2.extensions import   ISOLATION_LEVEL_REPEATABLE_READ

class Bolletta(models.Model):

    _name = "aeegsi_energia.bolletta"
    _inherit = ['mail.thread']

    codice = fields.Char(string="Codice")
    data_emissione = fields.Date(string="Data emissione", required=True)
    data_scadenza = fields.Date(string="Data scadenza", required=True)
    servizio_elaborato_ids = fields.One2many('aeegsi_energia_bolletta.servizio_elaborato', 'bolletta_id', 'Righe servizio elaborato')   # Righe della fattura
    servizio_dettaglio_ids = fields.One2many('aeegsi_energia_bolletta.servizio_dettaglio', 'bolletta_id', 'Righe servizio dettaglio')   # Righe della fattura di dettaglio, raggruppa i servizi elaborati
    servizio_ids = fields.One2many('aeegsi_energia_bolletta.servizio', 'bolletta_id', 'Righe servizio')   # Righe della fattura semplice, raggruppa i servizi di dettaglio

    # Creazione ServiziElaborato

    def creaServizioElaboratoEnergia(self, dizionarioContratto, listaDictConsumoPeriodi, listaDictConsumoPeriodiPrecedente):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_elaborato'].creaElaboratoEnergia(dizionarioContratto, listaDictConsumoPeriodi, listaDictConsumoPeriodiPrecedente)
        return listaOggettiCreati

    def creaServizioElaboratoTrasporto(self, dizionarioContratto, listaDictConsumoPeriodi):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_elaborato'].creaElaboratoTrasporto(dizionarioContratto, listaDictConsumoPeriodi)
        return listaOggettiCreati

    def creaServizioElaboratoOneri(self, dizionarioContratto, listaDictConsumoPeriodi):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_elaborato'].creaElaboratoOneri(dizionarioContratto, listaDictConsumoPeriodi)
        return listaOggettiCreati

    def creaServizioElaboratoCanoneRai(self, dizionarioContratto):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_elaborato'].creaElaboratoCanoneRai(dizionarioContratto)
        return listaOggettiCreati

    # Creazione ServiziDettaglio
    def creaServizioDettaglioEnergia(self, listaOggettiServizioElaboratoEnergia):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_dettaglio'].creaDettaglioEnergia(listaOggettiServizioElaboratoEnergia)
        return listaOggettiCreati

    def creaServizioDettaglioTrasporto(self, listaOggettiServizioElaboratoTrasporto):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_dettaglio'].creaDettaglioTrasporto(listaOggettiServizioElaboratoTrasporto)
        return listaOggettiCreati

    def creaServizioDettaglioOneri(self, listaOggettiServizioElaboratoOneri):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_dettaglio'].creaDettaglioOneri(listaOggettiServizioElaboratoOneri)
        return listaOggettiCreati

    def creaServizioDettaglioCanoneRai(self, listaOggettiServizioElaboratoCanoneRai):
        listaOggettiCreati = self.env['aeegsi_energia_bolletta.servizio_dettaglio'].creaDettaglioCanoneRai(listaOggettiServizioElaboratoCanoneRai)
        return listaOggettiCreati

    # Creazione ServiziSemplice
    def creaServizioTrasporto(self, listaOggettiServizioDettaglioTrasporto):
        servizioTrasporto = self.env['aeegsi_energia_bolletta.servizio'].creaServizioTrasporto(listaOggettiServizioDettaglioTrasporto)
        return servizioTrasporto

    def creaServizioOneri(self, listaOggettiServizioDettaglioOneri):
        servizioOneri= self.env['aeegsi_energia_bolletta.servizio'].creaServizioOneri(listaOggettiServizioDettaglioOneri)
        return servizioOneri

    def creaServizioCanoneRai(self, listaOggettiServizioDettaglioCanoneRai):
        servizioCanoneRai = self.env['aeegsi_energia_bolletta.servizio'].creaServizioCanoneRai(listaOggettiServizioDettaglioCanoneRai)
        return servizioCanoneRai


    def getComunicazione(self, tipo):

         if not isinstance(self.id, models.NewId):

            comunicazione = self.env['aeegsi_energia_bolletta.conf_comunicazioni'].search( [
                ('company_id', '=', 1),
                ('tipo_id.tipo', '=', tipo)], limit=1 )
            if comunicazione is not None and comunicazione.id is not False:
                return comunicazione
            else: return None

         else: return None


    @api.model
    def create(self, vals):
        #self._cr._cnx.set_isolation_level(ISOLATION_LEVEL_REPEATABLE_READ)
        return super(Bolletta, self).create(vals)

    @api.one
    def name_get(self):
        return self.id, self.codice
