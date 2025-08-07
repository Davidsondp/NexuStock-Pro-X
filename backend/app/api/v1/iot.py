from fastapi import APIRouter, Request
import json

router = APIRouter()

@router.post("/scanner/register")
async def register_iot_scanner(request: Request):
    body = await request.json()
    
    # Validar dispositivo
    if body.get('serial_number') not in AUTHORIZED_SCANNERS:
        raise HTTPException(403, "Dispositivo no autorizado")
    
    # Guardar conexión
    IOT_DEVICES[body['serial_number']] = {
        "last_seen": datetime.now(),
        "status": "connected"
    }
    
    return {"status": "success"}

@router.websocket("/scanner/{serial_number}/ws")
async def websocket_scanner(websocket: WebSocket, serial_number: str):
    await websocket.accept()
    
    if serial_number not in AUTHORIZED_SCANNERS:
        await websocket.close(code=1008)
        return
    
    try:
        while True:
            data = await websocket.receive_text()
            await process_scan_data(json.loads(data))
    except WebSocketDisconnect:
        IOT_DEVICES[serial_number]["status"] = "disconnected"
