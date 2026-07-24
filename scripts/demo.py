"""
Demo script for CandidateOps.
Shows basic usage of the CandidateOps orchestrator.
"""


import tempfile
import shutil
from pathlib import Path
from app.main import CandidateOpsOrchestrator
from utils.logging_setup import setup_logging


def demo_single_cycle():
    """Demonstrate a single processing cycle."""
    print("=== CandidateOps Demo: Single Cycle ===")

    # Setup logging
    setup_logging()

    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Override config paths for demo
        import os
        os.environ['EXCEL__TEMPLATE_PATH'] = str(temp_path / 'templates' / 'candidate_template.xlsx')
        os.environ['EXCEL__OUTPUT_PATH'] = str(temp_path / 'output' / 'candidates_tracking.xlsx')
        os.environ['FILE__BASE_OUTPUT_DIR'] = str(temp_path / 'candidates_data')
        os.environ['LOGGING__FILE_PATH'] = str(temp_path / 'logs' / 'candidate_ops.log')

        # Initialize orchestrator (will use mock SAP client by default)
        orchestrator = CandidateOpsOrchestrator()

        try:
            # Run a single cycle with demo credentials
            # In real usage, you would provide actual SAP credentials
            results = orchestrator.run_single_cycle(
                username="demo_user",
                password="demo_pass",
                position_ids=["POS001"]  # Process just one position for demo
            )

            print(f"Cycle Status: {results['status']}")
            print(f"Positions Processed: {results['positions_processed']}")
            print(f"Candidates Found: {results['candidates_found']}")
            print(f"New Candidates: {results['candidates_new']}")
            print(f"Updated Candidates: {results['candidates_updated']}")
            print(f"Attachments Downloaded: {results['attachments_downloaded']}")

            if results.get('errors'):
                print(f"Errors Encountered: {len(results['errors'])}")
                for error in results['errors'][:3]:
                    print(f"  - {error}")

            print("\nDemo completed successfully!")
            print(f"Check the output in: {temp_path}")

        except Exception as e:
            print(f"Demo failed with error: {e}")
            print("Note: This demo uses the mock SAP client. For real SAP,")
            print("you would need to implement the real SAP client or")
            print("configure the mock to match your SAP environment.")


def demo_continuous_mode_info():
    """Show information about continuous mode."""
    print("\n=== CandidateOps Demo: Continuous Mode Info ===")
    print("To run in continuous monitoring mode:")
    print("  python -m app.main --username your_user --continuous")
    print("\nThis will:")
    print("  1. Authenticate to SAP Career portal")
    print("  2. Process positions POS001 and POS002 (default)")
    print("  3. Check for new applications every 5 minutes (configurable)")
    print("  4. Continue until stopped with Ctrl+C")
    print("\nFor position-specific monitoring:")
    print("  python -m app.main --username your_user --positions POS001 POS003 --continuous")


if __name__ == "__main__":
    demo_single_cycle()
    demo_continuous_mode_info()
    print("\n=== CandidateOps Demo Complete ===")
    print("See README.md for full usage instructions.")