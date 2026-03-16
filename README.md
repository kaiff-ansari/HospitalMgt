# Blockchain Integration — Simple Steps

---

## Step 1 — Created BlockchainAudit Model

First I created a table called `blockchain_audit` that stores information about every block.

**Each block stores this information:**

| Field | What it stores |
|-------|---------------|
| `id` | Unique number of the block |
| `table_name` | Which module this block belongs to — doctors, blood_inventory |
| `record_id` | The ID of that record |
| `previous_hash` | Hash of the previous block |
| `current_hash` | Hash of this block |
| `data` | Original data in JSON format |
| `timestamp` | When the block was created |

**This is how the chain looks:**

```
Block 1                       Block 2                       Block 3
previous_hash = "0"     --->  previous_hash = "abc123" ---> previous_hash = "def456"
current_hash  = "abc123"      current_hash  = "def456"      current_hash  = "ghi789"
table_name    = "doctors"     table_name    = "doctors"      table_name    = "blood_inventory"
```

> The first block always has `previous_hash = "0"` because there is no block before it. This is called the **Genesis Block**.

---

## Step 2 — Created Blockchain Folder

I created a `blockchain` folder with 2 files:

### `hashservice.py`
This file has one job — it converts data into a SHA-256 hash.
```
Data  →  JSON String  →  SHA-256  →  Hash value
```

### `blockservice.py`
This file has 3 functions:

**1. add_block** — Creates a new block
```
Find the last block in the chain
          ↓
Take its hash as previous_hash
          ↓
Generate a new hash for current block
          ↓
Save the new block in database
```

**2. verify_chain** — Checks if the chain is valid
```
Get all blocks from oldest to newest
          ↓
Recompute the hash of each block from stored data
          ↓
Compare recomputed hash with stored hash
          ↓
If they do not match  →  Tamper detected ❌
If they match         →  Chain is valid ✅
```

**3. fix_tampered_block** — Admin uses this to fix a tampered block
```
Take the stored original data
          ↓
Recompute the correct hash
          ↓
Restore the correct hash in the block
          ↓
Chain becomes valid again ✅
```

---

## Step 3 — Applied Blockchain in Doctor Module

### POST — Register a Doctor
```
Doctor registers
      ↓
Data is saved in the doctors table
      ↓
A new block is created with doctor data
      ↓
Block is stored in blockchain_audit table
```

### PUT — Update a Doctor
```
Update request comes in
      ↓
First verify_chain() is called — is the chain valid?
      ↓
Valid   →  Update the doctor  →  Create a new block
Invalid →  Return 409 Error — "Blockchain compromised"
```

### DELETE — Delete a Doctor
```
Delete request comes in
      ↓
First verify_chain() is called — is the chain valid?
      ↓
Capture the doctor data before deleting
      ↓
Create a block with action = "deleted"
      ↓
Then delete the doctor record
```

> **Important** — Always create the block BEFORE deleting.
> If you delete first, the data will be gone and the block cannot be created.

---

## Step 4 — Applied Blockchain in Blood Inventory Module

Exact same logic as Doctor — only the `table_name` is different.

### POST — Add Blood Inventory
```
Blood inventory record is added
      ↓
Data is saved in blood_inventory table
      ↓
A new block is created — table_name = "blood_inventory"
      ↓
Block is stored in blockchain_audit table
```

### PUT — Update Blood Inventory
```
First verify_chain()
      ↓
Update the record
      ↓
Create a new block
```

### DELETE — Delete Blood Inventory
```
First verify_chain()
      ↓
Create a block with action = "deleted"
      ↓
Delete the record
```

---

## Full Flow — At a Glance

```
Doctor Registers
      ↓
Block 1 created  →  table: doctors,          previous_hash: "0"

Blood Inventory Added
      ↓
Block 2 created  →  table: blood_inventory,  previous_hash: Block 1 hash

Doctor Updated
      ↓
verify_chain → valid ✅
Block 3 created  →  table: doctors,          previous_hash: Block 2 hash

Doctor Deleted
      ↓
verify_chain → valid ✅
Block 4 created  →  table: doctors,          previous_hash: Block 3 hash, action: deleted
```

All modules share **one single chain** — every block is linked to the previous one regardless of which module it belongs to.

---

## What Happens When Tampering is Detected

```
Someone changes data or hash directly in the database
                    ↓
verify_chain() detects the mismatch
                    ↓
All operations are blocked
register ❌    update ❌    delete ❌
                    ↓
Admin calls  GET /blockchain/verify
                    ↓
Gets the tampered block ID
                    ↓
Admin calls  POST /blockchain/fix/{id}
                    ↓
Correct hash is restored from original stored data
                    ↓
System is unlocked — everything works normally ✅
```

---

Key Benefits
• Data tamper detection
• Immutable audit trail
• Secure change tracking
• Blockchain-style integrity without external network|
