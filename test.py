import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def setup_chrome_driver():
    """
    針對你的 EC2 aarch64 環境優化的 Chrome WebDriver 設置
    使用已安裝的 Chromium 和 ChromeDriver
    """
    print("[開始] 初始化 Chrome WebDriver...")
    
    # Chrome 選項設置
    chrome_options = Options()
    
    # 基本 headless 設置
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    
    # 安全性設置
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-certificate-errors-spki-ca-list')
    
    # 性能優化設置（針對 ARM64 架構）
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-images')  # 可選：如果不需要圖片可以加速
    chrome_options.add_argument('--disable-javascript')  # 可選：如果不需要 JS 可以加速
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--log-level=3')
    
    # EC2 環境專用設置
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    
    # 記憶體優化（你的系統有 3.7GB 記憶體）
    chrome_options.add_argument('--memory-pressure-off')
    chrome_options.add_argument('--max_old_space_size=2048')
    chrome_options.add_argument('--disable-background-networking')
    
    # 根據診斷結果，設置正確的路徑
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    
    # 使用已確認存在的 ChromeDriver
    chromedriver_path = '/usr/bin/chromedriver'
    
    try:
        print(f"[資訊] 使用 Chromium: {chrome_options.binary_location}")
        print(f"[資訊] 使用 ChromeDriver: {chromedriver_path}")
        
        # 創建 Service 對象
        service = Service(executable_path=chromedriver_path)
        
        # 啟動 WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 測試 driver 是否正常工作
        print("[測試] 測試 WebDriver 是否正常...")
        driver.get("data:text/html,<html><body><h1>Test OK</h1></body></html>")
        
        print("[成功] WebDriver 啟動並測試成功！")
        return driver
        
    except WebDriverException as e:
        print(f"[錯誤] WebDriver 啟動失敗: {e}")
        
        # 嘗試備用方案：使用 snap 版本的 chromedriver
        try:
            print("[重試] 嘗試使用 snap 版本的 ChromeDriver...")
            snap_chromedriver = '/snap/chromium/current/usr/lib/chromium-browser/chromedriver'
            service = Service(executable_path=snap_chromedriver)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("data:text/html,<html><body><h1>Test OK</h1></body></html>")
            print("[成功] 使用 snap ChromeDriver 啟動成功！")
            return driver
        except Exception as e2:
            print(f"[錯誤] snap ChromeDriver 也失敗: {e2}")
    
    except Exception as e:
        print(f"[錯誤] 未預期的錯誤: {e}")
    
    return None

def safe_driver_quit(driver):
    """
    安全地關閉 WebDriver
    """
    if driver is not None:
        try:
            driver.quit()
            print("[資訊] WebDriver 已成功關閉")
        except Exception as e:
            print(f"[警告] 關閉 WebDriver 時發生錯誤: {e}")
    else:
        print("[警告] driver 為 None，無需關閉")

def test_webdriver():
    """
    測試 WebDriver 是否正常工作
    """
    print("=== 測試 WebDriver ===")
    
    driver = setup_chrome_driver()
    if driver:
        try:
            # 測試訪問一個網頁
            print("[測試] 訪問測試網頁...")
            driver.get("https://httpbin.org/get")
            
            # 檢查頁面是否載入
            title = driver.title
            print(f"[成功] 頁面標題: {title}")
            
            # 檢查頁面內容
            if "httpbin" in driver.page_source.lower():
                print("[成功] 頁面內容載入正常")
                return True
            else:
                print("[警告] 頁面內容可能有問題")
                return False
                
        except Exception as e:
            print(f"[錯誤] 測試過程中發生錯誤: {e}")
            return False
        finally:
            safe_driver_quit(driver)
    else:
        print("[失敗] WebDriver 初始化失敗")
        return False

# 你的爬蟲函數應該這樣寫
def crawler_first_stage():
    """
    修正後的爬蟲函數 - 不會再有 NoneType 錯誤
    """
    driver = None
    try:
        print("[開始] 啟動爬蟲任務...")
        
        # 啟動 WebDriver
        driver = setup_chrome_driver()
        if driver is None:
            error_msg = "WebDriver 啟動失敗，請檢查 Chrome 和 ChromeDriver 安裝"
            print(f"[錯誤] {error_msg}")
            return {"status": "error", "message": error_msg}
        
        print("[進行中] WebDriver 啟動成功，開始執行爬蟲邏輯...")
        
        # ==========================================
        # 在這裡加入你的實際爬蟲代碼
        # ==========================================
        
        # 範例：訪問新聞網站
        # driver.get("https://example-news-site.com")
        # 
        # # 等待頁面載入
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # from selenium.webdriver.common.by import By
        # 
        # wait = WebDriverWait(driver, 10)
        # news_elements = wait.until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, "news-item"))
        # )
        # 
        # # 提取新聞數據
        # news_data = []
        # for element in news_elements:
        #     title = element.find_element(By.TAG_NAME, "h3").text
        #     link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
        #     news_data.append({"title": title, "link": link})
        
        # 暫時的測試代碼
        driver.get("https://httpbin.org/get")
        print("[測試] 成功訪問測試頁面")
        
        print("[完成] 爬蟲任務執行完成")
        return {"status": "success", "message": "爬蟲任務完成"}
        
    except Exception as e:
        error_msg = f"爬蟲過程中發生錯誤: {str(e)}"
        print(f"[錯誤] {error_msg}")
        return {"status": "error", "message": error_msg}
    
    finally:
        # 這裡絕對不會出現 NoneType 錯誤了
        safe_driver_quit(driver)

# 如果直接執行此檔案，會進行測試
if __name__ == "__main__":
    print("執行 WebDriver 測試...")
    success = test_webdriver()
    if success:
        print("\n✅ 測試成功！你可以開始使用爬蟲了。")
        print("\n測試爬蟲函數...")
        result = crawler_first_stage()
        print(f"爬蟲結果: {result}")
    else:
        print("\n❌ 測試失敗，請檢查配置。")