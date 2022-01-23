
from django.shortcuts import render
import matplotlib, io, base64, urllib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import control as co

def index(request):
    if request.method == 'POST':
        data = request.POST
        return render(request, "input.html", result(data))
    else:
        data = {}
        data['exemplo'] = True
        data['ampdg'] = '1'
        data['num1'] = '1'
        data['num2'] = '1 2'
        data['numcomp'] = '1'
        data['dencomp'] = '1 0'
        data['kp'] = ''
        data['ki'] = ''
        data['kd'] = ''
        return render(request, "input.html", result(data))

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
    # plt.xticks(np.arange(0,X[-1] + .001,X[-1]/10))
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

def result(data):
    exemplo = False
    try:
        exemplo = data['exemplo'] 
    except:
        pass

    degrau = data['ampdg']
    num1 = data['num1']
    num2 = data['num2']
    numcomp = data['numcomp']
    dencomp = data['dencomp']
    kp = data['kp']
    ki = data['ki']
    kd = data['kd']
    
    if kp.isdigit():
        kp = float(kp)
    else:
        kp = 0
    
    if ki.isdigit():
        ki = float(ki)
    else:
        ki = 0
    
    if kd.isdigit():
        kd = float(kd)
    else:
        kd = 0
    
    ampdegrau = float(degrau)
    
    conv_num = num1.split()
    num = []
    for casa in conv_num:
        num.append(float(casa))
    #convertendo denominador
    conv_den = num2.split()
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
    res = co.feedback(res,1,1)
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
            }
        


def subtraction(request):

    num1 = request.POST['num1']
    num2 = request.POST['num2']

    if num1.isdigit() and num2.isdigit():
        a = int(num1)
        b = int(num2)
        res = a - b

        return render(request, "result.html", {"result": res})
    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})


def multiplication(request):

    num1 = request.POST['num1']
    num2 = request.POST['num2']

    if num1.isdigit() and num2.isdigit():
        a = int(num1)
        b = int(num2)
        res = a * b

        return render(request, "result.html", {"result": res})
    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})



def division(request):

    num1 = request.POST['num1']
    num2 = request.POST['num2']

    
    if num1.isdigit() and num2.isdigit():
        a = int(num1)
        b = int(num2)

        if b == 0:
            res = "Zero divide error"
            return render(request, "result.html", {"result": res})
        else:
            res = a / b
            return render(request, "result.html", {"result": res})
    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})
