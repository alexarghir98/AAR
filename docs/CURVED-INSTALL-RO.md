# AAR Cluster Themes: cum o pui pe mașină

**AAR Cluster Themes** e un fork după Cluster Themes de la bimmer-lab, dar are id-ul lui propriu: `aar_cluster_themes`. Așa poate sta pe unitate lângă aplicația bimmer-lab fără conflict. Tema implicită e **Curved**, în stilul clusterelor BMW noi (iDrive 8 / 8.5). Culorile se schimbă după modul de condus.

## Ce trebuie să ai deja

- **MGU Store** instalat pe unitate
- **cluster-render**, din sursa `robertnisipeanu/idrive-apps`. Dacă ai Waze on cluster, îl ai deja.

## 1. Pune proiectul pe GitHub

1. Repository-ul e `alexarghir98/AAR` pe GitHub, **public**, ca Store-ul să-l poată citi. Dacă trebuie făcut din nou: unul gol, fără README și fără licență.
2. Din Terminal, în folderul proiectului:

   ```sh
   cd ~/Documents/"Proiecte Coding BMW"/"AAR Cluster Themes"
   git remote add origin https://github.com/alexarghir98/AAR.git
   git push -u origin main
   ```

   Dacă GitHub cere parolă, folosește un Personal Access Token, nu parola contului. Sau rulează `gh auth login` dacă ai GitHub CLI.

## 2. Instalează din MGU Store

1. În Store mergi la **Settings → Add source** și scrie `alexarghir98/AAR`.
2. Instalează **AAR Cluster Themes**. Store-ul construiește aplicația direct pe mașină. SDK-ul BMW îl ia de pe unitatea ta, nu e în repository.
3. Deschide **AAR Cluster Themes** din meniul de aplicații:
   - **Lame** e deja aleasă pentru Comfort, **Bumerang** pentru Sport și **Curved** pentru Eco Pro. **Artifact** și **Apex** se aleg din listă. La Artifact, setarea **Artifact: the middle** alege ce e în mijloc: mașina cu roțile, cele patru valori (boost, ulei, răcire, combustibil) sau nimic.
   - **Show Waze map inside the theme** e deja pornit. Ca să apară harta în panoul din mijloc: ai instalat **Maps on cluster** (fostul Waze on Cluster), pornești navigația pe telefon, iar în setările mașinii pui **Instrument cluster > Central display area** pe **Map view**.
   - Unitățile sunt deja km/h, °C și bar.
   - Pune **Redline** la turația maximă a motorului tău.
   - Ceasul e deja pe 24 de ore, cu fusul orar Eastern Europe (România, cu ora de vară inclusă).
4. Dacă ai instalat și Cluster Themes de la bimmer-lab, pune-l pe **Off (BMW's own cluster)**. Folosește o singură aplicație de cluster odată.

## Test pe Mac, fără mașină

```sh
node bench/server.js      # apoi deschide http://localhost:8078
```

Ai nevoie de `node` și `python3`. Cu butoanele COMFORT / SPORT / SPORT+ / ECO PRO vezi culorile, iar cu sliderele schimbi viteza și turația.

## Modificări

- **Geometria temei** e în `tools/gen_curved.py`. Modifici acolo și rulezi `python3 tools/gen_curved.py`, nu modifici JSON-ul de mână.
- **Desenul** e shader-ul `cdash` din `shared/shaders.js`.
- **Culorile pe moduri** sunt în `shared/hud_themes.js`, la tema `curved`, în `modes`.
- **O versiune nouă:** crești `version` în `apps/aar_cluster_themes/app.json`, faci commit și `git push`. Store-ul îți oferă actualizarea.

## Atenție

- Tema a fost testată doar pe bench, nu încă pe mașină. Prima dată verifică dacă se vede tot pe cluster, mai ales colțurile de sus.
- Aplicația doar citește date (viteză, turație, temperaturi). Nu trimite comenzi la module.
- Dacă vrei înapoi clusterul BMW: în aplicație alegi **Off (BMW's own cluster)**, sau o dezinstalezi din Store.
