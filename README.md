# mlops_hw_docker_compose_and_k8s

1. docker tag mlops_hw_docker_compose_and_k8s-api:latest mlops_hw_docker_compose_and_k8s-api:1
2. docker tag mlops_hw_docker_compose_and_k8s-model:latest mlops_hw_docker_compose_and_k8s-model:1
3. minikube image load mlops_hw_docker_compose_and_k8s-api:1
4. minikube image load mlops_hw_docker_compose_and_k8s-model:1
5. kubectl apply -f rmq.yaml
6. kubectl apply -f postgres.yaml
7. kubectl apply -f model.yaml
8. kubectl apply -f api.yaml
9. minikube service api --url
10. [POST] http://127.0.0.1:61758/jobs 
    * body: {"image": "cat.jpg"}
    * response: { "job_id": "3b2d599d-caa5-4bfc-ae84-6359825ec2d8", "status": "in progress"}
11. [GET] http://127.0.0.1:61758/jobs
    * [
    {
        "id": "3b2d599d-caa5-4bfc-ae84-6359825ec2d8",
        "status": "completed"
    }
]
12. [GET] http://127.0.0.1:61758/jobs/3b2d599d-caa5-4bfc-ae84-6359825ec2d8
    * {
        "id": "3b2d599d-caa5-4bfc-ae84-6359825ec2d8",
        "status": "completed"
    }