# Django Models Documentation

This document was automatically generated from Django model files.

## Company App

### Company

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| name | CharField(200) | unique | - |
| slug | SlugField(200) | unique | - |
| logo | ImageField | - | Upload to: company_logos/ |
| description | TextField | - | - |

## Experience App

### Experience

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| cover_image | ImageField | null, blank | Upload to: experience_images/ |
| title | CharField(200) | - | - |
| role | CharField(100) | - | - |
| short_description | TextField | - | - |
| content | JSONField | null, blank | - |
| tips | TextField | null, blank | - |
| published_date | DateTimeField | auto_now_add | - |
| experience_date | DateField | - | - |
| visibility | BooleanField | - | Default: True |
| verified | BooleanField | - | Default: False |
| compensation | TextField | null, blank | - |
| job_type | CharField(20) | - | Choices: ['fte', 'internship', 'research', 'other'] |
| author | ForeignKey | - | Related name: experiences |
| company | ForeignKey | - | Related name: experiences |
| tags | ManyToManyField | blank | Related name: experiences |
| saved_by | ManyToManyField | blank | Related name: saved_experiences |

## Tag App

### TagType

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| name | CharField(100) | unique | - |

### Tag

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| title | CharField(100) | unique | - |
| type | ForeignKey | null, blank | Related name: tags |

## User App

### User

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| email | EmailField | unique | - |
| backup_email | EmailField | null, blank | - |
| name | CharField(100) | - | - |
| roll_number | CharField(20) | null, blank | - |
| department | CharField(100) | null, blank | - |
| programme | CharField(100) | null, blank | - |
| role | CharField(20) | - | Choices: ['student', 'spoc', 'pr', 'admin', 'other'] |
| is_active | BooleanField | - | Default: True |
| is_staff | BooleanField | - | Default: False |

