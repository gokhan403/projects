# uygulama 1

data1 <- left_join(flights, planes, by = "tailnum")
data1 %>% filter(air_time == max(air_time, na.rm = T)) %>%
  select(year.y, manufacturer, model)

data2 <- left_join(weather, flights, by = c("origin", "year", "month", "day", "hour"))
data2 %>% select(air_time, temp, wind_speed, humid) %>%
correlate()

data3 <- right_join(airlines, flights, by = "carrier")
data3 %>% filter(dep_delay > 0) %>% na.omit() %>% group_by(name) %>% summarise(mean = mean(dep_delay), median = median(dep_delay))

flights %>% filter(dep_delay > 0) %>% summarise(mean = mean(dep_delay))

# uygulama 2

t <- table(AwardsPlayers$playerID) %>% as.data.frame()
names(t) <- c("playerID", "num.of.aw")
data1 <- People %>% left_join(t, by = "playerID")
data1 %>% filter(num.of.aw == max(num.of.aw, na.rm = T)) %>%
  select(nameFirst, nameLast)

People %>% mutate(BMI = weight / (height^2) * 703) %>% filter(BMI >= 25 & BMI < 29.9) %>% nrow()

data2 <- Salaries %>% left_join(t, by = "playerID")
which.max(data2$salary) == which.max(data2$num.of.aw)
slice(data2, which.max(data2$salary))
slice(data2, which.max(data2$num.of.aw))

table(AwardsPlayers$awardID) %>% as.data.frame() %>% arrange(desc(Freq))

# uyulama 3

diamonds %>% mutate(t = x^2 - sqrt(y) + (1/z)) %>% filter(t == min(t)) %>% select(depth)

diamonds %>% mutate(discount = case_when(
  cut == "Fair" ~ price * 0.01,
  cut == "Good" ~ price * 0.02,
  cut == "Very Good" ~ price * 0.025,
  cut == "Premium" ~ price * 0.03,
  cut == "Ideal" ~ price * 0.03
), new.price = price - discount) %>% filter(color == "E" & clarity == "SI2" & new.price == min(new.price))

cl <- diamonds$clarity %>% as.factor()
cl %>% levels()
cl %>% nlevels()

diamonds %>% group_by(cut) %>% summarise(mean.pr = mean(price))
