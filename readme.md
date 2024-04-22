# Kleines Projekt um ein Kunstobjekt zu analysieren

## Installation

Install poetry

Windows:
`(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
-> https://python-poetry.org/docs/#installing-with-the-official-installer

Install requirements

```
cd ./src/
poetry install
```

For GPU accelation

```
conda install numba & conda install cudatoolkit
```

ggf. werden die https://www.microsoft.com/de-de/download/details.aspx?id=40784 benötigt, wenn die libzbar-64.dll fehlt

## Starten

```
python .\src\qrcode.py
```

Benötigt Python 3.11

## Hintergrund des Projekts

## ToDo
