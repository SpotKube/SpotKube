import os

current_dir = os.getcwd()
logger_dir = os.path.join(current_dir, "logs")

async def read_log(log_file):
    log_file_path = os.path.join(logger_dir, log_file)
    
    os.makedirs(logger_dir, exist_ok=True)
    lines_to_read = 1000  # Number of lines to read from the end of the file
    
    try:
        with open(log_file_path, "r") as file:
            lines = file.readlines()
            log_contents = "".join(lines[-lines_to_read:])
        return {"data": log_contents, "status": 200, "message": "Log file read successfully"}

    except FileNotFoundError:
        return {"error_message": "Log file not found", "status": 404}

    except Exception as e:
        return {"error_message": str(e), "status": 500}


    
    