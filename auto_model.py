#!/usr/bin/env python3
"""
Auto Model Documentation Generator
This script automatically extracts model information from Django models.py files
and generates a markdown documentation table.
"""

import os
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional


class ModelField:
    """Represents a field in a Django model"""
    
    def __init__(self, name: str, field_type: str, **kwargs):
        self.name = name
        self.field_type = field_type
        self.max_length = kwargs.get('max_length')
        self.null = kwargs.get('null', False)
        self.blank = kwargs.get('blank', False)
        self.unique = kwargs.get('unique', False)
        self.default = kwargs.get('default')
        self.choices = kwargs.get('choices')
        self.related_name = kwargs.get('related_name')
        self.on_delete = kwargs.get('on_delete')
        self.upload_to = kwargs.get('upload_to')
        self.auto_now_add = kwargs.get('auto_now_add', False)
        self.auto_now = kwargs.get('auto_now', False)
    
    def __str__(self) -> str:
        field_str = f"{self.name}: {self.field_type}"
        
        if self.max_length:
            field_str += f"({self.max_length})"
        
        constraints = []
        if self.null:
            constraints.append("null")
        if self.blank:
            constraints.append("blank")
        if self.unique:
            constraints.append("unique")
        if self.auto_now_add:
            constraints.append("auto_now_add")
        if self.auto_now:
            constraints.append("auto_now")
        
        if constraints:
            field_str += f" [{', '.join(constraints)}]"
        
        if self.choices:
            choices_str = ", ".join([f"'{choice[0]}'" for choice in self.choices])
            field_str += f" choices: [{choices_str}]"
        
        if self.related_name:
            field_str += f" related_name='{self.related_name}'"
        
        if self.on_delete:
            field_str += f" on_delete={self.on_delete}"
        
        if self.upload_to:
            field_str += f" upload_to='{self.upload_to}'"
        
        return field_str


class DjangoModel:
    """Represents a Django model"""
    
    def __init__(self, name: str, app_name: str):
        self.name = name
        self.app_name = app_name
        self.fields: List[ModelField] = []
        self.meta_options: Dict[str, Any] = {}
        self.docstring: Optional[str] = None
    
    def add_field(self, field: ModelField):
        self.fields.append(field)
    
    def __str__(self) -> str:
        return f"{self.app_name}.{self.name}"


