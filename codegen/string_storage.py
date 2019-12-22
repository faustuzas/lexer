from codegen.code_writer import Label, CodeWriter
from models.instructions import InstructionType


class Entry:

    def __init__(self, label, value) -> None:
        self.label = label
        self.value = value


class StringStorage:

    def __init__(self) -> None:
        self.entries = []

    def add_string(self, string):
        entry = Entry(Label(), string)
        self.entries.append(entry)
        return entry.label

    def place_labels(self, code_writer: CodeWriter):
        code_writer.write(InstructionType.MARKER_STATIC_START)
        for entry in self.entries:
            code_writer.place_label(entry.label)
            code_writer.write_raw(entry.value, str)

    def clear(self):
        self.entries = []


string_storage = StringStorage()
