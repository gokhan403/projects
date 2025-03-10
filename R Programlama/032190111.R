# veri seti yükleme
data <- read_csv("C:/Users/User/Desktop/year_lahore_weather_data.csv")

# ortalama sıcaklığı en yüksek olan ayın bulunması
data <- data %>%
  mutate(Mean_Temperature = Min_Temperature + Max_Temperature / 2) %>%
  mutate(Month = format(as.Date(Date), "%Y-%m"))

monthly_means <- data %>%
  group_by(Month) %>%
  summarize(Monthly_Mean_Temperature = mean(Mean_Temperature, na.rm=TRUE))

print(monthly_means)

max_month <- monthly_means %>%
  filter(Monthly_Mean_Temperature == max(Monthly_Mean_Temperature))

G1 <- max_month$Month
max_month_temp <- max_month$Monthly_Mean_Temperature

print(paste("The month with the highest mean temperature is", G1, "with a temperature of", max_month_temp))

# sıfırın altında sıcaklığa sahip günlerin bulunması
G2 <- data %>%
  filter(Min_Temperature < 0)

print(G2) # 0 altında sıcaklık olan gün yok

# sıcaklıkların fahrenheit cinsinden saklanması

G3_sicaklikFahrenheit <- data %>%
  mutate(Min_Temperature = Min_Temperature * 9/5 + 32,
         Max_Temperature = Max_Temperature * 9/5 + 32)

print(G3_sicaklikFahrenheit)

# sıcaklığın 25 derecenin üzerinde olduğu gün sayısı

daysover25 <- data %>%
  filter(Max_Temperature > 25)

G4Bonus <- nrow(daysover25)

print(G4Bonus)
