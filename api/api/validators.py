"""
This module contains custom validators
that override the default connexion behaviour.
"""

import logging

from connexion import decorators
from connexion.exceptions import BadRequestProblem
from jsonschema import ValidationError

# pylint: disable=invalid-name

logger = logging.getLogger("connexion.decorators.validation")


class RequestBodyValidator(decorators.validation.RequestBodyValidator):
    """
    This class overrides the default connexion RequestBodyValidator
    so that it returns the complete string representation of the
    error, rather than just returning the error message.

    For more information:
        - https://github.com/zalando/connexion/issues/558
        - https://connexion.readthedocs.io/en/latest/request.html
    """

    # pylint: disable=undefined-variable, logging-format-interpolation

    def validate_schema(self, data, url):
        # type: (dict, AnyStr) -> Union[ConnexionResponse, None]
        if self.is_null_value_valid and is_null(data):
            return None

        try:
            self.validator.validate(data)
        except ValidationError as exception:
            error_path = ".".join(str(item) for item in exception.path)
            error_path_msg = " - '{path}'".format(path=error_path) if error_path else ""
            logger.error(
                "{url} validation error: {error}{error_path_msg}".format(
                    url=url, error=exception, error_path_msg=error_path_msg
                ),
                extra={"validator": "body"},
            )
            raise BadRequestProblem(
                detail="{message}{error_path_msg}".format(
                    message=exception, error_path_msg=error_path_msg
                )
            )

        return None
