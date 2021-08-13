def penman_diario(J, T, UR, Rs, u, z, P, Lat, h,Tmax,Tmin):
    #J - Dia Juliano 
    #T - temperatura em ºC
	#UR - umidade relativa em %
	#Rs - radiação de onda curta medida no piranômetro em MJ/(m².dia)
	#u - velocidade do vento em m/s
	#z - altura de medição da velocidade do vento em metros
   	#P - pressão atmosférica em kPa
  	#Lat - latitude em graus
	#h - altitude da estação (metros acima do nível do mar)
    #Tmax - temperatura máxima do dia (ºC)
    #Tmin - temperatura mínima do dia (ºC)
    u2 = u*4.87/np.log(67.8*z-5.42)#altura a 2m
    G=0.6 #MJ/dia
    alfa=0.23 #coeficiente de reflexão da radiação

    lat=Lat*np.pi/180#latitude em radianos

    delta=4098*(0.6108*np.exp(17.27*T/(T+237.3)))/(T+237.3)**2
    gama=0.0665
    es=0.6108*np.exp(17.27*T/(T+237.3))
    ea=es*UR/100
    dr=1+0.033*np.cos(2*np.pi/365*J)
    dec=0.409*np.sin(2*np.pi*J/365-1.39)
    X=1-((np.tan(lat))**2)*((np.tan(dec))**2)
    if X<=0:
      X=0.00001

    ws=np.pi/2-np.arctan(-np.tan(lat)*np.tan(dec)/X**0.5)
    Ra=118.08*dr/np.pi*(ws*np.sin(lat)*np.sin(dec)+np.cos(lat)*np.cos(dec)*np.sin(ws))
    Rso=(0.75+2e-5*h)*Ra
    Rns=(1-alfa)*Rs
    sigma=4.903e-9
    Rnl=sigma*(((Tmax+273.16)**4+(Tmin+273.16)**4)/2)*(0.34-0.14*ea**0.5)*(1.35*Rs/Rso-0.35)
    Rn=Rns-Rnl
    evp=(0.408*delta*(Rn-G)+gama*900*u2*(es-ea)/(T+273))/(delta+gama*(1+0.34*u2))
    return evp

def calcular_EVP(tmed,tmax,tmin,latitude,dia_ano):
        lat=math.radians(latitude)
        j=dia_ano
        dr=1+0.033*math.cos(2*math.pi*j/365)
        d=0.409*math.sin(2*math.pi*dia_ano/365-1.39)
        X=(1-(math.tan(lat)**2)*(math.tan(d)**2))
        if X<0:
            X=0.00001
        ws=math.pi/2-math.atan(-math.tan(lat)*math.tan(d)/(X**0.5))
        Ra=118.08/math.pi*dr*(ws*math.sin(lat)*math.sin(d)+math.cos(lat)*math.cos(d)*math.sin(ws))
        ET=0.0023*Ra*((tmax-tmin)**0.5)*(tmed+17.8)
        try:
            a=float(ET)
            return ET
        except:
            return 0
def calcular_EVP2(temp,UR,latitude,dia_ano):
        lat=math.radians(latitude)
        j=dia_ano
        dr=1+0.033*math.cos(2*math.pi*j/365)
        d=0.409*math.sin(2*math.pi*dia_ano/365-1.39)
        X=(1-(math.tan(lat)**2)*(math.tan(d)**2))
        if X<0:
            X=0.00001
        ws=math.pi/2-math.atan(-math.tan(lat)*math.tan(d)/(X**0.5))
        Ra=118.08/math.pi*dr*(ws*math.sin(lat)*math.sin(d)+math.cos(lat)*math.cos(d)*math.sin(ws))
        ET=Ra*(1.8*temp+32)*0.0006*(100-UR)**0.5
        try:
            a=float(ET)
            return ET
        except:
            return 0

def calcular_EVP3(temp,latitude,dia_ano):#Fórmula de Oudim
        lat=math.radians(latitude)
        j=dia_ano
        dr=1+0.033*math.cos(2*math.pi*j/365)
        d=0.409*math.sin(2*math.pi*dia_ano/365-1.39)
        X=(1-(math.tan(lat)**2)*(math.tan(d)**2))
        if X<0:
            X=0.00001
        ws=math.pi/2-math.atan(-math.tan(lat)*math.tan(d)/(X**0.5))
        Ra=118.08/math.pi*dr*(ws*math.sin(lat)*math.sin(d)+math.cos(lat)*math.cos(d)*math.sin(ws))
        ET=Ra*(temp+5)/226
        if ET<0:
            ET=0
        return ET
