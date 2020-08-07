from abc import ABC, abstractmethod
from pydantic import BaseModel


class Signature(BaseModel):
    signature: str
    verify_fp: str


class AbstractSignatureGenerator(ABC):
    @abstractmethod
    async def initialization(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def generate_signature(self, url: str) -> Signature:
        raise NotImplementedError
