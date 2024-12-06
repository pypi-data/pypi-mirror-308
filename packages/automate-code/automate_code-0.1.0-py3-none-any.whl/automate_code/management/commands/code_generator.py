from django.core.management.base import BaseCommand
import os
import importlib
from django.conf import settings

class Command(BaseCommand):
    help = "Automatically generates views and serializers for a given app's models."

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help="The name of the app for which to generate views and serializers.")

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        
        # Dynamically import the models from the specified app
        try:
            models_module = importlib.import_module(f"{app_name}.models")
        except ModuleNotFoundError:
            self.stdout.write(self.style.ERROR(f"App '{app_name}' not found."))
            return

        # Get all models from the app's models module
        model_names = [attr for attr in dir(models_module) if not attr.startswith("_")]
        model_classes = [getattr(models_module, name) for name in model_names if isinstance(getattr(models_module, name), type)]

        if not model_classes:
            self.stdout.write(self.style.WARNING(f"No models found in app '{app_name}'."))
            return

        # Define paths for the serializers and views files
        serializers_path = os.path.join(settings.BASE_DIR, app_name, "serializers.py")
        views_path = os.path.join(settings.BASE_DIR, app_name, "views.py")

        # Check if the files exist, if not, create them
        if not os.path.exists(serializers_path):
            with open(serializers_path, "w") as serializers_file:
                serializers_file.write("from rest_framework import serializers\n")
                serializers_file.write("from .models import *\n\n")

        if not os.path.exists(views_path):
            with open(views_path, "w") as views_file:
                views_file.write("from rest_framework import generics\n")  # Ensure generics is imported
                views_file.write("from .models import *\n")
                views_file.write("from .serializers import *\n\n")

        # Read existing code in serializers.py to check for duplicates
        with open(serializers_path, "r") as file:
            existing_serializers_code = file.read()

        # Append to `serializers.py`
        with open(serializers_path, "a") as serializers_file:
            # Check each model and generate serializers if they don't already exist
            for model in model_classes:
                model_name = model.__name__
                if f"class {model_name}Serializer" not in existing_serializers_code:
                    serializers_file.write(f"class {model_name}Serializer(serializers.ModelSerializer):\n")
                    serializers_file.write(f"    class Meta:\n")
                    serializers_file.write(f"        model = {model_name}\n")
                    serializers_file.write(f"        fields = '__all__'\n\n")

        # Read existing code in views.py to check for duplicates
        with open(views_path, "r") as file:
            existing_views_code = file.read()

        # Append to `views.py`
        with open(views_path, "a") as views_file:
            # Add imports if they are missing (ensure we do not overwrite)
            if 'from rest_framework import generics' not in existing_views_code:
                views_file.write("from rest_framework import generics\n")
            if 'from .models import *' not in existing_views_code:
                views_file.write("from .models import *\n")
            if 'from .serializers import *' not in existing_views_code:
                views_file.write("from .serializers import *\n")

            # Check each model and generate views if they don't already exist
            for model in model_classes:
                model_name = model.__name__
                if f"class {model_name}ListCreateView" not in existing_views_code:
                    views_file.write(f"\nclass {model_name}ListCreateView(generics.ListCreateAPIView):\n")
                    views_file.write(f"    queryset = {model_name}.objects.all()\n")
                    views_file.write(f"    serializer_class = {model_name}Serializer\n")

                if f"class {model_name}RetrieveUpdateDestroyView" not in existing_views_code:
                    views_file.write(f"\nclass {model_name}RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):\n")
                    views_file.write(f"    queryset = {model_name}.objects.all()\n")
                    views_file.write(f"    serializer_class = {model_name}Serializer\n")

        self.stdout.write(self.style.SUCCESS(f"Appended serializers and views for models in '{app_name}' app."))
