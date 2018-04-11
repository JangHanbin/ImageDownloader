import requests
import os
from bs4 import BeautifulSoup
import base64

def do_crawling():

    print("Number :", end=" ")
    choice = int(input())

    if choice == 1:
        print("Enter Naver Webtoon titleId (ex : 703845 ) :", end=" ")
        url = "http://comic.naver.com/webtoon//detail.nhn?titleId=" + input() + "&no="
        print("Enter Range of start :", end=" ")
        start_num = input()
        print("Enter Range of end :", end=" ")
        end_num = input()
        print("Enter name of to save folder :", end=" ")
        directory = input()
        naver_crawling(url, start_num, end_num , directory)

    elif choice == 2:
        print("Enter Bamtoki Webtoon Name (ex : 헬퍼 ) :", end=" ")
        url = "https://webtoon.bamtoki.com/" + input() + "-"
        print("Enter Range of start :", end=" ")
        start_num = input()
        print("Enter Range of end :", end=" ")
        end_num = input()
        print("Enter name of to save folder :", end=" ")
        directory = input()
        bamtoki_crawling(url, start_num, end_num,directory)

    else:
        print("You are choose wrong number Please Check the menu")
        exit(1)


def naver_crawling(url, start_num, end_num, directory):

    if not os.path.exists(directory):
        os.mkdir(directory)
    while int(start_num) <= int(end_num):
        if not os.path.exists(directory+"/"+start_num):
            os.mkdir(directory+"/"+start_num)
        res = requests.get(url + start_num)
        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            imgs = soup.select(
                "#comic_view_area > div.wt_viewer > img"
            )
            file_index = 0

            custom_headers = {
                "Referer": url + start_num,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
            }

            for img in imgs:
                r = requests.get(img["src"], headers=custom_headers)

                # loop until take code 200
                while r.status_code != 200:
                    r = requests.get(img["src"])
                    
                print(img["src"] + " downloaded!")
                with open("{0}/{1}/{2}.jpg".format(directory, start_num, str(file_index)), 'wb') as f:
                    f.write(r.content)
                file_index = file_index + 1

        print("{0} of range Saved!".format(start_num))
        start_num = str(int(start_num) + 1) # add sequence

#This web site img src encoded by Base64

def bamtoki_crawling(url, start_num, end_num,directory):

    if not os.path.exists(directory):
        os.mkdir(directory)

    while int(start_num) <= int(end_num):

        if not os.path.exists(directory+"/"+start_num):
            os.mkdir(directory+"/"+start_num)

        res = requests.get(url +start_num.zfill(2)+".html")

        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')

            file_index = 0
            encoded_content_datas = soup.find_all("div", attrs={"id": "tooncontentdata"})

            for encoded_content_data in encoded_content_datas:
                decoded_content_data = str(base64.b64decode(encoded_content_data.text))
                # cut <div> && " ' " to leave only img tag and reparsing by beautifulsoup
                imgs = BeautifulSoup(decoded_content_data[decoded_content_data.find("<img"):decoded_content_data.rfind("'")], 'html.parser')

                # there is don't need to add header info
                for img in imgs:
                    r = requests.get(img["src"])

                    # loop until take code 200
                    while r.status_code != 200:
                        r = requests.get(img["src"])

                    print(img["src"] + " downloaded!")
                    with open("{0}/{1}/{2}.jpg".format(directory, start_num, str(file_index)), 'wb') as f:
                        f.write(r.content)
                    file_index = file_index + 1

        print("{0} of range Saved!".format(start_num))
        start_num = str(int(start_num) + 1) # add sequence


if __name__ == "__main__":
    print("Choose URL number what you want to download image")
    print("1 : Naver Webtoon")
    print("2 : bamtoki")
    do_crawling()

