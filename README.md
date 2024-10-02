# LoL analytics website

![width:500px](docs/../docs/assets/concept.png)

## Setup

Create a virtual environment, activate and install the requirements:

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Setup the local sqlite db by running:

```
make setup
```

and then start the website by running:

```
make website
```