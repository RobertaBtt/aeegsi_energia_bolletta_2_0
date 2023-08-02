# -*- coding: utf-8 -*-
__author__ = 'roberta@enermed.it'

from openerp import models, fields, api
from datetime import datetime
from decimal import *
from datetime import timedelta, date, datetime, time
from ..servizio_elaborato import SupportoServizioElaborato

class ServizioElaboratoTrasporto(models.Model):

    _inherit = "aeegsi_energia_bolletta.servizio_elaborato"

    def creaElaboratoTrasporto(self, dizionarioContratto, listaDictConsumoPeriodi):

        listaOggettiCreati = []

        listaOggettiCreati.extend( self.creaUC3V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC3F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC6V(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC6F(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaUC6P(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaPER33(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaPER75(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaTF(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaTP(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaTRASp(dizionarioContratto, listaDictConsumoPeriodi))

        listaOggettiCreati.extend( self.creaTE(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaMISF(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaMISV(dizionarioContratto, listaDictConsumoPeriodi))
        listaOggettiCreati.extend( self.creaCT(dizionarioContratto, listaDictConsumoPeriodi))

        ultimaLista = self.creaB(listaOggettiCreati, dizionarioContratto)
        listaOggettiCreati.extend(ultimaLista)

        return listaOggettiCreati

    def creaUC3V(self, dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'UC3V')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "UC3"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaUC3F(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'UC3F')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "UC3"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = (valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)

                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:

                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaUC6F(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'UC6F')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "UC6"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0 )/ float(valoreTrovato.tipo_valore_euro)

                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:

                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaUC6V(self, dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'UC6V')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "UC6"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaUC6P(self, dizionarioContratto, listaDictConsumoPeriodi):
        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'UC6P')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "potenza"
            codiceComponente = "UC6"

        if dizionarioContratto.has_key('potenza_contrattuale'):
            potenza_contrattuale = dizionarioContratto['potenza_contrattuale']

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0 ) / float(valoreTrovato.tipo_valore_euro)
                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = potenza_contrattuale
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] =  Decimal(corrUnitarioRounded * potenza_contrattuale).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaPER33(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'PER33')])
        valoreEnv = self.env['aeegsi_energia.valore']
        servizioElaborato = None

        if dizionarioContratto.has_key('potenza_disponibile'):
            potenza_disponibile = dizionarioContratto['potenza_disponibile']
            # Solo se potenza_disponibile é >= 16,5 faccio tutto il resto
            # Il calcolo della penale vale solo per potenza >= 16,5
            if potenza_disponibile > 16.5:
                if len(categoriaElaboratoList) == 1:
                    tipoComponente = "variabile"
                    codiceComponente = "PER"

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  None, None, None, 33, 75)

                    if valoreTrovato is not None:

                        if len(listaDictConsumoPeriodi) >=1:
                            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                                 if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                                    and dictConsumoPeriodo.has_key('kWh_F1')\
                                    and dictConsumoPeriodo.has_key('kWh_F2')\
                                    and dictConsumoPeriodo.has_key('kWh_F3')\
                                    and dictConsumoPeriodo.has_key('KVarh_F1')\
                                    and dictConsumoPeriodo.has_key('KVarh_F2')\
                                    and dictConsumoPeriodo.has_key('KVarh_F3'):

                                        # solo Fasce F1 e F2
                                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2']
                                        quantitaTotaleKVarh = dictConsumoPeriodo['KVarh_F1'] + dictConsumoPeriodo['KVarh_F2']

                                        if quantitaTotaleKVarh > quantitaTotaleKwhConsumo / 2.0:

                                            if quantitaTotaleKVarh > (0.75* quantitaTotaleKwhConsumo):
                                                penale33 =  (0.75 * quantitaTotaleKwhConsumo) - (0.33 * quantitaTotaleKwhConsumo)
                                            else:
                                                penale33 =  quantitaTotaleKVarh - (0.33 * quantitaTotaleKwhConsumo)

                                            quantitaPenale50Rounded = float(Decimal(penale33).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP))

                                            dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                                            dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                                            dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                                            dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                                            dizionarioServizioElaborato['quantita'] = quantitaPenale50Rounded
                                            dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)) * quantitaPenale50Rounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                            servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)

                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaPER75(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        servizioElaborato = None
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'PER75')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if dizionarioContratto.has_key('potenza_disponibile'):
            potenza_disponibile = dizionarioContratto['potenza_disponibile']
            # Solo se potenza_disponibile é >= 16,5 faccio tutto il resto
            # Il calcolo della penale vale solo per potenza >= 16,5
            if potenza_disponibile > 16.5:
                if len(categoriaElaboratoList) == 1:
                    tipoComponente = "variabile"
                    codiceComponente = "PER"

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  None, None, None, 75, 100)

                    if valoreTrovato is not None:

                        if len(listaDictConsumoPeriodi) >=1:
                            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                                 if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                                    and dictConsumoPeriodo.has_key('kWh_F1')\
                                    and dictConsumoPeriodo.has_key('kWh_F2')\
                                    and dictConsumoPeriodo.has_key('kWh_F3')\
                                    and dictConsumoPeriodo.has_key('KVarh_F1')\
                                    and dictConsumoPeriodo.has_key('KVarh_F2')\
                                    and dictConsumoPeriodo.has_key('KVarh_F3'):

                                        # solo Fasce F1 e F2
                                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2']
                                        quantitaTotaleKVarh = dictConsumoPeriodo['KVarh_F1'] + dictConsumoPeriodo['KVarh_F2']

                                        if quantitaTotaleKVarh > (0.75 * quantitaTotaleKwhConsumo) :

                                            penale75 = quantitaTotaleKVarh - (0.75 * quantitaTotaleKwhConsumo)

                                            if penale75 > 0:
                                                quantitaPenale75Rounded = float(Decimal(penale75).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP))

                                                dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                                                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                                                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                                                dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                                                dizionarioServizioElaborato['quantita'] = quantitaPenale75Rounded
                                                dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                                                dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)) * quantitaPenale75Rounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                                                dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                                                servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato



    def creaTF(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        valoreEnv = self.env['aeegsi_energia.valore']

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'b'),
            ('etichetta', '=', 'TF')
        ])

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "TF"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                    and dictConsumoPeriodo.has_key('kWh_F1')\
                    and dictConsumoPeriodo.has_key('kWh_F2')\
                    and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        corrUnitario = ( valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)

                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato


    def creaTP(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        valoreEnv = self.env['aeegsi_energia.valore']

        if dizionarioContratto.has_key('potenza_contrattuale'):
            potenza_contrattuale = dizionarioContratto['potenza_contrattuale']

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([
            ('categoria_id.lettera', '=', 'b'),
            ('etichetta', '=', 'TP')
        ])

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "potenza"
            codiceComponente = "TP"


        if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                        consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12
                        if consumoAnnuoPresunto < 0:
                            consumoAnnuoPresunto  = 0

                        dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                        valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dataInizioValidita, None, None, None, True)

                        if valoreTrovato is not None:
                            corrUnitario = (valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                            if float(valoreTrovato.tipo_valore_euro) == 1:
                                corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                            elif float(valoreTrovato.tipo_valore_euro) == 100:
                                corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                            dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                            dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                            dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                            dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                            dizionarioServizioElaborato['quantita'] = potenza_contrattuale
                            dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded  * potenza_contrattuale).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                            servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                            listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaTRASp(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        valoreEnv = self.env['aeegsi_energia.valore']

        if dizionarioContratto.has_key('potenza_contrattuale'):
            potenza_contrattuale = dizionarioContratto['potenza_contrattuale']

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'TRASp') ])

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "potenza"
            codiceComponente = "TRASp"


        if len(listaDictConsumoPeriodi) >=1:
                for dictConsumoPeriodo in listaDictConsumoPeriodi:
                    if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                        quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                        consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12
                        if consumoAnnuoPresunto < 0:
                            consumoAnnuoPresunto  = 0

                        valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                        if valoreTrovato is not None:
                            corrUnitario = (valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)
                            if float(valoreTrovato.tipo_valore_euro) == 1:
                                corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                            elif float(valoreTrovato.tipo_valore_euro) == 100:
                                corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                            dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                            dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                            dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                            dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                            dizionarioServizioElaborato['quantita'] = potenza_contrattuale
                            dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded  * potenza_contrattuale).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                            servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                            listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaTE(self, dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        dominioRicercaValore = []
        valoreEnv = self.env['aeegsi_energia.valore']
        tipoComponente = "variabile"
        codiceComponente = "TE"

        kwhRimanenti  = 0
        numGiorni = 0

        # Dovrebbe trovare tutti i valori della categoria T3 che sono 6 perché ci sono 6 scaglioni

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                numGiorni =  dictConsumoPeriodo['n_giorni']

                dataInizioValidita = date(day=1, month=1, year=int(dictConsumoPeriodo['al'][:4]))

                quantita900  = 0
                quantita1800 = 0
                quantita2640 = 0
                quantita3540 = 0
                quantita4440 = 0
                quantita4441 = 0
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1') and dictConsumoPeriodo.has_key('kWh_F2') and dictConsumoPeriodo.has_key('kWh_F3'):

                    kwhPeriodo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  900, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'TE900')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id

                        quantita900 =  float(Decimal((900 / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhPeriodo >= quantita900:
                            kwhRimanenti = kwhPeriodo - quantita900
                            dizionarioServizioElaborato['quantita'] = quantita900
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro))  * quantita900).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']
                        elif kwhPeriodo < quantita900 and kwhPeriodo > 0:
                            kwhRimanenti = 0
                            kwhPeriodoRounded = float(Decimal(kwhPeriodo).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhPeriodoRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhPeriodoRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  1800, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'TE1800')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id

                        quantita1800 =  float(Decimal (((1800 - 901)/365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))

                        if kwhRimanenti >= quantita1800:
                            kwhRimanenti = kwhRimanenti - quantita1800
                            dizionarioServizioElaborato['quantita'] = quantita1800
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro))  * quantita1800).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']
                        elif kwhRimanenti < quantita1800 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00
                            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  2640, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'TE2640')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        # elaboro il componente quota energia per il primo scaglione
                        quantita2640 = float(Decimal( ((2640 - 1801)/365.0 )*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita2640:
                            kwhRimanenti = kwhRimanenti - quantita2640
                            dizionarioServizioElaborato['quantita'] = quantita2640
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro))  * quantita2640).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita2640 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  3540, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'TE3540')])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        # elaboro il componente quota energia per il primo scaglione
                        quantita3540 = float(Decimal( ((3540-2641) / 365.0)*numGiorni).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita3540:
                            kwhRimanenti = kwhRimanenti - quantita3540
                            dizionarioServizioElaborato['quantita'] = quantita3540
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita3540).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita3540 and kwhRimanenti >0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  4440, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'TE4440') ])
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        quantita4440 = float(Decimal( ((4440-3541)/365.0)*numGiorni ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                        if kwhRimanenti >= quantita4440:
                            kwhRimanenti = kwhRimanenti - quantita4440
                            dizionarioServizioElaborato['quantita'] = quantita4440
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * quantita4440).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        elif kwhRimanenti < quantita4440 and kwhRimanenti > 0:
                            kwhRimanentiRounded = float(Decimal( kwhRimanenti ).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] =  Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                            kwhRimanenti = 0
                        elif kwhRimanenti == 0:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  4441, dataInizioValidita, None, None, None, True)

                    if valoreTrovato is not None:
                        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'TE4441') ])
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore / float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        if kwhRimanenti >= 0:
                            kwhRimanentiRounded = float(Decimal(kwhRimanenti).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP))
                            dizionarioServizioElaborato['quantita'] = kwhRimanentiRounded
                            dizionarioServizioElaborato['imponibile'] = Decimal((valoreTrovato.valore/ float(valoreTrovato.tipo_valore_euro)) * kwhRimanentiRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        else:
                            dizionarioServizioElaborato['quantita'] = 0
                            dizionarioServizioElaborato['imponibile'] = 0.00

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaMISF(self, dizionarioContratto, listaDictConsumoPeriodi):

        # Serve per l'arrotondamento
        setcontext(ExtendedContext)
        getcontext().clear_flags()
        listaServiziElaborato = []
        dizionarioServizioElaborato = {}
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'),('etichetta', '=', 'CMF')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "fisso"
            codiceComponente = "MISF"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  None, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)


                    if valoreTrovato is not None:
                        corrUnitario = (valoreTrovato.valore / 12.0) / float(valoreTrovato.tipo_valore_euro)

                        if float(valoreTrovato.tipo_valore_euro) == 1:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))
                        elif float(valoreTrovato.tipo_valore_euro) == 100:
                            corrUnitarioRounded = float(Decimal(corrUnitario).quantize(Decimal('1.0000'), rounding=ROUND_HALF_UP))

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = 1
                        dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitarioRounded
                        dizionarioServizioElaborato['imponibile'] = Decimal(corrUnitarioRounded).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']


                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaMISV(self,  dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'CMV')])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "MISV"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']
                    consumoAnnuoPresunto = quantitaTotaleKwhConsumo * 12

                    if consumoAnnuoPresunto < 0:
                        consumoAnnuoPresunto = 0

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  consumoAnnuoPresunto, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:

                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaCT(self, dizionarioContratto, listaDictConsumoPeriodi):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([ ('categoria_id.lettera', '=', 'b'), ('etichetta', '=', 'CT') ])
        valoreEnv = self.env['aeegsi_energia.valore']

        if len(categoriaElaboratoList) == 1:
            tipoComponente = "variabile"
            codiceComponente = "TRASe"

        if len(listaDictConsumoPeriodi) >=1:
            for dictConsumoPeriodo in listaDictConsumoPeriodi:
                if dictConsumoPeriodo.has_key('dal') and dictConsumoPeriodo.has_key('al') \
                        and dictConsumoPeriodo.has_key('kWh_F1')\
                        and dictConsumoPeriodo.has_key('kWh_F2')\
                        and dictConsumoPeriodo.has_key('kWh_F3'):

                    quantitaTotaleKwhConsumo = dictConsumoPeriodo['kWh_F1'] + dictConsumoPeriodo['kWh_F2'] + dictConsumoPeriodo['kWh_F3']

                    valoreTrovato = SupportoServizioElaborato.SupportoServizioElaborato.trovaValore\
                        (valoreEnv, tipoComponente, codiceComponente, dizionarioContratto,  None, dictConsumoPeriodo['dal'][:10], dictConsumoPeriodo['al'][:10], None, None, False)

                    if valoreTrovato is not None:
                        dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
                        dizionarioServizioElaborato['periodo_dal'] = dictConsumoPeriodo['dal']
                        dizionarioServizioElaborato['periodo_al'] = dictConsumoPeriodo['al']
                        dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
                        dizionarioServizioElaborato['quantita'] = quantitaTotaleKwhConsumo
                        dizionarioServizioElaborato['corrispettivo_unitario'] = valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro)
                        dizionarioServizioElaborato['imponibile'] = Decimal(valoreTrovato.valore/float(valoreTrovato.tipo_valore_euro) * quantitaTotaleKwhConsumo).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                        dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

                        servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
                        listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato

    def creaB(self, listaOggettiServizioElaborato, dizionarioContratto):

        dizionarioServizioElaborato = {}
        listaServiziElaborato = []
        totaleImponibileServizioB = 0
        totaleQuantitaServizioB = 0
        listaDateString = set()
        listaDateObj = []

        categoriaElaboratoList = self.env['aeegsi_energia_bolletta.categoria_elaborato'].search([('categoria_id.lettera', '=', 'b'),  ('etichetta', '=', 'B')])

        if len(listaOggettiServizioElaborato) !=0 and  len(categoriaElaboratoList) == 1:
            for servizioElaborato in listaOggettiServizioElaborato:
                if servizioElaborato is not None:
                    listaDateString.add(servizioElaborato.periodo_dal)
                    listaDateString.add(servizioElaborato.periodo_al)

                    totaleImponibileServizioB += servizioElaborato.imponibile

                    # Solo con una qualsiasi delle etichette di tipo variabile,
                    # salvo la quantita. Sarebbe stata la stessa cosa prendere un altro servizio di tipo variabile B
                    if servizioElaborato.categoria_elaborato_id.etichetta == "UC3V":
                        totaleQuantitaServizioB += servizioElaborato.quantita

            for data in listaDateString:
                listaDateObj.append(datetime.strptime(data, '%Y-%m-%d').date())

            listaDateObj.sort()

            dizionarioServizioElaborato['categoria_elaborato_id'] = categoriaElaboratoList[0].id
            dizionarioServizioElaborato['periodo_dal'] = listaDateObj[0]
            dizionarioServizioElaborato['periodo_al'] = listaDateObj[len(listaDateString)-1]
            dizionarioServizioElaborato['tipo_unita_misura_id'] = categoriaElaboratoList[0].tipo_unita_di_misura_id.id
            dizionarioServizioElaborato['iva'] = dizionarioContratto['iva']

            dizionarioServizioElaborato['quantita'] = totaleQuantitaServizioB
            if totaleQuantitaServizioB > 0:
                corrUnitario = totaleImponibileServizioB / totaleQuantitaServizioB
            else:
                corrUnitario = 0
            dizionarioServizioElaborato['corrispettivo_unitario'] = corrUnitario
            dizionarioServizioElaborato['imponibile'] = Decimal(totaleImponibileServizioB).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)

            servizioElaborato = super(ServizioElaboratoTrasporto,self).create(dizionarioServizioElaborato)
            listaServiziElaborato.append(servizioElaborato)

        return listaServiziElaborato
