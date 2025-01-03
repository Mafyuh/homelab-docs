---
title: "First Steps"
description: ""
summary: ""
date: 2023-09-07T16:06:50+02:00
draft: false
weight: 110
---

## Docker
The Docker install script I run on my hosts is:

```bash
curl -fsSL https://get.docker.com | sudo sh
```

This installs Docker Engine (v2) along with Docker Compose

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}} You cannot use `docker-compose` commands and need to add a space to make it `docker compose` {{< /callout >}}

