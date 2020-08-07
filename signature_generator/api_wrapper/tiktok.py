from typing import Optional

from signature_generator.api_wrapper.signature.base import AbstractSignatureGenerator, Signature
from signature_generator.api_wrapper.signature.beside import BesideSignatureGenerator


async def _url_addition(url: str, signature: Signature) -> str:
    return f"{url}&verifyFp={signature.verify_fp}&_signature={signature.signature}"


class TikTokApi:
    def __init__(self, *, signature_generator: Optional[AbstractSignatureGenerator] = None) -> None:
        self.signature_generator = signature_generator or BesideSignatureGenerator()

    async def initialization(self) -> None:
        await self.signature_generator.initialization()

    async def close(self) -> None:
        await self.signature_generator.close()
