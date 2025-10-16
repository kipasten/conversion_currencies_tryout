# Buda Conversion API Project Structure

Este proyecto implementa una **API en FastAPI** que permite encontrar la mejor conversión entre monedas dentro del exchange **Buda.com**, considerando conversiones vía criptomonedas intermediarias.

## 📁 Estructura del proyecto

```
buda_conversion_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── client.py            # Cliente para obtener datos de Buda (real o mock)
│   ├── conversion.py        # Lógica de simulación y búsqueda de mejor conversión
│   └── schemas.py           # Modelos Pydantic para request/response
├── tests/
│   ├── __init__.py
│   ├── test_conversion.py   # Tests unitarios y de integración (pytest)
└── README.md
```

---

## 🧠 Descripción general

### 1️⃣ `main.py`
Expone el endpoint principal de la API:
```python
POST /convert
```
Recibe un JSON:
```json
{
  "source": "CLP",
  "dest": "PEN",
  "amount": 10000
}
```
Devuelve:
```json
{
  "amount": 12.45,
  "via": "BTC",
  "path": ["BTC-CLP", "BTC-PEN"],
  "notes": "Used intermediary: BTC"
}
```

### 2️⃣ `client.py`
Define la clase abstracta `BudaClient` y las implementaciones:
- `InMemoryBudaClient`: usada en pruebas.
- `RealBudaClient`: conecta a la API pública de Buda.com para obtener libros de órdenes reales (`/markets/{market}/order_book`).

### 3️⃣ `conversion.py`
Contiene la lógica para:
- Simular compra/venta según la profundidad del libro (`simulate_buy_with_quote`, `simulate_sell_base`).
- Buscar la mejor conversión directa o vía intermediario.
- Comparar resultados entre múltiples rutas y devolver la óptima.

### 4️⃣ `schemas.py`
Modelos Pydantic que definen la estructura de entrada y salida de la API.


---

## 🚀 Ejecución

### Instalar dependencias
```bash
pip install fastapi uvicorn pydantic pytest
```

### Ejecutar el servidor local
```bash
uvicorn app.main:app --reload
```

Endpoint disponible en: `http://127.0.0.1:8000/convert`

### Ejecutar tests
```bash
pytest -v
```

---

## 🧩 Supuestos del modelo
- Los mercados siguen el formato `{base}-{quote}` (ej: `BTC-CLP`).
- Los precios de los **asks** y **bids** son expresados en la moneda de cotización (`quote`).
- No se incluyen comisiones ni deslizamientos por defecto, pero se pueden configurar fácilmente.
- Solo se consideran rutas con un máximo de **un intermediario** (por simplicidad y rendimiento).
- El resultado se redondea a 6 decimales 

---

## 📚 Ejemplo de uso (demo)

```bash
curl -X POST http://127.0.0.1:8000/convert \
     -H "Content-Type: application/json" \
     -d '{"source": "CLP", "dest": "PEN", "amount": 10000}'
```

Resultado esperado:
```json
{
  "amount": 3562.381937,
  "via": "USDT",
  "path": [
    "USDT-CLP",
    "USDT-PEN"
  ],
  "notes": "Used intermediary: USDT"
}
```


---

## 🧭 Próximas mejoras sugeridas
- [ ] Agregar soporte para comisiones por transacción.
- [ ] Incluir más de un intermediario (rutas de 3 o más saltos).
- [ ] Soporte para caching local y logging estructurado.

---

**Autor:** Ignacio Pastén  
**Versión:** 1.0.0  
**Framework:** FastAPI  
**Testing:** Pytest
