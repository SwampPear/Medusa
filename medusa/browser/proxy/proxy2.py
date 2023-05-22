from mitmproxy import ctx, http
from mitmproxy.net import tcp

def tcp_connect(flow: tcp.TCPFlow):
    # Redirect the client connection to mitmproxy
    flow.client_replay = tcp.TCPReplay(ctx.client)
    flow.server_replay = tcp.TCPReplay(ctx.server)
    flow.live = True
    ctx.log("Redirecting client connection to mitmproxy")

def request(flow: http.HTTPFlow):
    # Modify the request if needed
    flow.request.host = "www.example.com"  # Modify the destination hostname
    ctx.log("Modified request hostname to www.example.com")

def response(flow: http.HTTPFlow):
    # Modify the response if needed
    ctx.log("Received response from server")

# Main entry point
def main():
    # Start mitmproxy
    ctx.log("Starting mitmproxy")
    config = ctx.options
    config.update(
        ssl_insecure=True,  # Ignore SSL certificate errors
        listen_host='localhost',
        listen_port=8080
    )
    ctx.master.addons.add(tcp_connect)
    ctx.master.addons.add(request)
    ctx.master.addons.add(response)
    ctx.master.run()

if __name__ == '__main__':
    main()
