from fastapi import FastAPI, HTTPException
from .schemas import ConversionRequest, ConversionResponse
from .client import InMemoryBudaClient, RealBudaClient
from .conversion import find_best_conversion

app = FastAPI(title="Buda Conversion API")

client = RealBudaClient()


@app.post("/convert", response_model=ConversionResponse)
def convert_currency(req: ConversionRequest):
    result, via, path = find_best_conversion(req.source, req.dest, req.amount, client)
    if result == 0:
        raise HTTPException(status_code=404, detail="No conversion path found")
    notes = f"Used intermediary: {via}" if via else "Direct conversion"
    return ConversionResponse(amount=round(result,6), via=via or "-", path=path, notes=notes)
