package handlewebsite

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"reflect"
	"strings"

	"github.com/sunkaiiii/reptiles/mongodb"
	"golang.org/x/net/html"
	"golang.org/x/net/html/atom"
)

const mainPage = "http://www.ihchina.cn/"
const newsListURL = mainPage + "Article/Index/getList.html"
const imageLabel = "img scaleimg"
const contentLabel = "cont"

//ReadNewsList 读取新闻列表
func ReadNewsList() {
	page := 1
	errorTime := 0
	pictureChan := make(chan string)
	go startPictureDownloader(pictureChan)
	defer close(pictureChan)
	for ; page < 255; page++ {
		if errorTime > 10 {
			log.Println("reach the limitation of error time")
			return
		}
		pageUrl := newsListURL + fmt.Sprintf("?category_id=9&page=%d&limit=0", page)
		fmt.Println(pageUrl)
		resp, err := http.Get(pageUrl)
		if err != nil {
			log.Println(err)
			errorTime++
			continue
		}
		responseData, err := ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			log.Println(err)
			errorTime++
			continue
		}
		if len(responseData) == 0 {
			errorTime++
			continue
		}
		var resultMap map[string]interface{}
		err = json.Unmarshal(responseData, &resultMap)
		if err != nil {
			log.Println(err)
			errorTime++
			continue
		}
		fmt.Println(reflect.TypeOf(resultMap["data"]))
		listDataString := resultMap["data"]
		node, err := html.ParseFragment(strings.NewReader(fmt.Sprintf("%s", listDataString)), &html.Node{
			Type:     html.ElementNode,
			Data:     "body",
			DataAtom: atom.Body,
		})
		if err != nil {
			log.Println(err)
			errorTime++
			continue
		}
		errorTime += walkNewsList(node, pictureChan)
	}
}

func walkNewsList(nodes []*html.Node, pictureChan chan string) int {
	fmt.Println("analyze...")
	fmt.Println(len(nodes))
	duplicatedTime := 0
	for _, n := range nodes {
		if generateEachNews(n, pictureChan) == mongodb.DUPLICATED {
			duplicatedTime++
		}
	}
	return duplicatedTime
}

func generateEachNews(n *html.Node, pictureChan chan string) int {
	resultMap := map[string]string{}
	startToParse(resultMap, n)
	fmt.Println(resultMap)
	if mongodb.FindNewsListTitleInMongoDB(resultMap["href"]) != mongodb.DUPLICATED {
		resultMap["type"] = "新闻动态"
		mongodb.WriteNewsToMongoDB(resultMap)
	} else {
		log.Println("Duplicated " + resultMap["href"])
		return mongodb.DUPLICATED
	}
	//如果页面有图片，加入图片下载队列。
	if imageName, ok := resultMap["image"]; ok {
		pictureChan <- imageName
	}
	return 0
}

func startToParse(resultMap map[string]string, n *html.Node) {
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		if len(c.Attr) > 0 {
			switch c.Attr[0].Val {
			case imageLabel:
				handleImageLabel(resultMap, c)
			case contentLabel:
				handleContentLabel(resultMap, c)
			}
		}
		startToParse(resultMap, c)
	}
}

func handleImageLabel(resultMap map[string]string, node *html.Node) {
	c := node.FirstChild.FirstChild
	for _, a := range c.Attr {
		if a.Key == "src" {
			resultMap["image"] = a.Val
		}
	}
}

func handleContentLabel(resultMap map[string]string, node *html.Node) bool {
	for c := node.FirstChild; c != nil; c = c.NextSibling {
		for _, name := range c.Attr {
			if name.Key == "class" {
				switch name.Val {
				case "date":
					resultMap["date"] = c.FirstChild.FirstChild.Data
				case "h16":
					for _, name := range c.FirstChild.Attr {
						resultMap[name.Key] = name.Val
					}
				case "p":
					resultMap["shortContent"] = c.FirstChild.Data
				}
			}
		}
	}
	return true
}

func startPictureDownloader(pictureChan chan string) {
	for pictureURL := range pictureChan {
		go downloadNewsImage(pictureURL)
	}
}
