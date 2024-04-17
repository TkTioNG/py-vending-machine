# Simple Vending Machine

Simple vending machine written in python

## Setup

Build the project with docker:

```sh
docker compose build
docker compose up
```

Entering the container:

```sh
docker compose exec machine bash
```

Start the vending machine:

```sh
python main.py
```

## Basic Usage

To **reload**, press `r`.

To **purchase** a drink, press `p`.

To **quit**, press `q`.

To **return** to main page, press `b`.

When reloading, we only accept integer, _may be check for precise note value like 1, 5, 10, 20, 50, 100?_

When purchase a drink, press the drink number shown on the left of the drink list.

When all stock are gone, vending machine will be closed.

When there's any remaining balance in the machine, before closing or quitting, it will be return to user.
