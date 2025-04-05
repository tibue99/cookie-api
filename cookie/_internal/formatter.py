from datamodel_code_generator.format import CustomCodeFormatter


class CodeFormatter(CustomCodeFormatter):
    def apply(self, code: str) -> str:
        # Import BaseChart
        code = code.replace("\nclass", "from ._internal import BaseChart\n\n\nclass", 1)

        # Let BaseChart inherit from BaseModel
        code = code.replace("class Chart(BaseModel)", "class Chart(BaseChart)")

        return code
