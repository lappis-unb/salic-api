.. image:: https://travis-ci.org/lappis-unb/salic-api.svg?branch=master
   :target: https://travis-ci.org/lappis-unb/salic-api
   :alt: Build status

.. image:: https://codecov.io/gh/lappis-unb/salic-api/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/lappis-unb/salic-api
   :alt: Code coverage

.. image:: https://media.readthedocs.org/static/projects/badges/passing.svg
   :target: https://salic-api.readthedocs.io/pt/latest/
   :alt: Documentation

.. image:: https://api.codeclimate.com/v1/badges/864270a3891b6750927e/maintainability
   :target: https://codeclimate.com/github/lappis-unb/salic-api/maintainability
   :alt: Maintainability


API aberta para o sistema
`SALIC <http://salic.cultura.gov.br/cidadao/consultar>`_. Tem por
objetivo expor os dados de projetos da lei Rouanet. A API está implantada em
http://api.salic.cultura.gov.br/doc/ e possui uma documentação para o
usuário no formato OpenAPI/Swagger.

O projeto ainda se encontra em fase de **homologação**, sujeito ainda a muitas
alterações, reformulações e atualizacões.


Requisitos
----------

A aplicação foi testada em ambientes LINUX com distribuições Debian, Archlinux e
Ubuntu. A implantação é feita utilizando Docker/Docker Compose ou Docker/Rancher.
O ambiente de desenvolvimento utiliza uma conexão com um banco de dados local
em Sqlite, onde podemos testar a aplicação com dados sintéticos.

A instância principal do Salic-API se conecta no banco de dados MS SQL Server
no Ministério da Cultura.


Instalação
----------

Recomendamos que o desenvolvimento seja feito no virtualenv.

Virtualenv
----------

Git clone + virtualenv + pip:

Instale o virtualenvwrapper::

    $ sudo apt-get install virtualenvwrapper
    $ virtualenvwrapper.sh
    $ source `which virtualenvwrapper.sh`
    $ mkvirtualenv -p /usr/bin/python3 salic-api
    $ workon salic-api

Clone o repositorio::

    $ git clone https://github.com/lappis-unb/salic-api

Instale as dependencias::

    $ python setup.py develop
    $ pip install -e ".[dev]"

Inicialize o banco de desenvolvimento antes de rodar a aplicação::

    $ inv db -f
    $ inv run

Não esqueça de rodar os testes com frequência::

    $ inv test

Docker
------

Para executar o ambiente utilizando o Docker execute os seguintes comandos::

    $ docker build -t salic-api .
    $ docker run -it --name salic-api -p 5000:5000 -v $PWD:/app salic-api

Para executar os testes com o docker execute o seguinte comando::

    $ docker run -it --name salic-api -p 5000:5000 -v $PWD:/app salic-api inv test

Docker Compose
--------------

O sistema possui dois docker-compose, um para o ambiente de desenvolvimento e
outro para o ambiente de produção, para escolher qual docker compose usar
passe o arquivo docker-compose.dev.yml ou docker-compose.prod.yml na flag '-f'
no comando docker-compose, como no exemplo a seguir::

    $ docker-compose -f docker-compose.dev.yml
    ou
    $ docker-compose -f docker-compose.prod.yml

Para executar o ambiente utilizando o docker-compose execute os seguintes
comandos::

    $ docker-compose -f [docker-compose file] build
    $ docker-compose -f [docker-compose file] up

Dependências básicas
--------------------

-  ``python-dev``
-  ``python-pip``
-  ``freetds-bin``
-  ``freetds-dev``
-  ``libxml2-dev``
-  ``libxslt1-dev``
-  ``libz-dev``
-  ``unixodbc-dev``


Configuração
------------

Edite o arquivo **salic-api/app/example_config.py** de acordo com seu
ambiente. Edite o arquivo **salic-api/app/general_config.py** apontando
o arquivo de configuração a ser usado.


Documentação
------------

A documentação da API é feita  de 2 formas:

* `SWAGGER <https://swagger.io/>`_

  * SWAGGER está sendo usado para documentar os `endpoints` do projeto. Seus arquivos estáticos estão na pasta:

    **salic-api/salic_api/static**

  * A documentação em produção pode ser acessada através desse link:

    `Documentação ENDPOINTS <http://api.salic.cultura.gov.br/doc/>`_.

* `SPHINX <http://www.sphinx-doc.org/en/master/>`_

  * Sphinx está sendo usado para a documentação do projeto como um todo, aproveitando as *docstrings* no código e também acrescentando informações nos arquivos de documentação que estão na pasta `docs/` no formato rst.

  * A documentação em produção pode ser acessada através desse link:

    `Documentação API <https://salic-api.readthedocs.org/pt/latest/>`_.

  * Para construir a documentação do SPHINX é necessário criar uma pasta que irá conter os arquivos de documentação.

    Crie a pasta `build` na raiz do projeto.

    .. code-block:: shell

      mkdir build

    Construa a documentação na pasta criada:

    .. code-block:: shell

      sphinx-autobuild docs build/docs

    Para acessar a documentação acesse:

    **localhost:8000**

Licença
-------

Licensed under the `GPL
License <http://www.gnu.org/licenses/gpl.html>`__.

.. |Open Source Love| image:: https://badges.frapsoft.com/os/gpl/gpl.svg?v=102
   :target: http://www.gnu.org/licenses/gpl.html
