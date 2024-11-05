import runpod
from queue_processor import QueueProcessor

request_processor = QueueProcessor()

def handler(job):
    infer_props = job["input"]
    response = request_processor.process_request(infer_props=infer_props)
    return response

runpod.serverless.start({"handler": handler})