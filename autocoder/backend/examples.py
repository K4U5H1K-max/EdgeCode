"""
Example usage of AutoCoder API
"""

import asyncio
import aiohttp
import json


async def example_generate_project():
    """Example: Generate a project"""
    
    async with aiohttp.ClientSession() as session:
        # Generate project
        prompt = "Create a jewelry website with product catalog and shopping cart"
        
        print(f"Generating project from prompt: {prompt}\n")
        
        async with session.post(
            "http://localhost:8000/api/generate",
            json={"prompt": prompt}
        ) as resp:
            result = await resp.json()
            
            if result["success"]:
                print(f"✓ Project generated successfully!")
                print(f"  Project ID: {result['project_id']}")
                print(f"  Project Dir: {result['project_dir']}")
                print(f"  Project Type: {result['project_spec']['project_type']}")
                print(f"  Features: {', '.join(result['project_spec']['features'])}\n")
                
                return result
            else:
                print(f"✗ Generation failed: {result['error']}")
                return None


async def example_monitor_generation():
    """Example: Monitor generation progress"""
    
    async with aiohttp.ClientSession() as session:
        print("Monitoring generation progress...\n")
        
        for i in range(30):  # Monitor for 30 seconds
            async with session.get("http://localhost:8000/api/status") as resp:
                status_data = await resp.json()
                
                print(f"Status: {status_data['status']}")
                print(f"  Errors: {status_data['error_count']}")
                
                # Show agent statuses
                for agent, agent_status in status_data['agents_status'].items():
                    print(f"  - {agent}: {agent_status['status']}")
                
                if status_data['status'] == 'completed':
                    print("\n✓ Generation completed!")
                    break
                
                await asyncio.sleep(1)


async def example_view_logs():
    """Example: View execution logs"""
    
    async with aiohttp.ClientSession() as session:
        print("Fetching execution logs...\n")
        
        async with session.get("http://localhost:8000/api/logs?limit=20") as resp:
            logs_data = await resp.json()
            
            print(f"Total logs: {logs_data['total']}")
            print(f"Showing last {len(logs_data['logs'])} logs:\n")
            
            for log in logs_data['logs']:
                print(f"[{log['timestamp']}] [{log['agent']}] {log['message']}")


async def example_view_memory():
    """Example: View shared memory"""
    
    async with aiohttp.ClientSession() as session:
        print("Fetching shared memory...\n")
        
        async with session.get("http://localhost:8000/api/memory") as resp:
            memory = await resp.json()
            
            if memory['project_id']:
                print(f"Project ID: {memory['project_id']}")
                print(f"Status: {memory['status']}")
                print(f"Project Type: {memory['project_spec'].get('project_type', 'N/A')}")
                print(f"Errors: {len(memory['errors'])}")
                
                # Show first few artifacts
                total_artifacts = (
                    len(memory['generated_artifacts']['frontend']) +
                    len(memory['generated_artifacts']['backend']) +
                    len(memory['generated_artifacts']['database']) +
                    len(memory['generated_artifacts']['config'])
                )
                print(f"Generated Artifacts: {total_artifacts}")


async def main():
    """Run examples"""
    
    print("=" * 50)
    print("AutoCoder API Examples")
    print("=" * 50)
    print()
    
    # Check health
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as resp:
                if resp.status == 200:
                    print("✓ Backend is running\n")
                else:
                    print("✗ Backend is not responding\n")
                    return
    except Exception as e:
        print(f"✗ Cannot connect to backend: {e}\n")
        return
    
    # Run examples
    print("1. GENERATE PROJECT")
    print("-" * 50)
    result = await example_generate_project()
    
    if result:
        print("\n2. MONITOR GENERATION")
        print("-" * 50)
        await example_monitor_generation()
        
        print("\n3. VIEW EXECUTION LOGS")
        print("-" * 50)
        await example_view_logs()
        
        print("\n4. VIEW SHARED MEMORY")
        print("-" * 50)
        await example_view_memory()


if __name__ == "__main__":
    asyncio.run(main())
