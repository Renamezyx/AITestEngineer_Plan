import warnings


def render_prompt(template_text: str, variable_dict: dict) -> str:
    for key, value in variable_dict.items():
        placeholder = "{{" + key + "}}"
        if placeholder in template_text:
            template_text = template_text.replace(placeholder, str(value))
        else:
            warnings.warn(f"\n render_prompt 时，传入的变量 {key} = {value} 在模板不存在相应占位符")

    return template_text
