# ASK-Zadanie_2
Projekt stworzony w Pythonie 3.6 przy pomocy frameworka PyQt5.
Wykorzystując dowolny język programowania dla komputerów w standardzie PC napisać aplikację stanowiącą model
programowego symulatora mikroprocesora. Program powinien mieć przyjazny interfejs użytkownika graficzny lub znakowy do
uznania przez autorów.
Umożliwia on symulację realizacji dziesięciu funkcji przerwań procesora oferowanych przez moduł BIOS (można też użyć przerwań DOS).
Wybrane funkcje powinny być różnorodne, dotyczyć różnych zasobów komputera PC np. zegara RTC, klawiatury, monitora
ekranowego, pamięci dyskowej. Aplikacja powinna realizować dwa wątki:

* dydaktyczny – prezentujący w wyczerpujący sposób opis działania funkcji oraz sposób jej programowego
wykorzystania obejmujący sposób wywoływania oraz przekazywania parametrów oraz wyjaśniający znaczenie tych
parametrów.
* demonstracyjny – prezentujący wybrane funkcje w działaniu.

W celu realizacji wątku demonstracyjnego do zbioru nazw dotychczas realizowanych komend (MOV, ADD, SUB) należy dodać
INTxx, INTyy, INTzz, ….. , gdzie xx, yy, zz, …. oznaczają numery wybranych przerwań. W programie należy utworzyć STOS
służący do przechowywania zawartości rejestrów procesora na czas wykonywania przerwań. (Szczegółowy opis mechanizmu
wywoływania przerwań procesora zostanie podany przez prowadzącego w odrębnym załączniku.)
## Autor : Bartosz Żbikowski
