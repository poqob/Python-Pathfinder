# 🤖 Roomba Pathfinding AI Simulator

Bu proje, Python ve Pygame kullanılarak geliştirilmiş kapsamlı bir **Otonom Yol Bulma (Pathfinding)** simülasyonudur. Proje, **A\***, **RRT** ve **RRT\*** gibi popüler algoritmaları görselleştirerek, statik bir harita üzerinde bir robotun (Roomba) hedefe ulaşmasını simüle eder.

## 🌟 Özellikler

* **Çoklu Algoritma Desteği:** A* (A-Star), RRT ve RRT* algoritmaları arasında anlık geçiş.
* **Görüntü İşleme Tabanlı Harita:** Herhangi bir siyah-beyaz resmi (`map.png`) otomatik olarak engeller matrisine dönüştürür.
* **Dahili Harita Editörü:** Kendi haritalarınızı çizip kaydedebileceğiniz entegre araç.
* **Geçmiş (History) Sistemi:** Çizilen rotaları JSON formatında kaydeder ve görsel bir arayüz ile tekrar oynatmanızı sağlar.
* **Dinamik UI:** Yan panel menüsü ile geçmiş rotalar arasında gezinme ve detayları görme imkanı.

---

## 🚀 Kurulum

Projeyi çalıştırmak için Python 3.x ve gerekli kütüphanelerin yüklü olması gerekir.

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/poqob/roomba-pathfinder.git](https://github.com/poqob/roomba-pathfinder.git)
    cd roomba-pathfinder
    ```

2.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamayı Başlatın:**
    ```bash
    python main.py
    ```

---

## 🎮 Kullanım ve Kontroller

Simülasyon açıldığında varsayılan olarak A* algoritması seçilidir.

| Tuş | Eylem | Açıklama |
| :--- | :--- | :--- |
| **Sol Tık** | Hedef Belirleme | Hedef noktayı seçer ve yolu hesaplar. |
| **1** | A* Modu | A* algoritmasına geçer (Grid tabanlı, en kısa yol). |
| **2** | RRT Modu | RRT algoritmasına geçer (Rastgele ağaç, hızlı keşif). |
| **3** | RRT* Modu | RRT* algoritmasına geçer (Optimize edilmiş ağaç). |
| **H** | Geçmiş Paneli | Geçmiş (History) panelini açar/kapatır. |
| **Sol/Sağ Ok**| Gezinme | Geçmiş kayıtları arasında gezilir (History modu açıkken). |

---

## 🧠 Algoritmalar

### 1. A* (A-Star) Algoritması
Grid (ızgara) tabanlı çalışır. Başlangıçtan hedefe olan en kısa yolu garanti eder. Kare kare ilerler ve engellerin etrafından en optimum yolu çizer.

![A* Algoritması](presentation/astar_demo.png)

### 2. RRT (Rapidly-exploring Random Tree)
Örnekleme (sampling) tabanlıdır. Rastgele noktalar seçerek hızla bir ağaç oluşturur. Yolu bulur ancak yol genellikle zikzaklıdır ve en kısa yol garantisi yoktur. Geniş alanlarda hızlı sonuç verir.

![RRT Algoritması](presentation/rrt_demo.png)

### 3. RRT* (RRT Star)
RRT'nin optimize edilmiş versiyonudur. Yeni eklenen düğümler, komşularını kontrol ederek yolu kısaltacak bir bağlantı (rewiring) arar. Süre arttıkça yol düzleşir ve optimale yaklaşır.

![RRT* Algoritması](presentation/rrt_star_demo.png)

---

## 🛠 Araçlar

### 🗺️ Harita Editörü
Kendi seviyelerinizi oluşturmak için `map_creator.py` dosyasını çalıştırın.
* **Sol Tık:** Duvar Çizer.
* **Sağ Tık:** Siler.
* **Kaydet:** `assets/map.png` olarak kaydeder.

![Harita Editörü](presentation/map_editor.png)

### 📜 Geçmiş ve Log Sistemi
Her başarılı rota hesaplaması `history.json` dosyasına kaydedilir. **'H'** tuşuna basarak yan paneli açabilir ve önceki denemelerinizi, hangi algoritmanın kullanıldığını ve zaman damgasını görebilirsiniz.

![Geçmiş Paneli](presentation/history_ui.png)

---

## 📂 Proje Yapısı

```text
../
├── assets/                 # Görsel materyaller ve haritalar
│   ├── map.png
│   ├── roomba.png
│   └── ...
├── src/                    # Kaynak kodlar
│   ├── history_manager.py  # JSON okuma/yazma işlemleri
│   ├── pathfinder_manager.py # Algoritma yönetim merkezi
│   ├── romba_sprite.py     # Robot hareket fiziği
│   ├── rrt_algorithms.py   # RRT ve RRT* implementasyonu
│   ├── ui_manager.py       # Arayüz çizim işlemleri
│   └── utils.py            # Görüntü işleme araçları
├── presentation/           # README ekran görüntüleri
│   ├── demo.gif
│   ├── astar_demo.png
│   ├── rrt_demo.png
│   └── ...
├── history.json            # Kayıt dosyası
├── main.py                 # Ana çalışma dosyası
├── map_creator.py          # Harita oluşturucu
└── requirements.txt        # Kütüphane gereksinimleri