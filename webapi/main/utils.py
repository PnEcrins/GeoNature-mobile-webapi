import logging
from operator import itemgetter
import uuid

from django.db import connections, transaction, IntegrityError, DatabaseError
from django.conf import settings
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


class QueryBuildError(Exception):
    pass


class SynchronizeError(Exception):
    pass


def commit_transaction(database_id):
    """
    Commit the transaction
    """
    transaction.commit_unless_managed(using=database_id)
    logger.debug(_("GeoNature SQL: COMMIT"))


def check_connection(database_id):
    """
    Check if connexion to database is active
    """
    try:
        cursor = connections[database_id].cursor()
        return True
    except:
        return False


def query_db(sqlquery, database_id):
    """
    Executes a single query on the GeoNature database defined in project settings.
    Returns a `cursor`

    sqlquery -- a SQL statement
    """
    # Connect to correct DB
    cursor = connections[database_id].cursor()
    # Execute SQL
    logger.debug(_("GeoNature SQL: %s") % sqlquery)
    cursor.execute(sqlquery)
    return cursor


def sync_db(objects, table_infos, database_id):
    """
    From a specified list of objects, executes equivalent insert or update
    statements on the gr@ce database.

    objects -- a list of dicts, as used in ``build_sync_query()``
    """
    logger.info(_("Synchronize %s objects") % len(objects))
    sid = transaction.savepoint()
    try:
        for feature in objects:
            q = build_sync_query(feature, table_infos)
            cursor = query_db(q, database_id)
        return cursor
    except (IntegrityError, DatabaseError), e:
        logger.error(e)
        logger.info(_("ROLLBACK"))
        transaction.savepoint_rollback(sid)
        raise SynchronizeError(str(e))


def build_sync_query(datafields, table_infos, table_name=None):
    """
    Builds a SQL statement from a dict of (fields, values).

    datafields -- a dict with field names and related values.
    table_name -- the SQL table name (Default: check if `datafields` has an item `table_name`)
    """
    if table_name is None:
        if 'table_name' in datafields:
            table_name = datafields.pop('table_name')
        else:
            raise QueryBuildError(_("Table name cannot be determined"))

    # Lower-case
    table_name = table_name.lower()
    datafields = dict((k.lower(), v) for k, v in datafields.iteritems())

    # Get column ID for the current table
    id_col = table_infos.get(table_name).get('id_col')

    updates = []
    for field, value in datafields.items():
        if value != None:
            value = unicode(value).replace("`", "'")   # Single quotes
            if "ST_" not in value:  # Do not escape PostGIS functions
                value = unicode(value).replace("'", "''")  # Double quotes
                value = unicode(value).replace("%", "%%")  # Double %
                value = "'%s'" % value
        else:
            value = "NULL_VALUE"
        updates.append((field, value))

    sql_string = ""

    # Retreive a new ID from the table
    id_col_string = ""
    if id_col:
        id_col_string = " RETURNING %s" % id_col

    sql_string = u"INSERT INTO %s (%s) VALUES (%s) %s" % (table_name,
                                                          ', '.join(
                                                              map(itemgetter(0), updates)),
                                                          ', '.join(
                                                              map(itemgetter(1), updates)),
                                                          id_col_string)
    # Manage null values
    sql_string = sql_string.replace("'NULL_VALUE'", "Null")
    sql_string = sql_string.replace("NULL_VALUE", "Null")
    return sql_string
