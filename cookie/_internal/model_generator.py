"""Code for model generation."""

from pathlib import Path
from urllib.parse import urlparse

from datamodel_code_generator import (
    DataModelType,
    InputFileType,
    PythonVersion,
    generate,
)

generate(
    urlparse("https://api.cookieapp.me/openapi.json"),
    input_file_type=InputFileType.OpenAPI,
    use_union_operator=True,
    use_double_quotes=True,
    use_standard_collections=True,
    target_python_version=PythonVersion.PY_39,
    custom_formatters=["formatter"],
    output=Path("cookie/models.py"),
    output_model_type=DataModelType.PydanticV2BaseModel,
    disable_timestamp=True,
)
