# drf-excel-export

**drf-excel-export** is a Django package that enables easy export of Django REST Framework (DRF) API documentation to an Excel file. It is compatible with both `drf-spectacular` and `drf-yasg` for generating OpenAPI schemas, providing flexibility based on your existing DRF setup.

## Features
- Exports API endpoint information, including paths, HTTP methods, descriptions, parameters, and response codes.
- Compatible with both `drf-spectacular` and `drf-yasg` for OpenAPI schema generation.
- Outputs an organized Excel file (`api_documentation.xlsx`) with all API documentation.

## Installation

1. **Install the Package**:
   ```bash
   pip install drf-excel-export
   ```

2. **Add to Django `INSTALLED_APPS`**:
   Add `drf_excel_export` to your `INSTALLED_APPS` in your Django project’s `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...,
       'drf_excel_export',
   ]
   ```

3. **Configure drf-spectacular or drf-yasg** (if not already installed):
   Install and configure either `drf-spectacular` or `drf-yasg`, as one of these libraries is required for schema generation:
   - For `drf-spectacular`:
     ```bash
     pip install drf-spectacular
     ```
     Then, in `settings.py`:
     ```python
     REST_FRAMEWORK = {
         'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
     }

     SPECTACULAR_SETTINGS = {
         'TITLE': 'Your API Title',
         'DESCRIPTION': 'API description here',
         'VERSION': '1.0.0',
     }
     ```

   - For `drf-yasg`:
     ```bash
     pip install drf-yasg
     ```
     Add a schema view in your `urls.py` if you wish to view the schema:
     ```python
     from rest_framework import permissions
     from drf_yasg.views import get_schema_view
     from drf_yasg import openapi

     schema_view = get_schema_view(
         openapi.Info(
             title="Your API Title",
             default_version='v1',
             description="API description here",
         ),
         public=True,
         permission_classes=(permissions.AllowAny,),
     )
     ```

## Usage

To generate the API documentation in Excel format, run the following management command from your Django project’s root directory:

```bash
python manage.py export-excel
```

This command will generate an Excel file, `api_documentation.xlsx`, in the current directory, containing details of all API endpoints.

## Excel File Structure
The exported Excel file contains the following columns:
- **Endpoint**: The URL path of the endpoint.
- **Method**: HTTP method (GET, POST, etc.).
- **Description**: Description of the endpoint.
- **Parameters**: List of parameters (query, path, etc.).
- **Response Codes**: List of possible HTTP response codes for the endpoint.

## Example Output
| Endpoint          | Method | Description              | Parameters    | Response Codes |
|-------------------|--------|--------------------------|---------------|----------------|
| /api/sample/      | GET    | Returns a sample message | -             | 200            |
| /api/sample/      | POST   | Receives data            | data, id      | 201, 400       |

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`feature/my-feature`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support or questions, please open an issue on the [GitHub repository](https://github.com/donaldte/drf-excel-export) or contact the author via [email][mailto:donaldtedom0@gmail.com].

