from enum import Enum

class ExitCodes(Enum):
    SUCCESS = 0

    CONFLICTING_PROGRAM_ARGS = 1
    MODEL_FILE_NOT_FOUND = 2
    YAML_PARSING_ERROR = 3
    MODEL_PARSING_ERROR = 4
    MODEL_VALIDATION_ERROR = 5
    TEST_FILE_NOT_FOUND = 6
    TEST_PARSING_ERROR = 7

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value
    

