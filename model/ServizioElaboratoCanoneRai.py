# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import datetime
from decimal import *
from datetime import date, datetime

class ServizioElaboratoCanoneRai(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_elaborato"

    def creaElaboratoCanoneRai(self, dizionarioContratto):

        listaOggettiCreati = []
        listaOggettiCreati.extend( self.creaCanoneRai(dizionarioContratto))

        return listaOggettiCreati

    def creaCanoneRai(self, dizionarioContratto):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        listaServiziElaborato = []

        if dizionarioContratto.has_key('canone_rai_quantita') \
            and dizionarioContratto.has_key('canone_rai_unita')\
            and dizionarioContratto.has_key('canone_rai_dal')\
            and dizionarioContratto.has_key('canone_rai_al'):

            dizionarioServizioElaborato = {}

            categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'h'), ('etichetta', '=', 'RAI')])

            if len(categoriaElaboratoList) == 1:
                dataDal = dizionarioContratto['canone_rai_dal']
                dataAl = dizionarioContratto['canone_rai_al']

                if not isinstance(dataDal, date):
                    if len(dataDal) == 10:
                        dataDal = datetime.strptime(dataDal, '%Y-%m-%d').date()
                    else:
                        dataDal = datetime.strptime(dataDal, '%Y-%m-%d %H:%M:%S').date()

                if not isinstance(dataAl, date):
                    if len(dataAl) == 10:
                        dataAl = datetime.strptime(dataAl, '%Y-%m-%d').date()
                    else:
                        dataAl = datetime.strptime(dataAl, '%Y-%m-%d %H:%M:%S').date()

                imponibile  = Decimal(dizionarioContratto['canone_rai_unita'] * dizionarioContratto['canone_rai_quantita']).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

                dizionarioServizioElaborato['periodo_dal'] = dataDal
                dizionarioServizioElaborato['periodo_al'] = dataAl
                dizionarioServizioElaborato['corrispettivo_unitario'] = dizionarioContratto['canone_rai_unita']
                dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                dizionarioServizioElaborato['quantita'] = dizionarioContratto['canone_rai_quantita']
                dizionarioServizioElaborato['imponibile'] = imponibile

                if categoriaElaboratoList.iva_compresa:
                    dizionarioServizioElaborato['iva'] = 0
                else:
                    dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                servizioElaborato = super(ServizioElaboratoCanoneRai,self).create(dizionarioServizioElaborato)
                listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

