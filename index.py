import argparse
import random
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility
from w_bitget import Auto as BitgetAuto, Setup as BitgetSetup, EXTENSION_URL

QUESTIONS = [
    "What is artificial intelligence?",
    "How does machine learning work?",
    "What are the benefits of automation?",
    "Can you explain blockchain technology?",
    "What is cloud computing?",
    "How does cybersecurity work?",
    "What is the future of technology?",
    "How do neural networks function?",
    "What is quantum computing?",
    "How does data science work?",
    "What are the applications of IoT?",
    "How does virtual reality work?",
    "What is augmented reality?",
    "How does 5G technology work?",
    "What is edge computing?",
    "How does robotics work?",
    "What is natural language processing?",
    "How does computer vision work?",
    "What is deep learning?",
    "How does big data work?",
    "What is the role of AI in healthcare?",
    "How does autonomous driving work?",
    "What is smart home technology?",
    "How does renewable energy work?",
    "What is sustainable technology?",
    "How does digital transformation work?",
    "What is the future of work?",
    "How does remote work technology work?",
    "What is digital marketing?",
    "How does social media work?",
    "What is e-commerce?",
    "How does online payment work?",
    "What is digital banking?",
    "How does cryptocurrency work?",
    "What is fintech?",
    "How does mobile banking work?",
    "What is digital identity?",
    "How does biometric authentication work?",
    "What is cloud storage?",
    "How does data backup work?",
    "What is network security?",
    "How does encryption work?",
    "What is digital privacy?",
    "How does password protection work?",
    "What is two-factor authentication?",
    "How does VPN work?",
    "What is firewall protection?",
    "How does antivirus software work?",
    "What is malware protection?",
    "How does phishing protection work?",
    "What is ransomware protection?",
    "How does data recovery work?",
    "What is system optimization?",
    "How does computer maintenance work?",
    "What is software development?",
    "How does coding work?",
    "What is web development?",
    "How does mobile app development work?",
    "What is game development?",
    "How does UI/UX design work?",
    "What is responsive design?",
    "How does cross-platform development work?",
    "What is agile methodology?",
    "How does project management work?",
    "What is quality assurance?",
    "How does testing work?",
    "What is continuous integration?",
    "How does DevOps work?",
    "What is containerization?",
    "How does Docker work?",
    "What is Kubernetes?",
    "How does microservices work?",
    "What is API development?",
    "How does REST API work?",
    "What is GraphQL?",
    "How does WebSocket work?",
    "What is real-time communication?",
    "How does streaming work?",
    "What is content delivery?",
    "How does CDN work?",
    "What is load balancing?",
    "How does scaling work?",
    "What is high availability?",
    "How does disaster recovery work?",
    "What is business continuity?",
    "How does risk management work?",
    "What is compliance?",
    "How does data governance work?",
]

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        self.bitget_setup = BitgetSetup(node, profile)

    def _run(self):
        self.bitget_setup._run()
        self.node.new_tab('https://app.quackai.ai')#quackipedia?inviterCode=hj7kay&

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.profile_name = profile.get('profile_name')
        self.password = profile.get('password')
        self.seeds = profile.get('seeds')
        self.bitget_auto = BitgetAuto(node, profile)
        self.click_first = True

    def connect_wallet(self):
        text_button = self.node.get_text(By.XPATH, '//button[contains(@class, "whitespace-nowrap")]')
        if '...' in text_button:
            if self.node.find(By.XPATH, '//div[contains(text(), "Invite to Earn")]'):
                self.node.log('Đã connect wallet')
                return True
            else:
                self.node.snapshot(f'Cần Connect bằng tay')
        elif 'Connect Wallet' in text_button:
            self.node.find_and_click(By.XPATH, '//button[contains(text(),"Connect Wallet")]')
            self.node.find_and_click(By.XPATH, '//div[contains(text(), "Bitget Wallet")]')
            self.bitget_auto.confirm('connect')
            self.bitget_auto.confirm('approve')
            return self.connect_wallet()
        else:
            return False

    def handle_popup(self):
        h2_els = self.node.find_all(By.XPATH, '//div[h2]')
        popup = None
        for h2 in h2_els:
            if 'Get Started with Quack AI'.lower() in h2.text.lower():
                popup = h2
        if popup:
            buttons = self.node.find_all(By.TAG_NAME, 'button', popup)
            for button in buttons:
                if 'GO'.lower() in button.text.lower():
                    button.click()
                    if self.click_first:
                        if self.bitget_auto.confirm('Agree'):
                            self.click_first = False
                            button.click()
                    self.node.switch_tab('https://app.quackai.ai')
            self.node.find_and_click(By.XPATH, '//button[contains(text(), "Start Chatting")]')

    def send_message(self):
        send_button = self.node.find(By.XPATH, '//div[div[contains(text(),"Send")]]')
        question = random.choice(QUESTIONS)
        # Kiểm tra trạng thái nút Send
        if send_button:
            # Nếu nút bị disable (có class pointer-events-none)
            if 'cursor-not-allowed' in send_button.get_attribute('class'):
                self.node.find_and_input(By.TAG_NAME, 'textarea', question)
                send_button = self.node.find(By.XPATH, '//div[div[contains(text(),"Send")]]')
            # Nếu nút đang active (có class cursor-pointer)
            if 'cursor-pointer' in send_button.get_attribute('class'):
                self.node.press_key('Enter')
                
                # Đợi và xử lý popup MetaMask
                if self.click_first:
                    self.bitget_auto.confirm('Agree')
                    self.click_first = False
                
            # Kiểm tra daily limit message
            daily_limit_xpaths = [
                '//p[contains(text(),"daily") and contains(text(),"limit")]',
                '//div[contains(text(),"daily") and contains(text(),"limit")]'
            ]
            Utility.wait_time(10)
            for xpath in daily_limit_xpaths:
                limit_message = self.node.find(By.XPATH, xpath, wait=0, timeout=0)
                if limit_message:
                    point = self.node.get_text(By.XPATH, '//span[contains(@class, "font-[Poppins]")]')
                    self.node.snapshot(f'Đã đạt giới hạn chat hàng ngày: {point}')
                    return False

        else:
            self.node.log('Không tìm thấy nút Send')
            return False
    
        return True
    
    def _run(self):
        self.bitget_auto._run()
        self.bitget_auto.change_network('Duck chain', 'https://rpc.duckchain.io', '5545', 'TON', 'https://scan.duckchain.io/')
        self.node.new_tab('https://app.quackai.ai/')

        if not self.connect_wallet():
            return False
        
        self.handle_popup()
        while True:
            if not self.send_message():
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.get_data('profile_name', 'password', 'seeds')
    if not profiles:
        print("Không có dữ liệu để chạy")
        exit()

    browser_manager = BrowserManager(AutoHandlerClass=Auto, SetupHandlerClass=Setup)
    browser_manager.config_extension('Bitget-Wallet-*.crx')
    # browser_manager.run_browser(profiles[1])
    browser_manager.run_terminal(
        profiles=profiles,
        max_concurrent_profiles=4,
        block_media=False,
        auto=args.auto,
        headless=args.headless,
        disable_gpu=args.disable_gpu,
    )