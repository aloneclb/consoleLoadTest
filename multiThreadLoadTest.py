import asyncio
import aiohttp
import time
import concurrent.futures

# Yükleme testi için gereken parametreler
url = "https://denemekoleji.okulsepeti.com.tr/sinif-paket-detayi/59655/"  # İstek göndermek istediğiniz URL'yi buraya yerleştirin
total_requests = 30
# 10 saniye cinsinden süre
duration = 10

# İstek başına geçen süreleri saklamak için boş bir liste oluşturun
response_times = []

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
    start_time = time.time()  # İstek gönderme zamanını kaydedin

    async with session.get(url) as response:
        response_time = time.time() - start_time  # İstek yanıtının alındığı süreyi hesaplayın
        response_times.append((start_time, response_time))  # İstek süresini listeye ekleyin

# Asenkron yükleme testini başlatın
async def run_load_test():
    loop = asyncio.get_running_loop()
    start_time = time.time()  # Yükleme testinin başlangıç zamanını kaydedin
    end_time = start_time + duration  # Yükleme testinin bitiş zamanını hesaplayın
    while time.time() < end_time:
        await load_test()

# Yükleme testini aynı anda 10 thread'de gerçekleştirmek için yardımcı işlev
def run_in_thread():
    asyncio.run(run_load_test())

# Aynı anda 10 thread'de yükleme testini başlatın
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for _ in range(10):
        executor.submit(run_in_thread)

# # Elde edilen istek sürelerini yazdırın
for i, response_time in enumerate(response_times, start=1):
    request_number = i
    elapsed_time = response_time[1]
    print(f"Istek {request_number}: {elapsed_time:.2f} saniye")