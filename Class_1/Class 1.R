

library(tidyverse)
library(ggplot2)
library(dplyr)
library(tinytex)
auto <- read.csv("C:\\Users\\finle\\OneDrive\\University\\Econometrics and Statistics\\Computer stuff\\auto.csv", header = TRUE)

glimpse(auto)

expensive <- filter(auto, price>5000)
mpg_efficient <- filter(auto, mpg > 30)

auto <-  auto %>%
  mutate(mpg_metric = 0.425144 * mpg)


auto_summary <- auto %>% 
  summarise(across(where(is.numeric), \(x) mean(x, na.rm = TRUE)))

print(auto_summary)


p <- ggplot(auto, aes(x=mpg, y=weight)) +
  geom_point() + 
  geom_smooth(method = "lm", se = FALSE, color = "black", linetype = "dashed") +
  labs(title = "Car weight vs Miles per Gallon", 
       x = "Miles per Gallon (mpg)", 
       y = "Weight (lbs) ",
       color = "Car Origin") + 
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold"),
    legend.position = "right"
  )

print(p)


  