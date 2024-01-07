---
layout: page
---

#### Why?
I've been doing remote work since 2019.  At one gig, _everybody_ had a great looking 
setup for their online meetings.  So I looked at what was available on the market,
like "nanoleaf" and "govee" products, but ultimately decided to build my own.
I'm putting this guide together to provide a resource to anyone else that wants to build something similar.


Here is a short list of the problems I "solved":
- **developement env**
  - Who wants to `ssh` into a RPI and hack around with `vim` or `nano`?  Not this guy!
    I want to use VSCode and need all the syntax highlighting, linting, and type correction I can get.
    Also, I wanted to write and build on my desk, and deploy to the RPi.
- **dependency management**
  - Pretty new to Python.  Not really clear on the dependency management story here.  Settled on Poetry.
    Is it supposed to be this slow? :/
- **project organization**
  - Followed a pretty neat project (Pi Light)
- **API and web server**
  - FastAPI and Uvicorn
- **hardware**
  - What LEDs do you use? What size power supply?  How should you wire up the RPi?
- **physical hexagons**
  - MDF molding, plexiglass, tablesaw, routing table, 2 custom jigs, tricky glue-up, 
    sanding, painting, soldering 336 individually addressable LEDs

#### Installation
If you have `docker-compose` and `docker` on your system, you can clone the repo and `docker-compose up` and get started.  Sort of.
Its a start.

```bash
#clone the repository
git clone http://github.com/dakerr/rpi-hex-control
cd ./rpi-hex-control

# build the container
docker-compose build

# or build, (re)create, start, and attach to a container for a service 
docker-compose up
```

This creates a docker container using a `rasbian/bullseye` image from `navikey` then adds some build essentials, python3, pip and poetry.
The `docker-compose.yaml` actually binds your local development folder to the file system in the container and exposes port 9000 for the API.
But **most importantly**, it elevates the privilege so that the code can *actually* write to the RPi SPI. You don't need to do this quite 
yet but trust me, its a thing.  I would have had to resolder the RPi if I didn't find this bit!


Next, open up the project in VSCode.  You may need to add `Dev Containers` from the VSCode marketplace.

```bash
  shift-cmd-P > Dev Containers: Attach to a Running Container
```
Select the container you are running.  This will install vscode-server in that container. The entrypoint to the container 
started the main app with `poetry`.  You should be able to select your Python interpreter.

```bash
  shift-cmd-P > Select Python Interpreter
```
And now you have syntax highlighting!

#### A few more things...
- The image built _is_ an linux/arm image but its not compatible with the Raspberry Pi Zero. :(
- vscode-server is not compatible with ARMhf
- to build on the RPi you need to install: git, docker, and docker-compose then clone a