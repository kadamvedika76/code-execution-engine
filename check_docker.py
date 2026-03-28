import docker

client = docker.from_env()


try:
    client.ping()
    print("Docker:  Running")
except:
    print("Docker:  Not running")


images = client.images.list()
image_names = [
    tag for img in images 
    for tag in img.tags
]

if "judge:latest" in image_names:
    print("judge:latest image:  Found")
else:
    print("judge:latest image:  Not found")

containers = client.containers.list()
print(f"Running containers: {len(containers)}")

if len(containers) == 0:
    print("No containers running ")
else:
    for c in containers:
        print(f"→ {c.id[:12]} {c.status}")