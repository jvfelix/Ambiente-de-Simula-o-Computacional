from django import forms

class SystemForm(forms.Form):
    ampdg = forms.FloatField(label='Amplitude', required=True)
    num = forms.CharField(label='Numerador', max_length=100, required=True)
    den = forms.CharField(label='Denominador', max_length=100, required=True)

class CompensatorForm(forms.Form):
    numcomp = forms.CharField(label='Numerador', max_length=100, required=True)
    dencomp = forms.CharField(label='Denominador', max_length=100, required=True)

class PIDForm(forms.Form):
    kp = forms.FloatField(label='Ganho Proporcional', required=True)
    ki = forms.FloatField(label='Ganho Integral', required=True)
    kd = forms.FloatField(label='Ganho Derivativo', required=True)

