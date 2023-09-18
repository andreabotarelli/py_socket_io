import asyncio
from json import load


NEW_CLIENT = "@@@NEW@@@"


async def rcv_message(reader):
    while True:
        response = await reader.read(100)
        if not response:
            break
        print(f"{response.decode()}")


async def send_message(writer):
    while True:
        message = await asyncio.to_thread(input, "")
        if message.strip().lower() == "exit":
            break
        writer.write(message.encode())
        await writer.drain()


async def main():
    try:
        conn = {'ip': '127.0.0.1', 'port': 23, 'name': 'NONE'}
        with open('conn.json') as r_file:
            conn = load(r_file)
        ip = conn['ip']
        port = conn['port']
        name = conn['name']
        print(f'Connecting socket client on {ip}:{port} for {name}')
        reader, writer = await asyncio.open_connection(ip, port)
        message = f"{NEW_CLIENT}{name}"
        writer.write(message.encode())
        await writer.drain()
        receive_task = asyncio.create_task(rcv_message(reader))
        send_task = asyncio.create_task(send_message(writer))
        await asyncio.wait([receive_task, send_task], return_when=asyncio.FIRST_COMPLETED)
        receive_task.cancel()
        send_task.cancel()
    except ConnectionRefusedError:
        print("The server is not running or the address is incorrect.")


if __name__ == '__main__':
    asyncio.run(main())
