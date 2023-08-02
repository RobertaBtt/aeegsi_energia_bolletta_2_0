{
    'name': "AEEGSI Energia - Bolletta 2.0",
    'version': "1.0",
    'description': """Bolletta 2.0 per l'Energia (AEEGSI)
=======================================================""",

    'author': " Roberta B, roberta@enermed.it",
    'website': "http://www.enermed.it",
    'category': "Sales, Energy, Invoice, Bolletta 2.0",
    'summary': 'AEEGSI Gestione Fatturazione 2.0 Energia Elettrica',
    'depends': ['aeegsi_energia', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/categoria.xml',
        'data/sotto_categoria_a.xml',
        'data/sotto_categoria_b.xml',
        'data/sotto_categoria_c.xml',
        'data/sotto_categoria_d.xml',
        'data/sotto_categoria_g.xml',
        'data/sotto_categoria_h.xml',
        'data/sotto_categoria_f.xml',

        'data/tipo_componente.xml',
        'data/tipo_comunicazione.xml',
        'data/tipo_unita_misura.xml',
        'data/categoria_elaborato_a.xml',
        'data/categoria_elaborato_b.xml',
        'data/categoria_elaborato_c.xml',
        'data/categoria_elaborato_d.xml',
        'data/categoria_elaborato_g.xml',
        'data/categoria_elaborato_h.xml',
        'data/categoria_elaborato_f.xml',

        'data/categoria_sconto.xml',
        'data/tipologia_prezzo_energia.xml',
        'data/tipo_mercato.xml',
        'data/sequence_bolletta.xml',
        'data/tipo_tensione.xml',
        'data/canone_rai_default.xml',

        'view/categoria_view.xml',
        'view/sotto_categoria_view.xml',
        'view/categoria_elaborato_view.xml',
        'view/categoria_sconto_view.xml',
        'view/sconto_view.xml',
        'view/tipologie_prezzo_energia_view.xml',
        'view/costo_acquisto_energia_view.xml',
        'view/tipo_unita_misura_view.xml',
        'view/tipo_mercato_view.xml',
        'view/bolletta_view.xml',
        'view/servizio_view.xml',
        'view/servizio_elaborato_view.xml',
        'view/servizio_dettaglio_view.xml',
        'view/tipo_tensione_view.xml',
        'view/tipo_componente_view.xml',
        'view/tipo_componente_view.xml',
        'view/canone_rai.xml',
        'view/config_comunicazioni_view.xml',
        'view/config_comunicazioni_tipo_view.xml',
        'view/config_altre_partite_view.xml',
        'view/main_view.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True
}