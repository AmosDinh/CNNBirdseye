from playwright.sync_api import sync_playwright


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

def move_map_to_center(page):
    center_x = 110
    center_y = 110
    #map_ = page.locator('[aria-label="Interaktive Karte"]')
    margin = 10
    while True:
        x, y = get_parent_parent_pegman_translate(page)
        print(x)
        if abs(center_x-x)<margin and abs(center_y-y)<margin:
            page.keyboard.up("ArrowLeft")
            page.keyboard.up("ArrowRight")
            page.keyboard.up("ArrowUp")
            page.keyboard.up("ArrowDown")
            break
        # drag mouse
        if x < center_x:
            mouse_drag_on_minimap(page, center_x-x, 0)
        elif x > center_x:
            mouse_drag_on_minimap(page, center_x-x, 0)
        
        if y < center_y:
            mouse_drag_on_minimap(page, 0, center_y-y)
        elif y > center_y:
            mouse_drag_on_minimap(page, 0, center_y-y)
        
    
        
        
    

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
    

def launch_google_maps():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Open a new page
        page = context.new_page()

        # Navigate to Google Maps
        page.goto("https://www.google.com/maps")
        # alles akzeptieren
        # timeout
        accept_button_selector = '[aria-label="Alle akzeptieren"]'
        page.click(accept_button_selector)
        
        # write text in id="searchboxinput" and name="q"
        # click on button
        search_input_name = '[name="q"]'
        page.type(search_input_name, 'Tokyo')
        accept_button_selector = '[aria-label="Suche"]'
        page.click(accept_button_selector)
        
        
        accept_button_selector = '[aria-label="Street View-Abdeckung anzeigen"]'
        page.click(accept_button_selector)
        
        # Get the dimensions of the viewport
        viewport_size = page.viewport_size

        # Calculate the center coordinates
        center_x = viewport_size["width"] / 2
        center_x = 1.2 * center_x
        center_y = viewport_size["height"] / 2

        # Click at the center of the screen
        page.mouse.click(center_x, center_y)
        interaktive_karte_selector = '[aria-label="Interaktive Karte"]'
        interaktive_karte_element = page.locator(interaktive_karte_selector)
        interaktive_karte_element.hover()
        
        for _ in range(6):
            page.click('[jsaction="minimap.zoom-in"]')
        page.click('[jsaction="minimap.zoom-out"]')
        page.click('[jsaction="minimap.zoom-out"]')
        # page.click('.id-content-container')
        # page.focus('body')
      
        get_parent_parent_pegman_translate(page)
        
        #page.locator('[aria-label="Street View"]').click()
        #rotate_to(page, 0)
        # Wait for a while to let the page load (you can adjust the time based on your network speed)
        while True:
            page.wait_for_timeout(5000)
            move_map_to_center(page)
        page.wait_for_timeout(50000000)

        # Take a screenshot (optional)
        page.screenshot(path="google_maps.png")

        # Close the browser
        browser.close()

if __name__ == "__main__":
    launch_google_maps()
