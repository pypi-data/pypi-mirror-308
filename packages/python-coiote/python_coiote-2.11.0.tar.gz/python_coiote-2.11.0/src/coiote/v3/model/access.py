from dataclasses import dataclass

@dataclass
class UserAccess:
    userId: str
    username: str
    isDefaultDomain: bool

@dataclass
class Access:
    domain: str
    userAccesses: list[UserAccess]

@dataclass
class AccessGetResponse:
    accesses: list[Access]

@dataclass
class DefaultAccessPatchRequest:
    defaultDomain: str

@dataclass
class UserAccessPutModel:
    userId: str

@dataclass
class AccessPutRequest:
    userAccesses: list[UserAccessPutModel]