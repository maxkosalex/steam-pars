# steam-pars
Парсинг Предметов на торговой площадке стим.

•Данный код парсит до 10 предметов в час.

•Для перехода на другие страницы и изменение кол-ва предметов на торговой площадки steam, необходимо изменить параметр "params" и ключи, под названием:"start";"count".  

•Для того чтобы воспользоваться кодом необходимо установить следующие библиотеки для вашей среды:

$ python -m pip install requests

$ python -m pip install beautifulsoup4

$ python -m pip install lxml

•Далее, нужно задать cookies и headers.
Если вы хотите запустить программу без этих параметров, во всех методах "GET" уберите параметры cookies и headers.




