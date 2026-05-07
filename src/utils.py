import logging
import json
from datetime import datetime

def get_logger(name):
    """Configura un logger estándar para el pipeline."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s: %(asctime)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def generate_execution_summary(stage_name, total_in, total_out, start_time):
    """Genera un reporte de ejecución en formato JSON."""
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    summary = {
        "pipeline_stage": stage_name,
        "status": "SUCCESS",
        "timestamp": end_time.isoformat(),
        "metrics": {
            "records_read": total_in,
            "records_written": total_out,
            "records_discarded": total_in - total_out,
            "duration_seconds": duration
        }
    }
    return json.dumps(summary, indent=4)
