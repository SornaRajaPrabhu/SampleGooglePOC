import logging
import time

class log_information:

    def log(self):
        current_time = time.strftime("%Y_%m_%d-%I_%M_%S_%p")
        #filepath = filepath.replace("\\", "\\\\")
        #filepath = filepath + "\\\\" + str(current_time)+".txt"
        filepath = str(current_time)+".txt"
        logging.basicConfig(
            filename=filepath,
            level=logging.INFO,
            filemode="w",
            format='%(asctime)s -- %(message)s'
        )
        log_info = logging.getLogger(__name__)
        return log_info
