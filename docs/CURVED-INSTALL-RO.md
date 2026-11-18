# Tema Curved: cum o pui pe mașină

Tema **Curved** e o temă nouă în Cluster Themes (fork după bimmer-lab/apps). Arată ca clusterele BMW noi (iDrive 8 / 8.5, Curved Display) și merge pe iDrive 7 (MGU).

## Ce trebuie să ai deja

- **MGU Store** instalat pe unitate
- **cluster-render**, din sursa `robertnisipeanu/idrive-apps`. Dacă ai Waze on cluster, îl ai deja.

## 1. Pune proiectul pe GitHub

1. Pe github.com fă un repository nou, de exemplu `bmw-cluster-curved`. Poate fi public sau privat, dar Store-ul citește cel mai simplu unul public.
2. Din folderul acesta rulează:

   ```sh
   git remote set-url origin https://github.com/<userul-tau>/bmw-cluster-curved.git
   git push -u origin main
   ```

## 2. Instalează din MGU Store

1. Dacă ai deja **Cluster Themes** de la sursa `bimmer-lab/apps`, dezinstalează-l întâi. Store-ul actualizează o aplicație doar din sursa de unde a venit. Altfel o instalează pe a ta separat, cu id-ul `cluster_themes2`.
2. În Store mergi la **Settings → Add source** și scrie `<userul-tau>/bmw-cluster-curved`.
3. Instalează **Cluster Themes**. Store-ul construiește aplicația direct pe mașină din cod. SDK-ul BMW îl ia de pe unitatea ta, nu e în repository.
4. Deschide **Cluster Themes** din meniul de aplicații. La **Themes** alege **Curved**.
   - **Settings → Units** pune pe km/h, °C, bar.
   - **Redline** pune turația maximă a motorului tău.
   - Dacă vrei ca tema să rămână Curved în toate modurile, setează **In Comfort / In Sport / In Eco Pro** pe Curved. Culorile se schimbă singure după mod.

## Test pe Mac, fără mașină

```sh
node bench/server.js cluster_themes     # apoi deschide http://localhost:8078
```

Ai nevoie de `node` și `python3`. La Themes alegi Curved. Cu butoanele COMFORT / SPORT / SPORT+ / ECO PRO vezi culorile, iar cu sliderele schimbi viteza și turația.

## Modificări

Geometria temei e în `tools/gen_curved.py`. Modifici acolo și rulezi `python3 tools/gen_curved.py`, nu modifici JSON-ul de mână. Desenul e shader-ul `cdash` din `shared/shaders.js`, iar culorile pe moduri sunt în `shared/hud_themes.js` (tema `curved`, `modes`).

## Atenție

- Tema a fost testată doar pe bench, nu încă pe mașină. Prima dată verifică dacă se vede tot pe cluster.
- Aplicația doar citește date (viteză, turație, temperaturi). Nu trimite comenzi la module.
- Dacă vrei să revii la clusterul BMW: în aplicație alegi **Off (BMW's own cluster)**, sau o dezinstalezi din Store.
