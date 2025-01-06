---
title: "First Steps"
description: ""
summary: ""
weight: 110
sidebar:
  open: true
---

I try to follow GitOps and treat all infrastructure as code, this Homelab uses a combination of Packer VM templates, OpenTofu for provisioning VM's, Docker for running everything, Ansible for running playbooks on all hosts at once, and Actions for automating repeated tasks. That being said this is a mixed repository for various sorts of purposes and thus there is no easy way to get started. This is not a project that can be easily copy/pasted and am only posting this for the philosophies and techniques used in a Homelab.

The first thing to do would be to install tools. Here are install instructions for services used:

## Docker
The Docker install script I run on my hosts is:

```bash
curl -fsSL https://get.docker.com | sudo sh
```

This installs Docker Engine (v2) along with Docker Compose

> [!NOTE]
> You cannot use `docker-compose` commands and need to add a space to make it `docker compose`

## Ansible

For Ubuntu:

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

## OpenTofu
For Ubuntu:
```bash
# Download the installer script:
curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
# Alternatively: wget --secure-protocol=TLSv1_2 --https-only https://get.opentofu.org/install-opentofu.sh -O install-opentofu.sh

# Give it execution permissions:
chmod +x install-opentofu.sh

# Please inspect the downloaded script

# Run the installer:
./install-opentofu.sh --install-method deb

# Remove the installer:
rm -f install-opentofu.sh
```


## Packer
For Ubuntu;
```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
```

```bash
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
```

```bash
sudo apt-get update && sudo apt-get install packer
```

## VCS
You can use Github as this is the easiest way of getting started, however in the self-hosted nature of this Homelab I have chosen to use Forgejo and host my VCS system myself. There are few drawbacks to using this, such as Actions not being an exact 1to1 of Github Actions

See the FAQ for why Forgejo is used as opposed to Gitlab or Gitea.

Install instructions for Forgejo are [here](https://forgejo.org/docs/latest/admin/installation/)

## Loki (logs)

A great video to get setup with Loki is available here