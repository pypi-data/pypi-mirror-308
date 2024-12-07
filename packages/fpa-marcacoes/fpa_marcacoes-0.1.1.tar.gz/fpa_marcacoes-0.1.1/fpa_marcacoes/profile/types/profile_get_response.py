from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic

class ProfileGetResponse(UniversalBaseModel):
    profile_image: str = pydantic.Field()
    """
    Path to the user's profile image
    """

    name: str = pydantic.Field()
    """
    The athlete's name
    """

    email: str = pydantic.Field()
    """
    The athlete's email
    """

    nif: int = pydantic.Field()
    """
    The athlete's nif (Número de Indentifição Fiscal)
    """

    priority: int = pydantic.Field()
    """
    The priority level on the website. The lower the value, the more important the athlete is
    """

    coach: str = pydantic.Field()
    """
    The coach's name
    """