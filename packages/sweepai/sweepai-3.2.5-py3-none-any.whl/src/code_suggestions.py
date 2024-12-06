import difflib
from dataclasses import dataclass
from typing import Literal, Optional

def generate_diff(old_code: str, new_code: str, **kwargs):
    if old_code == new_code:
        return ""
    stripped_old_code = old_code.strip("\n") + "\n"
    stripped_new_code = new_code.strip("\n") + "\n"

    # Split the code into lines, preserving the line endings
    old_lines = old_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)

    # Add a newline character at the end if it's missing
    if not old_code.endswith("\n"):
        old_lines.append("\n")
    if not new_code.endswith("\n"):
        new_lines.append("\n")

    default_kwargs = {"n": 5}
    default_kwargs.update(kwargs)

    diff = difflib.unified_diff(
        stripped_old_code.splitlines(keepends=True), stripped_new_code.splitlines(keepends=True), **kwargs
    )

    diff_result = ""

    for line in diff:
        if not line.endswith("\n"):
            line += "\n"
        diff_result += line

    return diff_result


@dataclass
class CodeSuggestion:
    file_path: str
    original_code: str
    new_code: str
    file_contents: str = ""

    def to_camel_case(self):
        return {
            "filePath": self.file_path,
            "originalCode": self.original_code,
            "newCode": self.new_code,
        }
    
    @classmethod
    def from_camel_case(cls, data: dict):
        return cls(
            file_path=data["filePath"],
            original_code=data["originalCode"],
            new_code=data["newCode"],
        )
    
    def __str__(self):
        diff = generate_diff(self.original_code, self.new_code)
        return f"CodeSuggestion(file_path={self.file_path}, diff=```{diff}```)"


@dataclass
class StatefulCodeSuggestion(CodeSuggestion):
    state: Literal["pending", "processing", "done", "error"] = "pending"
    error: Optional[str] = None

    def to_camel_case(self):
        return {
            **super().to_camel_case(),
            "state": self.state,
        }
    
    @classmethod
    def from_camel_case(cls, data: dict):
        suggestion = super().from_camel_case(data)
        suggestion.state = data["state"]
        return suggestion
