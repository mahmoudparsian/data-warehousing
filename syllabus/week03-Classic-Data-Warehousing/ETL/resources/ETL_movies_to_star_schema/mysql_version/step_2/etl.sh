TRANSACTION_DB="db_config_source.json"
STAR_SCHEMA_DB="db_config_target.json"
ETL_PROG="etl.py"
#
python3  ${ETL_PROG} ${TRANSACTION_DB} ${STAR_SCHEMA_DB}
