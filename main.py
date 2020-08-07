from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from signature_generator import SignatureGenerator
from pydantic import BaseModel

app = FastAPI(title="TikTok signature generator", description="This is an api for generating signatures tiktok "
                                                              "private api")
generator = SignatureGenerator()


@app.on_event("startup")
async def startup_event():
    await generator.initialization()


@app.on_event("shutdown")
async def shutdown_event():
    await generator.close()


class SignatureResponse(BaseModel):
    signature: str
    verify_fp: str


@app.get("/signature", response_model=SignatureResponse, response_class=UJSONResponse, tags=["Signature"])
async def signature(url: str):
    verify_fp = await generator.verify_fp()
    signature = await generator.signature(url)
    return {"signature": signature, "verify_fp": verify_fp}
