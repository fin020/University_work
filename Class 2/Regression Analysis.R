library(tidyverse)
library(ggplot2)
library(dplyr)

RD <- read.csv("C:\\Users\\finle\\OneDrive\\University\\Econometrics and Statistics\\Computer stuff\\RDCHEM.csv", header = TRUE)
var.labels <- c(rd = "R&D Spending, £M", sales = "firm Sales, £M", profits =  "Profits, £M")
attr(RD, "variable.labels") <- var.labels

glimpse(RD)

RD <- RD %>% 
  mutate(
    profmarg = profits/sales * 100, 
    rdintens = rd / sales * 100, 
    salessq = sales ** 2, 
    lnsales = log(sales), 
    lnrd = log(rd))

glimpse(RD)

var.labels <- c(var.labels, profmarg = "Profit Margins (%)",
                rdintens = "R&D as a percentage of sales",
                salessq = "Sales squared",
                lnsales = "natural log of sales", 
                lnrd = "natural log of R&D")
rd.lm <- lm(data =RD, rdintens~ lnsales + profmarg)
summary(rd.lm)
