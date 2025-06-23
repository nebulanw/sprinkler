from sprinkler.db import config, log_sql, metrics

db_config = config.Database("config/config.json")
#db_log = log.Database("config/log.json")
db_log = log_sql.Database("config/log.sqlite3")
db_metrics = metrics.Database("config/metrics.json")
