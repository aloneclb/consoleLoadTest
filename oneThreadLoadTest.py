import asyncio
import aiohttp
import time
import datetime

# parametreler
url = "https://denemekoleji.panelkitap.com/sinif-paket-detayi/59655/" 
total_requests = 300
duration = 10

gecen_sureler = [] # gecen süreler

# Session bilgisi için headers ayarlayın
headers = {"Cookie": "session=sessionid=hijmo50ud2m6y4h7vtkt83a5blz81rqx;"}

# Asenkron yükleme testi işlevi
async def load_test():
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for _ in range(total_requests):
            task = asyncio.ensure_future(send_request(session))
            tasks.append(task)

        # tüm taskların tamamlanmasını bekle
        await asyncio.gather(*tasks)

# Asenkron istek gönderme işlevi
async def send_request(session):
    start_time = time.time()  # İstek gönderme zamanı

    async with session.get(url) as response:
        response_time = time.time() - start_time  # İstek yanıtının alındığı süreyi hesaplayın
        start_datetime = datetime.datetime.fromtimestamp(start_time)
        formatted_time = start_datetime.strftime("%H:%M:%S")
        gecen_sureler.append((start_time, response_time, formatted_time))  # İstek süresini listeye ekleyin

# yükleme testini başlatın
loop = asyncio.get_event_loop()
start_time = time.time()  # Yükleme testinin başlangıç zamanı
end_time = start_time + duration  # Yükleme testinin bitiş zamanı

while time.time() < end_time:
    loop.run_until_complete(load_test())

# süreleri yazdır
for i, response_time in enumerate(gecen_sureler, start=1):
    request_number = i
    elapsed_time = response_time[1]
    print(f"Istek {request_number}: {elapsed_time:.2f} saniye, istek {response_time[2]} de başladı.")














# import matplotlib.pyplot as plt


# request_numbers, gecen_sureler = zip(*gecen_sureler)
# plt.plot(request_numbers, gecen_sureler, marker='o', linestyle='None')
# plt.xlabel('Istek')
# plt.ylabel('(saniye)')
# plt.title('GET İstekleri Geçen Süreleri')
# plt.xticks(request_numbers, [f"{n}" for n in request_numbers])

# plt.show()