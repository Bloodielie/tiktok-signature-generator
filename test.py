from signature_generator.generator import SignatureGenerator
import asyncio
import requests


async def main():
    s = SignatureGenerator()
    await s.initialization()
    username = "0udanovskiy2"
    url = f"https://m.tiktok.com/api/user/detail/?uniqueId={username}&language=ru&secUid="
    verify_fp = await s.verify_fp()
    signature = await s.signature(url)
    await s.close()
    r = requests.get(f"{url}&verifyFp={verify_fp}&_signature={signature}", headers={"user-agent": s.user_agent})
    print(r.text)


asyncio.run(main())
