<h2>Лабораторна робота №4 студента групи КМ-81 Волинця Сергія</h2>

<p>Перед виконанням програми додайте в кореневу папку файли зі ЗНО за 
2019-2020 роки за наступною структурою:</p>

<ol>
  <li>OpenDataZNO2019/Odata2019FileUTF.csv</li>
  <li>OpenDataZNO2020/Odata2020FileUTF.csv</li>
</ol>

<h3>Запуск програми</h3>
<p>Для всіх варіантів ОС треба виконати:</p>

```
docker-compose up
```

Далі запуск відрізняється залежно від системи. GNU/Linux Для того щоб запустити:
```
python3 -m pip install virtualenv
python3 -m venv env
source env/bin/activate
source .env
python3 -m pip install -r requirements.txt
python3 main.py
```

Windows OS Треба послідовно виконати наступні дії в окремому терміналі:
```
python -m pip install --user virtualenv
pyython -m venv env
.\env\Scripts\activate
python -m pip install -r requirements.txt
source .env
python main.py
```
<p>python це execute команда python3, можливо у вас вона відрізняється
Також можливо, що у Вас замість python може бути команда py. За більш детальною
інформацією звертайтесь до документації пайтона по вашій ОC.</p>

<h3>Легенда до query_result.csv</h3>
Файл містить результати порівняння найгірших балів по українській мові у кожному регіоні за 2019-2020
роки.
