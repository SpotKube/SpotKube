import logging
import subprocess
import re
import os

def get_logger(path, log_level=logging.DEBUG, log_file="log.log"):
    # # Set up the logger
    # logger = logging.getLogger(__name__)
    # logger.setLevel(log_level)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler = logging.FileHandler(f"{path}/{log_file}")
    # file_handler.setLevel(log_level)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    # # return logger
    # Check if log file exists
    # Create the directory if it doesn't exist
    os.makedirs(path, exist_ok=True)
    
    log_file_path = os.path.join(path, log_file)
    if not os.path.exists(log_file_path):
        # Create the log file if it doesn't exist
        open(log_file_path, 'a').close()

    # Set up the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file_path)
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

def run_subprocess_cmd(command, cwd):
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
    if result.returncode != 0:
        error = result.stderr.decode('utf-8')
        raise Exception(error if error  else "Internal Server Error")
    return output
    

def run_subprocess_popen_cmd(command, cwd):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    while proc.poll() is None:
        line = proc.stdout.readline()
        print(line.strip())

    output, error = proc.communicate()
    print(output.strip())
    if proc.returncode != 0:
        print(error.strip())
        raise Exception(error.strip() if error.strip() else "Internal Server Error")
    
    return output.strip()