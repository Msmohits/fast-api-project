from fastapi import FastAPI
import aio_pika

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!!!!!"}

@app.get("/send/{message}")
async def send_message(message: str):
    # Connect to RabbitMQ server
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    # Declare a queue to send messages to
    queue_name = "my_queue"
    queue = await channel.declare_queue(queue_name, durable=True)

    # Create a message to send
    message_body = message.encode()
    message = aio_pika.Message(body=message_body, content_type='text/plain', delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

    # Publish the message to the queue
    await channel.default_exchange.publish(message, routing_key=queue_name)

    # Close the connection to RabbitMQ
    await connection.close()

    return {"message": f"Sent '{message}' to {queue_name}"}


# @app.get("/receive")
# async def receive_message():
#     # Connect to RabbitMQ server
#     connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
#     channel = await connection.channel()
#
#     # Declare the same queue that we sent messages to
#     queue_name = "my_queue"
#     queue = await channel.declare_queue(queue_name, durable=True)
#     print('qqqqqqqqqqqqqq',queue.iterator())
#     # Get the next message from the queue
#     async with queue.iterator() as queue_iter:
#         async for message in queue_iter:
#             async with message.process():
#                 body = message.body.decode()
#                 return {"message": f"Received '{body}' from {queue_name}"}
#
#     # Close the connection to RabbitMQ
#     await connection.close()
#
#     return {"message": "No messages in queue"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)