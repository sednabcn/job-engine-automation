#!/usr/bin/env python3
"""
Custom Resources - Learning Resource Management
Allows users to add, manage, and customize learning resources for skill development
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class LearningResource:
    """Represents a learning resource"""
    id: str
    title: str
    url: str
    type: str  # course, book, article, video, tutorial, project
    platform: str  # Udemy, Coursera, YouTube, etc.
    skill: str  # Target skill
    level: str  # beginner, intermediate, advanced, expert
    duration_hours: float
    cost: float  # 0 for free
    rating: float  # 0-5
    description: str
    prerequisites: List[str]
    tags: List[str]
    added_date: str
    last_updated: str
    custom: bool = True  # True if user-added
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningResource':
        """Create from dictionary"""
        return cls(**data)


class CustomResourceManager:
    """Manage custom learning resources"""
    
    def __init__(self, resources_path: str = "job_search_data/custom_resources.json"):
        self.resources_path = Path(resources_path)
        self.resources_path.parent.mkdir(parents=True, exist_ok=True)
        self.resources = self._load_resources()
    
    def add_resource(
        self,
        title: str,
        url: str,
        resource_type: str,
        skill: str,
        level: str,
        duration_hours: float,
        platform: str = "Custom",
        cost: float = 0.0,
        rating: float = 0.0,
        description: str = "",
        prerequisites: List[str] = None,
        tags: List[str] = None
    ) -> LearningResource:
        """
        Add a new custom learning resource
        
        Example:
            manager.add_resource(
                title="Advanced Kubernetes Patterns",
                url="https://example.com/k8s-course",
                resource_type="course",
                skill="Kubernetes",
                level="advanced",
                duration_hours=20,
                platform="Udemy",
                cost=49.99,
                rating=4.7,
                description="Master GraphQL schema design and optimization",
        prerequisites=["Basic GraphQL", "JavaScript"],
        tags=["graphql", "apollo", "api"]
    )
    
    manager.add_resource(
        title="Istio Service Mesh Deep Dive",
        url="https://acloudguru.com/course/istio-service-mesh",
        resource_type="course",
        skill="Service Mesh",
        level="intermediate",
        duration_hours=6,
        platform="A Cloud Guru",
        cost=29.0,
        rating=4.6,
        description="Complete guide to Istio deployment and management",
        prerequisites=["Kubernetes", "Microservices"],
        tags=["istio", "service-mesh", "kubernetes"]
    )
    
    manager.add_resource(
        title="gRPC Microservices in Go",
        url="https://www.udemy.com/course/grpc-golang/",
        resource_type="course",
        skill="gRPC",
        level="intermediate",
        duration_hours=8,
        platform="Udemy",
        cost=19.99,
        rating=4.7,
        description="Build efficient gRPC services in Go",
        prerequisites=["Go", "REST APIs"],
        tags=["grpc", "go", "microservices"]
    )
    
    # Search resources
    print("\n2️⃣  Searching Resources...")
    
    go_resources = manager.search_resources(skill="Go", min_rating=4.5)
    print(f"Found {len(go_resources)} high-rated Go resources:")
    for r in go_resources:
        print(f"  • {r.title} ({r.rating}⭐) - ${r.cost}")
    
    # Get learning path
    print("\n3️⃣  Getting Learning Path...")
    
    go_path = manager.get_learning_path("Go")
    print("Go Learning Path:")
    for level, resources in go_path.items():
        if resources:
            print(f"\n  {level.upper()}:")
            for r in resources:
                print(f"    • {r.title} ({r.duration_hours}h)")
    
    # Get recommendations
    print("\n4️⃣  Getting Recommendations...")
    
    recommendations = manager.recommend_resources(
        skill="Go",
        current_level="beginner",
        budget=50,
        max_hours=20
    )
    print(f"Top recommendations for Go (beginner → intermediate):")
    for i, r in enumerate(recommendations, 1):
        print(f"  {i}. {r.title}")
        print(f"     Platform: {r.platform} | Duration: {r.duration_hours}h | Cost: ${r.cost}")
        print(f"     Rating: {r.rating}⭐ | Level: {r.level}")
    
    # Statistics
    print("\n5️⃣  Resource Statistics...")
    
    stats = manager.get_statistics()
    print(f"Total Resources: {stats['total']}")
    print(f"Total Learning Hours: {stats['total_hours']:.1f}h")
    print(f"Total Cost: ${stats['total_cost']:.2f}")
    print(f"Free Resources: {stats['free_resources']}")
    print(f"Average Rating: {stats['average_rating']:.2f}⭐")
    print(f"Custom Resources: {stats['custom_count']}")
    
    print("\nResources by Skill:")
    for skill, count in stats['by_skill'].items():
        print(f"  • {skill}: {count}")
    
    print("\nResources by Type:")
    for rtype, count in stats['by_type'].items():
        print(f"  • {rtype}: {count}")
    
    # Export
    print("\n6️⃣  Exporting Resources...")
    manager.export_resources()
    
    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)


