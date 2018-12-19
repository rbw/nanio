# nanio

The main goal with Nanio is to provide a pluggable Nano platform with a rich internal API / Service Layer, to simplify the process of developing Nano backend applications.

At its core you'll find a Nano RPC gateway and an API browser, with OAuth and Monitoring components soon to be added.

Why use it?
---

If you're just after a Nano API browser or Nano RPC gateway, but don't want to set up your own server; feel free to use my [publicly available Nanio server](https://nanio.vault13.org), connected to the Nano Live network.

If you want to build a Nano application, be it a light-wallet or something else, and you're familiar with Python and async programming, then might speed up the process of doing so while providing a lightweight, high-performance and scalable base platform.

Also, it comes with a configurable Docker stack for easy deployment. 

Highlights
---
- Lightweight (Uses non-blocking IO in multiprocessing mode, no threading)
- Fast (>30k RPS when benchmarking on low-end hardware)
- Pluggable (Easily build extensions)
- Scalable (Spin up new instances using pre-made Docker images)
- Customizable (Well structured and extensive configuration, but with working defaults)
- Secure (Requests relayed to the Node RPC server are carefully sanity checked)
