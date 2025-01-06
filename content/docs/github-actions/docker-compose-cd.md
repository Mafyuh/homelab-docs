---
title: "Docker Compose CD"
description: ""
summary: ""
draft: false
weight: 910
toc: true
---
Similar to Flux or ArgoCD in Kubernetes, this is my implementation of Continuous Deployment using Docker with Docker Compose.

This implementation is entirely custom and built for my Homelab with numerous hosts. It has gone through 3 re-iterations, and probably will again in the future.

The whole idea is I just want to merge a PR, and have my infrastructure update itself automatically. 
##  Current Implementation 

Link to current workflow https://git.mafyuh.dev/mafyuh/iac/src/branch/main/.forgejo/workflows/CD.yml

### Breakdown

I have various Docker hosts each with it's own Docker Compose stack. This setup allows me to have as many hosts as I want, just with a mapping to a DNS name.

1. Only runs on merged Pull Requests
2. Runs my custom Docker image `mafyuh/ansible-bws` 
3. Runs logic to determine which Docker Compose stack has been edited
4. Extracts the folder and maps it to a host (static mapping)
5. Reach out to Bitwarden Secrets for Ansible Hosts (hide IP addresses from Git)
6. Map those secrets to system env variables
7. Create Ansible hosts file on the Runner
8. Creates SSH private key on Runner (from Bitwarden)
9. Runs [Docker CD Ansible Playbook](https://git.mafyuh.dev/mafyuh/iac/src/branch/main/ansible/playbooks/deploy-docker.yml) passing through the `$folder`, `$target_host` and `$bws_access_key`

### Playbook Steps

Now that we know which Stack and which host to SSH into, we basically just SSH into the correct machine, grab the required `.env` variables from Bitwarden, create the `.env` file, and redeploy the Stack.

1. Only runs on the `$target_host`
2. Read's predefined `secret-mappings.yml` which maps the `.env` variables for the `$target_host` with Bitwarden Secrets
3. Sets the required `.env` file in the stack folder
4. Runs Git Pull on the repo to update it and so it's aware of the new Docker image version
5. Uses Ansible built in Docker Compose plugin to restart the services
6. The best way I have found other than having no errors on the previous step is to run `docker compose ps` to ensure the new version is running.

## Previous Implementations
### Initial Implementation
Ran [this script](https://git.mafyuh.dev/mafyuh/Auto-Homelab/src/branch/main/scripts/dccd.sh) on each Docker hosts via Crontab, it basically just ran `git pull` and `docker compose up -d` and I had it run every 30 minutes. It did work, just with too many caveats.

1. Hit Docker rate limits multiple times daily
2. Wasn't very IaC
3. Infrastructure could be out of date by 30 mins so didn't feel like a true CD option.

### 2nd Implementation 

N8N via webhooks

Before I understood Git and Bash fully, I used N8n to essentially just filter the folder name to host and SSH in and run `git pull` and `docker compose up -d`

Env variables were just set on the host manually.

Link to JSON for N8N import https://git.mafyuh.dev/mafyuh/Auto-Homelab/src/branch/main/scripts/CD.json
### 3rd Implementation

Link to workflow: https://git.mafyuh.dev/mafyuh/Auto-Homelab/src/branch/main/.forgejo/workflows/CD.yml

Used AWX to run Ansible playbooks, just ended up hitting my AWX API to run the playbook, then hit another endpoint to grab the logs for the run. The playbook at this point was basically just to SSH in and run `git pull` and `docker compose up -d`

Link to playbook: https://git.mafyuh.dev/mafyuh/ansible-playbooks/src/branch/main/deploy.yml#

Env variables were just set on the host manually.

The logic for hitting the API was changed as it wasn't always catching logs here https://git.mafyuh.dev/mafyuh/iac/src/commit/c7a98bcf020389c7d025c9a3e512d271a9e3427d/.forgejo/workflows/CD.yml

This is where I switched to raw Ansible using a custom Docker image and where the current implementation starts.

## Why this vs. alternatives?

While tools like Watchtower, Duin, and Harbormaster offer convenient container update functionalities, they require access to the Docker socket. Providing access to the Docker socket is generally considered a security risk as it grants significant control over the host system.

If you have ever had watchtower break something you know the annoyance. Also what if the update fails? How are you gonna know if there's breaking changes? After or before breaking a database?

Harbormaster almost pulls this off, however it requires changing path mappings in order to work, which is a no-go for me.

Duin just notifies you if there's an update, which you then manually update it. Again this is a no-go.

Portainer also allows for Docket CD just with a simple toggle, however I choose not do this as there are no logs of the redeployment, I would need to add Portainer Agents to all hosts and pass through the Docker socket from each, and I prefer to keep all logs in Git as this is where I try to keep IaC. 

This Homelab prioritizes security and adopts a more controlled approach to updates by leveraging Git and Renovate bot. This combination allows for automated dependency updates and controlled deployments through a dedicated CI/CD pipeline, ensuring both security and stability.