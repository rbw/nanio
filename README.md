# nanio

Nanio provides a modular backend platform on top of Nano, at its core you'll find a Nano RPC gateway and API browser - with OAuth, a Monitoring component and WebSocket support soon to be added.


Why use it?
---
Depends. If you're just after an internet connected Nano network RPC relay, or the API browser provided by Nanio--but don't want to set up your own server--then my [publicly available Nanio server](https://nanio.vault13.org), connected to the Nano Live network, might suit your needs.

If you want to build a Nano application--be it a light wallet or something else, and you're familiar with Python and async programming--then Nanio might speed up the process of doing so by providing a lightweight, high-performance and scalable backend platform that comes with an easy to use API.

If you want to set up your own Nanio stack, then I'd recommend using Docker for, check out the [docker-compose examples](https://github.com/rbw/nanio/tree/master/examples/docker).

Highlights
---
- Lightweight (Uses non-blocking IO in multiprocessing mode, no threading)
- Performant (>30k RPS when benchmarking on low-end hardware)
- Pluggable (Easily build your own extensions)
- Scalable (Spin up new instances using pre-made Docker images)
- Customizable (Well structured and extensive configuration, with working set of defaults)
- Secure (Requests relayed to the Node RPC server are carefully sanity checked)

Contributions
---
If you think there's something missing or broken, please create a PR or send me an email.

Author
---
Robert Wikman <rbw@vault13.org>
