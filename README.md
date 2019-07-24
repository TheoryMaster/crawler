# crawler

http://weather.rda.go.kr/weather/observation.jsp


농업진흥청에서 제공하는 기상 데이터를 크롤링합니다.
서버에서 쉘 스크립트의 크론탭을 사용해 주기적으로 프로그램을 실행하면 농장에서 기상데이터를 수집하는 것과 같은 효과를 낼 수 있습니다.

usr/bin/crontab

*/10 * * * * /root/publisher.py


실행에 앞서 파이썬 bs4, paho의 라이브러리가 필요합니다.

┌ pip install bs4

┕ pip install paho-mqtt

를 실행해 라이브러리를 설치해주세요
