import asyncio
from json import load


clients = set()


async def handle_client(reader, writer):
    clients.add(writer)
    while True:
        data = await reader.read(100)
        if not data:
            break  # Connection closed
        for client in clients:
            if client != writer:
                print('Routing message to client')
                client.write(data)
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
