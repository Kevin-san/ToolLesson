import pymysql
pymysql.install_as_MySQLdb()
import tools.common_logger as log
current_log=log.get_log('pdfweb', '/temp', 'pdfweb')