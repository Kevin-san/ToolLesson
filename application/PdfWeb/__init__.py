import pymysql
pymysql.install_as_MySQLdb()
import alvintools.common_logger as log
current_log=log.get_log('pdfweb', '/temp', 'pdfweb')