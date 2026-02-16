#!/usr/bin/env python3
"""
Technical Debt Negotiator - CLI Tool
Analyze repositories for technical debt
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzers.code_analyzer import CodeAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description='Analyze repository for technical debt'
    )
    parser.add_argument(
        'repo_path',
        help='Path to repository to analyze'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file for results (JSON)',
        default=None
    )
    parser.add_argument(
        '--format',
        choices=['json', 'summary'],
        default='summary',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    # Validate repository path
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Run analysis
    print(f"Analyzing repository: {repo_path}")
    print("=" * 60)
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_repository(str(repo_path))
    
    # Output results
    if args.format == 'json':
        output = json.dumps(results, indent=2)
        print(output)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"\nResults saved to: {args.output}")
    
    else:  # summary format
        print_summary(results)
        
        if args.output:
            Path(args.output).write_text(json.dumps(results, indent=2))
            print(f"\nFull results saved to: {args.output}")


def print_summary(results: dict):
    """Print human-readable summary"""
    
    summary = results['summary']
    
    print("\n" + "=" * 60)
    print("TECHNICAL DEBT ANALYSIS SUMMARY")
    print("=" * 60)
    
    print(f"\nRepository: {results['repository']}")
    print(f"Scan Date: {results['scan_date']}")
    
    print(f"\n📊 Debt Items Found: {summary['total_debt_items']}")
    print(f"   🔴 Critical: {summary['critical']}")
    print(f"   🟡 High: {summary['high']}")
    print(f"   🟠 Medium: {summary['medium']}")
    
    print(f"\n💰 Total Annual Cost: ${summary['total_annual_cost']:,}")
    print(f"🔧 Refactoring Effort: {summary['refactoring_effort_weeks']} weeks")
    print(f"📈 Break Even: Week {summary['break_even_weeks']}")
    
    # Print critical items
    critical_items = [
        item for item in results['debt_items']
        if item['severity'] == 'critical'
    ]
    
    if critical_items:
        print(f"\n🚨 CRITICAL ISSUES ({len(critical_items)}):")
        for item in critical_items[:5]:  # Top 5
            print(f"\n   {item['type']}")
            print(f"   Location: {item['location']}")
            print(f"   Description: {item['description']}")
            print(f"   Cost: ${item['annual_cost']:,}/year")
            print(f"   Fix: {item['fix_effort_weeks']} weeks")
    
    # Print recommendations
    if results.get('recommendations'):
        print(f"\n✅ RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"\n   Priority {rec['priority']}: {rec['title']}")
            print(f"   Effort: {rec['effort_weeks']} weeks")
            print(f"   Savings: ${rec['annual_savings']:,}/year")
    
    print("\n" + "=" * 60)
    print("\n💡 Next Steps:")
    print("   1. Review critical issues first")
    print("   2. Calculate ROI for refactoring")
    print("   3. Compare with new feature development")
    print("   4. Make data-driven decision")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
