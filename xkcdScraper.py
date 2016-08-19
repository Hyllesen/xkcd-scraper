import requests, bs4

#Let's go to the frontpage and get the first image, and the first prev number!

xkcdUrl = 'http://xkcd.com'

res = requests.get(xkcdUrl)

#Check for errors
res.raise_for_status()

xkcdSoup = bs4.BeautifulSoup(res.text)

#Select the image element
imgElem = xkcdSoup.select('#comic img')

#Get img url
imgUrl = imgElem[0].attrs['src']

#Download the image
imgRequest = requests.get('http:'+ imgUrl)

if imgRequest.status_code == 200:
    with open('latest.png', 'wb') as f:
        for chunk in imgRequest:
            f.write(chunk)

f.close()

print("Done scraping latest image")

#Now lets get the previous comics!

#Get the latest prev link
prevLink = xkcdSoup.select('.comicNav li a[rel="prev"]')[0].attrs['href']

comicNumber = prevLink.replace('/', "")

while (1 < comicNumber):
    prevLink = xkcdSoup.select('.comicNav li a[rel="prev"]')[0].attrs['href']
    res = requests.get(xkcdUrl + prevLink)
    res.raise_for_status()
    xkcdSoup = bs4.BeautifulSoup(res.text)
    imgElem = xkcdSoup.select('#comic img')
    if(len(imgElem) >= 1):
        imgUrl = imgElem[0].attrs['src']
        comicNumber = prevLink.replace('/', "")
        imgRequest = requests.get('http:' + imgUrl)
        if imgRequest.status_code == 200:
            with open(comicNumber, 'wb') as f:
                for chunk in imgRequest:
                    f.write(chunk)
        f.close()
        print("Done scraping comic number: " + comicNumber)

print("Done scraping all xkcd comics!")
