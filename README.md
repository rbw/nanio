# nanio

The main goal with Nanio is to provide a flexible Nano backend platform, with a rich internal service layer to simplify the process of developing Nano backend applications.
At its core you'll find a Nano RPC gateway for both internal and (optional) external consumption, and an API browser.
Shortly, authentication and monitoring layers will be added to its core.

Why use it?
---

Nanio simplifies the process of building lightweight, high-performance and scalable backend applications on top Nano.
Also, it comes with a configurable Docker stack for easy deployment. 

Main features
---
- Lightweight (Uses non-blocking IO in multiprocessing mode, no threading)
- Fast (>30k RPS when benchmarking on low-end hardware)
- Pluggable (Easily build extensions)
- Scalable (Spin up new instances using pre-made Docker images)
- Customizable (Well structured and extensive configuration, but with working defaults)
- Secure (Requests relayed to the Node RPC server are carefully sanity checked)
