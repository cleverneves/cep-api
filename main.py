from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="API de CEP")


@app.get("/cep/{cep}")
async def consultar_cep(cep: str):
    cep = cep.replace('-', '').strip()
    if len(cep) != 8 or not cep.isdigit():
        raise HTTPException(status_code=400, details='CEP inválido.')

    url = f"https://viacep.com.br/ws/{cep}/json/"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502, details='Falha ao consultar o ViaCEP.')

    data = resp.json()
    if data.get('erro'):
        raise HTTPException(status_code=404, details='CEP não encontrado.')

    return data
