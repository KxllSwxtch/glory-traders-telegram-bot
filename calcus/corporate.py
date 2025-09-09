import requests

cookies = {
    'PHPSESSID': '4ughb6p2v438t06g0ajp5vf9a9',
    '_ym_uid': '1757376960886759190',
    '_ym_d': '1757376960',
    '_ym_isad': '1',
    'fid': '3a6aa8a1-b495-4c6a-933d-8860f61a6ca6',
    '_ac_oid': 'bf0966cc65751955b3a5bc2b645d8ed9%3A1757380561489',
    'accept_cookie': '1',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en,ru;q=0.9,en-CA;q=0.8,la;q=0.7,fr;q=0.6,ko;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryBJoNLh01XkNfd7PA',
    'Origin': 'https://calcus.ru',
    'Referer': 'https://calcus.ru/rastamozhka-auto',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'PHPSESSID=4ughb6p2v438t06g0ajp5vf9a9; _ym_uid=1757376960886759190; _ym_d=1757376960; _ym_isad=1; fid=3a6aa8a1-b495-4c6a-933d-8860f61a6ca6; _ac_oid=bf0966cc65751955b3a5bc2b645d8ed9%3A1757380561489; accept_cookie=1',
}

files = {
    'owner': (None, '2'),
    'age': (None, '3-5'),
    'engine': (None, '1'),
    'power': (None, '1'),
    'power_unit': (None, '1'),
    'value': (None, '1999'),
    'price': (None, '45000000'),
    'curr': (None, 'KRW'),
}

response = requests.post('https://calcus.ru/calculate/Customs', cookies=cookies, headers=headers, files=files)