class ModelParser:
    """Parser for Django model files"""
    
    def __init__(self):
        self.models: List[DjangoModel] = []
    
    def parse_field_arguments(self, args: List[ast.expr], keywords: List[ast.keyword]) -> Dict[str, Any]:
        """Parse field arguments and keywords"""
        kwargs = {}
        
        # Handle positional arguments
        if args:
            if len(args) > 0:
                # First arg is usually max_length for CharField
                if isinstance(args[0], ast.Constant):
                    kwargs['max_length'] = args[0].value
        
        # Handle keyword arguments
        for keyword in keywords:
            key = keyword.arg
            if key is None:
                continue
                
            if isinstance(keyword.value, ast.Constant):
                kwargs[key] = keyword.value.value
            elif isinstance(keyword.value, ast.Name):
                kwargs[key] = keyword.value.id
            elif isinstance(keyword.value, ast.List):
                # Handle choices
                if key == 'choices':
                    choices = []
                    for item in keyword.value.elts:
                        if isinstance(item, ast.Tuple) and len(item.elts) == 2:
                            key_val = item.elts[0].value if isinstance(item.elts[0], ast.Constant) else str(item.elts[0])
                            display_val = item.elts[1].value if isinstance(item.elts[1], ast.Constant) else str(item.elts[1])
                            choices.append((key_val, display_val))
                    kwargs[key] = choices
        
        return kwargs
    
    def get_field_type(self, field_class: str) -> str:
        """Convert Django field class to readable type name"""
        field_mapping = {
            'CharField': 'CharField',
            'TextField': 'TextField',
            'EmailField': 'EmailField',
            'BooleanField': 'BooleanField',
            'IntegerField': 'IntegerField',
            'DecimalField': 'DecimalField',
            'DateField': 'DateField',
            'DateTimeField': 'DateTimeField',
            'ImageField': 'ImageField',
            'FileField': 'FileField',
            'ForeignKey': 'ForeignKey',
            'ManyToManyField': 'ManyToManyField',
            'OneToOneField': 'OneToOneField',
            'SlugField': 'SlugField',
            'URLField': 'URLField',
            'JSONField': 'JSONField',
        }
        return field_mapping.get(field_class, field_class)
    
    def parse_models_file(self, file_path: str, app_name: str):
        """Parse a models.py file and extract model information"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it's a Django model (inherits from models.Model or other Django base classes)
                    is_model = False
                    for base in node.bases:
                        if isinstance(base, ast.Attribute):
                            if base.attr == 'Model' and isinstance(base.value, ast.Attribute):
                                if base.value.attr == 'models':
                                    is_model = True
                                    break
                        elif isinstance(base, ast.Name):
                            # Handle cases like class User(AbstractBaseUser, PermissionsMixin)
                            if base.id in ['AbstractBaseUser', 'PermissionsMixin', 'Model']:
                                is_model = True
                                break
                    
                    # Also check for any class that has field assignments (common Django pattern)
                    if not is_model:
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for target in item.targets:
                                    if isinstance(target, ast.Name):
                                        if isinstance(item.value, ast.Call):
                                            # Check if it's a Django field
                                            if isinstance(item.value.func, ast.Attribute):
                                                field_class = item.value.func.attr
                                                if field_class in ['CharField', 'TextField', 'EmailField', 'BooleanField', 
                                                                  'IntegerField', 'DateField', 'DateTimeField', 'ImageField', 
                                                                  'ForeignKey', 'ManyToManyField', 'SlugField', 'JSONField']:
                                                    is_model = True
                                                    break
                                            elif isinstance(item.value.func, ast.Name):
                                                field_class = item.value.func.id
                                                if field_class in ['CharField', 'TextField', 'EmailField', 'BooleanField', 
                                                                  'IntegerField', 'DateField', 'DateTimeField', 'ImageField', 
                                                                  'ForeignKey', 'ManyToManyField', 'SlugField', 'JSONField']:
                                                    is_model = True
                                                    break
                                if is_model:
                                    break
                    

                    
                    if is_model:
                        model = DjangoModel(node.name, app_name)
                        
                        # Extract docstring
                        if ast.get_docstring(node):
                            model.docstring = ast.get_docstring(node)
                        
                        # Parse fields
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for target in item.targets:
                                    if isinstance(target, ast.Name):
                                        field_name = target.id
                                        
                                        # Skip if it's not a field assignment
                                        if field_name in ['objects', 'USERNAME_FIELD', 'REQUIRED_FIELDS']:
                                            continue
                                        
                                        if isinstance(item.value, ast.Call):
                                            # Get the field class name
                                            if isinstance(item.value.func, ast.Attribute):
                                                field_class = item.value.func.attr
                                            elif isinstance(item.value.func, ast.Name):
                                                field_class = item.value.func.id
                                            else:
                                                continue
                                            
                                            # Parse field arguments
                                            kwargs = self.parse_field_arguments(
                                                item.value.args, 
                                                item.value.keywords
                                            )
                                            
                                            # Create field object
                                            field = ModelField(field_name, self.get_field_type(field_class), **kwargs)
                                            model.add_field(field)
                        
                        self.models.append(model)
        
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
    
    def find_models_files(self, base_path: str) -> List[tuple]:
        """Find all models.py files in the project"""
        models_files = []
        base_path = Path(base_path)
        
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file == 'models.py':
                    file_path = os.path.join(root, file)
                    # Extract app name from path
                    app_name = os.path.basename(os.path.dirname(file_path))
                    models_files.append((file_path, app_name))
        
        return models_files
    
    def generate_markdown(self) -> str:
        """Generate markdown documentation"""
        markdown = "# Django Models Documentation\n\n"
        markdown += "This document was automatically generated from Django model files.\n\n"
        
        # Group models by app
        apps = {}
        for model in self.models:
            if model.app_name not in apps:
                apps[model.app_name] = []
            apps[model.app_name].append(model)
        
        # Generate documentation for each app
        for app_name, models in apps.items():
            markdown += f"## {app_name.title()} App\n\n"
            
            for model in models:
                markdown += f"### {model.name}\n\n"
                
                if model.docstring:
                    markdown += f"**Description:** {model.docstring}\n\n"
                
                if model.fields:
                    markdown += "| Field Name | Type | Constraints | Description |\n"
                    markdown += "|------------|------|-------------|-------------|\n"
                    
                    for field in model.fields:
                        constraints = []
                        if field.null:
                            constraints.append("null")
                        if field.blank:
                            constraints.append("blank")
                        if field.unique:
                            constraints.append("unique")
                        if field.auto_now_add:
                            constraints.append("auto_now_add")
                        if field.auto_now:
                            constraints.append("auto_now")
                        
                        constraints_str = ", ".join(constraints) if constraints else "-"
                        
                        # Generate description
                        description_parts = []
                        if field.choices:
                            choices_str = ", ".join([f"'{choice[0]}'" for choice in field.choices])
                            description_parts.append(f"Choices: [{choices_str}]")
                        if field.related_name:
                            description_parts.append(f"Related name: {field.related_name}")
                        if field.on_delete:
                            description_parts.append(f"On delete: {field.on_delete}")
                        if field.upload_to:
                            description_parts.append(f"Upload to: {field.upload_to}")
                        if field.default is not None:
                            description_parts.append(f"Default: {field.default}")
                        
                        description = "; ".join(description_parts) if description_parts else "-"
                        
                        markdown += f"| {field.name} | {field.field_type}"
                        if field.max_length:
                            markdown += f"({field.max_length})"
                        markdown += f" | {constraints_str} | {description} |\n"
                
                markdown += "\n"
        
        return markdown


def main():
    """Main function to run the model documentation generator"""
    # Get the backend directory path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    
    if not os.path.exists(backend_path):
        print(f"Backend directory not found at: {backend_path}")
        return
    
    parser = ModelParser()
    
    # Find all models.py files
    models_files = parser.find_models_files(backend_path)
    
    if not models_files:
        print("No models.py files found!")
        return
    
    print(f"Found {len(models_files)} models.py files:")
    for file_path, app_name in models_files:
        print(f"  - {app_name}: {file_path}")
    
    # Parse each models.py file
    for file_path, app_name in models_files:
        print(f"\nParsing {app_name}...")
        parser.parse_models_file(file_path, app_name)
    
    # Generate markdown documentation
    markdown_content = parser.generate_markdown()
    
    # Write to file
    output_file = os.path.join(os.path.dirname(__file__), 'MODELS_DOCUMENTATION.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\nDocumentation generated successfully!")
    print(f"Output file: {output_file}")
    print(f"Total models found: {len(parser.models)}")
    
    # Print summary
    print("\nModel Summary:")
    for model in parser.models:
        print(f"  - {model.app_name}.{model.name}: {len(model.fields)} fields")


if __name__ == "__main__":
    main()
