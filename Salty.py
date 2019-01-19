from threading import Timer
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


class SaltyTimer():
    def __init__(self, driver):
        self._timer = Timer(60,self.timer_end)
        self._timer_on = False
        self._driver = driver

    def start_timer(self):
        if (self._timer_on == False):
            self._timer_on = True
            self._timer.start()

    def stop_timer(self):
        self._timer_on = False
        self._timer.cancel()

    def timer_end(self):
        driver = self._driver
        driver.set_network_conditions(latency=driver.get_network_conditions()['latency'],
                                      download_throughput=driver.get_network_conditions()['download_throughput'] *0.5,
                                      upload_throughput=driver.get_network_conditions()['upload_throughput']*0.5)
        self._timer = Timer(60,self.timer_end)
        self._timer_on = False
        print("lowered time")

class SaltyEventListener(AbstractEventListener):
    def __init__(self,driver):
        self._timer = SaltyTimer(driver)
        self._driver = driver

    def add_url_list(self,url_list):
        self._url_list= url_list

    def after_navigate_to(self, url, driver):
        url_combined = '\t'.join(self._url_list)
        while(url in url_combined):
            self._timer.start_timer()

        if (url not in url_combined):
            self._timer.stop_timer()

    def lower_network_rate(self,url,driver):
        driver.set_network_conditions(latency=driver.get_network_conditions()['latency'],
                                      download_throughput=driver.get_network_conditions()['download_throughput'] *0.5,
                                      upload_throughput=driver.get_network_conditions()['upload_throughput']*0.5)

        print("After navigate to %s" % driver.get_network_conditions()['download_throughput'])

class Salty():

    #NEED ATTRIBUTE OF DICTIONARY OF DICTIONARIES
    #Current Attributes
    # requests =
    # mp_request_status is a multiprocess array to indicate the
    # mp_request_inv is a multiprocess array indicating the inventory of each request, based on index
    #needs to be given an input file for both
    def __init__(self,url_list):
        self._url_list = url_list
        self._driver = webdriver.Chrome()
        self._driver.set_network_conditions(latency=20,download_throughput=500 * 1024,upload_throughput=5000 * 1024)
        self._salty_listener = SaltyEventListener(self._driver)
        self._salty_listener.add_url_list(url_list)

        self._event_driver = EventFiringWebDriver(self._driver, self._salty_listener)

    def run(self):
        pass


if __name__ == '__main__':
    url_list = ["https://www.youtube.com","https://www.reddit.com"]
    saltyBrowser = Salty(url_list)
    saltyBrowser._event_driver.get("https://www.youtube.com")
    saltyBrowser._event_driver.get("https://www.reddit.com")
    saltyBrowser._event_driver.get("https://www.youtube.com")
    saltyBrowser._event_driver.get("https://www.reddit.com")
    saltyBrowser._event_driver.get("https://www.youtube.com")