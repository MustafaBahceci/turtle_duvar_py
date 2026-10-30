# Turtle Duvar Kontrol Projesi

## Proje Hakkında
Bu projede Turtlesim ekranındaki kaplumbağanın duvarlara çarpmasını önleyen bir sistem geliştirilmiştir.

Kaplumbağa hareket ederken duvara yaklaştığında bulunduğu konuma bakılır. Daha sonra ekranın ortasına doğru dönmesi sağlanır. Yönünü düzelttikten sonra tekrar ilerlemeye devam eder.

Kaplumbağanın konumu ve yön değiştirdiği zamanlar terminalde gösterilir.

## Kullanılan Teknolojiler
- Ubuntu 22.04
- ROS 2 Humble
- Python
- Turtlesim

## Çalıştırma

İlk terminalde:

```bash
ros2 run turtlesim turtlesim_node
```

İkinci terminalde:

```bash
ros2 run turtle_duvar_py duvar_kontrol
```

## Geliştirici
Mustafa Bahçeci# turtle_duvar_py
