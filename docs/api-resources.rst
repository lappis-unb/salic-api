Resources
---------

Este módulo que contem as queries de acordo com cada entidade do projeto.

.. automodule:: salic_api.resources
    :members:

Fornecedor
~~~~~~~~~~

  .. autoclass:: salic_api.resources.FornecedorDetail
      :members:
  .. autoclass:: salic_api.resources.FornecedorList
      :members:
  .. autoclass:: salic_api.resources.ProdutoDetail
      :members:
  .. autoclass:: salic_api.resources.Produto
      :members:

Incentivador
~~~~~~~~~~~~

  .. autoclass:: salic_api.resources.DoacaoList
    :members:

  .. autoclass:: salic_api.resources.DoacaoDetail
    :members:

  .. autoclass:: salic_api.resources.IncentivadorDetail
    :members:

  .. autoclass:: salic_api.resources.IncentivadorList
    :members:

  .. autoclass:: salic_api.resources.IncentivadorQuery
    :members:

  .. autoclass:: salic_api.resources.DoacaoQuery
    :members:

Pre Projeto
~~~~~~~~~~~~~

  .. autoclass:: salic_api.resources.PreProjetoDetail
    :members:

  .. autoclass:: salic_api.resources.PreProjetoList
    :members:

  .. autoclass:: salic_api.resources.PreProjetoQuery
    :members:

Projeto
~~~~~~~

  .. autoclass:: salic_api.resources.Area
    :members:

  .. autoclass:: salic_api.resources.Captacao
    :members:

  .. autoclass:: salic_api.resources.ProjetoDetail
    :members:

  .. autoclass:: salic_api.resources.ProjetoList
    :members:

  .. autoclass:: salic_api.resources.Segmento
    :members:

Query
=====

    .. autoclass:: salic_api.resources.ProjetoQuery

    .. autoclass:: salic_api.resources.CaptacaoQuery

    .. autoclass:: salic_api.resources.AreaQuery

    .. autoclass:: salic_api.resources.SegmentoQuery

    .. autoclass:: salic_api.resources.CertidoesNegativasQuery

    .. autoclass:: salic_api.resources.DivulgacaoQuery

    .. autoclass:: salic_api.resources.DeslocamentoQuery

    .. autoclass:: salic_api.resources.DistribuicaoQuery

    .. autoclass:: salic_api.resources.ReadequacaoQuery

    .. autoclass:: salic_api.resources.AdequacoesPedidoQuery

  .. automethod:: salic_api.resources.normalize_sql

  .. automethod:: salic_api.resources.clean_sql_fields

  .. automethod:: salic_api.resources.payments_listing_sql

  .. automethod:: salic_api.resources.build_brand_link

  .. automethod:: salic_api.resources.build_file_link

Proponente
~~~~~~~~~~

  .. autoclass:: salic_api.resources.ProponenteDetail
    :members:

  .. autoclass:: salic_api.resources.ProponenteList
    :members:

  .. autoclass:: salic_api.resources.ProponenteQuery
    :members:

format_utils
~~~~~~~~~~~~

  .. automethod:: salic_api.resources.format_utils.cgccpf_mask

  .. automethod:: salic_api.resources.format_utils.sanitize

query
~~~~~

  .. autoclass:: salic_api.resources.Query
    :members:

resource
~~~~~~~~

  .. autoclass:: salic_api.resources.SalicResource
    :members:

  .. autoclass:: salic_api.resources.ListResource
    :members:

  .. autoclass:: salic_api.resources.DetailResource
    :members:

  .. autoclass:: salic_api.resources.InvalidResult
    :members:

serialization
~~~~~~~~~~~~~

  .. automethod:: salic_api.resources.serialization.listify_queryset

  .. automethod:: salic_api.resources.serialization.serialize

  .. automethod:: salic_api.resources.serialization.convert_atom

  .. automethod:: salic_api.resources.serialization.convert_object

  .. automethod:: salic_api.resources.serialization.to_xml

  .. automethod:: salic_api.resources.serialization.to_json

  .. automethod:: salic_api.resources.serialization.to_csv

test_resource
~~~~~~~~~~~~~

  .. autoclass:: salic_api.resources.TestResource
    :members:
