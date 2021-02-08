
library(trend)
library(changepoint)
library(ggplot2)
library(mblm)

estacoes_parana = "~/Dropbox/Artigos_Bruno/XIII SBRH/STATIONS"
figuras = "~/Dropbox/Artigos_Bruno/XIII SBRH/Figuras"

sen <- function(..., weights = NULL) {
  mblm::mblm(...)
}
setwd(estacoes_parana)
lista_estacoes <- list("01. Andira", "02. Tomazina", "03. Tibagi", "04. Capela", "05. Colonia",
                       "06. Curitiba", "07. Morretes", "08. P_Amazonas", "09. P_Vitoria",
                       "10. Rio_da_Varzea", "11. Rio_dos_Patos", "12. Santa_Cruz", "13. Turvo")

Resultados <- data.frame()
for(estacao in lista_estacoes){

  Data.mensal <- data.frame(read.csv(paste(estacao,".csv",sep = ""), sep = ";", dec = ","))
  Data.mensal$ANUAL <- rowSums(Data.mensal)
  colnames(Data.mensal)[1] <- 'ANO'
  Data.mensal_30_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1979",]
  Data.mensal_30_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="1989",]
  Data.mensal_30_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="1999",]
  Data.mensal_30_80 <- Data.mensal[Data.mensal$ANO >= "1980" & Data.mensal$ANO <="2009",]
  Data.mensal_30_90 <- Data.mensal[Data.mensal$ANO >= "1990" & Data.mensal$ANO <="2019",]
  
  Resultados_30_50 <- data.frame(Estacao = estacao)
  Resultados_30_50$N_Anos <- 30
  Resultados_30_50$Inicio <- 1950
  Resultados_30_50$MK_p <- mk.test(Data.mensal_30_50$ANUAL)$p.value
  Resultados_30_50$Theil_Sen <- sens.slope(Data.mensal_30_50$ANUAL)$estimates
  Resultados_30_50$Pettitt_p <- pettitt.test(Data.mensal_30_50$ANUAL)$p.value
  Resultados_30_50$Pettitt_Ano <- Data.mensal_30_50[pettitt.test(Data.mensal_30_50$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_30_50)
  
  Resultados_30_60 <- data.frame(Estacao = estacao)
  Resultados_30_60$N_Anos <- 30
  Resultados_30_60$Inicio <- 1960
  Resultados_30_60$MK_p <- mk.test(Data.mensal_30_60$ANUAL)$p.value
  Resultados_30_60$Theil_Sen <- sens.slope(Data.mensal_30_60$ANUAL)$estimates
  Resultados_30_60$Pettitt_p <- pettitt.test(Data.mensal_30_60$ANUAL)$p.value
  Resultados_30_60$Pettitt_Ano <- Data.mensal_30_60[pettitt.test(Data.mensal_30_60$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_30_60)
  
  Resultados_30_70 <- data.frame(Estacao = estacao)
  Resultados_30_70$N_Anos <- 30
  Resultados_30_70$Inicio <- 1970
  Resultados_30_70$MK_p <- mk.test(Data.mensal_30_70$ANUAL)$p.value
  Resultados_30_70$Theil_Sen <- sens.slope(Data.mensal_30_70$ANUAL)$estimates
  Resultados_30_70$Pettitt_p <- pettitt.test(Data.mensal_30_70$ANUAL)$p.value
  Resultados_30_70$Pettitt_Ano <- Data.mensal_30_70[pettitt.test(Data.mensal_30_70$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_30_70)
  
  Resultados_30_80 <- data.frame(Estacao = estacao)
  Resultados_30_80$N_Anos <- 30
  Resultados_30_80$Inicio <- 1980
  Resultados_30_80$MK_p <- mk.test(Data.mensal_30_80$ANUAL)$p.value
  Resultados_30_80$Theil_Sen <- sens.slope(Data.mensal_30_80$ANUAL)$estimates
  Resultados_30_80$Pettitt_p <- pettitt.test(Data.mensal_30_80$ANUAL)$p.value
  Resultados_30_80$Pettitt_Ano <- Data.mensal_30_80[pettitt.test(Data.mensal_30_80$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_30_80)
  
  Resultados_30_90 <- data.frame(Estacao = estacao)
  Resultados_30_90$N_Anos <- 30
  Resultados_30_90$Inicio <- 1990
  Resultados_30_90$MK_p <- mk.test(Data.mensal_30_90$ANUAL)$p.value
  Resultados_30_90$Theil_Sen <- sens.slope(Data.mensal_30_90$ANUAL)$estimates
  Resultados_30_90$Pettitt_p <- pettitt.test(Data.mensal_30_90$ANUAL)$p.value
  Resultados_30_90$Pettitt_Ano <- Data.mensal_30_90[pettitt.test(Data.mensal_30_90$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_30_90)
  
  
  Data.mensal_40_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1989",]
  Data.mensal_40_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="1999",]
  Data.mensal_40_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="2009",]
  Data.mensal_40_80 <- Data.mensal[Data.mensal$ANO >= "1980" & Data.mensal$ANO <="2019",]
  
  Resultados_40_50 <- data.frame(Estacao = estacao)
  Resultados_40_50$N_Anos <- 40
  Resultados_40_50$Inicio <- 1950
  Resultados_40_50$MK_p <- mk.test(Data.mensal_40_50$ANUAL)$p.value
  Resultados_40_50$Theil_Sen <- sens.slope(Data.mensal_40_50$ANUAL)$estimates
  Resultados_40_50$Pettitt_p <- pettitt.test(Data.mensal_40_50$ANUAL)$p.value
  Resultados_40_50$Pettitt_Ano <- Data.mensal_40_50[pettitt.test(Data.mensal_40_50$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_40_50)
  
  Resultados_40_60 <- data.frame(Estacao = estacao)
  Resultados_40_60$N_Anos <- 40
  Resultados_40_60$Inicio <- 1960
  Resultados_40_60$MK_p <- mk.test(Data.mensal_40_60$ANUAL)$p.value
  Resultados_40_60$Theil_Sen <- sens.slope(Data.mensal_40_60$ANUAL)$estimates
  Resultados_40_60$Pettitt_p <- pettitt.test(Data.mensal_40_60$ANUAL)$p.value
  Resultados_40_60$Pettitt_Ano <- Data.mensal_40_60[pettitt.test(Data.mensal_40_60$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_40_60)
  
  Resultados_40_70 <- data.frame(Estacao = estacao)
  Resultados_40_70$N_Anos <- 40
  Resultados_40_70$Inicio <- 1970
  Resultados_40_70$MK_p <- mk.test(Data.mensal_40_70$ANUAL)$p.value
  Resultados_40_70$Theil_Sen <- sens.slope(Data.mensal_40_70$ANUAL)$estimates
  Resultados_40_70$Pettitt_p <- pettitt.test(Data.mensal_40_70$ANUAL)$p.value
  Resultados_40_70$Pettitt_Ano <- Data.mensal_40_70[pettitt.test(Data.mensal_40_70$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_40_70)
  
  Resultados_40_80 <- data.frame(Estacao = estacao)
  Resultados_40_80$N_Anos <- 40
  Resultados_40_80$Inicio <- 1980
  Resultados_40_80$MK_p <- mk.test(Data.mensal_40_80$ANUAL)$p.value
  Resultados_40_80$Theil_Sen <- sens.slope(Data.mensal_40_80$ANUAL)$estimates
  Resultados_40_80$Pettitt_p <- pettitt.test(Data.mensal_40_80$ANUAL)$p.value
  Resultados_40_80$Pettitt_Ano <- Data.mensal_40_80[pettitt.test(Data.mensal_40_80$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_40_80)
  
  
  Data.mensal_50_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1999",]
  Data.mensal_50_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="2009",]
  Data.mensal_50_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="2019",]
  
  Resultados_50_50 <- data.frame(Estacao = estacao)
  Resultados_50_50$N_Anos <- 50
  Resultados_50_50$Inicio <- 1950
  Resultados_50_50$MK_p <- mk.test(Data.mensal_50_50$ANUAL)$p.value
  Resultados_50_50$Theil_Sen <- sens.slope(Data.mensal_50_50$ANUAL)$estimates
  Resultados_50_50$Pettitt_p <- pettitt.test(Data.mensal_50_50$ANUAL)$p.value
  Resultados_50_50$Pettitt_Ano <- Data.mensal_50_50[pettitt.test(Data.mensal_50_50$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_50_50)
  
  Resultados_50_60 <- data.frame(Estacao = estacao)
  Resultados_50_60$N_Anos <- 50
  Resultados_50_60$Inicio <- 1960
  Resultados_50_60$MK_p <- mk.test(Data.mensal_50_60$ANUAL)$p.value
  Resultados_50_60$Theil_Sen <- sens.slope(Data.mensal_50_60$ANUAL)$estimates
  Resultados_50_60$Pettitt_p <- pettitt.test(Data.mensal_50_60$ANUAL)$p.value
  Resultados_50_60$Pettitt_Ano <- Data.mensal_50_60[pettitt.test(Data.mensal_50_60$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_50_60)
  
  Resultados_50_70 <- data.frame(Estacao = estacao)
  Resultados_50_70$N_Anos <- 50
  Resultados_50_70$Inicio <- 1970
  Resultados_50_70$MK_p <- mk.test(Data.mensal_50_70$ANUAL)$p.value
  Resultados_50_70$Theil_Sen <- sens.slope(Data.mensal_50_70$ANUAL)$estimates
  Resultados_50_70$Pettitt_p <- pettitt.test(Data.mensal_50_70$ANUAL)$p.value
  Resultados_50_70$Pettitt_Ano <- Data.mensal_50_70[pettitt.test(Data.mensal_50_70$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_50_70)
  
  
  Data.mensal_60_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="2009",]
  Data.mensal_60_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="2019",]
  
  Resultados_60_50 <- data.frame(Estacao = estacao)
  Resultados_60_50$N_Anos <- 60
  Resultados_60_50$Inicio <- 1950
  Resultados_60_50$MK_p <- mk.test(Data.mensal_60_50$ANUAL)$p.value
  Resultados_60_50$Theil_Sen <- sens.slope(Data.mensal_60_50$ANUAL)$estimates
  Resultados_60_50$Pettitt_p <- pettitt.test(Data.mensal_60_50$ANUAL)$p.value
  Resultados_60_50$Pettitt_Ano <- Data.mensal_60_50[pettitt.test(Data.mensal_60_50$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_60_50)
  
  Resultados_60_60 <- data.frame(Estacao = estacao)
  Resultados_60_60$N_Anos <- 60
  Resultados_60_60$Inicio <- 1960
  Resultados_60_60$MK_p <- mk.test(Data.mensal_60_60$ANUAL)$p.value
  Resultados_60_60$Theil_Sen <- sens.slope(Data.mensal_60_60$ANUAL)$estimates
  Resultados_60_60$Pettitt_p <- pettitt.test(Data.mensal_60_60$ANUAL)$p.value
  Resultados_60_60$Pettitt_Ano <- Data.mensal_60_60[pettitt.test(Data.mensal_60_60$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_60_60)
  
  
  Data.mensal_70_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="2019",]
  
  Resultados_70_50 <- data.frame(Estacao = estacao)
  Resultados_70_50$N_Anos <- 70
  Resultados_70_50$Inicio <- 1950
  Resultados_70_50$MK_p <- mk.test(Data.mensal_70_50$ANUAL)$p.value
  Resultados_70_50$Theil_Sen <- sens.slope(Data.mensal_70_50$ANUAL)$estimates
  Resultados_70_50$Pettitt_p <- pettitt.test(Data.mensal_70_50$ANUAL)$p.value
  Resultados_70_50$Pettitt_Ano <- Data.mensal_70_50[pettitt.test(Data.mensal_70_50$ANUAL)$estimate[1],"ANO"]
  Resultados <- rbind(Resultados, Resultados_70_50)
  

}

print(Resultados)
write.csv(Resultados, file = "Resultados_MK.csv", sep = ";", dec = ",")


###### PLOT THEIL SEN CAPELA DO RIBEIRA ######
sen <- function(..., weights = NULL) {
  mblm::mblm(...)
}
setwd(estacoes_parana)
Data.mensal <- data.frame(read.csv(paste("04. Capela",".csv",sep = ""), sep = ";", dec = ","))
Data.mensal$ANUAL <- rowSums(Data.mensal)
colnames(Data.mensal)[1] <- 'ANO'

Data.mensal_70_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="2019",]
Data.mensal_30_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1979",]
Data.mensal_30_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="1989",]
Data.mensal_30_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="1999",]
Data.mensal_30_80 <- Data.mensal[Data.mensal$ANO >= "1980" & Data.mensal$ANO <="2009",]
Data.mensal_30_90 <- Data.mensal[Data.mensal$ANO >= "1990" & Data.mensal$ANO <="2019",]

Trend.70_50 <- mblm(ANUAL ~ ANO, data = Data.mensal_70_50)
ano1.70_50 <- 1950
ano2.70_50 <- 2019
xs.70_50 = c(ano1.70_50, ano2.70_50)
intercept.70_50 <- coef(Trend.70_50)[1]
slope.70_50 <- coef(Trend.70_50)[2]
beta.70_50 = c(intercept.70_50, slope.70_50)
ys.70_50 = cbind(1, xs.70_50) %*% beta.70_50

Trend.30_60 <- mblm(ANUAL ~ ANO, data = Data.mensal_30_60)
ano1.30_60 <- 1960
ano2.30_60 <- 1989
xs.30_60 = c(ano1.30_60, ano2.30_60)
intercept.30_60 <- coef(Trend.30_60)[1]
slope.30_60 <- coef(Trend.30_60)[2]
beta.30_60 = c(intercept.30_60, slope.30_60)
ys.30_60 = cbind(1, xs.30_60) %*% beta.30_60

Trend.30_90 <- mblm(ANUAL ~ ANO, data = Data.mensal_30_90)
ano1.30_90 <- 1990
ano2.30_90 <- 2019
xs.30_90 = c(ano1.30_90, ano2.30_90)
intercept.30_90 <- coef(Trend.30_90)[1]
slope.30_90 <- coef(Trend.30_90)[2]
beta.30_90 = c(intercept.30_90, slope.30_90)
ys.30_90 = cbind(1, xs.30_90) %*% beta.30_90

setwd(figuras)
png(file = paste('Capela_trends.png', sep = ''), width = 879, height = 618, res = 130)
ggplot(Data.mensal_70_50, aes((Data.mensal_70_50$ANO), Data.mensal_70_50$ANUAL)) + 
  geom_line() + 
  xlab("Year") + 
  ylab("Annual Precipitation (mm)") + 
  geom_segment(aes(x = xs.70_50[1], xend = xs.70_50[2], y = ys.70_50[1], 
                   yend = ys.70_50[2]), 
               color = "red", linetype=3, lwd=.5) +
  geom_segment(aes(x = 1950, xend = 1979, y = mean(Data.mensal_30_50$ANUAL), 
                   yend = mean(Data.mensal_30_50$ANUAL)), 
               color = "blue", linetype = 1, lwd=.2) +
  geom_segment(aes(x = xs.30_60[1], xend = xs.30_60[2], y = ys.30_60[1], 
                   yend = ys.30_60[2]), 
               color = "blue", linetype = 1, lwd=.2) + 
  geom_segment(aes(x = 1970, xend = 1999, y = mean(Data.mensal_30_70$ANUAL), 
                   yend = mean(Data.mensal_30_70$ANUAL)), 
               color = "blue", linetype = 1, lwd=.2) +
  geom_segment(aes(x = 1980, xend = 2009, y = mean(Data.mensal_30_80$ANUAL), 
                   yend = mean(Data.mensal_30_80$ANUAL)), 
               color = "blue", linetype = 1, lwd=.2) +
  geom_segment(aes(x = xs.30_90[1], xend = xs.30_90[2], y = ys.30_90[1], 
                   yend = ys.30_90[2]), 
               color = "blue", linetype = 1, lwd=.2) + 
  ggtitle('Capela da Ribeira') + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  theme(legend.position = "top")
dev.off()

###### PLOT THEIL SEN PORTO VITORIA ######
sen <- function(..., weights = NULL) {
  mblm::mblm(...)
}
setwd(estacoes_parana)
Data.mensal <- data.frame(read.csv(paste("09. P_Vitoria",".csv",sep = ""), sep = ";", dec = ","))
Data.mensal$ANUAL <- rowSums(Data.mensal)
colnames(Data.mensal)[1] <- 'ANO'

Data.mensal_70_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="2019",]
Data.mensal_30_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1979",]
Data.mensal_30_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="1989",]
Data.mensal_30_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="1999",]
Data.mensal_30_80 <- Data.mensal[Data.mensal$ANO >= "1980" & Data.mensal$ANO <="2009",]
Data.mensal_30_90 <- Data.mensal[Data.mensal$ANO >= "1990" & Data.mensal$ANO <="2019",]
Data.mensal_50_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1999",]
Data.mensal_50_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="2009",]
Data.mensal_50_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="2019",]



