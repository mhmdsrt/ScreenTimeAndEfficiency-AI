import time  #Zaman ölçümleri ve bekleme sürelerini hesaplamak için kullanıldı.
import win32gui #Şu anda odaklanmış (aktif) pencerenin başlığını almak için kullanıldı.


# Şu anda odaklanmış pencerenin başlığını alır
def get_focused_window_title():
    hndl = win32gui.GetForegroundWindow() #Şu anda odaklanmış olan pencerenin pencere tanıtıcısını(handle),eşsiz kimliğini döndürür.
    return win32gui.GetWindowText(hndl) # Odaklamış pencerenin tanıtıcının(handle) ismini alıyoruz.


# Odaklanmış pencerenin Eğitim uygulaması olup olmadığını kontrol etme.
def is_training_application(window_title):
    training_keywords = [
        "C#", "C++", "Java", "React", "NodeJs", "Programlama", "Veri Analizi","Ders","Konu Anlatım",
        "GitHub", "Udemy", "Word", "Visual Studio", "DevC++", "Veri Yapıları",
        "Analiz", "Visual Studio Code", "SQL", "Youtube ders videoları",
        "Anaconda", "Python", "Code", "WireShark", "İşletim Sistemleri",
        "Bilgisayar", "Donanım", "Yazılım", "CPU", "Bellek", "Yapay Zeka"
    ]
    for keyword in training_keywords: # C# daki foreach döngüsü! Dizinin içindeki elemanları sırasıyla kontrol et.
        if keyword.lower() in window_title.lower(): # Pencernin başlığını ile eğitim uygulamasını küçük harfe dönüştürüp kontrol et
            return True
    return False



data_collection_interval = 60   # Veri toplama aralığı: 1 dakika (60 saniye)
total_score = 0         #Başlangıç puanı.
work_duration = 0        # Toplam çalışma süresi (saniye cinsinden)
mola_kontrol_suresi = 3600      # Mola kontrol aralığı: 60 dakika (3600 saniye)
minute_count=1

while True:
    start_time = time.time()  # Başlangıç zamanı , şuanki zamanı(saniye cinsine çevir- time.time() ile) başlangıç zamanı olarak al.
    training_seconds = 0  # Eğitim pencerelerinde geçirilen toplam süre
    non_training_seconds = 0  # Eğitim dışı pencerelerde geçirilen toplam süre
    
    # 60 saniyelik periyotta geçen süreyi hesapla
    while time.time() - start_time < data_collection_interval: # Anlık olarak alınan zaman ile başlangıç zamanı arasındaki farkı 60 olana kadar döngü devam etsin
        active_window_title = get_focused_window_title()  # Şu anda odaklanmış pencerenin başlığını al
        if is_training_application(active_window_title): #Eğer odaklanılmış pencere eğitim uygulaması ise:
            training_seconds += 1
        else:
            non_training_seconds += 1
        
        time.sleep(1)  # Bir saniye bekle
    
    # Eğitim uygulamasında geçirilen her saniye 0.05 puan arttırsın
    total_score += training_seconds * 0.05
    
    # Eğitim dışı pencerelerde geçirilen her saniye 0.03 puan eksiltsin
    total_score -= non_training_seconds * 0.03
    
    # Negatif puanı düzelt
    if total_score < 0:
        total_score_str = f"-{abs(total_score):.5f}" #Eğer toplam puan negatif ise mutlak değerini alıp önüne - işareti koy
    else:
        total_score_str = f"{total_score:.5f}" #f sembolü süslü parantez içindekileri string ifadeye dönüştüyoruz.

    # Her dakika sonunda mesajı ve puanı yazdır
    print(f"{minute_count}. dakika sonunda: Verimlilik: {total_score_str}, Durum: ", end="") # end ifadesi ile alt satıra geçmeden string ifadenin sonuna ekleme yapıyoruz aşağıda
    if total_score >= 6.00:
        print("Verimli Çalışma")
    elif 3.00 <= total_score < 6.00:
        print("Orta Verimli Çalışma")
    else:
        print("Verimsiz Çalışma")

    # Her dakika sonunda puan ve durumu dosyaya kaydet
    with open("output.txt", "a") as file: # "a" ile dosya oluşturuyoruz,eğer dosya varsa eski verileyi koruyup üstüne yeni veri ekle!
        if total_score >= 6.00:
            file.write(f"{minute_count}. sonunda: Verimlilik: {total_score_str}, Durum: Verimli Çalışma\n")
        elif 3.00 <= total_score < 6.00:
            file.write(f"{minute_count}. sonunda: Verimlilik: {total_score_str}, Durum: Orta Verimli Çalışma\n")
        else:
            file.write(f"{minute_count}. sonunda: Verimlilik: {total_score_str}, Durum: Verimsiz Çalışma\n")
    minute_count += 1  

    # Her 60 dakikada bir mola mesajını kontrol et
    work_duration += data_collection_interval  # Toplam çalışma süresini güncelle
    if work_duration >= mola_kontrol_suresi:
        if total_score >= 120:
            print("Verimli Çalışma 15 dakika molaya çıkabilirsiniz.")
            with open("output.txt", "a") as file:
                file.write("Verimli Çalışma 20 dakika molaya çıkabilirsiniz.\n")
        else:
            print("Verimsiz Çalışma 30 dakika molaya çıkmalısınız.")
            with open("output.txt", "a") as file:
                file.write("Verimsiz Çalışma 7 dakika molaya çıkmalısınız.\n")
        work_duration = 0  # Toplam çalışma süresini sıfırla
        