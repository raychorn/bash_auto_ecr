# Auto-ECR for Bash

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Automates the Docker Push for AWS ECR via git bash for Windows 10. This assumes your paths are setup correctly.

## Getting Started <a name = "getting_started"></a>

Not gonna work in Windows via "git bash"

### Prerequisites

Requires Docker without sudo.

Add the docker group if it doesn't already exist:

 sudo groupadd docker

Add the connected user "$USER" to the docker group. Change the user name to match your preferred user if you do not want to use your current user:

 sudo gpasswd -a $USER docker

Either do a "newgrp docker" or log out/in to activate the changes to groups.

### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.

## Usage <a name = "usage"></a>

Add notes about how to use the system.

(c). Copyright 2021, Ray C Horn, All Rights Reserved.