Trend.30_50 <- mblm(ANUAL ~ ANO, data = Data.mensal_30_50)
ano1.30_50 <- 1950
ano2.30_50 <- 1979
xs.30_50 = c(ano1.30_50, ano2.30_50)
intercept.30_50 <- coef(Trend.30_50)[1]
slope.30_50 <- coef(Trend.30_50)[2]
beta.30_50 = c(intercept.30_50, slope.30_50)
ys.30_50 = cbind(1, xs.30_50) %*% beta.30_50

Trend.50_50 <- mblm(ANUAL ~ ANO, data = Data.mensal_50_50)
ano1.50_50 <- 1950
ano2.50_50 <- 1999
xs.50_50 = c(ano1.50_50, ano2.50_50)
intercept.50_50 <- coef(Trend.50_50)[1]
slope.50_50 <- coef(Trend.50_50)[2]
beta.50_50 = c(intercept.50_50, slope.50_50)
ys.50_50 = cbind(1, xs.50_50) %*% beta.50_50

setwd(figuras)
png(file = paste('P_Vitoria_trends.png', sep = ''), width = 879, height = 618, res = 130)
ggplot(Data.mensal_70_50, aes((Data.mensal_70_50$ANO), Data.mensal_70_50$ANUAL)) + 
  geom_line() + 
  xlab("Year") + 
  ylab("Annual Precipitation (mm)") + 
  geom_segment(aes(x = 1950, xend = 2019, y = mean(Data.mensal_70_50$ANUAL), 
                   yend = mean(Data.mensal_70_50$ANUAL)), 
               color = "red", linetype = 3, lwd=.5) +
  geom_segment(aes(x = xs.50_50[1], xend = xs.50_50[2], y = ys.50_50[1], 
                   yend = ys.50_50[2]), 
               color = "blue", linetype = 1, lwd=.2) +
  geom_segment(aes(x = 1960, xend = 2009, y = mean(Data.mensal_50_60$ANUAL), 
                   yend = mean(Data.mensal_50_60$ANUAL)), 
               color = "blue", linetype = 1, lwd=.3) +
  geom_segment(aes(x = 1970, xend = 2019, y = mean(Data.mensal_50_70$ANUAL), 
                   yend = mean(Data.mensal_50_70$ANUAL)), 
               color = "blue", linetype = 1, lwd=.2) +
  ggtitle('Porto Vitoria') + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  theme(legend.position = "top")
