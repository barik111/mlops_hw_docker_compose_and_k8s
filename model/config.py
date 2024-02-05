import os


class Config:
    RABBIT_MQ_HOST = os.environ.get('RABBIT_MQ_HOST') or 'localhost'
    RABBITMQ_USER = os.environ.get('RABBITMQ_USER') or 'rmuser'
    RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS') or 'rmpassword'
    MODEL_QUEUE_NAME = os.environ.get('MODEL_QUEUE_NAME') or 'model_q'
    JOB_QUEUE_NAME = os.environ.get('JOB_QUEUE_NAME') or 'job_q'
