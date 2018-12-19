# nanio

The main goal with Nanio is to provide a pluggable Nano platform with a rich internal service layer.

At its core you'll find a Nano RPC gateway and an API browser, with OAuth and Monitoring components and WebSocket support soon to be added.

Why use it?
---

If you're just after the API browser or RPC gateway, but don't want to set up your own server; feel free to use my [publicly available Nanio server](https://nanio.vault13.org), connected to the Nano Live network.

If you want to build a Nano application, be it a light-wallet or something else, and you're familiar with Python and async programming, then Nanio might speed up the process of doing so by providing a lightweight, high-performance and scalable backend platform with a rich API.

Also, it comes with a configurable Docker stack for easy deployment. 

Highlights
---
- Lightweight (Uses non-blocking IO in multiprocessing mode, no threading)
- Performant (>30k RPS when benchmarking on low-end hardware)
- Pluggable (Easily build your own extensions)
- Scalable (Spin up new instances using pre-made Docker images)
- Customizable (Well structured and extensive configuration, with working set of defaults)
- Secure (Requests relayed to the Node RPC server are carefully sanity checked)
