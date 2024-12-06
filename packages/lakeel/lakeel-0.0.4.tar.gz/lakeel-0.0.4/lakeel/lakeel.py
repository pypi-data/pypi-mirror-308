import platform
import subprocess
import sys
import importlib.util
import os

# pip로 패키지 설치 함수
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 패키지가 설치되어 있는지 확인하는 함수
def is_installed(package_name):
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

# 운영체제에 맞는 폰트 설정 함수
def sfo():
    current_os = platform.system()

    # matplotlib이 설치되어 있는지 확인
    if not is_installed('matplotlib'):
        print("matplotlib가 설치되어 있지 않습니다.")
        install('matplotlib')
    else:
        print("matplotlib가 이미 설치되어 있습니다 :)")

    import matplotlib.pyplot as plt
    from matplotlib import rc

    if current_os == 'Darwin':  # macOS
        print("폰트가 AppleGothic font로 설정되었습니다.")
        rc('font', family='AppleGothic')
        
    elif current_os == 'Windows':  # Windows
        print("폰트가 Malgun Gothic font로 설정되었습니다.")
        rc('font', family='Malgun Gothic')
        
    else:
        print(f"Unknown OS: {current_os}. Please set the font manually.")

    # 음수 부호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    print("Font setup is complete.")

# 1. 현재 파이썬 코드가 실행되는 경로를 반환하는 함수
def dir():
    return os.getcwd()

# 2. 설치된 pip 패키지 목록을 알파벳 순서대로 출력하는 함수
def pip():
    # pip list 명령 실행
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    
    # 결과를 줄 단위로 분리
    lines = result.stdout.splitlines()

    # 첫 두 줄은 헤더이므로 제외하고, 나머지 줄을 알파벳 순서대로 정렬
    package_list = lines[2:]  # 첫 두 줄을 제거
    sorted_list = sorted(package_list)

    # 정렬된 패키지 목록을 한 줄씩 출력
    for package in sorted_list:
        print(package)

# 새로운 함수들 추가
def update(package=None):
    """
    지정된 패키지를 최신 버전으로 업데이트합니다.
    package가 None이면 모든 패키지를 업데이트합니다.
    """
    try:
        if package:
            print(f"{package} 패키지를 업데이트하는 중...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            print(f"{package} 패키지가 성공적으로 업데이트되었습니다.")
        else:
            print("모든 패키지를 업데이트하는 중...")
            subprocess.check_call([sys.executable, "-m", "pip", "list", "--outdated"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"], 
                                 capture_output=True, text=True)
            packages = eval(result.stdout)
            for package in packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package['name']])
            print("모든 패키지가 성공적으로 업데이트되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"업데이트 중 오류가 발생했습니다: {e}")

def uninstall(package):
    """
    지정된 패키지를 제거합니다.
    """
    try:
        if is_installed(package):
            print(f"{package} 패키지를 제거하는 중...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            print(f"{package} 패키지가 성공적으로 제거되었습니다.")
        else:
            print(f"{package} 패키지가 설치되어 있지 않습니다.")
    except subprocess.CalledProcessError as e:
        print(f"제거 중 오류가 발생했습니다: {e}")

def info(package):
    """
    지정된 패키지의 상세 정보를 조회합니다.
    """
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "show", package], 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        else:
            print(f"{package} 패키지를 찾을 수 없습니다.")
    except subprocess.CalledProcessError as e:
        print(f"정보 조회 중 오류가 발생했습니다: {e}")

def search(query):
    """
    PyPI에서 패키지를 검색합니다.
    """
    try:
        print(f"'{query}' 관련 패키지 검색 중...")
        subprocess.check_call([sys.executable, "-m", "pip", "search", query])
    except subprocess.CalledProcessError as e:
        print(f"검색 중 오류가 발생했습니다: {e}")
        print("참고: pip search 기능이 비활성화된 경우 https://pypi.org 에서 직접 검색해주세요.")

