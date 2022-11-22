from django.forms.widgets import Input


class MuxInput(Input):
    needs_multipart_form = True
    input_type = "url"
    template_name = "django_mux/forms/widgets/mux.html"

    def get_context(self, name, value, attrs):
        if self.check_test(value):
            attrs = {**(attrs or {}), "checked": True}
        return super().get_context(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        if name not in data:
            # A missing value means False because HTML form submission does not
            # send results for unselected checkboxes.
            return False
        value = data.get(name)
        # Translate true and false strings to boolean values.
        values = {"true": True, "false": False}
        if isinstance(value, str):
            value = values.get(value.lower(), value)
        return bool(value)
