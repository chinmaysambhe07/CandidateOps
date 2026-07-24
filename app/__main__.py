#!/usr/bin/env python3
"""
CandidateOps - Main entry point.
Command-line interface for the CandidateOps application.
"""


import argparse
import sys
import getpass
from pathlib import Path

from app.main import CandidateOpsOrchestrator
from utils.logging_setup import setup_logging
from infrastructure.config.settings import settings


def main() -> None:
    """Main entry point for CandidateOps application."""
    # Set up logging
    setup_logging()
    logger = setup_logging(__name__)

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="CandidateOps - Automated candidate tracking from SAP Career portal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run single cycle with interactive password
  python -m app.main --username hr_user --single-cycle

  # Run continuous monitoring
  python -m app.main --username hr_user --continuous

  # Process specific positions
  python -m app.main --username hr_user --positions POS001 POS002 --single-cycle

  # Show current status
  python -m app.main --status
        """
    )

    parser.add_argument(
        "--username",
        "-u",
        required=True,
        help="Username for SAP SSO authentication"
    )

    parser.add_argument(
        "--password",
        "-p",
        help="Password for SAP SSO authentication (if not provided, will prompt)"
    )

    parser.add_argument(
        "--single-cycle",
        action="store_true",
        help="Run a single processing cycle and exit"
    )

    parser.add_argument(
        "--continuous",
        "-c",
        action="store_true",
        help="Run in continuous monitoring mode (default behavior)"
    )

    parser.add_argument(
        "--positions",
        "-pos",
        nargs="+",
        help="List of position IDs to process (e.g., POS001 POS002)"
    )

    parser.add_argument(
        "--check-interval",
        "-i",
        type=int,
        help="Check interval in seconds for continuous mode (overrides config)"
    )

    parser.add_argument(
        "--status",
        "-s",
        action="store_true",
        help="Show current application status and exit"
    )

    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Show version information and exit"
    )

    args = parser.parse_args()

    # Handle version request
    if args.version:
        print(f"CandidateOps v{settings.version}")
        sys.exit(0)

    # Handle status request
    if args.status:
        orchestrator = CandidateOpsOrchestrator()
        status = orchestrator.get_status()
        print("CandidateOps Status:")
        print(f"  Running: {status['running']}")
        print(f"  Shutdown Requested: {status['shutdown_requested']}")
        print(f"  SAP Authenticated: {status['sap_authenticated']}")
        print(f"  Processed Candidates: {status['processed_candidates_count']}")
        print(f"  SAP Client Type: {status['sap_client_type']}")
        sys.exit(0)

    # Validate arguments
    if not args.single_cycle and not args.continuous:
        # Default to continuous mode if neither specified
        args.continuous = True

    if args.single_cycle and args.continuous:
        logger.error("Cannot specify both --single-cycle and --continuous")
        parser.error("Cannot specify both --single-cycle and --continuous")

    # Get password if not provided
    password = args.password
    if not password:
        try:
            password = getpass.getpass("Password for SAP SSO: ")
        except Exception as e:
            logger.error(f"Failed to get password: {e}")
            sys.exit(1)

    # Initialize orchestrator
    logger.info("Initializing CandidateOps...")
    orchestrator = CandidateOpsOrchestrator()

    try:
        if args.single_cycle:
            # Run single cycle
            logger.info("Running single processing cycle...")
            results = orchestrator.run_single_cycle(
                username=args.username,
                password=password,
                position_ids=args.positions
            )

            print("\n=== CandidateOps Single Cycle Results ===")
            print(f"Status: {results['status'].upper()}")
            print(f"Duration: {results.get('duration_seconds', 0):.2f} seconds")
            print(f"Positions Processed: {results['positions_processed']}")
            print(f"Candidates Found: {results['candidates_found']}")
            print(f"New Candidates: {results['candidates_new']}")
            print(f"Updated Candidates: {results['candidates_updated']}")
            print(f"Attachments Downloaded: {results['attachments_downloaded']}")

            if results['errors']:
                print(f"\nErrors Encountered ({len(results['errors'])}):")
                for error in results['errors'][:5]:  # Show first 5 errors
                    print(f"  - {error}")
                if len(results['errors']) > 5:
                    print(f"  ... and {len(results['errors']) - 5} more")

        else:
            # Run continuous monitoring
            logger.info("Starting continuous monitoring mode...")
            orchestrator.run_continuous(
                username=args.username,
                password=password,
                position_ids=args.posents,
                check_interval=args.check_interval
            )

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down gracefully...")
        orchestrator.stop()
        print("\nShutdown complete.")
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        # Clean up
        orchestrator.sap_client.close()
        logger.info("CandidateOps shutdown complete")


if __name__ == "__main__":
    main()