dev.off()

###### PLOT THEIL SEN TURVO ######
sen <- function(..., weights = NULL) {
  mblm::mblm(...)
}
setwd(estacoes_parana)
Data.mensal <- data.frame(read.csv(paste("03. Turvo",".csv",sep = ""), sep = ";", dec = ","))
Data.mensal$ANUAL <- rowSums(Data.mensal)
colnames(Data.mensal)[1] <- 'ANO'

Data.mensal_70_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="2019",]
Data.mensal_40_50 <- Data.mensal[Data.mensal$ANO >= "1950" & Data.mensal$ANO <="1989",]
Data.mensal_40_60 <- Data.mensal[Data.mensal$ANO >= "1960" & Data.mensal$ANO <="1999",]
Data.mensal_40_70 <- Data.mensal[Data.mensal$ANO >= "1970" & Data.mensal$ANO <="2009",]
Data.mensal_40_80 <- Data.mensal[Data.mensal$ANO >= "1980" & Data.mensal$ANO <="2019",]

Trend.70_50 <- mblm(ANUAL ~ ANO, data = Data.mensal_70_50)
ano1.70_50 <- 1950
ano2.70_50 <- 2019
xs.70_50 = c(ano1.70_50, ano2.70_50)
intercept.70_50 <- coef(Trend.70_50)[1]
slope.70_50 <- coef(Trend.70_50)[2]
beta.70_50 = c(intercept.70_50, slope.70_50)
ys.70_50 = cbind(1, xs.70_50) %*% beta.70_50

