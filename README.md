# Blockchain App
A web and terminal blockchain implementation in Python from scratch

## Features
- Peer-to-Peer network with decentralized communication
- Public/private key-based account system
- Digital signature verification
- Selectable consensus mechanism - PoW, PoS, PoA
- Smart contract deployment
- IPFS integration
- Persistent storage
- Malicious node to test security
- Command line & web interface

## Contents
- [Theory](#theory)
- [About this project](#about-this-project)
- [How to run this project](#how-to-run-this-project)

## Theory
### What is blockchain?
A blockchain is a decentralized, distributed digital ledger where data is stored in blocks linked together in a chain
- A block is made of list of transactions
### Peer-to-Peer Network
Since, there is no central authority, network is formed in a peer-to-peer fashion.
### Consensus Mechanism
Blockchain involves transactions in a trustless environment. So there is need for a mechanism to ensure integrity of the chain. There comes the need of consensus mechanisms. Each consensus mechanism ensures integrity of the chain in their own way.
#### Proof of Work(PoW)
- Nodes compete to solve a cryptographic puzzle
- The winner gets to add the next block to the chain
#### Proof of Stake(PoS)
- Nodes run vrf to generate vrf output and vrf proof to simulate a lottery system
- The winner of the lottery gets to generate the block.
#### Proof of Authority(PoA)
- A limited set of trusted nodes(authorities) validate and create new blocks
### Smart Contracts
- A smart contract is like a digital agreement written in code
- It sits on the blockchain and runs automatically when certain rules are met
### IPFS
Blockchains are not designed for storing large amount of data. That's where IPFS comes in.
- It's a decentralized file storage system
- Each file is identified by its content
- A unique hash called CID(Content Identifiers) is generated based on the content(Files with same content will have same CID)
- IPFS uses a Distributed Hash Table(DHT), similar to BitTorrent's Kademlia DHT
- When you request a CID, your node queries the DHT to ask "Which peers are providing this CID?"
- Nodes that have previously announced that CID to the DHT will be returned as providers
- Your node then directly connects to those providers via IPFS's peer-to-peer transport protocols(libp2p)

## About this project
### Basic Structure
Each **node** contains its own set of
- Known peers list (members of the network)
- Client connections (connection established by your node to other nodes)
- Server connections (connection established by other nodes to your node)
- Wallet (acts as your account in the network)
- Transaction pool (contains all transactions pending to be mined)
- Chain (personal copy of the blockchain)

Each **account** contains
- Private key
- Public key

**Transactions** are of 3 types

- **Coin Transaction** - To transfer money
  - Timestamp
  - Public key of the sender
  - Public key of the receiver
  - Transaction amount
- **Deploy Transaction** - To deploy contract
  - Timestamp
  - Public key of the sender
  - Contract code
  - Deploy charge

- **Invoke Transaction** - To invoke contract
  - Timestamp  
  - Public key of the sender  
  - Contract ID  
  - Function name  
  - Arguments  
  - New state  
  - Invoke charge  

Each **block** contains
- Timestamp
- List of transactions
- Hash of previous block
- Current block hash
- Miner info
- List of files
### Handshake Protocol
- Client: Sends ping
- Server: Receives ping &rightarrow; sends pong
- Client: Receives pong &rightarrow; Sends peer info (information about itself)
- Server: Receives peer info &rightarrow; adds it to its known peers (if not already present) &rightarrow; sends back known_peers (list of all nodes it knows)
- Client: Receives known_peers &rightarrow; adds new peers to its own known_peers &rightarrow; requests the chain
- Server: Receives chain request &rightarrow; sends its current chain
- Client: Receives the chain &rightarrow; replaces its own if the length of new chain is longer than the current one
### Peer-to-Peer Network
If the total number of nodes in the network is less than 10, it forms a mesh network. If the node count exceeds 9, Gossip-based Random Peer Sampling is used
- Each node maintains a list of 8 connected peers
- At regular intervals, a node drops one connection and connects to a new, previously unconnected peer from the known peers list
- This prevents network congestion by limiting the number of connections per node
- It also prevents sub-network formation by randomly switching connections  

**Implemented Using:** python websockets, asyncio
### Consensus Mechanism
Users can select their prefered consensus mechanism from the list of three available
#### Proof of Work(PoW)
- A new block is mined every 30 secs, if there are pending transactions in the transaction pool
- Mining nodes collect transactions into a block
- Node that first finds a valid hash gets the chance to mine
- Difficulty is set to 5. That means, a valid hash is the one which starts with five zeroes
- Nonce is incremented until finding a valid hash
- Once mined, the block is broadcasted to the network
- All nodes validate the block before adding it to their chain
#### Proof of Stake(PoS)
- One node is mined every epoch
- The timings are synchronized between peers based on the time since last block was created
- Each node can stake a certain amount of their cryptocurrency in order to run vrf.
- VRF is a verifiable random function. The stakers generate a vrf proof and vrf output
- If the vrf output generated by a node is less than (max value of vrf output) * (amount staked by this node/total amount staked by all nodes), then
- This node wins the lottery and create a block. (Notice that the greater the amount staked the greater the chance of winning the lottery)
- VRF Proof is used to check whether the one who claims to win the lottery actually generated the vrf output from the correct seed
- If node attempts double signing their stake is slashed.
- If multiple nodes win and creates blocks then the chain is forked.
- We use the heaviest chain rule to arrive at a consensus. (i.e the chain with the most amount staked is the valid chain)
#### Proof of Authority(PoA)
- Initially, admin, the one who started the chain is the only miner
- Admin can add or remove miners
- Each block can be mined only by the assigned miner
- If that miner is inactive, mining will be handed over to the next miner
### Smart Contracts
In this project
- Smart Contracts are written in python
- Users can write their own smart contracts and deploy
- Users can also invoke the deployed contract using their deployed address
- They run inside a sandboxed environment with time limit, memory limit and operation limit  

**Implemented Using:** RestrictedPython, multiprocessing
### IPFS
IPFS is integrated as a wrapper for the existing IPFS network. IPFS hashes of the user uploaded files are stored in the blocks. Other users can use this to download the file.  

**Implemented Using:** IPFS
### Persistent Storage
Persistent storage is implemented to enable nodes to reconnect to the network using there previous network data
### Malicious Node
- To test the security and robustness of our networks we created a malicious node that attempts
    1. Generate invalid transactions (amt>account balance or amount<=0)
    2. Double Sign
- We have tested our blockchain networks using this malicious nodes to verify that our protocols are working and that our network is functional

## How to run this project
### Prerequisites
- `CPython 3.10 or newer`
- `pip` (python package manager)
- `venv` (for creating virtual environment)
### Installation & Setup
Clone project into your local machine
```bash
git clone https://github.com/TatHack-Tathva/Blockchain-Simulation.git
```
Enter into the project folder
```bash
cd BlockChain_Prototype
```
Create and activate a virtual environment. Use any installed CPython 3.10+ interpreter.
Windows PowerShell:
```powershell
py -0p
py -3.10 -m venv venv       # or py -3.11 / py -3.12 / py -3.13 / py -3.14
.\venv\Scripts\Activate.ps1
```
Install runtime dependencies:
```powershell
python -m pip install -r requirements.txt
```
For development/testing, install:
```powershell
python -m pip install -r requirements-dev.txt
```
### Terminal App
Start terminal app
```bash
python start_peer.py
```

sample:
  host: localhost
  port: 5000
  name: john

## Authors

**Rahan M**
[GitHub](https://github.com/Rahan-M) | [LinkedIn](https://www.linkedin.com/in/rahan-m-077a32254?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

**Jefin Joji**
[GitHub](https://github.com/JefinCodes) | [LinkedIn](https://www.linkedin.com/in/jefin-joji-659354313?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)


## Room-based signalling and web dashboard

The PoS implementation now supports an optional signalling station. The station
only performs peer discovery; blockchain messages continue to use direct
WebSocket connections between nodes.

### Start the signalling server

From the project root:

```bash
python -m signalling.server --host 0.0.0.0 --port 8765
```

### Start a PoS node with room discovery

In another terminal:

```bash
python start_peer.py
```

Choose:

- consensus: `pos`
- signalling room discovery: `y`
- room ID: for example `tathva-pos`
- signalling server: `ws://127.0.0.1:8765`
- dashboard: `y`

Run the same procedure for additional nodes, changing their ports and names
while keeping the same room ID.

The resulting topology is:

```text
                    Signalling Station
                         /       \
                        /         \
                    Node A <----> Node B
                      \             /
                       \           /
                         Node C
```

The signalling station is not a blockchain authority. It only tells nodes
which peers are available in the same room.

### Web dashboard

The default dashboard is available at:

```text
http://127.0.0.1:8000
```

It exposes:

- node status
- peer list and connection state
- blockchain height
- current validators and stake
- pending transactions
- chain weight
- valid/invalid block counts
- recent block data
- transaction submission
- stake submission

### PoS hardening

The corrected PoS path now:

1. Verifies the proposer block signature.
2. Verifies the VRF proof against the deterministic epoch seed.
3. Uses strict `VRF < threshold` eligibility.
4. Requires the creator's declared stake to equal its authenticated stake entry.
5. Rejects duplicate stake entries.
6. Rejects an incomplete or altered live stake snapshot.
7. Validates every stake signature.
8. Checks transaction signatures and sequential account balances.
9. Rejects future/backward/too-fast blocks.
10. Prevents the normal PoS node from producing two conflicting blocks in one epoch.
11. Validates both signatures in double-sign evidence before slashing.
12. Uses strictly heavier validated chains for PoS fork replacement.