if __name__ == '__main__':
    demo_usage()
Deep dive into K8s operators and CRDs",
                prerequisites=["Basic Kubernetes", "Docker"],
                tags=["kubernetes", "cloud-native", "operators"]
            )
        """
        resource = LearningResource(
            id=str(uuid.uuid4()),
            title=title,
            url=url,
            type=resource_type,
            platform=platform,
            skill=skill,
            level=level,
            duration_hours=duration_hours,
            cost=cost,
            rating=rating,
            description=description,
            prerequisites=prerequisites or [],
            tags=tags or [],
            added_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            custom=True
        )
        
        self.resources.append(resource)
        self._save_resources()
        
        print(f"✅ Added resource: {title}")
        return resource
    
    def update_resource(self, resource_id: str, **updates) -> Optional[LearningResource]:
        """Update an existing resource"""
        for resource in self.resources:
            if resource.id == resource_id:
                for key, value in updates.items():
                    if hasattr(resource, key):
                        setattr(resource, key, value)
                resource.last_updated = datetime.now().isoformat()
                self._save_resources()
                print(f"✅ Updated resource: {resource.title}")
                return resource
        
        print(f"❌ Resource not found: {resource_id}")
        return None
    
    def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource"""
        initial_count = len(self.resources)
        self.resources = [r for r in self.resources if r.id != resource_id]
        
        if len(self.resources) < initial_count:
            self._save_resources()
            print(f"✅ Deleted resource: {resource_id}")
            return True
        
        print(f"❌ Resource not found: {resource_id}")
        return False
    
    def search_resources(
        self,
        skill: str = None,
        level: str = None,
        resource_type: str = None,
        max_cost: float = None,
        min_rating: float = None,
        platform: str = None,
        tags: List[str] = None
    ) -> List[LearningResource]:
        """
        Search resources with filters
        
        Example:
            # Find free advanced Go courses with rating 4+
            results = manager.search_resources(
                skill="Go",
                level="advanced",
                resource_type="course",
                max_cost=0,
                min_rating=4.0
            )
        """
        results = self.resources.copy()
        
        if skill:
            results = [r for r in results if r.skill.lower() == skill.lower()]
        
        if level:
            results = [r for r in results if r.level.lower() == level.lower()]
        
        if resource_type:
            results = [r for r in results if r.type.lower() == resource_type.lower()]
        
        if max_cost is not None:
            results = [r for r in results if r.cost <= max_cost]
        
        if min_rating is not None:
            results = [r for r in results if r.rating >= min_rating]
        
        if platform:
            results = [r for r in results if r.platform.lower() == platform.lower()]
        
        if tags:
            results = [r for r in results if any(tag.lower() in [t.lower() for t in r.tags] for tag in tags)]
        
        return results
    
    def get_resources_for_skill(self, skill: str, level: str = None) -> List[LearningResource]:
        """Get all resources for a specific skill"""
        return self.search_resources(skill=skill, level=level)
    
    def get_learning_path(self, skill: str) -> Dict[str, List[LearningResource]]:
        """
        Get a complete learning path for a skill (beginner -> expert)
        
        Returns resources organized by level
        """
        all_resources = self.get_resources_for_skill(skill)
        
        path = {
            'beginner': [r for r in all_resources if r.level == 'beginner'],
            'intermediate': [r for r in all_resources if r.level == 'intermediate'],
            'advanced': [r for r in all_resources if r.level == 'advanced'],
            'expert': [r for r in all_resources if r.level == 'expert']
        }
        
        # Sort by rating within each level
        for level in path:
            path[level].sort(key=lambda x: x.rating, reverse=True)
        
        return path
    
    def calculate_learning_time(self, resources: List[LearningResource]) -> float:
        """Calculate total hours needed for a set of resources"""
        return sum(r.duration_hours for r in resources)
    
    def calculate_total_cost(self, resources: List[LearningResource]) -> float:
        """Calculate total cost for a set of resources"""
        return sum(r.cost for r in resources)
    
    def export_resources(self, output_path: str = None):
        """Export resources to JSON"""
        output_path = output_path or "job_search_data/resources_export.json"
        
        data = {
            'exported_at': datetime.now().isoformat(),
            'total_resources': len(self.resources),
            'resources': [r.to_dict() for r in self.resources]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Exported {len(self.resources)} resources to {output_path}")
    
    def import_resources(self, input_path: str) -> int:
        """Import resources from JSON"""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        imported = 0
        for resource_data in data.get('resources', []):
            try:
                resource = LearningResource.from_dict(resource_data)
                # Check for duplicates by URL
                if not any(r.url == resource.url for r in self.resources):
                    self.resources.append(resource)
                    imported += 1
            except Exception as e:
                print(f"⚠️  Error importing resource: {e}")
        
        self._save_resources()
        print(f"✅ Imported {imported} new resources")
        return imported
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the resource collection"""
        if not self.resources:
            return {'total': 0}
        
        stats = {
            'total': len(self.resources),
            'by_skill': {},
            'by_level': {},
            'by_type': {},
            'by_platform': {},
            'total_hours': sum(r.duration_hours for r in self.resources),
            'total_cost': sum(r.cost for r in self.resources),
            'free_resources': len([r for r in self.resources if r.cost == 0]),
            'average_rating': sum(r.rating for r in self.resources) / len(self.resources),
            'custom_count': len([r for r in self.resources if r.custom])
        }
        
        # Count by categories
        for resource in self.resources:
            stats['by_skill'][resource.skill] = stats['by_skill'].get(resource.skill, 0) + 1
            stats['by_level'][resource.level] = stats['by_level'].get(resource.level, 0) + 1
            stats['by_type'][resource.type] = stats['by_type'].get(resource.type, 0) + 1
            stats['by_platform'][resource.platform] = stats['by_platform'].get(resource.platform, 0) + 1
        
        return stats
    
    def recommend_resources(
        self,
        skill: str,
        current_level: str,
        budget: float = None,
        max_hours: float = None
    ) -> List[LearningResource]:
        """
        Recommend best resources based on criteria
        
        Example:
            # Get best Go resources for someone at intermediate level
            # Budget $100, max 40 hours
            recommendations = manager.recommend_resources(
                skill="Go",
                current_level="intermediate",
                budget=100,
                max_hours=40
            )
        """
        # Get resources for next level
        level_progression = {
            'beginner': 'intermediate',
            'intermediate': 'advanced',
            'advanced': 'expert',
            'expert': 'expert'
        }
        
        target_level = level_progression.get(current_level, 'intermediate')
        candidates = self.search_resources(skill=skill, level=target_level)
        
        # Apply filters
        if budget is not None:
            candidates = [r for r in candidates if r.cost <= budget]
        
        if max_hours is not None:
            candidates = [r for r in candidates if r.duration_hours <= max_hours]
        
        # Sort by rating
        candidates.sort(key=lambda x: x.rating, reverse=True)
        
        return candidates[:5]  # Top 5 recommendations
    
    def _load_resources(self) -> List[LearningResource]:
        """Load resources from file"""
        if not self.resources_path.exists():
            return self._get_default_resources()
        
        try:
            with open(self.resources_path, 'r') as f:
                data = json.load(f)
                return [LearningResource.from_dict(r) for r in data]
        except Exception as e:
            print(f"⚠️  Error loading resources: {e}")
            return self._get_default_resources()
    
    def _save_resources(self):
        """Save resources to file"""
        data = [r.to_dict() for r in self.resources]
        with open(self.resources_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_default_resources(self) -> List[LearningResource]:
        """Get default resource catalog"""
        defaults = [
            {
                'title': 'Go: The Complete Developer\'s Guide',
                'url': 'https://www.udemy.com/course/go-the-complete-developers-guide/',
                'type': 'course',
                'platform': 'Udemy',
                'skill': 'Go',
                'level': 'beginner',
                'duration_hours': 12,
                'cost': 19.99,
                'rating': 4.6,
                'description': 'Master Go fundamentals',
                'prerequisites': ['Basic programming'],
                'tags': ['go', 'golang', 'programming']
            },
            {
                'title': 'Concurrency in Go',
                'url': 'https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/',
                'type': 'book',
                'platform': "O'Reilly",
                'skill': 'Go',
                'level': 'intermediate',
                'duration_hours': 15,
                'cost': 39.99,
                'rating': 4.7,
                'description': 'Deep dive into goroutines and channels',
                'prerequisites': ['Basic Go'],
                'tags': ['go', 'concurrency', 'goroutines']
            },
            {
                'title': 'Kubernetes for Developers',
                'url': 'https://www.udemy.com/course/kubernetes-for-developers/',
                'type': 'course',
                'platform': 'Udemy',
                'skill': 'Kubernetes',
                'level': 'intermediate',
                'duration_hours': 8,
                'cost': 29.99,
                'rating': 4.5,
                'description': 'Deploy and manage applications on K8s',
                'prerequisites': ['Docker', 'Basic Linux'],
                'tags': ['kubernetes', 'k8s', 'devops']
            }
        ]
        
        return [
            LearningResource(
                id=str(uuid.uuid4()),
                added_date=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat(),
                custom=False,
                **resource
            )
            for resource in defaults
        ]


def demo_usage():
    """Demonstrate resource management features"""
    print("=" * 60)
    print("Custom Resources Manager - Demo")
    print("=" * 60)
    
    manager = CustomResourceManager()
    
    # Add custom resources
    print("\n1️⃣  Adding Custom Resources...")
    
    manager.add_resource(
        title="Advanced GraphQL with Apollo",
        url="https://frontendmasters.com/courses/advanced-graphql-v2/",
        resource_type="course",
        skill="GraphQL",
        level="advanced",
        duration_hours=4,
        platform="Frontend Masters",
        cost=39.0,
        rating=4.8,
        description="
