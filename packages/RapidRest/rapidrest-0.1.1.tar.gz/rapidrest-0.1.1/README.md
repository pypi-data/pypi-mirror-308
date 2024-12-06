# RapidRest

**RapidRest** is a Django management command package designed to speed up the creation of REST serializers and views for Django models. By running a simple command, it generates serializers and views for each model in a specified Django app, making it easy to get started with Django REST API development.

## Features

- Automatically generates ModelSerializers for Django models.
- Creates ListCreateAPIView and RetrieveUpdateDestroyAPIView classes for each model.
- Detects existing serializers and views to prevent duplicates.

## Installation

To install RapidRest from PyPI (after you publish it), use:
```bash
pip install RapidRest
