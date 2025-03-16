# G??rev 1 
install.packages("rsample")
library(rsample)
library(tidyverse)
library(readr)
library(dplyr)

data <- read.csv("C:/Users/User/Desktop/mtcars.csv")

set.seed(123) # reproducible sonu??lar
split <- initial_split(data, prop = 0.6)
training_data <- training(split)
testing_data <- testing(split)

print(paste("Train data rows: ", nrow(training_data)))
print(paste("Test data rows: ", nrow(testing_data)))

mean_mpg_training <- training_data %>%
  summarise(Mean_MPG = mean(mpg, na.rm=TRUE))
mean_mpg_testing <- testing_data %>%
  summarise(Mean_MPG = mean(mpg, na.rm=TRUE))

print(paste("Mean MPG (Train): ", mean_mpg_training$Mean_MPG))
print(paste("Mean MPG (Test): ", mean_mpg_testing$Mean_MPG))

# G??rev 2
install.packages("mlbench")
library(mlbench)

data <- PimaIndiansDiabetes

set.seed(123)
split <- initial_split(data, prop = 0.7, strat = diabetes)

training_data <- training(split)
testing_data <- testing(split)

print(paste("Train data rows: ", nrow(training_data)))
print(paste("Test data rows: ", nrow(testing_data)))

# stratified sampling kontrol??
original_distribution <- data %>%
  count(diabetes) %>%
  mutate(Proportion = n / nrow(data) * 100)

training_distribution <- training_data %>%
  count(diabetes) %>%
  mutate(Proportion = n / nrow(training_data) * 100)

testing_distribution <- testing_data %>%
  count(diabetes) %>% 
  mutate(Proportion = n / nrow(testing_data) * 100)

print(paste("Original distribution: %", original_distribution))
print(paste("Training distribution: %", training_distribution))
print(paste("testing distribution: %", testing_distribution))

# G??rev 3
install.packages("yardstick")
library(purrr)
library(yardstick)
library(ggplot2)

data <- diamonds

set.seed(123)
folds <- vfold_cv(diamonds, v = 5)

train_and_evaulate <- function(split) 
{
  train_data <- analysis(split)
  test_data <- assessment(split)
  
  model <- lm(price ~ ., data = train_data)
  
  predictions <- predict(model, newdata = test_data)
  
  rmse <- rmse_vec(test_data$price, predictions)
  
  return(rmse)
}

fold_rmse <- folds$splits %>%
  map_dbl(train_and_evaulate)

print("RMSE for each fold: ")
print(fold_rmse)

mean_rmse <- mean(fold_rmse)

print(paste("Mean RMSE: ", mean_rmse))

