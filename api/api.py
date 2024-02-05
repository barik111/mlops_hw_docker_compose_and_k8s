import json
import os
import sys
from threading import Thread

from flask import Flask, jsonify, request
import pika
import uuid
from config import Config
from database import db
from job import Job

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
app.app_context().push()

with app.app_context():
    def start_rmq_connection():
        def callback(ch, method, properties, body):
            message = json.loads(body)
            job_id = message["job_id"]
            with app.app_context():
                job = Job.query.get(job_id)
                job.status = "completed"
                db.session.commit()

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Config.RABBIT_MQ_HOST,
            virtual_host="/",
            credentials=pika.credentials.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)))
        channel = connection.channel()

        channel.queue_declare(queue=Config.JOB_QUEUE_NAME)
        channel.basic_consume(queue=Config.JOB_QUEUE_NAME, on_message_callback=callback, auto_ack=True)

        print(' [JOB QUEUE] Api waiting for messages.')
        channel.start_consuming()


@app.route("/jobs", methods=["POST"])
def create_job():
    message = {
        "job_id": str(uuid.uuid4()),
        "image": request.json["image"]
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=Config.RABBIT_MQ_HOST,
        virtual_host="/",
        credentials=pika.credentials.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)))
    channel = connection.channel()
    channel.queue_declare(queue=Config.MODEL_QUEUE_NAME)
    channel.basic_publish(exchange="", routing_key=Config.MODEL_QUEUE_NAME, body=json.dumps(message))
    connection.close()

    db.session.add(Job(id=message["job_id"], status="in progress"))
    db.session.commit()

    return jsonify({"job_id": message["job_id"], "status": "in progress"})


@app.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify([j.serialize for j in Job.query.all()]), 200


@app.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    job = Job.query.get(job_id)
    return jsonify({"job_id": job_id, "status": job.status})


if __name__ == '__main__':
    try:
        thread_1 = Thread(target=start_rmq_connection)
        thread_1.start()
        thread_1.join(0)
        app.run(debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
