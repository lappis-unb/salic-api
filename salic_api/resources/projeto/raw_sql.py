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
