#!/usr/bin/python3
import os
import time
import random
import sys
import traceback

from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from openpyxl import Workbook, load_workbook


Freq = 1500  # Set Frequency To 2500 Hertz
Dur = 500  # Set Duration To 1000 ms == 1 second


def solve_captcha():
    # winsound.Beep(Freq,Dur)
    print("asking for solving a captcha")
    raw_input("Please, solve the CAPTCHA and press ENTER: ")


def checkload(url, element_id):
    loaded_correctly = False
    attempt = 1
    while not loaded_correctly:
        try:
            print(url)
            br.get(url)
            html = (
                br.find_element_by_xpath("//html")
                .get_attribute("innerHTML")
                .encode("utf-8")
            )

            if html.find("Please show you're not a robot".encode("utf-8")) > 0:
                solve_captcha()
            elif (
                html.find(
                    "your computer or network \
                        may be sending automated queries".encode(
                        "utf-8"
                    )
                )
                > 0
            ):
                solve_captcha()
            elif html.find("Prouvez que vous n'êtes pas un robot".encode("utf-8")) > 0:
                solve_captcha()

            elif (
                html.find("inusual procedente de tu red de ordenadores".encode("utf-8"))
                > 0
            ):
                solve_captcha()
            elif (
                html.find(
                    "Our systems have detected \
                            unusual traffic from your computer".encode(
                        "utf-8"
                    )
                )
                > 0
            ):
                solve_captcha()
            loaded_correctly = True
        except Exception as e:
            print(e)
            traceback.print_exc()
            if attempt == 3:
                print("THE FOLLOWING URL COULDN'T BE DOWNLOADED:")
                print(url)
                break
            loaded_correctly = False
            print("Trying again " + url)
            attempt += 1
            time.sleep(2)


br = webdriver.Firefox()

br.get("http://scholar.google.com")


f = open(sys.argv[1], "r")
url_list = f.readlines()
f.close()


c_dir = os.path.dirname(os.path.abspath(__file__))

art_dir = "articles_html"
if not os.path.exists(art_dir):
    os.makedirs(art_dir)

i = 1
for c_url in url_list:
    more_results = True
    c_url = c_url.strip()
    sleep_seconds = random.randint(5, 15)
    checkload(c_url, "gs_rt")
    while more_results:
        html = (
            br.find_element_by_xpath("//html")
            .get_attribute("innerHTML")
            .encode("utf-8")
        )
        try:
            br.find_element_by_class_name("gs_rt")
        except Exception:
            # continues to next query if no results are shown in the page
            more_results = False
            continue
        html = (
            br.find_element_by_xpath("//html")
            .get_attribute("innerHTML")
            .encode("utf-8")
        )
        c_url = br.current_url
        if c_url.find("start=") == -1:
            start_page = "0"
        else:
            start_page = c_url[
                c_url.find("start=") + 6 : c_url.find("&", c_url.find("start=") + 6)
            ]
        write_path = art_dir + "/" + str(i) + "." + start_page + ".html"
        w = open(write_path, "w")
        w.write(str(html))
        w.close()
        try:
            next_page = br.find_element_by_xpath(
                '//span[contains(@class, "gs_ico_nav_next")]/..'
            ).get_attribute("href")
            time.sleep(sleep_seconds)
            checkload(next_page, "gs_rt")
        except Exception:
            more_results = False
            time.sleep(sleep_seconds)
        i += 1
br.close()
