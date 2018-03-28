PROJETOS_AREAS = {
    '_embedded': {
        'areas': [
            {
                '_links': {'self': 'v1/projetos/?area=1'},
                'codigo': '1',
                'nome': 'Artes Cênicas'
            },
            {
                '_links': {'self': 'v1/projetos/?area=2'},
                'codigo': '2',
                'nome': 'Audiovisual'
            },
            {
                '_links': {'self': 'v1/projetos/?area=3'},
                'codigo': '3',
                'nome': 'Música'
            },
        ],
    },
    '_links': {'self': 'v1/projetos/areas/'},
}
PROJETO_RESPONSE = {
    # Embedded data
    '_embedded': {
        'relacao_bens_captal': [
            {
                "Titulo": "Boleto Bancario",
                "vlTotal": 4665.1275000000005,
                "vlUnitario": 3.1415,
                "nrComprovante": "1",
                "Marca": "Descricao marca",
                "Especificacao": "Descricao item",
                "Fabricante": "Descricao fabricante",
                "dtPagamento": "2000-01-01",
                "Item": "Figurino 1",
                "Qtde": 1485
            }
        ],
        'marcas_anexadas': [
            {
                'id_arquivo': 1,
                'link': ''
            }
        ],
        'deslocamento': [
            {
                'uf_origem': 'UF 1',
                'uf_destino': 'UF 1',
                'pais_destino': 'Pais 1',
                'pais_origem': 'Pais 1',
                'municipio_destino': 'Municipio 1',
                'municipio_origem': 'Municipio 1',
                'quantidade': 2
            }
        ],
        'divulgacao': [
            {
                "veiculo": "Descricao 1",
                "peca": "Descricao 1"
            }
        ],
        'relatorio_fisco': [
            {
                "item": "Figurino 1",
                "perc_a_executar": 99.93,
                "valor_executado": 3.1415,
                "valor_programado": 4665.1275000000005,
                "perc_executado": 0.07,
                "id_planilha_etapa": 1,
                "qtd_programada": 1485,
                "unidade": "Planilha Unidade 1",
                "etapa": "Planilha Etapa 1"
            }
        ],
        'certidoes_negativas': [
            {
                'data_emissao': '2000-01-01',
                'data_validade': '2000-03-01',
                'descricao': None,
                'situacao': 'Não Pendente'
            }
        ],
        'relacao_pagamentos': [
            {
                'data_pagamento': '2000-01-01',
                'nome_fornecedor': 'Name 1',
                'nr_documento_pagamento': '1',
                'cgccpf': '1234',
                'data_aprovacao': '2000-02-02',
                'valor_pagamento': 2000.0,
                'nr_comprovante': '1',
                'justificativa': 'Descricao Justificativa',
                'tipo_documento': 'Boleto Bancario',
                'tipo_forma_pagamento': 'Cheque',
                'id_comprovante_pagamento': 1,
                'id_planilha_aprovacao': 1,
                'nm_arquivo': '1',
                'nome': 'Figurino 1',
                'id_arquivo': 1
            }
        ],
        'readequacoes': [
            {
                'data_avaliador': '2000-01-01 00:00:00',
                'data_solicitacao': '2000-01-01 00:00:00',
                'descricao_avaliacao': 'Descricao Avaliacao 1',
                'descricao_encaminhamento': 'Encaminhamento 1',
                'descricao_justificativa': 'Descricao Justificativa 1',
                'descricao_readequacao': 'Readequacao 1',
                'descricao_solicitacao': 'Solicitacao 1',
                'id_avaliador': 1,
                'id_readequacao': 1,
                'id_solicitante': 1,
                'id_tipo_readequacao': 1,
                'is_arquivo': 1,
                'nome_arquivo': '1',
                'si_encaminhamento': 1,
                'st_atendimento': 'Atendido',
                'st_estado': 'Estado 1'
            }
        ],
        'documentos_anexados': [],
        'distribuicao': [
            {
                'produto': 'Produto 1',
                'qtd_patrocinador': 0,
                'qtd_outros': 0,
                'receita_prevista': '',
                'posicao_logo': 'Descricao 1',
                'localizacao': 'Brazil',
                'segmento': 'Teatro',
                'preco_unitario_promocional': 'R$10',
                'qtd_venda_promocional': 0,
                'qtd_venda_normal': 0,
                'qtd_produzida': 0,
                'receita_promocional': '',
                'receita_normal': '',
                'area': 'Artes Cênicas',
                'preco_unitario_normal': 'R$100',
                'qtd_proponente': 0
            }
        ],
        'prorrogacao': [
            {
                'data_inicio': '2000-01-01',
                'usuario': 'nome1',
                'observacao': 'Observacao',
                'estado': 'Em analise',
                'data_final': '2000-03-01',
                'data_pedido': '2000-01-01',
                'atendimento': 'A'
            }
        ],
        'captacoes': [
            {
                'PRONAC': '20001234',
                'cgccpf': '1234',
                'data_recibo': '2000-01-01',
                'nome_doador': 'Nome 1',
                'nome_projeto': 'Test',
                'valor': 'CaptacaoReal'
            }
        ],
    },

    # Links
    '_links': {
        'fornecedores': 'v1/fornecedores/?pronac=20001234',
        'incentivadores': 'v1/incentivadores/?pronac=20001234',
        'self': 'v1/projetos/20001234',
        'proponente': 'v1/proponentes/30313233343536373839616263646566e0797636',
    },

    # Campos do objeto
    'PRONAC': '20001234',
    'UF': 'DF',
    'acessibilidade': 'Acessibilidade',
    'ano_projeto': '2000',
    'area': 'Artes Cênicas',
    'cgccpf': '1234',
    'data_inicio': '2000-01-01',
    'data_termino': '2000-02-01',
    'democratizacao': 'DemocratizacaoDeAcesso',
    'enquadramento': 'Artigo 26',
    'especificacao_tecnica': 'EspecificacaoTecnica 1',
    'estrategia_execucao': 'EstrategiadeExecucao 1',
    'etapa': 'EtapaDeTrabalho',
    'ficha_tecnica': 'FichaTecnica',
    'impacto_ambiental': 'ImpactoAmbiental 1',
    'justificativa': 'Justificativa 1',
    'mecanismo': 'Mecenato',
    'municipio': 'Cidade 1',
    'nome': 'Test',
    'objetivos': 'cultural',
    'outras_fontes': 0,
    'proponente': 'Nome 1',
    'providencia': 'nenhuma',
    'resumo': 'ResumoDoProjeto 1',
    'segmento': 'Teatro',
    'sinopse': 'Sinopse 1',
    'situacao': 'Descricao 1',
    'valor_aprovado': 1000,
    'valor_captado': 1000,
    'valor_projeto': 1000,
    'valor_proposta': 1000,
    'valor_solicitado': 1000,
}
INCENTIVADOR_RESPONSE = {
    'UF': 'UF 1',
    '_links': {
        'self': 'v1/incentivadores/30313233343536373839616263646566e0797636',
        'doacoes': 'v1/incentivadores/30313233343536373839616263646566e0797636/doacoes',
    },
    'cgccpf': '1234',
    'municipio': 'Cidade 1',
    'nome': 'Nome 1',
    'responsavel': 'Responsavel 1',
    'tipo_pessoa': 'juridica',
    'total_doado': 0.0,
}
FORNECEDOR_RESPONSE = {
    "cgccpf": "1234",
    "_links": {
        "self": "v1/fornecedores/30313233343536373839616263646566e0797636",
        "produtos": "v1/fornecedores/30313233343536373839616263646566e0797636/produtos"
    },
    "email": "email 1",
    "nome": "Name 1"
}
PROPONENTE_RESPONSE = {
    'nome': 'Nome 1',
    'cgccpf': '1234',
    '_links': {
        'self': 'v1/proponentes/30313233343536373839616263646566e0797636',
        'projetos': 'v1/projetos/?proponente_id=30313233343536373839616263646566e0797636'
    },
    'tipo_pessoa': 'juridica',
    'responsavel': 'Responsavel 1',
    'UF': 'UF 1',
    'total_captado': 1000,
    'municipio': 'Cidade 1',
}
PREPROJETO_RESPONSE = {
    'acessibilidade': 'Acessibilidade',
    'data_aceite': '2000-01-01',
    'data_arquivamento': '2000-03-01',
    'data_inicio': '2000-01-01',
    'data_termino': '2000-02-01',
    'democratizacao': 'DemocratizacaoDeAcesso',
    'especificacao_tecnica': 'EspecificacaoTecnica 1',
    'estrategia_execucao': 'EstrategiadeExecucao 1',
    'etapa': 'EtapaDeTrabalho',
    'ficha_tecnica': 'FichaTecnica',
    'id': 1,
    'impacto_ambiental': 'ImpactoAmbiental 1',
    'justificativa': 'Justificativa 1',
    'mecanismo': 'FNC',
    'nome': 'NomeProjeto 1',
    'objetivos': 'cultural',
    'resumo': 'ResumoDoProjeto 1',
    'sinopse': 'Sinopse 1',
    '_links': {
        'self': 'v1/propostas/1',
    },
}
CAPTACOES_RESPONSE = {
    '_embedded': {
        'captacoes': [
            {
                'PRONAC': '20001234',
                'cgccpf': '1234',
                'data_recibo': '2000-01-01',
                'nome_doador': 'Nome 1',
                'nome_projeto': 'Test',
                'valor': 'CaptacaoReal'
            }
        ]
    },
    '_links': {
        'first': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
        'last': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
        'self': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
        'next': 'v1/projetos/20001234/captacoes/?limit=100&offset=0',
    },
    'count': 1,
    'total': 1,
}
PRODUTOS_RESPONSE = {
    "total": 1,
    "count": 1,
    "_embedded": {
        "produtos": [
            {
                "id_planilha_aprovacao": 1,
                "justificativa": 'Descricao Justificativa',
                "data_pagamento": '2000-01-01',
                "nome": "Figurino 1",
                "cgccpf": "1234",
                "tipo_forma_pagamento": 'Cheque',
                "data_aprovacao": '2000-02-02',
                "valor_pagamento": 2000.0,
                "_links": {
                    "projeto": "v1/projetos/20001234",
                    "fornecedor": "v1/fornecedores/30313233343536373839616263646566e0797636"
                },
                "id_arquivo": 1,
                "nr_comprovante": '1',
                "nome_fornecedor": "Name 1",
                "id_comprovante_pagamento": 1,
                "tipo_documento": 1,
                "nr_documento_pagamento": '1',
                "nm_arquivo": '1',
                "PRONAC": "20001234",
            }
        ]
    },
    "total": 1,
    "_links": {
        "self": "v1/fornecedores/30313233343536373839616263646566e0797636/produtos/?limit=100&offset=0",
        "first": "v1/fornecedores/30313233343536373839616263646566e0797636/produtos/?limit=100&offset=0",
        "last": "v1/fornecedores/30313233343536373839616263646566e0797636/produtos/?limit=100&offset=0",
        "next": "v1/fornecedores/30313233343536373839616263646566e0797636/produtos/?limit=100&offset=0"
    }
}
