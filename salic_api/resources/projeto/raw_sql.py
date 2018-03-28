from os import environ as env

SALIC_SCHEMAS = {
    'BDCORPORATIVO.scSAC',
    'BDCORPORATIVO.scCorp',
    'SAC.dbo',
    'sac.dbo',
    'Sac.dbo',
    'Agentes.dbo',
    'TABELAS.dbo',
}

use_sqlite = True if env.get('SQL_DRIVER', 'sqlite') == 'sqlite' else False

def normalize_sql(sql):
    """
    Normalize raw sql before sending it to the database.
    """
    if use_sqlite:
        return clean_sql_fields(sql)
    return sql


def clean_sql_fields(sql):
    """
    Remove all references to different databases from the SQL command.

    This commands replaces 'BDCORPORATIVO.scSAC', 'SAC.dbo', etc by empty
    strings.
    """
    for db in SALIC_SCHEMAS:
        sql = sql.replace(db + '.', '')
    return sql


def payments_listing_sql(idPronac, paginate):
    """
    Create SQL to query payment listings.
    """

    fmt = {'extra_selects': '', 'tail': '', 'extra_joins': ''}

    if idPronac is None:
        fmt.update({
            'extra_selects': PAYMENT_LISTING_PRONAC_SELECT,
            'extra_joins': PAYMENT_LISTING_JOIN_IDPRONAC,
        })
    else:
        fmt['extra_joins'] = PAYMENT_LISTING_JOIN_CGCCPF
        if paginate:
            fmt['tail'] = PAGINATION_SQL

    sql = PAYMENT_LISTING_SQL.format(**fmt)
    normalized_sql = normalize_sql(sql)
    return normalized_sql


PAYMENT_LISTING_PRONAC_SELECT = (
    '\n    Projetos.AnoProjeto + Projetos.Sequencial as PRONAC,'
)
PAYMENT_LISTING_JOIN_IDPRONAC = (
    '\n    JOIN SAC.dbo.Projetos AS Projetos ON c.idPronac = Projetos.IdPRONAC'
    '\n    LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente'
    '          WHERE (g.CNPJCPF LIKE :cgccpf)'
)
PAYMENT_LISTING_JOIN_CGCCPF = (
    '\n    LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente'
    '          WHERE (c.idPronac = :idPronac)'
)
PAYMENT_LISTING_SQL = """
SELECT
    d.Descricao as nome,
    b.idComprovantePagamento as id_comprovante_pagamento,
    a.idPlanilhaAprovacao as id_planilha_aprovacao,
    g.CNPJCPF as cgccpf,
    e.Descricao as nome_fornecedor,
    b.DtPagamento as data_aprovacao,{extra_selects}
    CASE tpDocumento
        WHEN 1 THEN ('Boleto Bancario')
        WHEN 2 THEN ('Cupom Fiscal')
        WHEN 3 THEN ('Guia de Recolhimento')
        WHEN 4 THEN ('Nota Fiscal/Fatura')
        WHEN 5 THEN ('Recibo de Pagamento')
        WHEN 6 THEN ('RPA')
        ELSE ''
    END as tipo_documento,
    b.nrComprovante as nr_comprovante,
    b.dtEmissao as data_pagamento,
    CASE
      WHEN b.tpFormaDePagamento = '1'
         THEN 'Cheque'
      WHEN b.tpFormaDePagamento = '2'
         THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
         THEN 'Saque/Dinheiro'
         ELSE ''
    END as tipo_forma_pagamento,
    b.nrDocumentoDePagamento nr_documento_pagamento,
    a.vlComprovado as valor_pagamento,
    b.idArquivo as id_arquivo,
    b.dsJustificativa as justificativa,
    f.nmArquivo as nm_arquivo
    FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
    INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
    LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
    LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
    LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
    LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo{extra_joins}

    ORDER BY data_pagamento{tail};
"""

if use_sqlite:
    PAGINATION_SQL = (
        '\n    LIMIT :limit OFFSET :offset'
    )
else:
    PAGINATION_SQL = (
        '\n    OFFSET :offset ROWS'
        '\n    FETCH NEXT :limit ROWS ONLY'
    )
