import time

import pika
import json
from config import Config


def callback(ch, method, properties, body):
    task = json.loads(body)
    job_id = task["job_id"]
    image = task["image"]
    print(f"Job {job_id}. Processing {image}")

    time.sleep(5)

    print(f"Job {job_id} processing complete.")

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=Config.RABBIT_MQ_HOST,
        virtual_host="/",
        credentials=pika.credentials.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)))
    channel = connection.channel()
    channel.queue_declare(queue=Config.JOB_QUEUE_NAME)
    channel.basic_publish(exchange='', routing_key=Config.JOB_QUEUE_NAME, body=json.dumps({"job_id": job_id}))
    connection.close()


def run():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=Config.RABBIT_MQ_HOST,
        virtual_host="/",
        credentials=pika.credentials.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)))
    channel = connection.channel()

    channel.queue_declare(queue=Config.MODEL_QUEUE_NAME)
    channel.basic_consume(queue=Config.MODEL_QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print(' [MODEL QUEUE] Model service waiting for messages.')
    channel.start_consuming()


if __name__ == '__main__':
    run()
