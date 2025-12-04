#!/usr/bin/env python3
"""
Perplexity Enhancement MCP Evolution Tracker

Monitors and tracks the evolution of Perplexity Enhancement MCP capabilities.
Tracks learning progress, success rates, and optimization metrics.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import subprocess

@dataclass
class MCPToolExecution:
    """Record of MCP tool execution"""
    timestamp: str
    tool_name: str
    success: bool
    execution_time_ms: float
    input_tokens: int
    output_tokens: int
    error: Optional[str] = None

@dataclass
class LearningMetric:
    """Learning progress metric"""
    timestamp: str
    metric_type: str  # 'deployment', 'legal_motion', 'code_generation'
    success_rate: float
    avg_execution_time: float
    total_executions: int
    patterns_learned: int

@dataclass
class EvolutionSnapshot:
    """Complete evolution state snapshot"""
    timestamp: str
    total_tool_calls: int
    success_rate: float
    learned_patterns: int
    avg_execution_time: float
    memory_size_mb: float
    intelligence_score: float  # Calculated metric

class MCPEnhancementTracker:
    """Track evolution of Perplexity Enhancement MCP capabilities"""
    
    def __init__(self, db_path: str = "~/.goose-evolve/mcp_enhancement.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        cursor = self.conn.cursor()
        
        # Tool executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                execution_time_ms REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                error TEXT
            )
        """)
        
        # Learning metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                success_rate REAL,
                avg_execution_time REAL,
                total_executions INTEGER,
                patterns_learned INTEGER
            )
        """)
        
        # Evolution snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evolution_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_tool_calls INTEGER,
                success_rate REAL,
                learned_patterns INTEGER,
                avg_execution_time REAL,
                memory_size_mb REAL,
                intelligence_score REAL
            )
        """)
        
        self.conn.commit()
    
    def record_tool_execution(self, execution: MCPToolExecution):
        """Record MCP tool execution"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tool_executions 
            (timestamp, tool_name, success, execution_time_ms, input_tokens, output_tokens, error)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            execution.timestamp,
            execution.tool_name,
            execution.success,
            execution.execution_time_ms,
            execution.input_tokens,
            execution.output_tokens,
            execution.error
        ))
        self.conn.commit()
    
    def record_learning_metric(self, metric: LearningMetric):
        """Record learning progress metric"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO learning_metrics
            (timestamp, metric_type, success_rate, avg_execution_time, total_executions, patterns_learned)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            metric.timestamp,
            metric.metric_type,
            metric.success_rate,
            metric.avg_execution_time,
            metric.total_executions,
            metric.patterns_learned
        ))
        self.conn.commit()
    
    def create_evolution_snapshot(self) -> EvolutionSnapshot:
        """Create snapshot of current evolution state"""
        cursor = self.conn.cursor()
        
        # Get total tool calls
        cursor.execute("SELECT COUNT(*) FROM tool_executions")
        total_calls = cursor.fetchone()[0]
        
        # Get success rate
        cursor.execute("SELECT AVG(CAST(success AS FLOAT)) FROM tool_executions")
        success_rate = cursor.fetchone()[0] or 0.0
        
        # Get learned patterns (from memory)
        learned_patterns = self._count_learned_patterns()
        
        # Get average execution time
        cursor.execute("SELECT AVG(execution_time_ms) FROM tool_executions WHERE success = 1")
        avg_time = cursor.fetchone()[0] or 0.0
        
        # Get memory size
        memory_size = self._get_memory_size_mb()
        
        # Calculate intelligence score
        intelligence_score = self._calculate_intelligence_score(
            success_rate, learned_patterns, avg_time
        )
        
        snapshot = EvolutionSnapshot(
            timestamp=datetime.now().isoformat(),
            total_tool_calls=total_calls,
            success_rate=success_rate,
            learned_patterns=learned_patterns,
            avg_execution_time=avg_time,
            memory_size_mb=memory_size,
            intelligence_score=intelligence_score
        )
        
        # Save snapshot
        cursor.execute("""
            INSERT INTO evolution_snapshots
            (timestamp, total_tool_calls, success_rate, learned_patterns, 
             avg_execution_time, memory_size_mb, intelligence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            snapshot.timestamp,
            snapshot.total_tool_calls,
            snapshot.success_rate,
            snapshot.learned_patterns,
            snapshot.avg_execution_time,
            snapshot.memory_size_mb,
            snapshot.intelligence_score
        ))
        self.conn.commit()
        
        return snapshot
    
    def get_evolution_timeline(self, days: int = 30) -> List[EvolutionSnapshot]:
        """Get evolution timeline for last N days"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM evolution_snapshots
            WHERE timestamp > datetime('now', '-{} days')
            ORDER BY timestamp ASC
        """.format(days))
        
        snapshots = []
        for row in cursor.fetchall():
            snapshots.append(EvolutionSnapshot(
                timestamp=row[1],
                total_tool_calls=row[2],
                success_rate=row[3],
                learned_patterns=row[4],
                avg_execution_time=row[5],
                memory_size_mb=row[6],
                intelligence_score=row[7]
            ))
        
        return snapshots
    
    def get_tool_analytics(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get analytics for tool usage"""
        cursor = self.conn.cursor()
        
        if tool_name:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_calls,
                    AVG(CAST(success AS FLOAT)) as success_rate,
                    AVG(execution_time_ms) as avg_time,
                    SUM(input_tokens) as total_input_tokens,
                    SUM(output_tokens) as total_output_tokens
                FROM tool_executions
                WHERE tool_name = ?
            """, (tool_name,))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_calls,
                    AVG(CAST(success AS FLOAT)) as success_rate,
                    AVG(execution_time_ms) as avg_time,
                    SUM(input_tokens) as total_input_tokens,
                    SUM(output_tokens) as total_output_tokens
                FROM tool_executions
            """)
        
        row = cursor.fetchone()
        return {
            "tool_name": tool_name or "all",
            "total_calls": row[0],
            "success_rate": row[1] or 0.0,
            "avg_execution_time_ms": row[2] or 0.0,
            "total_input_tokens": row[3] or 0,
            "total_output_tokens": row[4] or 0
        }
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """Get overall learning progress"""
        timeline = self.get_evolution_timeline(30)
        
        if len(timeline) < 2:
            return {
                "status": "insufficient_data",
                "snapshots": len(timeline)
            }
        
        first = timeline[0]
        latest = timeline[-1]
        
        return {
            "status": "learning",
            "snapshots": len(timeline),
            "intelligence_growth": {
                "initial": first.intelligence_score,
                "current": latest.intelligence_score,
                "improvement": latest.intelligence_score - first.intelligence_score,
                "growth_rate": ((latest.intelligence_score - first.intelligence_score) / 
                               first.intelligence_score * 100) if first.intelligence_score > 0 else 0
            },
            "success_rate_improvement": latest.success_rate - first.success_rate,
            "patterns_learned": latest.learned_patterns,
            "execution_speed_improvement": first.avg_execution_time - latest.avg_execution_time
        }
    
    def _count_learned_patterns(self) -> int:
        """Count learned patterns from memory"""
        memory_dir = Path("~/.memory").expanduser()
        if not memory_dir.exists():
            return 0
        
        return len(list(memory_dir.glob("pattern_*.json")))
    
    def _get_memory_size_mb(self) -> float:
        """Get memory directory size in MB"""
        memory_dir = Path("~/.memory").expanduser()
        if not memory_dir.exists():
            return 0.0
        
        total_size = sum(f.stat().st_size for f in memory_dir.rglob('*') if f.is_file())
        return total_size / (1024 * 1024)  # Convert to MB
    
    def _calculate_intelligence_score(self, 
                                     success_rate: float,
                                     patterns_learned: int,
                                     avg_time: float) -> float:
        """Calculate intelligence score (0-100)
        
        Factors:
        - Success rate (40 points)
        - Patterns learned (30 points)
        - Execution speed (30 points)
        """
        score = 0.0
        
        # Success rate component (0-40)
        score += success_rate * 40
        
        # Patterns learned component (0-30)
        # Scale: 0 patterns = 0, 10+ patterns = 30
        score += min(patterns_learned * 3, 30)
        
        # Speed component (0-30)
        # Faster is better, scale based on reasonable execution times
        if avg_time > 0:
            # Assume 1000ms is baseline, lower is better
            speed_score = max(0, 30 - (avg_time / 1000) * 10)
            score += min(speed_score, 30)
        
        return min(score, 100.0)
    
    def generate_report(self) -> str:
        """Generate evolution report"""
        snapshot = self.create_evolution_snapshot()
        progress = self.get_learning_progress()
        
        report = []
        report.append("="*60)
        report.append("PERPLEXITY ENHANCEMENT MCP EVOLUTION REPORT")
        report.append("="*60)
        report.append("")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("CURRENT STATE:")
        report.append(f"  Intelligence Score: {snapshot.intelligence_score:.1f}/100")
        report.append(f"  Success Rate: {snapshot.success_rate*100:.1f}%")
        report.append(f"  Learned Patterns: {snapshot.learned_patterns}")
        report.append(f"  Total Tool Calls: {snapshot.total_tool_calls}")
        report.append(f"  Avg Execution Time: {snapshot.avg_execution_time:.0f}ms")
        report.append(f"  Memory Size: {snapshot.memory_size_mb:.2f}MB")
        report.append("")
        
        if progress.get("status") == "learning":
            report.append("LEARNING PROGRESS (30 days):")
            growth = progress["intelligence_growth"]
            report.append(f"  Intelligence Growth: {growth['improvement']:.1f} points ({growth['growth_rate']:.1f}%)")
            report.append(f"  Success Rate Improvement: {progress['success_rate_improvement']*100:.1f}%")
            report.append(f"  Execution Speed Improvement: {progress['execution_speed_improvement']:.0f}ms faster")
            report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)

if __name__ == "__main__":
    tracker = MCPEnhancementTracker()
    print(tracker.generate_report())
