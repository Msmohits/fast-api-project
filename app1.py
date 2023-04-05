from fastapi import FastAPI
import aio_pika

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/receive")
async def receive_message():

    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    queue_name = "my_queue"
    queue = await channel.declare_queue(queue_name, durable=True)
    print('qqqqqqqqqqqqqq',queue.iterator())

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode()
                return {"message": f"Received '{body}' from {queue_name}"}

    await connection.close()

    return {"message": "No messages in queue"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)