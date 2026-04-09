"""
Tracksy Global — Blockchain Ledger.
"""
import hashlib
import json
from database import get_db

class BlockchainLedger:
    def create_block(self, order_id, event_type, payload):
        db = get_db()
        last_block = db.execute("SELECT block_hash FROM blockchain_ledger WHERE order_id=? ORDER BY id DESC LIMIT 1", (order_id,)).fetchone()
        prev_hash = last_block['block_hash'] if last_block else "0" * 64
        
        block_data = {"order_id": order_id, "event": event_type, "payload": payload, "prev": prev_hash}
        block_hash = hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()
        
        db.execute(
            "INSERT INTO blockchain_ledger (order_id, block_hash, previous_hash, event_type, payload_json) VALUES (?, ?, ?, ?, ?)",
            (order_id, block_hash, prev_hash, event_type, json.dumps(payload))
        )
        db.execute("UPDATE orders SET blockchain_hash=? WHERE id=?", (block_hash, order_id))
        db.commit()
        return block_hash

    def verify_chain(self, order_id):
        db = get_db()
        blocks = db.execute("SELECT * FROM blockchain_ledger WHERE order_id=? ORDER BY id ASC", (order_id,)).fetchall()
        prev = "0" * 64
        for b in blocks:
            if b['previous_hash'] != prev:
                return False, len(blocks)
            prev = b['block_hash']
        return True, len(blocks)

    def get_audit_trail(self, order_id):
        db = get_db()
        blocks = db.execute("SELECT block_hash, previous_hash, event_type, timestamp FROM blockchain_ledger WHERE order_id=? ORDER BY id ASC", (order_id,)).fetchall()
        return [dict(b) for b in blocks]

blockchain_ledger = BlockchainLedger()
