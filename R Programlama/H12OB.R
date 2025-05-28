keras::install_keras()
library(keras)
library(dplyr)
library(ggplot2)

mnist <- dataset_mnist()

train_images <- mnist$train$x
train_labels <- mnist$train$y
test_images <- mnist$test$x
test_labels <- mnist$test$y

train_images <- train_images / 255
test_images <- test_images / 255

train_images <- array_reshape(train_images, c(nrow(train_images), 784))
test_images <- array_reshape(test_images, c(nrow(test_images), 784))

train_labels <- to_categorical(train_labels, 10)
test_labels <- to_categorical(test_labels, 10)

model <- keras_model_sequential() %>%
  layer_dense(units = 128, activation = "relu", input_shape = 784) %>%
  layer_dense(units = 64, activation = "relu") %>%
  layer_dense(units = 10, activation = "softmax") %>%
  compile(loss = "categorical_crossentropy", optimizer = optimizer_adam(), 
          metrics = c("accuracy"))

summary(model)

history <- model %>%
  fit(x = train_images, y = train_labels, epochs = 20, batch_size = 128, 
      validation_split = 0.2, verbose = FALSE)

plot(history)

result <- model %>%
  evaluate(test_images, test_labels)
