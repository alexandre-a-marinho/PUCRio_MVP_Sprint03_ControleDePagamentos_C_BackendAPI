# Payments Control

MVP of the first Sprint of the graduate program in Software Engineering at PUC-Rio (**MVP Sprint 03**)

Author: Alexandre Alves Marinho

---
## How to execute:

It is strongly recommended to use virtual environments like [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).
 
You will need to have all the python libs listed in `requirements.txt` installed.
After cloning the repository, it is necessary to go to the root directory, through the terminal, in order to execute the commands described below.

The command below installs the dependencies/libraries, described in the `requirements.txt` file (Python v3.10.0):
```
(env)$ pip install -r requirements.txt
```
To run the API just run:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```
In development mode it is recommended to run using the reload parameter, which will restart the server
automatically after a source code change.
```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Open [http://localhost:5000/#/](http://localhost:5000/#/) in browser to check status and documentation of running API.

## How to execute using the Docker container

Be sure to have [Docker](https://docs.docker.com/engine/install/) installed and in execution in your machine.

Navigate to the directory containing the Dockerfile and requirements.txt in the terminal.
Run **as administrator** the following command to build the Docker image:

```
$ docker build -t rest-api .
```

Once the image is created, to run the container simply execute, **as administrator**, the following command:

```
$ docker run -p 5000:5000 rest-api
```

Once running, to access the API, simply open [http://localhost:5000/#/](http://localhost:5000/#/) in the browser.
