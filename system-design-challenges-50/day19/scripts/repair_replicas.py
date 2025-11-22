import os
import shutil
import argparse
from typing import List, Dict
import sys

# Add parent directory to path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.services.replication_service import ReplicationService
from app.services.recovery_service import RecoveryService


def check_replica_consistency() -> Dict[str, dict]:
    """Check consistency between primary and replicas"""
    recovery_service = RecoveryService()
    return recovery_service.validate_consistency()


def repair_replicas(primary_path: str, replica_paths: List[str]) -> Dict[str, str]:
    """Repair replicas by synchronizing with primary"""
    results = {}
    
    for replica_path in replica_paths:
        try:
            # Clear replica directory
            if os.path.exists(replica_path):
                shutil.rmtree(replica_path)
            
            # Recreate directory
            os.makedirs(replica_path, exist_ok=True)
            
            # Copy files from primary to replica
            if os.path.exists(primary_path):
                for item in os.listdir(primary_path):
                    source_path = os.path.join(primary_path, item)
                    destination_path = os.path.join(replica_path, item)
                    
                    if os.path.isfile(source_path):
                        shutil.copy2(source_path, destination_path)
                    elif os.path.isdir(source_path):
                        shutil.copytree(source_path, destination_path)
            
            results[replica_path] = "repaired"
            print(f"Successfully repaired {replica_path}")
            
        except Exception as e:
            results[replica_path] = f"error: {e}"
            print(f"Error repairing {replica_path}: {e}")
    
    return results


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Repair replica consistency")
    parser.add_argument("--primary", default=settings.STORAGE_PATH, help="Primary storage path")
    parser.add_argument("--replica1", default=settings.REPLICA1_PATH, help="Replica 1 path")
    parser.add_argument("--replica2", default=settings.REPLICA2_PATH, help="Replica 2 path")
    parser.add_argument("--check-only", action="store_true", help="Only check consistency, don't repair")
    
    args = parser.parse_args()
    
    print("Checking replica consistency...")
    consistency = check_replica_consistency()
    
    print(f"Primary files: {consistency['primary']['file_count']}")
    print(f"Replica 1 files: {consistency['replica1']['file_count']} (consistent: {consistency['replica1']['consistent_with_primary']})")
    print(f"Replica 2 files: {consistency['replica2']['file_count']} (consistent: {consistency['replica2']['consistent_with_primary']})")
    print(f"Overall consistent: {consistency['overall_consistent']}")
    
    if args.check_only:
        return
    
    if not consistency['overall_consistent']:
        print("\nReplicas are inconsistent. Repairing...")
        replica_paths = [args.replica1, args.replica2]
        results = repair_replicas(args.primary, replica_paths)
        
        print("\nRepair results:")
        for path, result in results.items():
            print(f"  {path}: {result}")
        
        # Verify consistency after repair
        print("\nVerifying consistency after repair...")
        new_consistency = check_replica_consistency()
        print(f"Overall consistent after repair: {new_consistency['overall_consistent']}")
    else:
        print("\nAll replicas are consistent. No repair needed.")


if __name__ == "__main__":
    main()