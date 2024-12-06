import inquirer
import boto3
import subprocess
import argparse
import sys


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

def handle_exception(exc_type, exc_value, exc_traceback):
    print(f"Error: {exc_value}")

def main():
    # Handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--profile',
        type=str,
        help="Specify the AWS profile to use",
        default=None
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Show full stack trace on error",
    )
    args = parser.parse_args()

    if not args.verbose:
        sys.excepthook = handle_exception

    if args.profile:
        print(f"Using profile: {args.profile}")
        profile_arg = "--profile {}".format(args.profile)
        client = boto3.Session(profile_name=args.profile).client('ecs')
    else:
        print("No profile specified. Using default profile.")
        profile_arg = ""
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
                   '--interactive '
                   '{}'.format(cluster, task, container, profile_arg), shell=True)

if __name__ == "__main__":
    main()