Trend.40_50 <- mblm(ANUAL ~ ANO, data = Data.mensal_40_50)
ano1.40_50 <- 1950
ano2.40_50 <- 1989
xs.40_50 = c(ano1.40_50, ano2.40_50)
intercept.40_50 <- coef(Trend.40_50)[1]
slope.40_50 <- coef(Trend.40_50)[2]
beta.40_50 = c(intercept.40_50, slope.40_50)
ys.40_50 = cbind(1, xs.40_50) %*% beta.40_50

Trend.40_60 <- mblm(ANUAL ~ ANO, data = Data.mensal_40_60)
ano1.40_60 <- 1960
ano2.40_60 <- 1999
xs.40_60 = c(ano1.40_60, ano2.40_60)
intercept.40_60 <- coef(Trend.40_60)[1]
slope.40_60 <- coef(Trend.40_60)[2]
beta.40_60 = c(intercept.40_60, slope.40_60)
ys.40_60 = cbind(1, xs.40_60) %*% beta.40_60

setwd(figuras)
png(file = paste('Turvo_trends.png', sep = ''), width = 879, height = 618, res = 130)
ggplot(Data.mensal_70_50, aes((Data.mensal_70_50$ANO), Data.mensal_70_50$ANUAL)) + 
  geom_line() + 
  xlab("Year") + 
  ylab("Annual Precipitation (mm)") +
  geom_segment(aes(x = xs.70_50[1], xend = xs.70_50[2], y = ys.70_50[1], 
                   yend = ys.70_50[2]), 
               color = "red", linetype=3, lwd=.5) +
  geom_segment(aes(x = xs.40_50[1], xend = xs.40_50[2], y = ys.40_50[1], 
                   yend = ys.40_50[2]), 
               color = "blue", linetype = 1, lwd=.2) +
  geom_segment(aes(x = xs.40_60[1], xend = xs.40_60[2], y = ys.40_60[1], 
                   yend = ys.40_60[2]), 
               color = "blue", linetype = 1, lwd=.2) +
  geom_segment(aes(x = 1970, xend = 2009, y = mean(Data.mensal_40_70$ANUAL), 
                   yend = mean(Data.mensal_40_70$ANUAL)), 
               color = "blue", linetype = 1, lwd=.3) +
  geom_segment(aes(x = 1980, xend = 2019, y = mean(Data.mensal_40_80$ANUAL), 
                   yend = mean(Data.mensal_40_80$ANUAL)), 
               color = "blue", linetype = 1, lwd=.3) +
  ggtitle('Turvo') + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  theme(legend.position = "top")
dev.off()
