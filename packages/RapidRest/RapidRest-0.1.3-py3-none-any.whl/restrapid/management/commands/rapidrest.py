from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import os
import re

class Command(BaseCommand):
    help = 'Generate serializers and views for all models in the specified app'

    def add_arguments(self, parser):
        # Add an argument for app_name
        parser.add_argument('app_name', type=str, help='Name of the Django app')

    def handle(self, *args, **kwargs):
        # Get the app name from the arguments
        app_name = kwargs['app_name']

        # Check if the app exists
        try:
            app = apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f"App '{app_name}' not found. Please provide a valid app name.")

        # Get all models in the app
        models = app.get_models()

        for model in models:
            # Check if serializer and view already exist
            if not self.serializer_exists(app_name, model):
                self.generate_serializer(app_name, model)
            else:
                self.stdout.write(self.style.WARNING(f'Serializer for {model.__name__} already exists.'))

            if not self.view_exists(app_name, model):
                self.generate_view(app_name, model)
            else:
                self.stdout.write(self.style.WARNING(f'View for {model.__name__} already exists.'))

    def serializer_exists(self, app_name, model):
        # Define the path to the serializers file
        filepath = os.path.join(app_name, 'serializers.py')
        if not os.path.isfile(filepath):
            return False

        # Check if the serializer class exists in the file
        with open(filepath, 'r') as f:
            content = f.read()
            pattern = rf'class {model.__name__}Serializer\s*\(serializers\.ModelSerializer\):'
            return bool(re.search(pattern, content))

    def view_exists(self, app_name, model):
        # Define the path to the views file
        filepath = os.path.join(app_name, 'views.py')
        if not os.path.isfile(filepath):
            return False

        # Check if the view classes exist in the file
        with open(filepath, 'r') as f:
            content = f.read()
            list_create_pattern = rf'class {model.__name__}ListCreateView\s*\(generics\.ListCreateAPIView\):'
            retrieve_update_destroy_pattern = rf'class {model.__name__}RetrieveUpdateDestroyView\s*\(generics\.RetrieveUpdateDestroyAPIView\):'
            return (bool(re.search(list_create_pattern, content)) and 
                    bool(re.search(retrieve_update_destroy_pattern, content)))

    def generate_serializer(self, app_name, model):
        serializer_code = f"""
from rest_framework import serializers
from .models import {model.__name__}

class {model.__name__}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model.__name__}
        fields = '__all__'
"""
        self.write_to_file(app_name, 'serializers.py', serializer_code, model)

    def generate_view(self, app_name, model):
        view_code = f"""
from rest_framework import generics
from .models import {model.__name__}
from .serializers import {model.__name__}Serializer

class {model.__name__}ListCreateView(generics.ListCreateAPIView):
    queryset = {model.__name__}.objects.all()
    serializer_class = {model.__name__}Serializer

class {model.__name__}RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = {model.__name__}.objects.all()
    serializer_class = {model.__name__}Serializer
"""
        self.write_to_file(app_name, 'views.py', view_code, model)

    def write_to_file(self, app_name, filename, content, model):
        # Define the path to the file within the specified app's directory
        app_dir = os.path.join(os.getcwd(), app_name)
        filepath = os.path.join(app_dir, filename)

        # Ensure the app directory exists
        os.makedirs(app_dir, exist_ok=True)

        # Append or create the file as necessary
        with open(filepath, 'a') as f:
            # If the file already exists, add a newline before appending
            f.write('\n\n')  # Add two new lines for separation
            f.write(content)

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {filename} for {model.__name__}'))
