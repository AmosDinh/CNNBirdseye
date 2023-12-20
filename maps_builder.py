from playwright.sync_api import sync_playwright

def remove_all_background(page):
    remove = ["#omnibox-singlebox",".scene-footer-container", '.app-bottom-content-anchor','#play','.scene-footer-container', '#watermark','#titlecard', '#image-header']
    for selector in remove:
        page.evaluate(f"""selector => document.querySelector(selector).style.opactiy = 0 """, selector)
        
    
    
    
    
    # all buttons: display none
    # buttons = page.query_selector_all('button')
    # for button in buttons:
    #     parent = button.query_selector('xpath=..')
    #     # check if parent only has buttons as children
    #     children = parent.query_selector_all('div')
    #     if len(children) == 0:
    #         page.evaluate(f"""element => element.style.display = "none" """, parent)
    #     # page.evaluate(f"""element => element.style.display = "none" """, parent)
        
def get_pegman_background_position_y(page):
    minimap_div = page.query_selector('#minimap')
    pegman_div = minimap_div.query_selector("div[style*='rotating-1x.png']")
    background_position_y = page.evaluate('(element) => getComputedStyle(element).backgroundPositionY', pegman_div)
    # -364px to int
    y = int(background_position_y.replace("px", ""))

    return y

def get_parent_parent_pegman_translate(page):
    minimap_div = page.query_selector('#minimap')
    pegman_div = minimap_div.query_selector("div[style*='rotating-1x.png']")
    grandparent = pegman_div.query_selector('xpath=../..')
    #grandparent = parent.evaluate("""parent => parent.parentElement""")
    # get the translate x, and y
    translate = page.evaluate('(element) => getComputedStyle(element).transform', grandparent)
    x, y = translate.replace("matrix(", "").replace(")", "").split(", ")[-2:]
    x = int(x)
    y = int(y)
    return x, y

def mouse_drag_on_minimap(page, x_amount, y_amount):
    # get center of minimap
    #minimap_div = page.query_selector('#minimap')
    minimap_div = page.query_selector('[aria-label="Interaktive Karte"]').query_selector('xpath=..')
    center_x = minimap_div.bounding_box()["x"] + minimap_div.bounding_box()["width"] / 2
    center_y = minimap_div.bounding_box()["y"] + minimap_div.bounding_box()["height"] / 2
    print(center_x, center_y)
    print(minimap_div.bounding_box())
    # focus on minimap
    # minimap_div.click()
    print('click')
    while minimap_div.bounding_box()["width"]!=222 or minimap_div.bounding_box()["height"]!=222:
        #page.mouse.move(center_x, center_y)
        minimap_div.hover()
        minimap_div = page.query_selector('[aria-label="Interaktive Karte"]').query_selector('xpath=..')
        
    minimap_div = page.query_selector('[aria-label="Interaktive Karte"]').query_selector('xpath=..')
    center_x = minimap_div.bounding_box()["x"] + minimap_div.bounding_box()["width"] / 2
    center_y = minimap_div.bounding_box()["y"] + minimap_div.bounding_box()["height"] / 2
    page.mouse.move(center_x, center_y)
    page.mouse.down()
    page.mouse.move(center_x+x_amount, center_y+y_amount)
    page.mouse.up()
    minimap = page.query_selector('#minimap')
    first_child = minimap.query_selector_all('xpath=child::*')[0]
    second_child = first_child.query_selector_all('xpath=child::*')[1]
    third_child = second_child.query_selector_all('xpath=child::*')[2]
    fourth_child = second_child.query_selector_all('xpath=child::*')[3]
    # displaynone
    page.evaluate(f"""element => element.style.display = "none" """, third_child)
    page.evaluate(f"""element => element.style.display = "none" """, fourth_child)

def move_map_to_center(page):
    center_x = 110
    center_y = 110
    #map_ = page.locator('[aria-label="Interaktive Karte"]')
    margin = 2
    while True:
        x, y = get_parent_parent_pegman_translate(page)
        if abs(center_x-x)<margin and abs(center_y-y)<margin:
            break
        # drag mouse
        if x < center_x or y < center_y or x > center_x or y > center_y:
            mouse_drag_on_minimap(page, center_x-x, center_y-y)
        

    

