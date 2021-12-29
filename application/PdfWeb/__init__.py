import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
import alvintools.common_logger as log
current_log=log.get_log('pdfweb', '/temp', 'pdfweb')