# Payments Control

MVP of the first Sprint of the graduate program in Software Engineering at PUC-Rio (**MVP Sprint 01**)

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
