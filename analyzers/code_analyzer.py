"""
Code Analyzer for Technical Debt Detection
Scans repositories for technical debt patterns
"""

import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pathlib import Path


class DebtItem:
    """Represents a single technical debt item"""
    
    def __init__(self, debt_type: str, severity: str, location: str,
                 description: str, annual_cost: int, fix_effort_weeks: int):
        self.type = debt_type
        self.severity = severity
        self.location = location
        self.description = description
        self.annual_cost = annual_cost
        self.fix_effort_weeks = fix_effort_weeks
        self.details = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'severity': self.severity,
            'location': self.location,
            'description': self.description,
            'annual_cost': self.annual_cost,
            'fix_effort_weeks': self.fix_effort_weeks,
            'details': self.details
        }


class CodeAnalyzer:
    """Main analyzer for detecting technical debt"""
    
    def __init__(self):
        self.debt_items: List[DebtItem] = []
    
    def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Analyze a repository for technical debt
        
        Args:
            repo_path: Path to repository root
            
        Returns:
            Analysis results with debt items and costs
        """
        repo_path = Path(repo_path)
        
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        print(f"Analyzing repository: {repo_path}")
        
        # Reset debt items
        self.debt_items = []
        
        # Run various analyzers
        self._check_dependencies(repo_path)
        self._check_code_complexity(repo_path)
        self._check_security_issues(repo_path)
        
        # Check for ML-specific debt
        if self._is_ml_project(repo_path):
            self._check_ml_debt(repo_path)
        
        # Check for data pipeline debt
        if self._is_data_pipeline(repo_path):
            self._check_pipeline_debt(repo_path)
        
        # Calculate totals and generate report
        return self._generate_report(repo_path)
    
    def _check_dependencies(self, repo_path: Path):
        """Check for outdated dependencies"""
        
        # Check requirements.txt (Python)
        req_file = repo_path / 'requirements.txt'
        if req_file.exists():
            with open(req_file) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if '==' in line and not line.startswith('#'):
                        package, version = line.split('==')
                        package = package.strip()
                        version = version.strip()
                        
                        # Simple heuristic: check for old packages
                        if self._is_old_package(package, version):
                            self.debt_items.append(DebtItem(
                                debt_type='outdated_dependency',
                                severity='high',
                                location=f'requirements.txt:{line_num}',
                                description=f'{package}=={version} is outdated',
                                annual_cost=45000,
                                fix_effort_weeks=2
                            ))
        
        # Check pom.xml (Java)
        pom_file = repo_path / 'pom.xml'
        if pom_file.exists():
            content = pom_file.read_text()
            
            # Check for Log4j 1.x
            if '<artifactId>log4j</artifactId>' in content:
                if '<version>1.' in content:
                    self.debt_items.append(DebtItem(
                        debt_type='security_vulnerability',
                        severity='critical',
                        location='pom.xml',
                        description='Log4j 1.x - CVE-2021-44228 (Log4Shell)',
                        annual_cost=100000,
                        fix_effort_weeks=1
                    ))
    
    def _is_old_package(self, package: str, version: str) -> bool:
        """Heuristic to detect old packages"""
        
        # Known old packages (simplified)
        old_packages = {
            'tensorflow': {'1.15', '1.14', '1.13'},
            'pandas': {'0.25', '0.24', '0.23'},
            'numpy': {'1.16', '1.17', '1.18'},
            'scikit-learn': {'0.22', '0.21', '0.20'},
            'pyspark': {'2.4', '2.3'},
        }
        
        package_lower = package.lower()
        for pkg, old_versions in old_packages.items():
            if pkg in package_lower:
                for old_ver in old_versions:
                    if version.startswith(old_ver):
                        return True
        
        return False
    
    def _check_code_complexity(self, repo_path: Path):
        """Check for God classes and complex code"""
        
        for ext in ['*.py', '*.java', '*.js']:
            for file_path in repo_path.rglob(ext):
                # Skip test files and node_modules
                if 'test' in str(file_path) or 'node_modules' in str(file_path):
                    continue
                
                try:
                    content = file_path.read_text()
                    lines = content.split('\n')
                    
                    # Check file size
                    if len(lines) > 500:
                        self.debt_items.append(DebtItem(
                            debt_type='god_class',
                            severity='high',
                            location=str(file_path.relative_to(repo_path)),
                            description=f'{len(lines)} lines - should be split',
                            annual_cost=50000,
                            fix_effort_weeks=2
                        ))
                    
                    # Check for specific antipatterns
                    if '2,300 lines in one function' in content:
                        self.debt_items.append(DebtItem(
                            debt_type='god_function',
                            severity='critical',
                            location=str(file_path.relative_to(repo_path)),
                            description='Massive function that cannot be tested',
                            annual_cost=80000,
                            fix_effort_weeks=3
                        ))
                
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
    
    def _check_security_issues(self, repo_path: Path):
        """Check for security vulnerabilities"""
        
        # Patterns for hardcoded credentials
        credential_patterns = [
            r'password\s*=\s*["\'][\w!@#$%^&*]+["\']',
            r'api_key\s*=\s*["\'][A-Za-z0-9]+["\']',
            r'secret\s*=\s*["\'][A-Za-z0-9]+["\']',
            r'DB_PASSWORD\s*=\s*["\'][\w!@#$%^&*]+["\']',
        ]
        
        for file_path in repo_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Only check code and config files
            if file_path.suffix not in ['.py', '.java', '.js', '.yaml', '.yml', '.json', '.properties']:
                continue
            
            try:
                content = file_path.read_text()
                
                for pattern in credential_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.debt_items.append(DebtItem(
                            debt_type='hardcoded_credentials',
                            severity='critical',
                            location=str(file_path.relative_to(repo_path)),
                            description='Hardcoded credentials found',
                            annual_cost=100000,
                            fix_effort_weeks=1
                        ))
                        break  # One finding per file is enough
                
                # Check for SQL injection
                if file_path.suffix == '.py':
                    if re.search(r'f["\']SELECT.*\{|f["\']INSERT.*\{|f["\']UPDATE.*\{', content):
                        self.debt_items.append(DebtItem(
                            debt_type='sql_injection_risk',
                            severity='critical',
                            location=str(file_path.relative_to(repo_path)),
                            description='SQL query built with f-strings',
                            annual_cost=200000,
                            fix_effort_weeks=1
                        ))
            
            except Exception:
                pass  # Skip binary files
    
    def _is_ml_project(self, repo_path: Path) -> bool:
        """Detect if this is an ML project"""
        
        # Check for ML-related files
        indicators = [
            'train.py',
            'model.py',
            'feature_engineering.py',
            'requirements.txt'  # Will check content
        ]
        
        for indicator in indicators:
            if list(repo_path.rglob(indicator)):
                return True
        
        # Check requirements.txt for ML packages
        req_file = repo_path / 'requirements.txt'
        if req_file.exists():
            content = req_file.read_text().lower()
            if any(pkg in content for pkg in ['tensorflow', 'pytorch', 'scikit-learn', 'keras']):
                return True
        
        return False
    
    def _check_ml_debt(self, repo_path: Path):
        """Check for ML-specific debt"""
        
        # Check for model staleness
        for file_path in repo_path.rglob('*.py'):
            if 'train' in file_path.name.lower():
                try:
                    content = file_path.read_text()
                    
                    # Look for last training date
                    match = re.search(r'Last (?:run|trained?):\s*(\d{4}-\d{2}-\d{2})', content)
                    if match:
                        last_run_str = match.group(1)
                        last_run = datetime.strptime(last_run_str, '%Y-%m-%d')
                        days_ago = (datetime.now() - last_run).days
                        
                        if days_ago > 90:
                            self.debt_items.append(DebtItem(
                                debt_type='model_staleness',
                                severity='critical',
                                location=str(file_path.relative_to(repo_path)),
                                description=f'Model last trained {days_ago} days ago',
                                annual_cost=564000,
                                fix_effort_weeks=1
                            ))
                
                except Exception:
                    pass
        
        # Check for undocumented features
        for file_path in repo_path.rglob('*.py'):
            if 'feature' in file_path.name.lower():
                try:
                    content = file_path.read_text()
                    
                    # Count generic feature names
                    magic_features = len(re.findall(r'feature_\d+', content))
                    
                    if magic_features > 10:
                        self.debt_items.append(DebtItem(
                            debt_type='undocumented_features',
                            severity='high',
                            location=str(file_path.relative_to(repo_path)),
                            description=f'{magic_features} undocumented features found',
                            annual_cost=144000,
                            fix_effort_weeks=2
                        ))
                
                except Exception:
                    pass
    
    def _is_data_pipeline(self, repo_path: Path) -> bool:
        """Detect if this is a data pipeline project"""
        
        indicators = [
            'airflow',
            'kafka',
            'spark',
            'pipeline',
            'etl'
        ]
        
        # Check directory names
        for item in repo_path.iterdir():
            if item.is_dir() and any(ind in item.name.lower() for ind in indicators):
                return True
        
        return False
    
    def _check_pipeline_debt(self, repo_path: Path):
        """Check for data pipeline debt"""
        
        # Check for version sprawl
        dag_dir = repo_path / 'airflow-dags'
        if dag_dir.exists():
            etl_files = list(dag_dir.glob('etl_pipeline*.py'))
            if len(etl_files) > 2:
                self.debt_items.append(DebtItem(
                    debt_type='version_sprawl',
                    severity='high',
                    location='airflow-dags/',
                    description=f'{len(etl_files)} versions of ETL pipeline found',
                    annual_cost=78000,
                    fix_effort_weeks=3
                ))
        
        # Check for storage hoarding (simplified)
        for file_path in repo_path.rglob('*.py'):
            try:
                content = file_path.read_text()
                if '12 TB' in content and 'archive' in content.lower():
                    self.debt_items.append(DebtItem(
                        debt_type='storage_hoarding',
                        severity='critical',
                        location=str(file_path.relative_to(repo_path)),
                        description='Mystery archive folder with unknown contents',
                        annual_cost=216000,
                        fix_effort_weeks=4
                    ))
            except Exception:
                pass
    
    def _generate_report(self, repo_path: Path) -> Dict[str, Any]:
        """Generate analysis report"""
        
        # Calculate totals
        total_cost = sum(item.annual_cost for item in self.debt_items)
        total_effort = sum(item.fix_effort_weeks for item in self.debt_items)
        
        # Estimate break-even (simplified)
        team_size = 5
        weekly_rate = 10000
        refactoring_cost = total_effort * team_size * weekly_rate
        annual_savings = total_cost
        break_even_weeks = int(refactoring_cost / (annual_savings / 52)) if annual_savings > 0 else 0
        
        # Count by severity
        severity_counts = {
            'critical': sum(1 for item in self.debt_items if item.severity == 'critical'),
            'high': sum(1 for item in self.debt_items if item.severity == 'high'),
            'medium': sum(1 for item in self.debt_items if item.severity == 'medium'),
        }
        
        report = {
            'repository': repo_path.name,
            'scan_date': datetime.now().isoformat(),
            'summary': {
                'total_debt_items': len(self.debt_items),
                'critical': severity_counts['critical'],
                'high': severity_counts['high'],
                'medium': severity_counts['medium'],
                'total_annual_cost': total_cost,
                'refactoring_effort_weeks': total_effort,
                'break_even_weeks': break_even_weeks
            },
            'debt_items': [item.to_dict() for item in self.debt_items],
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations"""
        
        # Group by type
        recommendations = []
        
        # Critical security issues first
        security_items = [item for item in self.debt_items 
                         if item.severity == 'critical' and 'security' in item.type]
        if security_items:
            recommendations.append({
                'priority': 1,
                'title': 'Fix Critical Security Issues',
                'effort_weeks': sum(item.fix_effort_weeks for item in security_items),
                'annual_savings': sum(item.annual_cost for item in security_items),
                'items': [self.debt_items.index(item) for item in security_items]
            })
        
        # Architecture improvements
        arch_items = [item for item in self.debt_items 
                     if item.type in ['god_class', 'god_library']]
        if arch_items:
            recommendations.append({
                'priority': 2,
                'title': 'Refactor Architecture',
                'effort_weeks': sum(item.fix_effort_weeks for item in arch_items),
                'annual_savings': sum(item.annual_cost for item in arch_items),
                'items': [self.debt_items.index(item) for item in arch_items]
            })
        
        return recommendations


if __name__ == '__main__':
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python code_analyzer.py <repo_path>")
        sys.exit(1)
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_repository(sys.argv[1])
    
    print(json.dumps(results, indent=2))
