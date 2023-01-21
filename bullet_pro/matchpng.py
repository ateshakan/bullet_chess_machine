from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from stockfish import Stockfish
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import chess
import chess.engine
import random
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome(chrome_options=options,executable_path=PATH)
stockfish = Stockfish(r'C:\Users\user\Desktop\problemler\bullet_pro\stockfish_13_win_x64_ssse\stockfish_13_win_x64_ssse.exe')

engine = chess.engine.SimpleEngine.popen_uci(r'C:\Users\user\Desktop\problemler\bullet_pro\stockfish_13_win_x64_ssse\stockfish_13_win_x64_ssse.exe')

board = chess.Board()

def login():
    driver.get("https://lichess.org/login?referrer=/")

    user=driver.find_element_by_name("username")
    user.send_keys("") #username
    passw=driver.find_element_by_name("password")
    passw.send_keys("") #pass
    login=driver.find_element(By.XPATH,'//*[@id="main-wrap"]/main/form/div[1]/button').click()




time.sleep(1)
wait = WebDriverWait(driver, 10)

############################################################
############################################################
############################################################
############################################################
#driver.get("https://lichess.org/")
############################################################
############################################################
############################################################
############################################################







# nots=driver.find_element(By.CSS_SELECTOR,'l4x')
# nots_list=nots.text.split()

def drop(mylist, n):
    del mylist[0::n]
    return (mylist)




def get_notation():
    try:
        
        #nots1=driver.find_element(By.CSS_SELECTOR,'l4x')
        nots1=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'l4x')))
        nots_list1=nots1.text.split()
    except:
        time.sleep(1)
        get_notation()
    return drop(nots_list1,3)



def play_algo():
    try:
        notas=get_notation()
        board = chess.Board()
        while not board.is_game_over():
            for i in range(len(notas)):
                board.push_san(notas[i])
            

            result = engine.play(board, chess.engine.Limit(depth=10))
            board.push(result.move)
            a=result.move
            blindkey=driver.find_element(By.XPATH,'//*[@id="main-wrap"]/main/div[1]/div[10]/input')
            blindkey.send_keys(str(a)+Keys.RETURN)
            blindkey.clear()
            board=chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
            notas=get_notation()
            if 10<len(notas)<30:
                time.sleep(random.randrange(0,3000)/1000)
            else:
                pass
    except:
        time.sleep(1)
        play_algo()
        #time.sleep(1)


#You play the white pieces
#It's your turn!
#Your turn
def is_ur_turn():
    html = driver.execute_script("return document.documentElement.outerHTML;")
    if ("Your turn" or "your turn" in html):
        return True
    else:
        return False

hamle_sayisi=0

def play_algo_v2():
    try:
        notas=get_notation()
        board = chess.Board()
        while not board.is_game_over():
            if is_ur_turn():
                notas=get_notation()
                for i in range(len(notas)):
                    board.push_san(notas[i])
                

                result = engine.play(board, chess.engine.Limit(depth=10))
                board.push(result.move)
                a=result.move
                blindkey=driver.find_element(By.XPATH,'//*[@id="main-wrap"]/main/div[1]/div[10]/input')
                blindkey.send_keys(str(a)+Keys.RETURN)
                hamle_sayisi+=1
                blindkey.clear()
                board=chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
                notas=get_notation()
                print("Hamle sayısı "+str(hamle_sayisi))
                if 10<len(notas)<30:
                    time.sleep(random.randrange(0,3000)/1000)
                else:
                    pass
    except:
        time.sleep(1)
        play_algo_v2()
        #time.sleep(1)

def play_random_algo():
    try:
        notas=get_notation()
        board = chess.Board()
        while not board.is_game_over():
            if is_ur_turn():
                notas=get_notation()
                for i in range(len(notas)):
                    board.push_san(notas[i])
                

                # result = engine.play(board, chess.engine.Limit(depth=1))
                # board.push(result.move)
                a_list=list(board.legal_moves)
                a=a_list[random.randint(0,len(notas))]
                
                blindkey=driver.find_element(By.XPATH,'//*[@id="main-wrap"]/main/div[1]/div[10]/input')
                blindkey.send_keys(str(a)+Keys.RETURN)
                
                blindkey.clear()
                board=chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
                notas=get_notation()
                
                # if 10<len(notas)<30:
                #     time.sleep(random.randrange(0,3000)/1000)
                # else:
                #     pass
    except:
        time.sleep(1)
        play_random_algo()
        #time.sleep(1)


login()
play_algo_v2()
# play_algo_v2()



#engine.quit()


    