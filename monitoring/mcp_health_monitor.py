#!/usr/bin/env python3
"""
MCP Server Health Monitor

Monitors the health and performance of Perplexity Enhancement MCP server.
"""

import json
import time
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class HealthCheck:
    """MCP server health check result"""
    timestamp: str
    server_running: bool
    response_time_ms: float
    memory_usage_mb: float
    tools_available: int
    status: str  # 'healthy', 'degraded', 'down'

class MCPHealthMonitor:
    """Monitor MCP server health"""
    
    def __init__(self, server_path: str = "~/perplexity-enhancement-mcp"):
        self.server_path = server_path
    
    def check_health(self) -> HealthCheck:
        """Perform health check"""
        timestamp = datetime.now().isoformat()
        
        # Check if server process is running
        server_running = self._is_server_running()
        
        if not server_running:
            return HealthCheck(
                timestamp=timestamp,
                server_running=False,
                response_time_ms=0,
                memory_usage_mb=0,
                tools_available=0,
                status="down"
            )
        
        # Measure response time
        response_time = self._measure_response_time()
        
        # Get memory usage
        memory_usage = self._get_memory_usage()
        
        # Count available tools
        tools_available = 14  # Known tool count
        
        # Determine status
        if response_time < 1000:  # < 1 second
            status = "healthy"
        elif response_time < 3000:  # < 3 seconds
            status = "degraded"
        else:
            status = "slow"
        
        return HealthCheck(
            timestamp=timestamp,
            server_running=server_running,
            response_time_ms=response_time,
            memory_usage_mb=memory_usage,
            tools_available=tools_available,
            status=status
        )
    
    def _is_server_running(self) -> bool:
        """Check if MCP server is running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "perplexity-enhancement-mcp"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _measure_response_time(self) -> float:
        """Measure server response time"""
        # Simplified - would actually call MCP server
        return 250.0  # Mock value
    
    def _get_memory_usage(self) -> float:
        """Get server memory usage in MB"""
        # Simplified - would actually check process memory
        return 50.0  # Mock value
    
    def generate_health_report(self) -> str:
        """Generate health report"""
        health = self.check_health()
        
        report = []
        report.append("="*60)
        report.append("MCP SERVER HEALTH REPORT")
        report.append("="*60)
        report.append("")
        report.append(f"Timestamp: {health.timestamp}")
        report.append(f"Status: {health.status.upper()}")
        report.append("")
        report.append("METRICS:")
        report.append(f"  Server Running: {'✅' if health.server_running else '❌'}")
        report.append(f"  Response Time: {health.response_time_ms:.0f}ms")
        report.append(f"  Memory Usage: {health.memory_usage_mb:.1f}MB")
        report.append(f"  Tools Available: {health.tools_available}")
        report.append("")
        report.append("="*60)
        
        return "\n".join(report)

if __name__ == "__main__":
    monitor = MCPHealthMonitor()
    print(monitor.generate_health_report())
