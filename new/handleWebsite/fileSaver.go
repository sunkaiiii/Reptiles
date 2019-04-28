package handlewebsite

import (
	"io"
	"log"
	"net/http"
	"os"
	"path"

	"../mongodb"
)

const newsImageDir = "../img/newNewsImage/"
const newsImageDirSaveName = "/img/newNewsImage"

func downloadNewsImage(url string) {
	const mainPageNoEnd = "http://www.ihchina.cn"
	resp, err := http.Get(mainPageNoEnd + url)
	if err != nil {
		log.Println(err)
		return
	}
	defer resp.Body.Close()
	if err != nil {
		log.Println(err)
		return
	}
	filePath := newsImageDir + path.Base(url)
	filePathInDB := newsImageDirSaveName + path.Base(url)
	file, err := os.Create(filePath)
	if err != nil {
		log.Println(err)
	}
	defer file.Close()
	_, err = io.Copy(file, resp.Body)
	if err != nil {
		log.Println(err)
	}
	mongodb.UpdateNewsImage(filePathInDB, url)
}
