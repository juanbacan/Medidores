from django import forms
from django.utils.safestring import mark_safe
from .models import CustomUser

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.configure_field(field)

        try:
            errorList=list(self.errors)
            for item in errorList:
                self.fields[item].widget.attrs.update({'autofocus': ''})
                break
        except:
            pass

    def configure_field(self, field):
        if "class" in field.widget.attrs:
            field.widget.attrs["class"] += " form-control form-control-sm"
        else:
            field.widget.attrs["class"] = "form-control form-control-sm"

        # Check if field.widget has input_type attribute
        if hasattr(field.widget, "input_type"):
            if field.widget.input_type == "checkbox":
                field.widget.attrs["class"] = field.widget.attrs["class"].replace("form-control form-control-sm", "form-check-input")
            if field.widget.input_type == "select":
                field.widget.attrs["class"] += " form-select"

        if "validate" in field.widget.attrs:
            validation_attrs = self.get_validation_attrs(field.widget.attrs["validate"])
            field.widget.attrs.update(validation_attrs)

        if field.required:
            field.label = mark_safe(field.label + '<span class="text-danger">*</span> ')


    def get_validation_attrs(self, validation_type):
        validation_attrs = {}
        if validation_type == "telefono_movil":
            validation_attrs['pattern'] = "[0]{1}[9]{1}[0-9]{8}"
            validation_attrs['validate'] = "Núm. móvil incorrecto. Ejm: 0987654321"
        elif validation_type == "telefono_fijo":
            validation_attrs['pattern'] = "[0]{1}[2-8]{1}[0-9]{7}"
            validation_attrs['validate'] = "Núm. fijo incorrecto. Ejm: 022345678"
        elif validation_type == "cedula":
            validation_attrs['pattern'] = "[0-9]{10}"
            validation_attrs['validate'] = "La cédula debe tener 10 dígitos"
        elif validation_type == "email":
            validation_attrs['pattern'] = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
            validation_attrs['validate'] = "Correo electrónico incorrecto."
        return validation_attrs


class ModelBaseForm(BaseForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelBaseForm, self).__init__(*args, **kwargs)


class CustomUserForm(ModelBaseForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'cedula', 'fecha_nacimiento', 'celular']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'cedula': 'Cédula',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'celular': 'Celular',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(BaseForm):
    cedula = forms.CharField(label='Cédula Identidad', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())


class SignupForm(BaseForm):
    cedula = forms.CharField(label='Cédula Identidad', max_length=10)
    first_name = forms.CharField(label='Nombres', max_length=150)
    last_name = forms.CharField(label='Apellidos', max_length=150)
    email = forms.EmailField(label='Correo Electrónico')
    email2 = forms.EmailField(label='Confirmar Correo Electrónico')
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    celular = forms.CharField(label='Celular', max_length=10)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if email != email2:
            self.add_error('email2', 'Los correos electrónicos no coinciden')
        if password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data
    

class ResetPasswordForm(BaseForm):
    email = forms.EmailField(label='Correo Electrónico')

class ChangePasswordForm(BaseForm):
    password = forms.CharField(label='Contraseña Nueva', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data