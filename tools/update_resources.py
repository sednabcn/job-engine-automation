#!/usr/bin/env python3
"""
update_resources.py - Update learning resources database

This tool manages the learning resources database, including:
- Adding new resources
- Updating existing resources
- Validating resource links
- Categorizing resources by skill
- Checking for broken links
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urlparse


class ResourceManager:
    """Manage learning resources database."""
    
    def __init__(self, resources_file: Path):
        """
        Initialize the resource manager.
        
        Args:
            resources_file: Path to resources JSON file
        """
        self.resources_file = Path(resources_file)
        self.resources = self._load_resources()
    
    def _load_resources(self) -> Dict[str, Any]:
        """Load resources from JSON file."""
        if self.resources_file.exists():
            with open(self.resources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "last_updated": datetime.now().isoformat(),
                "categories": {},
                "resources": []
            }
    
    def _save_resources(self):
        """Save resources to JSON file."""
        self.resources["last_updated"] = datetime.now().isoformat()
        
        self.resources_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.resources_file, 'w', encoding='utf-8') as f:
            json.dump(self.resources, f, indent=2)
        
        print(f"✅ Resources saved to: {self.resources_file}")
    
    def add_resource(
        self,
        skill: str,
        title: str,
        url: str,
        resource_type: str,
        difficulty: str,
        duration_hours: Optional[int] = None,
        cost: str = "free",
        description: Optional[str] = None
    ):
        """
        Add a new learning resource.
        
        Args:
            skill: Skill category (e.g., 'GraphQL', 'Kubernetes')
            title: Resource title
            url: Resource URL
            resource_type: Type (tutorial, course, documentation, video, book)
            difficulty: Difficulty level (beginner, intermediate, advanced)
            duration_hours: Estimated hours to complete
            cost: Cost (free, paid, subscription)
            description: Resource description
        """
        resource = {
            "id": f"resource_{len(self.resources['resources']) + 1}",
            "skill": skill,
            "title": title,
            "url": url,
            "type": resource_type,
            "difficulty": difficulty,
            "duration_hours": duration_hours,
            "cost": cost,
            "description": description,
            "added_date": datetime.now().isoformat(),
            "verified": False,
            "rating": None
        }
        
        self.resources["resources"].append(resource)
        
        # Update categories
        if skill not in self.resources["categories"]:
            self.resources["categories"][skill] = {
                "total_resources": 0,
                "last_updated": datetime.now().isoformat()
            }
        
        self.resources["categories"][skill]["total_resources"] += 1
        self.resources["categories"][skill]["last_updated"] = datetime.now().isoformat()
        
        print(f"✅ Added resource: {title} ({skill})")
        return resource
    
    def update_resource(self, resource_id: str, **kwargs):
        """Update an existing resource."""
        for resource in self.resources["resources"]:
            if resource["id"] == resource_id:
                resource.update(kwargs)
                resource["last_modified"] = datetime.now().isoformat()
                print(f"✅ Updated resource: {resource_id}")
                return resource
        
        print(f"⚠️  Resource not found: {resource_id}")
        return None
    
    def remove_resource(self, resource_id: str):
        """Remove a resource."""
        initial_count = len(self.resources["resources"])
        self.resources["resources"] = [
            r for r in self.resources["resources"] if r["id"] != resource_id
        ]
        
        if len(self.resources["resources"]) < initial_count:
            print(f"✅ Removed resource: {resource_id}")
            return True
        else:
            print(f"⚠️  Resource not found: {resource_id}")
            return False
    
    def validate_links(self, timeout: int = 5):
        """Validate all resource URLs."""
        print("🔍 Validating resource links...")
        
        broken_links = []
        valid_links = []
        
        for resource in self.resources["resources"]:
            url = resource["url"]
            resource_id = resource["id"]
            
            try:
                response = requests.head(url, timeout=timeout, allow_redirects=True)
                if response.status_code < 400:
                    valid_links.append(resource_id)
                    resource["verified"] = True
                    resource["last_verified"] = datetime.now().isoformat()
                    print(f"  ✓ {resource['title']}: OK")
                else:
                    broken_links.append({
                        "id": resource_id,
                        "title": resource["title"],
                        "url": url,
                        "status_code": response.status_code
                    })
                    resource["verified"] = False
                    print(f"  ✗ {resource['title']}: {response.status_code}")
            
            except requests.RequestException as e:
                broken_links.append({
                    "id": resource_id,
                    "title": resource["title"],
                    "url": url,
                    "error": str(e)
                })
                resource["verified"] = False
                print(f"  ✗ {resource['title']}: {str(e)}")
        
        print(f"\n✅ Valid links: {len(valid_links)}")
        print(f"❌ Broken links: {len(broken_links)}")
        
        if broken_links:
            print("\nBroken Links:")
            for link in broken_links:
                print(f"  - {link['title']}: {link['url']}")
        
        return {"valid": valid_links, "broken": broken_links}
    
    def get_resources_by_skill(self, skill: str) -> List[Dict[str, Any]]:
        """Get all resources for a specific skill."""
        return [
            r for r in self.resources["resources"]
            if r["skill"].lower() == skill.lower()
        ]
    
    def get_resources_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get all resources of a specific difficulty level."""
        return [
            r for r in self.resources["resources"]
            if r["difficulty"].lower() == difficulty.lower()
        ]
    
    def generate_report(self) -> str:
        """Generate a summary report of resources."""
        report = []
        report.append("=" * 60)
        report.append("LEARNING RESOURCES REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Resources: {len(self.resources['resources'])}")
        report.append(f"Last Updated: {self.resources['last_updated']}")
        report.append("")
        
        report.append("RESOURCES BY SKILL:")
        report.append("-" * 60)
        for skill, info in sorted(self.resources["categories"].items()):
            report.append(f"  {skill}: {info['total_resources']} resources")
        report.append("")
        
        report.append("RESOURCES BY TYPE:")
        report.append("-" * 60)
        type_counts = {}
        for resource in self.resources["resources"]:
            res_type = resource["type"]
            type_counts[res_type] = type_counts.get(res_type, 0) + 1
        
        for res_type, count in sorted(type_counts.items()):
            report.append(f"  {res_type}: {count}")
        report.append("")
        
        report.append("RESOURCES BY DIFFICULTY:")
        report.append("-" * 60)
        diff_counts = {}
        for resource in self.resources["resources"]:
            difficulty = resource["difficulty"]
            diff_counts[difficulty] = diff_counts.get(difficulty, 0) + 1
        
        for difficulty, count in sorted(diff_counts.items()):
            report.append(f"  {difficulty}: {count}")
        report.append("")
        
        verified_count = sum(1 for r in self.resources["resources"] if r.get("verified", False))
        report.append(f"Verified Links: {verified_count}/{len(self.resources['resources'])}")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_markdown(self, output_file: Path):
        """Export resources as a markdown file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Learning Resources\n\n")
            f.write(f"*Last updated: {self.resources['last_updated']}*\n\n")
            
            for skill in sorted(self.resources["categories"].keys()):
                f.write(f"## {skill}\n\n")
                
                skill_resources = self.get_resources_by_skill(skill)
                
                for resource in sorted(skill_resources, key=lambda x: x["difficulty"]):
                    f.write(f"### {resource['title']}\n\n")
                    f.write(f"- **Type:** {resource['type']}\n")
                    f.write(f"- **Difficulty:** {resource['difficulty']}\n")
                    f.write(f"- **Cost:** {resource['cost']}\n")
                    
                    if resource.get('duration_hours'):
                        f.write(f"- **Duration:** ~{resource['duration_hours']} hours\n")
                    
                    f.write(f"- **URL:** [{resource['url']}]({resource['url']})\n")
                    
                    if resource.get('description'):
                        f.write(f"\n{resource['description']}\n")
                    
                    f.write("\n")
        
        print(f"✅ Resources exported to: {output_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage learning resources database"
    )
    
    parser.add_argument(
        '--resources-file',
        type=str,
        default='data/learning_resources.json',
        help='Path to resources JSON file'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add resource command
    add_parser = subparsers.add_parser('add', help='Add a new resource')
    add_parser.add_argument('--skill', required=True, help='Skill category')
    add_parser.add_argument('--title', required=True, help='Resource title')
    add_parser.add_argument('--url', required=True, help='Resource URL')
    add_parser.add_argument('--type', required=True, 
                           choices=['tutorial', 'course', 'documentation', 'video', 'book'],
                           help='Resource type')
    add_parser.add_argument('--difficulty', required=True,
                           choices=['beginner', 'intermediate', 'advanced'],
                           help='Difficulty level')
    add_parser.add_argument('--duration', type=int, help='Duration in hours')
    add_parser.add_argument('--cost', default='free',
                           choices=['free', 'paid', 'subscription'],
                           help='Cost type')
    add_parser.add_argument('--description', help='Resource description')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate all resource links')
    validate_parser.add_argument('--timeout', type=int, default=5,
                                help='Request timeout in seconds')
    
    # Report command
    subparsers.add_parser('report', help='Generate resources report')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export resources to markdown')
    export_parser.add_argument('--output', type=str, default='resources.md',
                              help='Output markdown file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        manager = ResourceManager(Path(args.resources_file))
        
        if args.command == 'add':
            manager.add_resource(
                skill=args.skill,
                title=args.title,
                url=args.url,
                resource_type=args.type,
                difficulty=args.difficulty,
                duration_hours=args.duration,
                cost=args.cost,
                description=args.description
            )
            manager._save_resources()
        
        elif args.command == 'validate':
            manager.validate_links(timeout=args.timeout)
            manager._save_resources()
        
        elif args.command == 'report':
            report = manager.generate_report()
            print("\n" + report)
        
        elif args.command == 'export':
            output_file = Path(args.output)
            manager.export_markdown(output_file)
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
