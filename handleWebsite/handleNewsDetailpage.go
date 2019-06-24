package handlewebsite

import (
	"log"
	"net/http"
)

func startAnalyseNewsDetail(newsDetailURLChan chan string) {
	for detailURL := range newsDetailURLChan {
		if len(detailURL) != 0 {
			absoluteURL := mainPage + detailURL
			startGenerateDetailPage(absoluteURL)
		}
	}
}

func startGenerateDetailPage(url string) {
	resp, err := http.Get(url)
	if err != nil {
		log.Println(err)
		return
	}
	if err != nil {
		log.Println(err)
		return
	}
	// var newsDetailMap map[string]interface{}
	// log.Println(resp.Body)
	// _, err := html.Parse()
	// resp.Body.Close()
	// if err != nil {
	// 	log.Println(err)
	// 	return
	// }
}
