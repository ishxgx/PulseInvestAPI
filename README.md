# PulseInvest API

PulseInvest API es un motor de señales de mercado en tiempo real desarrollado con FastAPI. El proyecto conecta con el WebSocket público de Binance para recibir precios en vivo, analiza el comportamiento del mercado y genera una recomendación automática: Comprar, Vender o Esperar.

Es un MVP educativo pensado para demostrar arquitectura backend en tiempo real, gestión de streams múltiples y lógica de decisión basada en datos. No constituye asesoramiento financiero.

## Qué hace este proyecto

La API se conecta en tiempo real a Binance y recibe cada trade del símbolo solicitado. A partir de esos datos calcula tendencia, volatilidad y una puntuación de fuerza del movimiento. Con esa información genera una recomendación automática acompañada de una explicación clara.

Además soporta múltiples símbolos de forma dinámica. Si alguien solicita señales para un nuevo símbolo, el sistema inicia automáticamente su stream sin necesidad de reiniciar el servidor.

También expone un WebSocket propio para que cualquier cliente pueda recibir precios en tiempo real directamente desde la API.

## Características principales

Streaming en tiempo real desde Binance
Soporte multi símbolo bajo demanda
Cálculo de medias móviles recientes y anteriores
Medición de volatilidad mediante desviación estándar
Sistema de puntuación de fuerza de tendencia
Recomendación automática BUY SELL WAIT
Explicación textual del motivo de la recomendación
API REST documentada automáticamente con Swagger
WebSocket para transmisión de precios en vivo

## Arquitectura general

La aplicación está dividida en varios componentes claros.

FastAPI actúa como servidor principal y expone los endpoints REST y WebSocket.
El StreamManager controla qué símbolos están activos y arranca o detiene streams cuando es necesario.
El servicio de mercado se conecta al WebSocket de Binance y guarda los precios en memoria.
El motor de señales analiza los datos acumulados y genera la recomendación final.

Todo funciona de manera asíncrona usando asyncio, lo que permite manejar múltiples símbolos sin bloquear el servidor.

## Instalación

Clona el repositorio:

git clone https://github.com/ishxgx/PulseInvestAPI.git

cd pulseinvest-api

Crea un entorno virtual:

py -3.13 -m venv .venv
source .venv/Scripts/activate

Instala las dependencias:

pip install -r requirements.txt

Inicia el servidor:

python -m uvicorn app.main:app --reload

Abre en el navegador:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Ahí encontrarás la documentación interactiva generada automáticamente.

## Endpoints disponibles

GET /health
Verifica que la API está funcionando correctamente.

GET /signals?symbol=btcusdt
Devuelve las señales calculadas para el símbolo indicado. Si el símbolo no estaba activo, el sistema inicia automáticamente su stream.

Ejemplo de respuesta:

{
"symbol": "btcusdt",
"status": "ok",
"last_price": 67316.36,
"trend": "down",
"volatility": 0.94,
"score": 0.01,
"action": "WAIT",
"reason": "Señal débil: no hay una ventaja clara.",
"note": "MVP educativo. No es consejo financiero."
}

GET /symbols/active
Devuelve la lista de símbolos que actualmente tienen un stream activo.

WebSocket /ws/prices/{symbol}
Permite recibir precios en tiempo real del símbolo solicitado. Si el símbolo no estaba activo, se inicia automáticamente.

Ejemplo en consola del navegador:

const ws = new WebSocket("ws://127.0.0.1:8000/ws/prices/btcusdt");
ws.onmessage = (e) => console.log(e.data);

## Cómo funciona la recomendación

La lógica actual es sencilla pero clara.

Se comparan medias móviles recientes frente a medias anteriores para determinar la tendencia.
Se calcula la volatilidad para evitar operar en condiciones demasiado inestables.
Se genera una puntuación basada en la diferencia relativa entre medias.

Si la tendencia es alcista y la fuerza supera un umbral mínimo, la acción será BUY.
Si la tendencia es bajista con suficiente fuerza, la acción será SELL.
Si la señal es débil o la volatilidad es elevada, la recomendación será WAIT.

Este sistema puede ampliarse fácilmente añadiendo RSI, EMA, MACD o gestión de riesgo.

## Próximas mejoras

Añadir indicadores técnicos más avanzados
Implementar modo paper trading
Persistencia en base de datos
Cache con Redis
Sistema de alertas por precio
Dashboard frontend conectado a la API
Dockerización completa para entorno productivo

## Advertencia

Este proyecto es únicamente educativo. No constituye asesoramiento financiero ni recomendación real de inversión. Operar en mercados financieros implica riesgo y cada persona debe realizar su propio análisis antes de tomar decisiones.

## Autor

IShxgx

Si te gusta el proyecto puedes darle una estrella y contribuir con mejoras.
