import asyncio

from consensus.poa.p2p import Peer as PoAPeer
from consensus.pos.p2p import Peer as PoSPeer
from consensus.pow.p2p import Peer as PoWPeer
from consensus.poa.mal_node import Peer as PoaMalPeer
from consensus.pos.mal_node import Peer as PosMalPeer
from consensus.pow.mal_node import Peer as PowMalPeer


def yn(prompt, default="n"):
    value = input(prompt).strip().lower()
    return value if value in ("y", "n") else default


def start_peer():
    host = input("Enter Host [127.0.0.1]: ").strip() or "127.0.0.1"
    port = int(input("Enter Port: "))
    name = input("Enter Name: ").strip() or f"node-{port}"
    consensus = (input("Enter Consensus [poa/pos/pow] (default: pow): ").strip().lower()
                 or "pow")
    activate_disk_load = yn("Load saved data if any? (y/n): ")
    activate_disk_save = yn("Continuously backup data to disk? (y/n): ")
    mal = yn("Malicious? (y/n): ")

    # PoS nodes can discover peers through the configured room.
    room_id = None
    signalling_url = "ws://127.0.0.1:8765"
    web_host = None
    web_port = 8000

    bootstrap_host = None
    bootstrap_port = None

    if consensus == "pos":
        use_room = input("Use signalling room discovery? (y/n, default y): ").strip().lower()
        if use_room != "n":
            room_id = input("Room ID [blockchain]: ").strip() or "blockchain"
            signalling_url = (
                input("Signalling server [ws://127.0.0.1:8765]: ").strip()
                or "ws://127.0.0.1:8765"
            )
        else:
            action = (input("Enter 'create' or 'connect' (default: create): ").strip().lower()
                      or "create")
            if action == "connect":
                bootstrap_host = input("Bootstrap host: ").strip()
                bootstrap_port = int(input("Bootstrap port: "))

        dashboard = input("Start web dashboard? (y/n, default y): ").strip().lower()
        if dashboard != "n":
            web_host = input("Dashboard host [127.0.0.1]: ").strip() or "127.0.0.1"
            web_port = int(input("Dashboard port [8000]: ").strip() or "8000")

    peer = None
    if consensus == "poa":
        peer = (PoaMalPeer if mal == "y" else PoAPeer)(
            host, port, name, activate_disk_load, activate_disk_save
        )
    elif consensus == "pos":
        if mal == "y":
            peer = PosMalPeer(
                host, port, name, True, activate_disk_load, activate_disk_save
            )
        else:
            staker = yn("Staker? (y/n, default y): ", "y") == "y"
            peer = PoSPeer(
                host, port, name, staker, activate_disk_load, activate_disk_save
            )
    else:
        miner = yn("Miner? (y/n, default y): ", "y") == "y"
        peer = (PowMalPeer if mal == "y" else PoWPeer)(
            host, port, name, miner, activate_disk_load, activate_disk_save
        )

    try:
        if consensus == "pos":
            asyncio.run(peer.start(
                bootstrap_host,
                bootstrap_port,
                room_id=room_id,
                signalling_url=signalling_url,
                web_host=web_host,
                web_port=web_port,
            ))
        else:
            asyncio.run(peer.start(bootstrap_host, bootstrap_port))
    except KeyboardInterrupt:
        print("\nShutting Down...")


if __name__ == "__main__":
    start_peer()
