# wal-iot

A simple Write Ahead Log (WAL) implementation for IoT devices to deal with network failures or power outages.

## Introduction

Unlike the formal WAL designed for databases, this WAL is not designed for ensuring the atomicity of transactions. 
Instead, it is designed to ensure that the data is not lost in case of network failures or power outages,
which are common in IoT or sensors networks.

## Installation

```bash
pip install wal-iot
```

