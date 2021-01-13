# BingeWatch

Proiect realizat pentru materia Python, din cadrul facultatii de Informatica "Alexandru Ioan Cuza" Iasi

Profesor coordonator: Postolachi Nicolae

Nume proiect: Binge Watch

Enunt:  Creați un tool care monitorizeaza serialele favorite. Într-o bază de date se va păstra numele
serialului, link către IMDB, ultimul episod vizionat, data ultimei vizionari, un scor ( setat de
user pentru serial ). Cand va fi rulat tool-ul va lista ce seriale noi apărute nu au fost vizionate
în funcție de scorul serialului. Tool-ul va cauta si traler-uri pe youtube sau upload-uri care au
legatura cu un anumit episod dintr-un serial și va oferi o lista a acestora (respectiv notificari
dacă apar altele).

API-uri folosite: TMDB, YouTube Search

Limbaj de programare: Python



Pentru a rula proiectul e suficient sa rulati comanda python main.py in terminal.
Dupa rulare se va deschide o fereastra full screen, unde vor aparea 15 postere cu serialele din trending din ultima zi. Pe partea stanga se vor regasi 5 butoane:

- Search: user-ul va putea introduce un string query, iar aplicatia va returna serialele relevante de pe TMDB.

- Trending: buton care practic duce inapoi in pagina initiala (home page-ul) cu cele 15 seriale din tranding din ultima zi.

-Favorites: -aici vor fi listate toate serialele adaugate de utilizator la favorite.
            -user-ul va putea seta un scor pentru fiecare serial in parte si va putea vedea la ce episod a ramas ultima data si cand a vizionat episodul respectiv.
            -user-ul va putea pune pe snooze anumite seriale pe care nu mai doreste sa le urmareasca pentru momentan.

-Collection: va lista toate serialele puse pe snooze de catre user si serialele terminate de acesta.

-Exit: exit din aplicatie.
            
  
