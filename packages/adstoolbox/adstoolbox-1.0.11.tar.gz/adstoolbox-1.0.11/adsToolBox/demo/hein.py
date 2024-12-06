from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql
from adsToolBox.dbPgsql import dbPgsql

logger = Logger(Logger.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source = dbPgsql({'database':env.PG_DWH_DB
                    , 'user':env.PG_DWH_USER
                    , 'password':env.PG_DWH_PWD
                    , 'port':env.PG_DWH_PORT
                    , 'host':env.PG_DWH_HOST}, logger)
source.connect()
logger.set_connection(source, logger.INFO)

logger.info("TEST")
logger.debug("TEST")
logger.warning("WARNING")
logger.error("ERROR")
logger.custom_log(21, "custom level")

logger.log_close("Succès?", "Fermeture des logs")

logger.info("Encore un test")

logger.enable(logger.DEBUG, logger.INFO, True)

logger.debug("Cela devrait s'afficher mais ne pas être inséré")
logger.enable(logger.INFO, logger.DEBUG, False)

logger.debug("Cela devrait s'insérer mais ne pas être affiché")