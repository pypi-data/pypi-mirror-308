class EnvironmentVariableNotFoundError(Exception):
    """自定义异常：当找不到环境变量时抛出"""

    def __init__(self, variable_name):
        message = f"Environment variable '{variable_name}' not found"
        super().__init__(message)


class WrongProgressTypeError(Exception):
    """自定义异常：当progress错误时抛出"""

    def __init__(self):
        message = 'Progress must be a integer >=0 and <=100'
        super().__init__(message)
