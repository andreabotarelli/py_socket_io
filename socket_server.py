import asyncio
from json import load
from socket_client import NEW_CLIENT


clients = dict()


async def handle_client(reader, writer):
    clients[writer] = dict()
    while True:
        data = await reader.read(100)
        if not data:
            break  # Connection closed
        message = data.decode()
        if NEW_CLIENT in message:
            clients[writer]['name'] = message.replace(NEW_CLIENT, '')
        else:
            for client in clients.keys():
                if client != writer:
                    print('Routing message to client')
                    forward_data = f"{clients[writer]['name']}: {message}"
                    client.write(forward_data.encode())
                    await client.drain()
    writer.close()


async def main():
    conn = {'ip': '127.0.0.1', 'port': 23}
    with open('conn.json') as r_file:
        conn = load(r_file)
    ip = conn['ip']
    port = conn['port']
    print(f'Starting socket forward server on {ip}:{port}')
    server = await asyncio.start_server(
        handle_client, ip, port
    )
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
