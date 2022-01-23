
from .forms import SystemForm, CompensatorForm, PIDForm
from django.shortcuts import render
import matplotlib, io, base64, urllib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import control as co

def index(request):
    if request.method == 'POST':
        system = SystemForm(request.POST)
        compensator = CompensatorForm(request.POST)
        pid = PIDForm(request.POST)
        return render(request, "input.html", result(system, compensator, pid))

    else:
        data = {}
        data['exemplo'] = True
        data['ampdg'] = '1'
        data['num'] = '1'
        data['den'] = '1 2'
        data['numcomp'] = '1'
        data['dencomp'] = '1 0'
        data['kp'] = ''
        data['ki'] = ''
        data['kd'] = ''
        return render(request, "input.html", result(SystemForm(data), CompensatorForm(data), PIDForm(data), True))

def get_pzmap(G):    
    plt.clf()
    plt.figure(figsize=(7, 7), dpi=100)
    co.pzmap(G, True, True)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def get_step_response(G, subtitle=''):
    plt.clf()
    plt.figure(figsize=(7, 7), dpi=100)
    X, Y = co.step_response(G)
    plt.plot(X, Y, label = subtitle)
    plt.grid()
    plt.legend()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def get_lgr(G, subtitle=''):
    plt.clf()
    plt.figure(figsize=(7, 7), dpi=100)
    co.root_locus(G, plot = True)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def result(system, compensator, pid, exemplo = False):
    
    if system.is_valid():
        system_data = system.cleaned_data
        ampdegrau = system_data['ampdg']
        num = system_data['num']
        den = system_data['den']

    if compensator.is_valid():
        compensator_data = compensator.cleaned_data
        numcomp = compensator_data['numcomp']
        dencomp = compensator_data['dencomp']

    if pid.is_valid():
        pid_data = pid.cleaned_data
        kp = pid_data['kp']
        ki = pid_data['ki']
        kd = pid_data['kd']
    else:
        ki = 0
        kp = 0
        kd = 0
    
    conv_num = num.split()
    num = []
    for casa in conv_num:
        num.append(float(casa))
    #convertendo denominador
    conv_den = den.split()
    den = []
    for casa in conv_den:
        den.append(float(casa))
    x = 1
    key = 0
    texto = ""
    texto2 = ""
    for i in num:
        if key == 0:
            frase = str(i) + "s^" + str((len(num)-x)) + " "
            key = 1
        else:
            if i > 0:
                texto = texto + "+"
                    
            frase = str(i) + "s^" + str((len(num)-x)) + " "
                
        x = x + 1
        texto = texto + frase
    
    x = 1
    key = 0
    for i in den:
        if key == 0:
            frase = str(i) + "s^" + str((len(den)-x)) + " "
            key = 1
        else:
            if i > 0:
                texto2 = texto2 + "+"
                    
            frase = str(i) + "s^" + str((len(den)-x)) + " "
                
                
        x = x + 1
        texto2 = texto2 + frase
    
    ##########################PID
    conv_num = numcomp.split()
    numcp = []
    for casa in conv_num:
        numcp.append(float(casa))
    #convertendo denominador
    conv_den = dencomp.split()
    dencp = []
    for casa in conv_den:
        dencp.append(float(casa))
    x = 1
    key = 0
    texto = ""
    texto2 = ""
    for i in num:
        if key == 0:
            frase = str(i) + "s^" + str((len(num)-x)) + " "
            key = 1
        else:
            if i > 0:
                texto = texto + "+"
                    
            frase = str(i) + "s^" + str((len(num)-x)) + " "
                
        x = x + 1
        texto = texto + frase
    
    x = 1
    key = 0
    for i in den:
        if key == 0:
            frase = str(i) + "s^" + str((len(den)-x)) + " "
            key = 1
        else:
            if i > 0:
                texto2 = texto2 + "+"
                    
            frase = str(i) + "s^" + str((len(den)-x)) + " "
                
                
        x = x + 1
        texto2 = texto2 + frase
    linha = ""
    for i in texto2:
        linha = linha + "-"
    #######################################################
    if kp == 0 and ki ==0 and kd == 0:
        comp = co.tf(numcp,dencp)
    else:
        #proporcional
        nump = [kp]
        denp = [1.0]
        gp = co.tf(nump,denp)
        #integral
        numi = [ki]
        deni = [1.0, 0.0]
        gi = co.tf(numi,deni)
        #derivativo
        numd = [kd, 0.0]
        dend = [1.0]
        gd = co.tf(numd,dend)

        comp = gp + gi + gd
    
    res = co.tf(num,den)
    print(res)
    res = co.feedback(res,1,1)
    print(res)
    Gpid = ampdegrau*res*comp
    G = co.feedback(Gpid,1,-1)

    return  {
                'type': ('exemplo' if exemplo else 'Resultado'),
                'step_response':get_step_response(res, res.__str__()),
                'step_response_comp':get_step_response(G, G.__str__()),
                'lgr':get_lgr(res),
                'lgr_comp':get_lgr(G),
                'pzmap':get_pzmap(res),
                'pzmap_comp':get_pzmap(G),
                'System':res.__str__(),
                'SystemComp':G.__str__(),
                'Comp':comp.__str__(),
                'system':system,
                'compensator':compensator,
                'pid':pid
            }
        


def subtraction(request):

    num = request.POST['num']
    den = request.POST['den']

    if num.isdigit() and den.isdigit():
        a = int(num)
        b = int(den)
        res = a - b

        return render(request, "result.html", {"result": res})
    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})


def multiplication(request):

    num = request.POST['num']
    den = request.POST['den']

    if num.isdigit() and den.isdigit():
        a = int(num)
        b = int(den)
        res = a * b

        return render(request, "result.html", {"result": res})
    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})



def division(request):

    num = request.POST['num']
    den = request.POST['den']

    
    if num.isdigit() and den.isdigit():
        a = int(num)
        b = int(den)

        if b == 0:
            res = "Zero divide error"
            return render(request, "result.html", {"result": res})
        else:
            res = a / b
            return render(request, "result.html", {"result": res})
    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})
