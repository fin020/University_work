library(ggplot2)
library(lmtest)
library(dplyr)

house_dta <- read.csv("C:\\Users\\finle\\OneDrive\\University\\Econometrics and Statistics\\Computer stuff\\house_dta.csv", header= TRUE)

summary(house_dta)

house_dta <- house_dta %>%
  mutate(
    lnprice = log(price),
    lnsqft = log(sqft),
    lnage  = log(age + 1)
  )



plot(lnprice ~ lnsqft, data = house_dta, 
     main = "Log of Price vs Log of Square Feet",
     xlab = "Log of Square Feet",
     ylab = "Log of Price")

plot(lnprice ~ lnage, data = house_dta, 
     main = "Log of Price vs Log of Age",
     xlab = "Log of Age",
     ylab = "Log of Price")



house_dta %>%
  select(lnsqft, lnage, school, fplace) %>%
  cor()

ggplot(house_dta, aes(x = lnprice)) +
  geom_histogram(fill = "skyblue", color = "white") + 
  labs(title = "Histogram of the natural logarithm of House prices",
       x = "ln(price)", 
       y = "Frequency"
       )



house_dta.lm <- lm(formula= lnprice ~ lnsqft + lnage + school + fplace, data = house_dta)
summary(house_dta.lm)
par(mfrow = c(1,2))
plot(house_dta.lm,1:2)

house_dta$group <- with(house_dta, 
                        ifelse(school == 1 & fplace == 1, "Both",
                               ifelse(school == 1, "School Only",
                                      ifelse(fplace == 1, "Fireplace Only", "Neither"))))




ggplot(house_dta, aes(x = lnsqft, y = lnprice, color = group)) +
  geom_point(size = 1) +
  labs(title = "House Prices by Group",
       x = "Log of Square Feet",
       y = "Log of Price") +
  facet_wrap(~ group) +  # This will create separate plots for each group
  theme_minimal()



