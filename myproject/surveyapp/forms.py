from django import forms
import json

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_structure = kwargs.pop('form_structure')

        # Deserialize JSON string if needed
        if isinstance(form_structure, str):
            try:
                form_structure = json.loads(form_structure)
            except json.JSONDecodeError:
                raise ValueError("form_structure is not valid JSON")

        # Ensure form_structure is a list
        if isinstance(form_structure, dict):
            form_structure = [form_structure]
        if not isinstance(form_structure, list):
            raise ValueError(f"form_structure must be a list, got {type(form_structure)}")

        super().__init__(*args, **kwargs)

        # Process each field in the form structure
        for field in form_structure:
            field_type = field.get('type')
            field_name = field.get('name')
            field_label = field.get('label', field_name)
            required = field.get('required', True)

            if not field_type or not field_name:
                raise ValueError(f"Field type or name is missing in {field}")

            # Handle different field types
            if field_type == 'text':
                self.fields[field_name] = forms.CharField(label=field_label, required=required)
            elif field_type == 'number':
                min_value = field.get('min')
                max_value = field.get('max')
                self.fields[field_name] = forms.IntegerField(
                    label=field_label, required=required, min_value=min_value, max_value=max_value
                )
            elif field_type == 'choice':
                choices = field.get('choices', [])
                self.fields[field_name] = forms.ChoiceField(
                    label=field_label, required=required,
                    choices=[(choice, choice) for choice in choices], 
                    widget=forms.RadioSelect
                )
            elif field_type == 'multi_choice':
                choices = field.get('choices', [])
                self.fields[field_name] = forms.MultipleChoiceField(
                    label=field_label, required=required,
                    choices=[(choice['value'], choice['label']) for choice in choices],
                    widget=forms.CheckboxSelectMultiple
                )
            elif field_type == 'textarea':
                self.fields[field_name] = forms.CharField(
                    label=field_label, required=required,
                    widget=forms.Textarea
                )
            else:
                raise ValueError(f"Unsupported field type: {field_type}")
# class DynamicForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         form_structure = kwargs.pop('form_structure')

#         # Deserialize JSON string if needed
#         if isinstance(form_structure, str):
#             try:
#                 form_structure = json.loads(form_structure)
#             except json.JSONDecodeError:
#                 raise ValueError("form_structure is not valid JSON")

#         # Convert a single dictionary to a list for uniform processing
#         if isinstance(form_structure, dict):
#             form_structure = [form_structure]

#         # Ensure form_structure is now a list of dictionaries
#         if not isinstance(form_structure, list):
#             raise ValueError(f"form_structure must be a list, got {type(form_structure)}")

#         super().__init__(*args, **kwargs)

#         # Process each field in the form structure
#         for field in form_structure:
#             if not isinstance(field, dict):
#                 raise ValueError(f"Each field in form_structure must be a dictionary, got {type(field)}")

#             # Check for required keys
#             field_type = field.get('type')
#             field_name = field.get('name')

#             if not field_type:
#                 raise ValueError(f"Field type is missing or invalid: {field}")
#             if not field_name:
#                 raise ValueError(f"Field name is missing or invalid: {field}")

#             field_label = field.get('label', field_name)
#             required = field.get('required', True)

#             if field_type == 'text':
#                 self.fields[field_name] = forms.CharField(label=field_label, required=required)
#             elif field_type == 'number':
#                 self.fields[field_name] = forms.DecimalField(label=field_label, required=required)
#             elif field_type == 'choice':
#                 choices = field.get('choices', [])
#                 self.fields[field_name] = forms.ChoiceField(
#                     label=field_label,
#                     choices=[(choice, choice) for choice in choices],
#                     required=required
#                 )
#             else:
#                 raise ValueError(f"Unsupported field type: {field_type}")
