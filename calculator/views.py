
from django.shortcuts import render
import control as co
# Create your views here.

def index(request):
    return render(request, "input.html")


def addition(request):
    labels = ['azul','verde','vermelho']
    lista = [1,2,3]
    kinho = True
    degrau = request.POST['ampdg']
    num1 = request.POST['num1']
    num2 = request.POST['num2']
    numcomp = request.POST['numcomp']
    dencomp = request.POST['dencomp']
    kp = request.POST['kp']
    ki = request.POST['ki']
    kd = request.POST['kd']
    
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
    
    if kinho == 1:
        #a = int(num1)
        #b = int(num2)
        res = co.tf(num,den)
        Gpid = ampdegrau*res*comp
        G = co.feedback(Gpid,1,-1)
        lista,labels = co.step_response(G)
        return render(request, "input.html", {"num_tf": texto, "linha_tf": linha,"den_tf": texto2 ,"labels":list(labels),"lista":list(lista)})
        
    

    

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

def degrau(request):
    print("kinho")
