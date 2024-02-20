#!/usr/bin/env python3.11

import docker
import random
import argparse
import time
import os

def terminate_containers(docker_client, container_ids):
    try:
        for container_id in container_ids:
            docker_client.containers.get(container_id).stop()
        return True
    except Exception as e:
        print("Error terminating containers:", e)
        return False

def main():
    parser = argparse.ArgumentParser(description="Docker Sabotage - Simulate chaos by terminating Docker containers")
    parser.add_argument("--count", type=int, choices=range(1, 6), default=1, help="Number of containers to terminate (1-5)")
    args = parser.parse_args()

    # Create logs directory if not exists
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    docker_client = docker.from_env()

    try:
        containers = [container.id for container in docker_client.containers.list()]
        containers_to_terminate = random.sample(containers, min(args.count, len(containers)))
        print("Terminating containers:", containers_to_terminate)
        if terminate_containers(docker_client, containers_to_terminate):
            print("Termination initiated. Waiting for containers to stop...")
            # Wait for containers to stop
            while any(container_id in containers_to_terminate for container_id in [container.id for container in docker_client.containers.list()]):
                time.sleep(1)
                print("Waiting for containers to stop...")
            print("Termination completed.")

            # Write results to log file
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            log_file = os.path.join(logs_dir, f"{timestamp}.log")
            with open(log_file, "w") as f:
                f.write("Termination results:\n")
                f.write("Containers terminated:\n")
                for container_id in containers_to_terminate:
                    f.write(f"{container_id}\n")
            print(f"Termination results saved to {log_file}")

            exit(0)
        else:
            exit(1)
    except Exception as e:
        print("Error:", e)
        exit(1)

if __name__ == "__main__":
    main()
