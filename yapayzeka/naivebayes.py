import re
import math
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Eğitim ve test verisini programa yükelemek için
# erişilecek dosya adresleri
culture_arts = "C:\\Users\\User\\Desktop\\training data\\culture_arts.txt"
health = "C:\\Users\\User\\Desktop\\training data\\health.txt"
politics = "C:\\Users\\User\\Desktop\\training data\\politics.txt"
sports = "C:\\Users\\User\\Desktop\\training data\\sports.txt"
test = "C:\\Users\\User\\Desktop\\testing data\\testData.txt"


# Eğitim verisini istenmeyen kelimelerden, sayılardan ve noktalama işaretlerinden
# arındıracak fonksiyon
def remove_words_and_punctuations(text):
    words_to_remove = ["the", "all", "off", "of", "or", "but", "and", "through", "though", "although",
                       "then", "not", "in", "out", "on", "about", "too", "yet", "nor", "either", "neither",
                       "so", "therefore", "moreover", "furthermore", "however", "also", "hence", "to", "at",
                       "from", "with", "by", "as", "this", "that", "these", "those", "between", "only",
                       "for", "a", "an", "into", "non", "no", "yes", "up", "down", "even", "ever", "am",
                       "is", "are", "was", "were", "will", "i", "he", "she", "we", "they", "it", "you", "my",
                       "its", "his", "her", "their", "our", "your", "have", "has", "be", "been", "do", "does",
                       "not", "thus", "would", "could", "can", "until", "him", "me", "them", "us", "if",
                       "unless", "who", "when", "where", "which", "whether", "what", "why", "whoever",
                       "whatever", "whom", "had", "away", "did", "there", "whose", "more", "most", "co",
                       "re", "la", "le", "any", "other", "each", "much", "than", "some", "every", "thing",
                       "else", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                       ",", ".", ";", ":", "-", "_", "“", "”", "‘", "’", "\n"]

    numbers_to_remove = '0123456789'

    translation_table = str.maketrans('', '', numbers_to_remove)

    text_without_punctuation = re.sub(r'[^\w\s]', '', text)

    words = text_without_punctuation.split()
    words = [word.lower() for word in words if word.lower() not in words_to_remove]

    ret = ' '.join(words).translate(translation_table)

    return ret


# Arındırılmış eğitim verisini kelime kelime ayırarak sözlüğe eklenecek hale getiren fonksiyon
def processed_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        clear_text = remove_words_and_punctuations(file_content)
        text_list = clear_text.split()

    return text_list


# Arındırılmış ve ayrıştırılmış eğitim verisi tekrarlayan kelimelerden de arındırılarak
# eşsiz bir sözlük oluşturulur
def create_dictionary(data1, data2, data3, data4):
    dictionary = set(data1 + data2 + data3 + data4)
    return dictionary


# Oluşturduğumuz eşlik sözlük içerisinde bulunan her kelime sırayla her kategoriye ait eğitim verisiyle
# karşılaştırılarak verilen kategoride verilen kelimenin geçme olasılığı (koşullu olasılıklar) hesaplanır
def conditional_probability(dictionary, data):
    # Her elemanı sıfır olan sözlük büyüklüğünde bir liste oluşturulur ve
    # sözlükteki kelimenin verilen kategoride kaç kez geçtiği sayılır ve saklanır
    initial_value = 0
    size = len(dictionary)
    word_count = [initial_value] * size
    h = 0

    for i in dictionary:
        word_count[h] += 1
        for j in data:
            if i == j:
                word_count[h] += 1

        h += 1

    # Verilen kategoride geçen kelimelerin toplam geçtikleri sayı toplanarak
    # toplam kelime sayısı bulunur ve her kelimenin geçme sayısı toplam kelime
    # sayısına bölünerek her kelimenin verilen kategori ile koşullu olasılıkları hesaplanır
    word_sum = 0
    for i in word_count:
        word_sum += i

    probabilities = dict()
    g = 0
    for i in dictionary:
        probability = word_count[g] / word_sum
        probabilities[i] = probability
        g += 1

    return probabilities


# Kategori tahmini yapılacak test verisi metin metin ayrılır
def adjust_test_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        texts = content.split('#')

    return texts


# Eğitim verisinden elde edilen öncül ve koşullu olasılıklar ve sözlük ile test verisi
# karşılaştırılarak test verisinin hangi kategoriye ait olduğu tahmin edilir
def guess_category(test_data, dictionary, init_prob, culture_arts_prob, health_prob, politics_prob, sports_prob):
    # Öncül olasılılar
    classification = {"Culture Arts": math.log10(init_prob['culture_arts']),
                      "Health": math.log10(init_prob['health']),
                      "Politics": math.log10(init_prob['politics']),
                      "Sports": math.log10(init_prob['sports'])}

    # Test verisindeki kelimeler sözlükteki kelime ile eşleştiği takdirde
    # her kategorinin koşullu olasılıkları test verisinin o kategoriye ait
    # olma olasılığını verecek şekilde hesaplama yapılır
    for i in test_data:
        for j in dictionary:
            if i == j:
                classification['Culture Arts'] += culture_arts_prob[i]
                classification['Health'] += health_prob[i]
                classification['Politics'] += politics_prob[i]
                classification['Sports'] += sports_prob[i]

    # En yüksek olasılık seçilir ve en yüksek olasılığın geldiği kategori
    # test verisinin tahmini olarak atanır
    values = [classification['Culture Arts'], classification['Health'],
              classification['Politics'], classification['Sports']]
    max_prob = max(values)

    return {k for k in classification if classification[k] == max_prob}


# Programı çalıştıran main
if __name__ == "__main__":
    # Her kategorinin eğitim verisi ayrılır
    training_data1 = processed_text(culture_arts)
    training_data2 = processed_text(health)
    training_data3 = processed_text(politics)
    training_data4 = processed_text(sports)

    # Öncül olasılıklar
    categories = {"culture_arts": 0.25, "health": 0.25, "politics": 0.25, "sports": 0.25}

    # Eğitim verisi ile eşsiz sözlük oluşur
    unique_dict = create_dictionary(training_data1, training_data2, training_data3, training_data4)

    # Koşullu olasılıklar
    culture_arts_dict = conditional_probability(unique_dict, training_data1)
    health_dict = conditional_probability(unique_dict, training_data2)
    politics_dict = conditional_probability(unique_dict, training_data3)
    sports_dict = conditional_probability(unique_dict, training_data4)

    # Test verisi metin metin ayrılır
    test_list = adjust_test_data(test)

    # 12 metin için tahmin yapılır
    x = 1
    while x < 13:
        test_text = remove_words_and_punctuations(test_list[x]).split()
        guess = guess_category(test_text, unique_dict, categories,
                               culture_arts_dict, health_dict, politics_dict, sports_dict)
        print(f"{x}. metnin kategori tahmini: {guess}")
        x += 1

    # Sınıflandırma sonunda karmaşa matrisi çizilir
    y_true = ["Culture Arts", "Culture Arts", "Culture Arts", "Politics", "Politics", "Politics",
              "Sports", "Sports", "Sports", "Health", "Health", "Health"]
    y_pred = ["Culture Arts", "Culture Arts", "Sports", "Politics", "Politics", "Politics",
              "Sports", "Sports", "Sports", "Health", "Health", "Health"]

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Culture Arts", "Health", "Politics", "Sports"],
                yticklabels=["Culture Arts", "Health", "Politics", "Sports"])
    plt.xlabel("Tahmin")
    plt.ylabel("Gerçek")
    plt.title("Karmaşa Matrisi")
    plt.show()
