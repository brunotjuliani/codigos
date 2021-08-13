def penman_horario(data_hora, T, UR, Rs, u, z, P, Lat, Long, Long_z, h):
    #Variáveis horárias:
	#T - temperatura em ºC
	#UR - umidade relativa em %
	#Rs - radiação de onda curta medida no piranômetro em kJ/(m².hr)
	#u - velocidade do vento em m/s
	#z - altura de medição da velocidade do vento em metros
	#P - pressão atmosférica em hPa = 10²Pa
	#Lat - latitude em graus
	#Long - longitude em graus
	#Long_z - longitude do centro do fuso horário
	#h - altitude da estação (metros acima do nível do mar)
	
	#Sequência de etapas para o cálculo da ET0 FAO - Evapotranspiração Potencial de referência da FAO:
	#1. es - Pressão de vapor de saturação
	es = 0.6108*np.exp(17.27*T/(T+237.3))
	#2. ea - Pressão real de vapor
	ea = es*UR/100.0
	#3. Declividade da curva de pressão de vapor de saturação (delta)
	Delta = 4098.0*es/(T+237.3)**2
	#4. Velocidade do vento a 2,0 metros de altura
	u2 = u*4.87/np.log(67.8*z-5.42)
	#5. Rns - Radiação líquida de onda curta (descontadso o albedo)
	a = 0.23 #Albedo recomendado
	Rs = Rs/1000. #Conversão de kJ/(m².hr) para MJ/(m².hr)
	Rns = (1.0 - a)*Rs
	#6. Ra - Radiação no topo da atmosfera (extraterrestre)
	#6.1 - Extrair dia juliano
	J = pd.to_datetime(data_hora).dayofyear
    
	#J = J.tm_yday
	#6.2 - Distância inversa relativa Terra- Sol (radianos)
	dr = 1. + 0.033*mt.cos(2.*mt.pi*J/365.)
	#6.3 - Declinação solar (radianos)
	delta = 0.409*mt.sin(2.*mt.pi*J/365.-1.39)
	#6.4 - Ângulo solar no tempo médio do intervalo
	hora_UTC = pd.to_datetime(data_hora).hour
	if(hora_UTC - 3 < 0):
		hora_local = 24 + hora_UTC - 3
	else:
		hora_local = hora_UTC - 3
	t = hora_local + 0.5
	b = 2.*mt.pi*(J-81.)/364.
	Sc = 0.1645*mt.sin(2*b)-0.1255*mt.cos(b)-0.025*mt.sin(b) #Correção segundo a estação do ano
	if(Long < 0):
		Long = (-1)*Long
	else:
		Long = 360 - Long
	w = mt.pi/12.*(t+0.06667*(Long_z-Long)+Sc-12)
	#6.5 - Ângulos solares no começo e fim do período
	w1 = w - mt.pi*1./24.
	w2 = w + mt.pi*1./24.
	#Cálculo de Ra
	Gsc = 0.0820 #Constante Solar - MJ/(m².hr)
	Lat = Lat * mt.pi/180 #Conversão da latitude em graus para radianos
	ws = mt.acos((-1.)*mt.tan(Lat)*mt.tan(delta))
	if (w < -1*ws or w > ws):
		Ra = 0.
	else:
		Ra = 12.*60./mt.pi*Gsc*dr*((w2-w1)*mt.sin(Lat)*mt.sin(delta)+mt.cos(Lat)*mt.cos(delta)*(mt.sin(w2)-mt.sin(w1)))
	#7. Rso - Radiação em céu limpo
	Rso = (0.75+2.*10**(-5.)*h)*Ra
		#8. Rnl - Radiação líquida de onda longa
	#8.1 - Relative shortwave radiation (f_nuvem = Rs/Rso)
	if Rso < 0.001:
		f_nuvem = 0.5 #Média dos valores possíveis (limites inferior e superior)
	else:
		if Rs/Rso < 0.33:
			f_nuvem = 0.33
		elif Rs/Rso > 1.:
			f_nuvem = 1. #Limite superior	
		else:
			f_nuvem = Rs/Rso	
	sigma = 4.903*10**(-9)/24. #Constante de Stefan Boltzman MJ/(m².hr)
	#8.2 Cálculo de Rnl
	Rnl = sigma*(T+273.16)**4*(0.34-0.14*mt.sqrt(ea))*(1.35*f_nuvem-0.35)
	#9. Radiação Líquida
	Rn = Rns - Rnl
	#10. Fluxo de calor para o solo
	if Rso < 0.001:
		G = 0.5*Rn #Período noturno
	else:
		G = 0.1*Rn #Período diurno
	#11. Constante psicrométrica (gama)
	P = P/10. #Convertendo de hPa para kPa
	gama = 0.665*10**(-3)*P
	#12. Aplicando a Equação FAO Penman-Monteith para evapotranspiração de referência
	ET0 = (0.408*Delta*(Rn-G)+gama*37./(T+273.16)*u2*(es-ea))/(Delta+gama*(1+0.34*u2)) #(mm/hr)
	if(ET0 < 0):
		ET0 = 0.
	return ET0
