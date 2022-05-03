# Optymalizacja trasy robota typu linefollower

Na ten moment w programie zaimplementowane jest:
- Wczytywanie zdjęć w formacie *.BMP
  
  Zdjęcia muszą być takie jak te, które wrzuciłem jako testowe - są wyłącznie dwukolorowe (białe i czarne), trasa musi być narysowana jako ciągła kreska idąca od dowolnego punktu na lewej krawędzi zdjęcia do dowolnego punktu na prawej krawędzi zdjęcia, dodatkowym warukniem brak krzyżowania się trasy. Trasa powinna być rysowana jako kreska o szerokości jednego pixela koloru czarnego na białym tle.

- Przekształcenie zdjęcia na wektor z trasą

  Tak właściwie są to dwa wektory, stanowiące wpółrzędną X oraz Y. Trasa jest reprezentowana jako ciąg następujących po sobie punktów w trasie.
  
- Wprowadzenie nieregularności odpowiadających symulacji trasy odczytanej przez robota przy pierwszym przejeździe
  
  Wektor z trasą stanowi docelową drogę po której powinien przejechać robot. W trakcie jazdy, robot odczytuje tą trasę, jednak odczytuje ją nie w idealnej postaci tylko z pewnymi zakłóceniami, błędami i oscylacjami. Dlatego trasa docelowa jest zmieniana na trasę z zakłóceniami, oraz ta nowo powstała trasa stanowi drogę jaką odczytał robot i ta trasa właśnie będzie dalej uznana za bazę do obliczeń i optymalizacji.

- Dodałem obliczenia związane z generowaniem trasy w formie drogi ograniczonej od dołu (albo jak kto woli od lewej) i od góry (albo od prawej)

  Działa to tak, że tworzona jest obdwódka trasy, którą odczytał robot w określonej odległości od odczytanej trasy. W tej przestrzeni będzie miała się znajdować przyszła optymalna (albo i nie XD) trasa robota

- dodałem też filtrowanie trasy

  Filtrowanie, a właściwie uśrednianie pozwala na pozbycie się poszarpanych krawędzie przy tworzeniu ograniczeń trasy

- Ogarnięte jest !!!
