import random

def modify_components(components, modified_components, A, B):
    modified_components_set = set(modified_components.values())
    new_components = []
    for component in components:
        if '(' in component:
            # Handle nested structures without recursion
            nested_components = component[1:-1].split(',')
            modified_nested_components = modify_components(nested_components, modified_components, A, B)
            new_component = '{' + ', '.join(modified_nested_components) + '}'
            new_components.append(new_component)
        elif component.startswith('q'):
            # Replace q components with unique random numbers
            if component in modified_components:
                new_component = modified_components[component]
            else:
                if A:
                    modified_component = random.randint(1, 100)
                if B:
                    modified_component = random.randint(101, 200)
                while modified_component in modified_components_set:
                    if A:
                        modified_component = random.randint(1, 100)
                    if B:
                        modified_component = random.randint(101, 200)
                modified_components[component] = modified_component
                modified_components_set.add(modified_component)
                new_component = modified_component
            new_components.append(new_component)
        else:
            new_components.append(component)
    return new_components

def modify_array(input_array, A, B):
    modified_components = {}
    modified_array = []
    for i, item in enumerate(input_array):
        if item.startswith('{'):
            # Modify components within curly braces
            components_list = item[1:-1].split(', ')
            modified_components_list = modify_components(components_list, modified_components, A, B)
            modified_item = '{' + ', '.join(str(comp) for comp in modified_components_list) + '}'
            modified_array.append(modified_item)
        else:
            modified_array.append(item)
    return modified_array


