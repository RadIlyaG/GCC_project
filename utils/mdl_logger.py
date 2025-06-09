import logging
from html import escape

#_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_format = f"%(asctime)s - [%(levelname)s] -  %(message)s"

class HtmlFormatter(logging.Formatter):
    def format(self, record):
        message = escape(super().format(record))
        color = {
            'DEBUG': '#e0e0e0',
            'INFO': '#d9edf7',
            'WARNING': '#fcf8e3',
            'ERROR': '#f2dede',
            'CRITICAL': '#f2b1b1',
        }.get(record.levelname, '#ffffff')
        #return f'<tr style="background-color:{color}"><td>{record.asctime}</td><td>{record.levelname}</td><td>{message}</td></tr>\n'
        return f'<div style="background-color:{color}; padding:4px; margin:2px 0;">' \
               f'<strong>{record.asctime}</strong> [{record.levelname}] {message}</div>'


def get_file_handler(log_file):
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    # file_handler.stream.write('<html><head><meta charset="utf-8"></head><body>\n')
    # file_handler.stream.write('<table border="1" cellspacing="0" cellpadding="4">\n')
    # file_handler.stream.write('<tr><th>Time</th><th>Level</th><th>Message</th></tr>\n')
    file_handler.stream.write('<html><head><meta charset="utf-8"></head>\n') #<body style="font-family:monospace;">

    #file_handler.setFormatter(logging.Formatter(_log_format))
    formatter = HtmlFormatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    import atexit
    def close_html():
        #file_handler.stream.write('</table></body></html>\n')
        file_handler.stream.write('</body></html>\n')
        file_handler.close()

    atexit.register(close_html)
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

def setup_logger(log_file='log.html'):
    logger = logging.getLogger()
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(log_file))
    logger.addHandler(get_stream_handler())
    return logger
