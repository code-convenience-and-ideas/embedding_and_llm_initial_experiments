import yaml
from typing import Dict, List, Optional

class PromptTemplateString:
    def __init__(self, prompt_template_dict: Dict[str, str]):
        """Initializes a PromptTemplateString object.

        Args:
            prompt_template_dict (Dict[str, str]): A dictionary containing 'name', 'button_label',
                and 'prompt' keys with string values representing a prompt template.
        """
        self.name = prompt_template_dict['name']
        self.button_label = prompt_template_dict['button_label']
        self.prompt = prompt_template_dict['prompt']

        # Specify information needed to verify + keep potential extra values
        self.needed_entries = ['name', 'button_label', 'prompt']
        self.template_dictionary = prompt_template_dict
    
    def get_button_label_dict(self):
        """Returns a dictionary keyed by button label with the name as the value.

        Returns:
            Dict[str, str]: A dictionary with the button label as key and the name as value.
        """
        return {self.button_label: self.name}
    
    def get_prompt_dict(self):
        """Returns a dictionary keyed by name with the prompt as the value.

        Returns:
            Dict[str, str]: A dictionary with the name as key and the prompt as value.
        """
        return {self.name: self.prompt}

class PromptTemplateCollection:
    def __init__(self, list_of_templates: List[PromptTemplateString]):
        """Initializes a PromptTemplateCollection object.
        
        Args:
            list_of_templates (List[PromptTemplateString]): A list of PromptTemplateString instances.
        """
        self.templates = list_of_templates
    
    def add_template(self, template: PromptTemplateString):
        """Adds a template to the collection.
        
        Args:
            template (PromptTemplateString): A PromptTemplateString instance to be added.
        """
        self.templates.append(template)
    
    def create_button_options(self) -> Dict[str, str]:
        """Creates a dictionary of button options from the collection.
        
        Returns:
            Dict[str, str]: A dictionary with button labels as keys and corresponding names as values.
        """
        return [
            {'label': item_pair[0], 'value': item_pair[1]} for template in self.templates for item_pair in template.get_button_label_dict().items()
        ]
    
    def create_template_lookup(self) -> Dict[str, str]:
        """Creates a dictionary lookup of templates from the collection.
        
        Returns:
            Dict[str, str]: A dictionary with names as keys and corresponding prompts as values.
        """
        return {
            item_pair[0]: item_pair[1] for template in self.templates for item_pair in template.get_prompt_dict().items()
        }
    
    def merge_template_collections(self, external_collection: 'PromptTemplateCollection'):
        """Merges another PromptTemplateCollection with this collection.
        
        Args:
            external_collection (PromptTemplateCollection): Another PromptTemplateCollection instance to merge.
        """
        self.templates.extend(external_collection.templates)


def load_yaml_prompt_templates(path_to_yaml: str) -> Optional[PromptTemplateCollection]:
    """Loads YAML prompt templates from a file and returns a PromptTemplateCollection.

    Args:
        path_to_yaml (str): The path to the YAML file containing prompt templates.

    Returns:
        Optional[PromptTemplateCollection]: A PromptTemplateCollection instance if successful, 
        otherwise returns None.
    """
    with open(path_to_yaml, 'r') as prompt_templates_file:
        prompt_templates = yaml.safe_load(prompt_templates_file)

    if not prompt_templates or 'templates' not in prompt_templates:
        return None  # Return None if the YAML file is empty or does not contain templates

    # Put files into the prompt template collection
    template_collection = PromptTemplateCollection([PromptTemplateString(template_data) for template_data in prompt_templates['templates']])
    
    return template_collection