def rotate_to(page, angle):
    # define top as 0°
    # define right as 90°
    # define bottom as 180°
    # define left as 270°
    # -780 is the maximum value for the background-position-y (top)
    # -780 = 2pi = 0
    #degree_of_freedom = 32
    # = degree_of_freedom/2
    # 0 is the minimum
    
    # angle to nearest 24 degrees
    angle = round(angle / 24) * 24
    
    page.locator('[aria-label="Street View"]').click()
    page.keyboard.down("ArrowRight")
    while True:
        
        y = get_pegman_background_position_y(page)
        
        current_angle = abs(y / -780 * 360)
        
        if abs(angle-current_angle) < 1 or abs(angle-current_angle) > 359:
            page.keyboard.up("ArrowRight")
            break
    page.keyboard.up("ArrowRight")
    print('done', angle)

import cv2
import numpy as np 
def click_on_interactive_street(page):  
    page.click('[aria-label="Street View-Abdeckung anzeigen"]')
   
    # analyze the image, get all the walkable sections by color
    # read in the image as a numpy array
    blue_pixels = [0]
    for _ in range(5):
        page.screenshot(path="google_maps_temp.png")
        img = cv2.imread('google_maps_temp.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        blue_color = [3, 169, 244]
        blue_color2 = [18,158,175]
        # get all the blue pixels
        blue_pixels1 = (img[:,:,0] == blue_color[0]) & (img[:,:,1] == blue_color[1]) & (img[:,:,2] == blue_color[2])
        blue_pixels2 = (img[:,:,0] == blue_color2[0]) & (img[:,:,1] == blue_color2[1]) & (img[:,:,2] == blue_color2[2])
        
        if np.sum(blue_pixels1) > np.sum(blue_pixels2):
            blue_pixels = blue_pixels1
            break
        elif np.sum(blue_pixels1) < np.sum(blue_pixels2):
            blue_pixels = blue_pixels2
            break
        
        page.wait_for_timeout(300)
        
    if np.sum(blue_pixels) == 0:
        print('no blue pixels')
        return False
    else:
        # mask back to full image with 
        # click on random blue pixel in the upper half, center of the image
        left =  img.shape[1]//4
        right = img.shape[1]-img.shape[1]//4
        top = img.shape[0]//4
        bottom = img.shape[0]-img.shape[0]//4
        
        upper_center_img_mask = np.zeros_like(img[:,:,0])
        upper_center_img_mask[:top, left:right] = 1
        upper_center_img_mask = np.array(np.where((upper_center_img_mask==1) & (blue_pixels==1)))
        
        lower_center_img_mask = np.zeros_like(img[:,:,0])
        lower_center_img_mask[bottom:, left:right] = 1
        lower_center_img_mask = np.array(np.where((lower_center_img_mask==1) & (blue_pixels==1)))
        
        left_img_mask = np.zeros_like(img[:,:,0])
        left_img_mask[:, :left] = 1
        left_img_mask = np.array(np.where((left_img_mask==1) & (blue_pixels==1)))
        
        right_img_mask = np.zeros_like(img[:,:,0])
        right_img_mask[:, right:] = 1
        right_img_mask = np.array(np.where((right_img_mask==1) & (blue_pixels==1)))
                
        all_img_mask = np.array(np.where(blue_pixels==1))

        # if at least one in lower_center_img_mask
        if len(upper_center_img_mask) > 0:
            # click on random pixel in lower_center_img_mask which has a blue pixel
            random_indices_with_1 = np.random.choice(np.arange(len(upper_center_img_mask[0])))
            random_indices_with_1 = upper_center_img_mask[:, random_indices_with_1]
            
        elif len(lower_center_img_mask) > 0:
            random_indices_with_1 = np.random.choice(np.arange(len(lower_center_img_mask[0])))
            random_indices_with_1 = lower_center_img_mask[:, random_indices_with_1]
            
        elif len(left_img_mask) > 0:
            random_indices_with_1 = np.random.choice(np.arange(len(left_img_mask[0])))  
            random_indices_with_1 = left_img_mask[:, random_indices_with_1]
            
        elif len(right_img_mask) > 0:
            random_indices_with_1 = np.random.choice(np.arange(len(right_img_mask[0])))
            random_indices_with_1 = right_img_mask[:, random_indices_with_1]
        else:
            random_indices_with_1 = np.random.choice(np.arange(len(all_img_mask[0])))
            random_indices_with_1 = all_img_mask[:, random_indices_with_1]

        # click on coordinate
        x = random_indices_with_1[1]
        y = random_indices_with_1[0]
        page.mouse.click(int(x), int(y))
    
def launch_google_maps():
    with sync_playwright() as p:
        user_data_dir = '/home/amos/.config/google-chrome/Default/'
        #user_data_dir = 'Profile 1'
        # Launch the browser with the custom user data directory
        # args = [
            # '--disable-background-networking',
            # '--no-sandbox',
            # '--disable-setuid-sandbox',
            # '--disable-infobars',#'--single-process',
            
            # '--no-zygote',
            # '--no-first-run',
            # '--window-position=0,0',
            # '--ignore-certificate-errors',
            # '--ignore-certificate-errors-skip-list',
            # '--disable-dev-shm-usage',
            # '--disable-accelerated-2d-canvas',
            # '--disable-gpu',
            # '--hide-scrollbars',
            # '--disable-notifications',
            # '--disable-background-timer-throttling',
            # '--disable-backgrounding-occluded-windows',
            # '--disable-breakpad',
            # '--disable-component-extensions-with-background-pages',
            # '--disable-extensions',
            # '--disable-features=TranslateUI,BlinkGenPropertyTrees',
            # '--disable-ipc-flooding-protection',
            # '--disable-renderer-backgrounding',
            # '--enable-features=NetworkService,NetworkServiceInProcess',
            # '--force-color-profile=srgb',
            # '--metrics-recording-only',
        #     # '--mute-audio']
        # browser = p.chromium.launch_persistent_context(
        #     '/usr/bin/google-chrome',
        #     #user_data_dir=user_data_dir,
        #     headless=False,
        #     args=['--profile-directory=Default'],
        #     # args=args,
        #     #
        #     # args=['---disable-blink-features=AutomationControlled',"--disable-dev-shm-usage",'--disable-component-extensions-with-background-pages'],
        #     #args=browser_args,
        #     #ignore_default_args=False,#['--enable-automation'],
        #     #user_data_dir=user_data_dir
        #     #executable_path='/usr/bin/google-chrome',
        # )
        browser = p.chromium.launch(headless=False)#args=['--profile-directory=Default'])

        # Create a new page
        page = browser.new_page()

        # Open a new page
        #page = browser.new_page()
        #page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

        # Navigate to Google Maps
        page.goto("https://www.google.com/maps")
        # alles akzeptieren
        # timeout
        accept_button_selector = '[aria-label="Alle akzeptieren"]'
        page.click(accept_button_selector)
        
        search_input_name = '[name="q"]'
        page.type(search_input_name, 'New York')
        accept_button_selector = '[aria-label="Suche"]'
        page.click(accept_button_selector)
        page.hover('[aria-labelledby="widget-minimap-icon-overlay"]')
        page.click('[jsaction="layerswitcher.quick.more"]')
        page.click('[jsaction="layerswitcher.intent.spherical"]')
        page.click('[jsaction="layerswitcher.close"]')
        
        
            
        page.wait_for_timeout(50000000)
        click_on_interactive_street(page)
        
        viewport_size = page.viewport_size

        # # Calculate the center coordinates
        center_x = viewport_size["width"] / 2
        center_x = 1.2 * center_x
        center_y = viewport_size["height"] / 2
        # move mouse to center
        page.mouse.move(center_x, center_y)
        # mouse wheel scroll in
        page.mouse.wheel(0, 100)
        
        
        # Get the dimensions of the viewport
        # viewport_size = page.viewport_size

        # # Calculate the center coordinates
        # center_x = viewport_size["width"] / 2
        # center_x = 1.2 * center_x
        # center_y = viewport_size["height"] / 2

        # # Click at the center of the screen
        # page.mouse.click(center_x, center_y)
        # interaktive_karte_selector = '[aria-label="Interaktive Karte"]'
        # interaktive_karte_element = page.locator(interaktive_karte_selector)
        # interaktive_karte_element.hover()
        # interaktive_karte_element.click()
        # page.wait_for_timeout(1000)
        
        # tilt.onTiltClick;mouseover:tilt.main;mouseout:tilt.main
        
        # for _ in range(6):
        #     page.click('[jsaction="minimap.zoom-in"]')
            
            
            
        # page.click('[jsaction="minimap.zoom-out"]')
        # page.click('[jsaction="minimap.zoom-out"]')

        # mouse wheel scroll in
        

        # while True:
            
        #     page.click('[jsaction="compass.needle"]')  # face north
        #     page.click('[jsaction="compass.right"]')
        #     page.click('[jsaction="compass.left"]')
        
        #get_parent_parent_pegman_translate(page)
        #page.screenshot(path="google_maps1.png")
        
        
         
        
        #page.locator('[aria-label="Street View"]').click()
        #rotate_to(page, 0)
        # Wait for a while to let the page load (you can adjust the time based on your network speed)
        #remove_all_background(page)
        # while True:
        #     move_map_to_center(page)
        #     #page.screenshot(path="google_maps6.png")
            
        page.wait_for_timeout(50000000)

        # Take a screenshot (optional)
        

        # Close the browser
        browser.close()

if __name__ == "__main__":
    launch_google_maps()
