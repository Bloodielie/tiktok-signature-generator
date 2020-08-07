from signature_generator import SignatureGenerator
from signature_generator.api_wrapper.signature.base import AbstractSignatureGenerator, Signature


class BesideSignatureGenerator(AbstractSignatureGenerator):
    def __init__(self) -> None:
        self.signature_generator = SignatureGenerator()

    async def initialization(self) -> None:
        await self.signature_generator.initialization()

    async def close(self) -> None:
        await self.signature_generator.close()

    async def generate_signature(self, url: str) -> Signature:
        verify_fp = await self.signature_generator.verify_fp()
        signature = await self.signature_generator.signature(url)
        return Signature(signature=signature, verify_fp=verify_fp)
