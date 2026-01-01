import json
import hashlib

def canonicalize_ax(ax_doc: dict) -> bytes:
    """
    Canonicalize an AX document for hashing.

    - Removes non-capability fields
    - Sorts keys deterministically
    - Produces UTF-8 encoded JSON bytes
    """

    capability_subset = {
        "agent": ax_doc.get("agent"),
        "endpoints": ax_doc.get("endpoints"),
        "capabilities": ax_doc.get("capabilities"),
        "schema": ax_doc.get("schema")
    }

    canonical_json = json.dumps(
        capability_subset,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    return canonical_json.encode("utf-8")


def hash_capabilities(ax_doc: dict) -> str:
    """
    Compute a SHA-256 capability hash for an AX document.
    """
    canonical_bytes = canonicalize_ax(ax_doc)
    return hashlib.sha256(canonical_bytes).hexdigest()


def verify_hash(ax_doc: dict, expected_hash: str) -> bool:
    """
    Verify an AX document against a previously known capability hash.
    """
    return hash_capabilities(ax_doc) == expected_hash


if __name__ == "__main__":
    with open("sample-ax.json", "r", encoding="utf-8") as f:
        ax = json.load(f)

    capability_hash = hash_capabilities(ax)
    print("Capability Hash:", capability_hash)
    
    # Test verification
    is_valid = verify_hash(ax, capability_hash)
    print("Hash verification:", is_valid)
    
    # Test with wrong hash
    wrong_hash = "wrong_hash_example"
    is_invalid = verify_hash(ax, wrong_hash)
    print("Wrong hash verification:", is_invalid)
