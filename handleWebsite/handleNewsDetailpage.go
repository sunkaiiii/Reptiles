package handlewebsite

import (
	"log"
	"net/http"

	"golang.org/x/net/html"
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
	defer resp.Body.Close()
	if err != nil {
		log.Println(err)
		return
	}
	node, err := html.Parse(resp.Body)
	if err != nil {
		log.Println(err)
		return
	}
	walkDetailList(node)
}

func walkDetailList(node *html.Node) {
	if node == nil {
		return
	}

}
