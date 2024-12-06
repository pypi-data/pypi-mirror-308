from importlib.metadata import version

from .factory import (
    assignment,
    cid,
    cohort,
    country,
    course,
    email,
    feedback,
    gender,
    mark,
    name,
    student,
    title,
    username,
)

__version__ = version("fakeitmakeit")

__all__ = [
    "cid",
    "gender",
    "title",
    "course",
    "country",
    "username",
    "email",
    "name",
    "mark",
    "feedback",
    "student",
    "cohort",
    "assignment",
]
