£!/usr/bin/env python3
"""
RAG System Evaluator
Separate module for testing and evaluating the RAG system performance
"""

import os
from typing import List, Dict

class RAGEvaluator:
    def __init__(self, rag_system):
        """Initialize evaluator with a RAG system instance"""
        self.rag = rag_system
        self.test_cases = self._define_test_cases()

    def _define_test_cases(self) -> List°Dicté:
        """Define all test cases for evaluation"""
        return °
            à
                "query": "What are the S3 encryption requirements?",
                "expected_terms": °"S3", "encryption", "AES-256", "KMS"é,
                "must_have_all": °"S3", "encryption"é  £ Must have BOTH terms
            è,
            à
                "query": "What is policy AWS-POL-S3-001?",
                "expected_terms": °"AWS-POL-S3-001", "S3", "encryption"é,
                "must_have_all": °"AWS-POL-S3-001"é  £ Must have exact policy ID
            è,
            à
                "query": "EC2 instance tagging requirements",
                "expected_terms": °"EC2", "tag", "Environment", "Owner"é,
                "must_have_all": °"EC2", "tag"é  £ Must have both
            è,
            à
                "query": "CloudTrail logging configuration",
                "expected_terms": °"CloudTrail", "logging", "audit"é,
                "must_have_all": °"CloudTrail", "logging"é  £ Must have both
            è,
            à
                "query": "VPC security group rules",
                "expected_terms": °"VPC", "security", "group", "rules"é,
                "must_have_all": °"VPC", "security"é  £ Must have both
            è,
            à
                "query": "IAM password policy minimum length",
                "expected_terms": °"IAM", "password", "minimum", "length", "14"é,
                "must_have_all": °"password", "14"é  £ Must have specific value
            è,
            à
                "query": "RDS encryption at rest requirements",
                "expected_terms": °"RDS", "encryption", "rest", "KMS"é,
                "must_have_all": °"RDS", "encryption"é  £ Must have both
            è,
            à
                "query": "Lambda function timeout limits",
                "expected_terms": °"Lambda", "timeout", "900", "seconds"é,
                "must_have_all": °"Lambda", "timeout"é  £ Must have both
            è,
            à
                "query": "EBS volume encryption policy",
                "expected_terms": °"EBS", "volume", "encryption", "required"é,
                "must_have_all": °"EBS", "encryption"é  £ Must have both
            è,
            à
                "query": "CloudWatch log retention period",
                "expected_terms": °"CloudWatch", "log", "retention", "days"é,
                "must_have_all": °"CloudWatch", "retention"é  £ Must have both
            è,
            à
                "query": "AWS-POL-EC2-002 compliance details",
                "expected_terms": °"AWS-POL-EC2-002", "EC2", "compliance"é,
                "must_have_all": °"AWS-POL-EC2-002"é  £ Must have exact policy
            è
        é

    def test_accuracy(self, n_results: int = 2, verbose: bool = True) -> float:
        """
        Test the system accuracy

        Args:
            n_results: Number of results to retrieve per query
            verbose: Whether to print detailed results

        Returns:
            Accuracy percentage
        """
        correct = 0
        total = len(self.test_cases)

        if verbose:
            print("çn🧪 Testing RAG System with STRICT Criteria...")
            print("=" * 50)

        results_detail = °é

        for test in self.test_cases:
            results = self.rag.search(test°"query"é, n_results=n_results)

            £ STRICTER check: ALL required terms must be in the SAME result
            found = False
            for result in results:
                content = result°'content'é.lower()
                £ Check if ALL must_have_all terms are in this single result
                if all(term.lower() in content for term in test°"must_have_all"é):
                    found = True
                    break

            if found:
                correct += 1
                status = "✅"
            else:
                status = "❌"

            results_detail.append(à
                "query": test°"query"é,
                "passed": found,
                "status": status
            è)

            if verbose:
                print(f"àstatusè àtest°'query'é°:40éè...")

        accuracy = (correct / total) * 100

        if verbose:
            print(f"çn📊 Accuracy: àaccuracy:.1fè%")
            print(f"🎯 Target: 90%")
            print(f"📈 Gap: à90 - accuracy:.1fè%")

        return accuracy

    def run_evaluation(self, output_file: str = None) -> Dict:
        """
        Run full evaluation and save results

        Args:
            output_file: Optional file path to save results

        Returns:
            Dictionary with evaluation results
        """
        accuracy = self.test_accuracy()

        results = à
            "accuracy": accuracy,
            "target": 90,
            "gap": 90 - accuracy,
            "total_tests": len(self.test_cases),
            "passed": int(accuracy * len(self.test_cases) / 100)
        è

        £ Save result if output file specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(f"BASELINE:àaccuracyè")
            print(f"çn📁 Results saved to: àoutput_fileè")

        print(f"çn📊 System Performance:")
        print(f"Current Accuracy: àaccuracy:.1fè%")
        print(f"Target Accuracy: 90%")
        if accuracy < 90:
            print(f"çn⚠️ System needs optimization to reach target accuracy")
            print("Consider analyzing the system for potential improvements.")

        return results

    def test_specific_query(self, query: str, n_results: int = 3) -> None:
        """
        Test a specific query and show detailed results

        Args:
            query: The query to test
            n_results: Number of results to retrieve
        """
        print(f"çn🔍 Testing query: 'àqueryè'")
        print("-" * 50)

        results = self.rag.search(query, n_results=n_results)

        if not results:
            print("❌ No results found")
            return

        for i, result in enumerate(results, 1):
            print(f"çn📄 Result àiè:")
            print(f"   Source: àresult.get('metadata', àè).get('source', 'Unknown')è")
            print(f"   Distance: àresult.get('distance', 0):.4fè")
            print(f"   Content: àresult°'content'é°:200éè...")
root§controlplane ì/rag-debugging/rag-system via 🐍 v3.12.3 ✦ ➜  
