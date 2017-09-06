import logging
import time

class logger:
    def  __init__(self,path,Clevel=logging.DEBUG,Flevel=logging.INFO):
        self.logger=logging.getLogger("无线WiFilog")
        self.logger.setLevel(logging.DEBUG)
        fmt=logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        ch=logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(Clevel)

        fh=logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
    def debug(self,message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)
now = time.strftime("%Y-%m-%d %H_%M_%S")
print(now)
logpath = './log/' + now + '.log'

L=logger(logpath)
print(L)
