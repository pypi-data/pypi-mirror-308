from selenium.webdriver.remote.webdriver import WebDriver
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.902.62 Safari/537.36 Edg/92.0.902.62",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",

    # Add more User-Agent strings as needed
]

def get(**kwargs) -> WebDriver:
    """
    browser: safari, edge, chrome, firefox...(default: chrome)\n
    driver_version: 크롬 드라이버 버전(default:None)
    headless: (default: True)\n
    geolocation: (default: False)
    """
    browser_type = kwargs.get("browser", "chrome")
    driver_version = kwargs.get("driver_version", None)
    headless = kwargs.get("headless", True)
    geolocation = kwargs.get("geolocation", False)

    if browser_type == 'safari':
        driver = get_safari()
    elif browser_type == 'edge':
        driver = get_edge()
    elif browser_type == 'chrome':
        driver = get_chrome(driver_version=driver_version, headless=headless, geolocation=geolocation)
    elif browser_type == 'firefox':
        driver = get_firefox(headless=headless)
    elif browser_type == 'chromium':
        driver = get_chromium(headless=headless)
    else:
        raise Exception(f"browser type error : {browser_type}")
    return driver


def get_safari() -> WebDriver:
    from selenium import webdriver

    # safari는 headless 모드를 지원하지 않음
    print("For using safari driver. You should safari setting first, 설정/개발자/원격자동화허용 on")
    driver = webdriver.Safari()
    print(f'Get safari driver successfully...')
    return driver


def get_edge() -> WebDriver:
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    print(f'Get edge driver successfully...')
    return driver


def get_firefox(headless=True) -> WebDriver:
    # refered from https://www.zenrows.com/blog/selenium-user-agent#what-is-selenium-user-agent
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

    # Set up Firefox profile
    profile = FirefoxProfile()

    # Choose a random User-Agent from the list
    random_user_agent = random.choice(user_agents)
    profile.set_preference("general.useragent.override", random_user_agent)

    # Set up Firefox options
    firefox_options = Options()
    if headless:
        firefox_options.add_argument("-headless")
    firefox_options.profile = profile

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install())
                               , options=firefox_options)

    print(f'Get firefox driver successfully...')
    return driver

def get_chromium(headless=True) -> WebDriver:
    def find_chromium_executable():
        # 우선 환경 변수에 설정된 경로 확인
        import shutil, os
        executable_path = shutil.which("chromium") or shutil.which("chromium-browser")

        if executable_path:
            return executable_path

        # OS별로 일반적인 설치 경로 확인
        if os.name == "nt":  # Windows
            possible_paths = [
                r"C:\Program Files\Chromium\Application\chromium.exe",
                r"C:\Program Files (x86)\Chromium\Application\chromium.exe",
            ]
        elif os.name == "posix":
            possible_paths = [
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
                "/usr/local/bin/chromium",
                "/usr/local/bin/chromium-browser",
                "/snap/bin/chromium",
            ]
        else:
            possible_paths = []

        for path in possible_paths:
            if os.path.exists(path):
                return path

        raise FileNotFoundError("Chromium 실행 파일을 찾을 수 없습니다.")

    def get_chromium_version():
        import subprocess
        import re
        chromium_path = find_chromium_executable()
        result = subprocess.run([chromium_path, '--version'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        print(f"Chromium --version 출력: {output}")

        # 정규식을 사용하여 버전 번호 추출
        match = re.search(r'Chromium (\d+\.\d+\.\d+\.\d+)', output)
        if match:
            version = match.group(1)
            return version
        else:
            raise Exception('Chromium 버전을 추출할 수 없습니다.')

    chromium_version = get_chromium_version()
    print(f"Chromium 버전: {chromium_version}")

    # Chromedriver 버전 결정 (주요 버전 번호 사용)
    major_version = chromium_version.split('.')[0]
    print(f"Chromedriver 주요 버전: {major_version}")

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options

    # ChromeOptions 설정
    chromium_options = Options()

    if headless:
        chromium_options.add_argument("--headless")

    # Choose a random User-Agent from the list
    random_user_agent = random.choice(user_agents)
    chromium_options.add_argument(f"--user-agent={random_user_agent}")

    chromium_options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (Linux에서 필요할 수 있음)
    chromium_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화 (Linux에서 필요할 수 있음)

    chromium_path = find_chromium_executable()
    print(f"Chromium path: {chromium_path}")
    chromium_options.binary_location = chromium_path  # Chromium 실행 파일 경로 설정

    # WebDriver 설정
    # Chromedriver 경로 설정
    service = Service(executable_path=ChromeDriverManager(driver_version=major_version).install())
    # WebDriver 생성
    driver = webdriver.Chrome(service=service, options=chromium_options)

    #service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f'Get chromium driver successfully... headless : {headless}')
    return driver


def get_chrome(driver_version: str = None, temp_dir: str = '', headless=True, geolocation=False) -> WebDriver:
    """ 크롬 드라이버를 반환
    Args:
        driver_version: 드라이버를 못찾는 에러가 가끔있으며 이때는 드라이버 버전을 넣어주면 해결됨
        temp_dir : 크롬에서 다운받은 파일을 저장하는 임시디렉토리 경로(주로 krx에서 사용)
        headless : 크롬 옵션 headless 여부
        geolocation : geolocation 사용여부

    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options


    # Set up Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    # Choose a random User-Agent from the list
    random_user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"--user-agent={random_user_agent}")

    chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (Linux에서 필요할 수 있음)
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화 (Linux에서 필요할 수 있음)

    prefs = {}

    if geolocation:
        # https://copyprogramming.com/howto/how-to-enable-geo-location-by-default-using-selenium-duplicate
        prefs.update(
            {
                'profile.default_content_setting_values': {'notifications': 1, 'geolocation': 1},
                'profile.managed_default_content_settings': {'geolocation': 1},
            }
        )

    if temp_dir != '':
        # print(f'Set temp dir : {temp_dir}')
        # referred from https://stackoverflow.com/questions/71716460/how-to-change-download-directory-location-path-in-selenium-using-chrome
        prefs.update({'download.default_directory': temp_dir,
                      "download.prompt_for_download": False,
                      "download.directory_upgrade": True})

    if prefs:
        chrome_options.add_experimental_option('prefs', prefs)

    """from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    capabilities = DesiredCapabilities().CHROME
    capabilities.update(chrome_options.to_capabilities())
"""

    # Initialize the Chrome driver
    service = ChromeService(ChromeDriverManager(driver_version=driver_version).install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f'Get chrome driver successfully... headless : {headless}, geolocation : {geolocation}')
    return driver
