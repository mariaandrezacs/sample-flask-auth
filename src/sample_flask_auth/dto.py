from dataclasses import dataclass


@dataclass
class LoginInput:
    username: str
    password: str


@dataclass
class CreateUserInput:
    username: str
    password: str
    role: str = "user"


@dataclass
class UpdatePasswordInput:
    password: str


@dataclass
class UserOutput:
    id: int
    username: str
    role: str
