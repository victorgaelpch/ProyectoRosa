from django import forms
from .models import Producto

TIPOS = [
    ('bebida_caliente', 'Bebida Caliente'),
    ('bebida_fria', 'Bebida Fría'),
    ('bocadillo', 'Bocadillo'),
    ('snack', 'Snack'),
    ('reposteria', 'Repostería'),
]


class ProductoForm(forms.ModelForm):
    tipo_producto = forms.ChoiceField(choices=TIPOS, label="Tipo de producto")

    # Campos extra
    tipo_vaso = forms.CharField(required=False, label="Tipo de vaso")
    tipo_leche = forms.CharField(required=False, label="Tipo de leche")
    tipo_hielo = forms.CharField(required=False, label="Tipo de hielo")
    sabor = forms.CharField(required=False, label="Sabor")
    tipo_pan = forms.CharField(required=False, label="Tipo de pan")
    relleno = forms.CharField(required=False, label="Relleno")
    tipo_snack = forms.CharField(required=False, label="Tipo de snack")
    tipo_sabor = forms.CharField(required=False, label="Tipo de sabor")
    tipo_reposteria = forms.CharField(
        required=False, label="Tipo de repostería")
    glaseado = forms.BooleanField(required=False, label="Glaseado")
    decorado = forms.BooleanField(required=False, label="Decorado")

    class Meta:
        model = Producto
        fields = [
            'nombre_producto', 'tamaño', 'descripcion', 'imagen', 'precio', 'tipo',
            'tipo_producto', 'tipo_vaso', 'tipo_leche', 'tipo_hielo', 'sabor',
            'tipo_pan', 'relleno', 'tipo_snack', 'tipo_sabor',
            'tipo_reposteria', 'glaseado', 'decorado'
        ]
