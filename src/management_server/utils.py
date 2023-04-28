import logging
import subprocess
import re

def get_logger(path, log_level=logging.DEBUG, log_file="log.log"):
    # Set up the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(f"{path}/{log_file}")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def format_terraform_error_message(error_message):
    # Replace escape characters with their printable equivalents
    error_message = error_message.replace('\n\n\n', '\n')
    error_message = error_message.replace('\n\n', '\n')
    error_message = error_message.replace('\u001b[1m', '')
    error_message = error_message.replace('\u001b[0m', '')
    error_message = error_message.replace('│\n \n', '')
    error_message = error_message.replace('╷\n\n', '')
    formatted_message = re.sub(r'\x1b\[\d+m', '', error_message)
    return str(formatted_message)

def rn_subprocess_cmd(command, cwd):
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error = result.stderr.decode('utf-8')
        raise Exception(error if error  else "Internal Server Error")
    return result.stdout.decode('utf-8')