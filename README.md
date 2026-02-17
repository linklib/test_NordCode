# test_NordCode
Тестовая задача


# Виртуальное окружение
pip install uv
uv init
uv venv --python 3.8
source .venv/bin/activate

# Зависимости 
pip install -r requirements.txt

# Запуск WireMock (необходимо скачать) и приложения
java -jar wiremock.jar --port 8888  

java -jar -Dsecret=qazWSXedc -Dmock=http://localhost:8888/ internal-0.0.1-SNAPSHOT.jar

# Запуск тестов с отчетом (должен быть установлен Allure CLI)
pytest test_app.py --alluredir=allure-results  

allure serve allure-results
