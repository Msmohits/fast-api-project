from fastapi import FastAPI
import aio_pika

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/send/{message}")
async def send_message(message: str):

    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    queue_name = "my_queue"
    queue = await channel.declare_queue(queue_name, durable=True)

    message_body = message.encode()
    message = aio_pika.Message(body=message_body, content_type='text/plain', delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

    await channel.default_exchange.publish(message, routing_key=queue_name)

    await connection.close()

    return {"message": f"Sent '{message}' to {queue_name}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
