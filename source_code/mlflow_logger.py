import mlflow
def set_attributes(attributes):
    mlflow.set_tags(attributes)

def start_experiment():
    mlflow.set_experiment("RAG_experiment")
    return mlflow.start_run()

def log_params(params):
    mlflow.log_params(params)

def log_metrics(metrics):
    mlflow.log_metrics(metrics)

def log_artifacts(query, chunks, response):
    mlflow.log_text(query, "query.txt")
    mlflow.log_text(str(chunks), "retrieved_chunks.txt")
    mlflow.log_text(response, "response.txt")