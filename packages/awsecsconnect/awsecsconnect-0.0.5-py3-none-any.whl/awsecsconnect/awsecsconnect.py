import inquirer
import boto3
import subprocess


def ask(name, choices):
    q = [
        inquirer.List(
            name=name,
            message="Select {}:".format(name).title(),
            choices=choices
        )
    ]
    a = inquirer.prompt(q)[name]
    return a


def get_containers(cluster_arn, task_arn):
    client = boto3.client('ecs')
    task = client.describe_tasks(cluster=cluster_arn, tasks=[task_arn])['tasks'][0]
    container_choices = []
    for container in task['containers']:
        container_choices.append(container['name'])
    return container_choices


def main():
    client = boto3.client('ecs')

    # Find Cluster
    cluster_list = client.list_clusters()['clusterArns']
    cluster_descriptions = client.describe_clusters(clusters=cluster_list)['clusters']
    cluster_choices = tuple((cluster['clusterName'], cluster['clusterArn']) for cluster in cluster_descriptions)
    cluster = ask('cluster', cluster_choices)

    # Find Service
    service_list = client.list_services(cluster=cluster)['serviceArns']
    service_descriptions = client.describe_services(cluster=cluster, services=service_list)['services']
    service_choices = tuple((service['serviceName'], service['serviceArn']) for service in service_descriptions)
    service = ask('service', service_choices)

    # Find Task
    task_list = client.list_tasks(cluster=cluster, serviceName=service)['taskArns']
    task_descriptions = client.describe_tasks(cluster=cluster, tasks=task_list)['tasks']
    task_choices = tuple(("{} - Containers: {} [Created: {}]| ".format(task['taskArn'], len(task['containers']), task['createdAt']), task['taskArn']) for task in task_descriptions)
    task = ask('task', task_choices)

    # Find Container
    container_list = client.describe_tasks(cluster=cluster, tasks=[task])['tasks'][0]['containers']
    container_choices = tuple((container['name'], container['name']) for container in container_list)
    container = ask('container', container_choices)

    print("Connecting to {} in {}".format(container,cluster))

    subprocess.run('aws ecs execute-command '
                   '--cluster {} '
                   '--task {} '
                   '--container {} '
                   '--command "/bin/bash" '
                   '--interactive'.format(cluster, task, container), shell=True)

if __name__ == "__main__":
    main()
