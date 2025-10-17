"""
Template Engine Module
A flexible template engine supporting variables, conditionals, loops, and filters.
"""

import re
from typing import Any, Dict, List, Callable, Optional
from datetime import datetime


class TemplateEngine:
    """
    A template engine for rendering templates with dynamic content.
    Supports variables, conditionals, loops, and custom filters.
    """
    
    def __init__(self):
        """Initialize the template engine with default filters."""
        self.filters = {
            'upper': lambda x: str(x).upper(),
            'lower': lambda x: str(x).lower(),
            'title': lambda x: str(x).title(),
            'capitalize': lambda x: str(x).capitalize(),
            'length': lambda x: len(x),
            'reverse': lambda x: str(x)[::-1] if isinstance(x, str) else list(reversed(x)),
            'default': lambda x, d: x if x else d,
            'date': lambda x, fmt='%Y-%m-%d': x.strftime(fmt) if isinstance(x, datetime) else str(x),
            'join': lambda x, sep=', ': sep.join(str(i) for i in x) if isinstance(x, (list, tuple)) else str(x),
            'round': lambda x, decimals=2: round(float(x), decimals),
            'abs': lambda x: abs(float(x)),
            'int': lambda x: int(x),
            'float': lambda x: float(x),
            'str': lambda x: str(x),
            'trim': lambda x: str(x).strip(),
            'truncate': lambda x, length=50: str(x)[:length] + '...' if len(str(x)) > length else str(x),
        }
        self.templates = {}
    
    def register_filter(self, name: str, func: Callable) -> None:
        """
        Register a custom filter function.
        
        Args:
            name: Name of the filter
            func: Function to apply (should accept value as first argument)
        """
        self.filters[name] = func
    
    def register_template(self, name: str, template: str) -> None:
        """
        Register a named template for reuse.
        
        Args:
            name: Template name
            template: Template string
        """
        self.templates[name] = template
    
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context.
        
        Args:
            template: Template string
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered template string
        """
        # Process includes first
        template = self._process_includes(template)
        
        # Process for loops
        template = self._process_loops(template, context)
        
        # Process conditionals
        template = self._process_conditionals(template, context)
        
        # Process variables and filters
        template = self._process_variables(template, context)
        
        return template
    
    def render_template(self, name: str, context: Dict[str, Any]) -> str:
        """
        Render a registered template by name.
        
        Args:
            name: Name of the registered template
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered template string
        """
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found")
        
        return self.render(self.templates[name], context)
    
    def _process_includes(self, template: str) -> str:
        """Process template includes: {% include template_name %}"""
        include_pattern = r'\{%\s*include\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*%\}'
        
        def replace_include(match):
            template_name = match.group(1)
            if template_name in self.templates:
                return self.templates[template_name]
            return f"[Template '{template_name}' not found]"
        
        return re.sub(include_pattern, replace_include, template)
    
    def _process_loops(self, template: str, context: Dict[str, Any]) -> str:
        """Process for loops: {% for item in items %}...{% endfor %}"""
        loop_pattern = r'\{%\s*for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        
        def replace_loop(match):
            var_name = match.group(1)
            collection_name = match.group(2)
            loop_body = match.group(3)
            
            # Get the collection from context
            collection = self._get_nested_value(context, collection_name)
            
            if not collection:
                return ''
            
            if not isinstance(collection, (list, tuple)):
                collection = [collection]
            
            results = []
            for idx, item in enumerate(collection):
                loop_context = context.copy()
                loop_context[var_name] = item
                loop_context['loop'] = {
                    'index': idx,
                    'index1': idx + 1,
                    'first': idx == 0,
                    'last': idx == len(collection) - 1,
                    'length': len(collection)
                }
                
                # Recursively process the loop body
                rendered = self._process_loops(loop_body, loop_context)
                rendered = self._process_conditionals(rendered, loop_context)
                rendered = self._process_variables(rendered, loop_context)
                results.append(rendered)
            
            return ''.join(results)
        
        return re.sub(loop_pattern, replace_loop, template, flags=re.DOTALL)
    
    def _process_conditionals(self, template: str, context: Dict[str, Any]) -> str:
        """Process conditionals: {% if condition %}...{% endif %}"""
        # Pattern for if-elif-else-endif
        if_pattern = r'\{%\s*if\s+([^%]+?)\s*%\}(.*?)(?:\{%\s*elif\s+([^%]+?)\s*%\}(.*?))*(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}'
        
        def replace_conditional(match):
            condition = match.group(1).strip()
            if_body = match.group(2)
            else_body = match.group(5) if match.group(5) else ''
            
            # Evaluate condition
            if self._evaluate_condition(condition, context):
                return if_body
            else:
                return else_body
        
        return re.sub(if_pattern, replace_conditional, template, flags=re.DOTALL)
    
    def _process_variables(self, template: str, context: Dict[str, Any]) -> str:
        """Process variables and filters: {{ variable|filter:arg }}"""
        var_pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_\.]*?)(?:\|([a-zA-Z_][a-zA-Z0-9_]*(?::[^}|]+)?(?:\|[a-zA-Z_][a-zA-Z0-9_]*(?::[^}|]+)?)*))?\s*\}\}'
        
        def replace_variable(match):
            var_path = match.group(1)
            filters_str = match.group(2)
            
            # Get variable value
            value = self._get_nested_value(context, var_path)
            
            # Apply filters if present
            if filters_str:
                filter_parts = filters_str.split('|')
                for filter_part in filter_parts:
                    if ':' in filter_part:
                        filter_name, *args = filter_part.split(':')
                        filter_name = filter_name.strip()
                        args = [arg.strip().strip('"\'') for arg in args]
                    else:
                        filter_name = filter_part.strip()
                        args = []
                    
                    if filter_name in self.filters:
                        try:
                            value = self.filters[filter_name](value, *args)
                        except Exception as e:
                            return f"[Filter error: {e}]"
                    else:
                        return f"[Unknown filter: {filter_name}]"
            
            return str(value) if value is not None else ''
        
        return re.sub(var_pattern, replace_variable, template)
    
    def _get_nested_value(self, context: Dict[str, Any], path: str) -> Any:
        """Get a nested value from context using dot notation."""
        keys = path.split('.')
        value = context
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            elif hasattr(value, key):
                value = getattr(value, key)
            else:
                return None
        
        return value
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a conditional expression."""
        condition = condition.strip()
        
        # Handle 'not' operator
        if condition.startswith('not '):
            return not self._evaluate_condition(condition[4:], context)
        
        # Handle comparison operators
        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in condition:
                left, right = condition.split(op, 1)
                left_val = self._get_value_or_literal(left.strip(), context)
                right_val = self._get_value_or_literal(right.strip(), context)
                
                if op == '==':
                    return left_val == right_val
                elif op == '!=':
                    return left_val != right_val
                elif op == '>':
                    return left_val > right_val
                elif op == '<':
                    return left_val < right_val
                elif op == '>=':
                    return left_val >= right_val
                elif op == '<=':
                    return left_val <= right_val
        
        # Handle 'and' and 'or' operators
        if ' and ' in condition:
            parts = condition.split(' and ')
            return all(self._evaluate_condition(part, context) for part in parts)
        
        if ' or ' in condition:
            parts = condition.split(' or ')
            return any(self._evaluate_condition(part, context) for part in parts)
        
        # Handle 'in' operator
        if ' in ' in condition:
            left, right = condition.split(' in ', 1)
            left_val = self._get_value_or_literal(left.strip(), context)
            right_val = self._get_value_or_literal(right.strip(), context)
            return left_val in right_val if right_val else False
        
        # Simple variable check (truthiness)
        value = self._get_value_or_literal(condition, context)
        return bool(value)
    
    def _get_value_or_literal(self, expr: str, context: Dict[str, Any]) -> Any:
        """Get value from context or parse as literal."""
        expr = expr.strip()
        
        # String literal
        if (expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Number literal
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass
        
        # Boolean literal
        if expr.lower() == 'true':
            return True
        if expr.lower() == 'false':
            return False
        
        # None literal
        if expr.lower() == 'none':
            return None
        
        # Variable from context
        return self._get_nested_value(context, expr)
    
    def load_from_file(self, filepath: str) -> str:
        """
        Load a template from a file.
        
        Args:
            filepath: Path to the template file
            
        Returns:
            Template content as string
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render_file(self, filepath: str, context: Dict[str, Any]) -> str:
        """
        Load and render a template from a file.
        
        Args:
            filepath: Path to the template file
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered template string
        """
        template = self.load_from_file(filepath)
        return self.render(template, context)


# Example usage
if __name__ == "__main__":
    engine = TemplateEngine()
    
    # Example 1: Simple variable substitution
    template1 = "Hello, {{ name|upper }}! Welcome to {{ site }}."
    context1 = {'name': 'John', 'site': 'Python World'}
    print("Example 1:")
    print(engine.render(template1, context1))
    print()
    
    # Example 2: Conditionals
    template2 = """
User: {{ user.name }}
{% if user.age >= 18 %}
Status: Adult
{% else %}
Status: Minor
{% endif %}
"""
    context2 = {'user': {'name': 'Alice', 'age': 25}}
    print("Example 2:")
    print(engine.render(template2, context2))
    
    # Example 3: Loops
    template3 = """
Shopping List:
{% for item in items %}
  {{ loop.index1 }}. {{ item|title }} {% if loop.last %}(last item){% endif %}
{% endfor %}
Total items: {{ items|length }}
"""
    context3 = {'items': ['apples', 'bananas', 'oranges']}
    print("Example 3:")
    print(engine.render(template3, context3))
    
    # Example 4: Custom filters
    engine.register_filter('double', lambda x: int(x) * 2)
    template4 = "Original: {{ number }}, Doubled: {{ number|double }}"
    context4 = {'number': 5}
    print("Example 4:")
    print(engine.render(template4, context4))
    print()
    
    # Example 5: Complex template
    template5 = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title|upper }}</h1>
    <p>Generated on: {{ date|date:%Y-%m-%d %H:%M }}</p>
    
    {% if users %}
    <h2>User List ({{ users|length }} users)</h2>
    <ul>
    {% for user in users %}
        <li>{{ user.name }} - {{ user.email }} {% if user.premium %}⭐{% endif %}</li>
    {% endfor %}
    </ul>
    {% else %}
    <p>No users found.</p>
    {% endif %}
</body>
</html>
"""
    context5 = {
        'title': 'User Dashboard',
        'date': datetime.now(),
        'users': [
            {'name': 'Alice', 'email': 'alice@example.com', 'premium': True},
            {'name': 'Bob', 'email': 'bob@example.com', 'premium': False},
            {'name': 'Charlie', 'email': 'charlie@example.com', 'premium': True}
        ]
    }
    print("Example 5:")
    print(engine.render(template5, context5))
