import asyncio
import aiohttp
import time
import concurrent.futures

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

        # İsteklerin tamamlanmasını bekleyin
        await asyncio.gather(*tasks)

# Asenkron istek gönderme işlevi
async def send_request(session):
    start_time = time.time()  # İstek gönderme zamanını al

    async with session.get(url) as response:
        response_time = time.time() - start_time  # İstek yanıtının alındığı süreyi hesaplayın
        gecen_sureler.append((start_time, response_time))  # İstek süresini listeye ekleyin

# Asenkron yükleme testini başlatın
async def run_load_test():
    loop = asyncio.get_running_loop()
    start_time = time.time()  # Yükleme testinin başlangıç zamanını al
    end_time = start_time + duration  # Yükleme testinin bitiş zamanını al
    while time.time() < end_time:
        await load_test()

def run_in_thread():
    asyncio.run(run_load_test())

# Aynı anda 10 thread'de yükleme testini başlatın
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for _ in range(10):
        executor.submit(run_in_thread)

# # Elde edilen istek sürelerini yazdırın
for i, response_time in enumerate(gecen_sureler, start=1):
    request_number = i
    elapsed_time = response_time[1]
    print(f"Istek {request_number}: {elapsed_time:.2f} saniye")