package handlewebsite

import (
	"encoding/json"
	"log"
	"net/http"

	mongodb "github.com/sunkaiiii/Reptiles/MongoDB"

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

func startGenerateDetailPage(url string) map[string]string {
	if mongodb.FindNewsDetailInMongodb(url) == mongodb.DUPLICATED {
		return nil
	}
	resp, err := http.Get(url)
	if err != nil {
		log.Println(err)
		return nil
	}
	defer resp.Body.Close()
	if err != nil {
		log.Println(err)
		return nil
	}
	node, err := html.Parse(resp.Body)
	if err != nil {
		log.Println(err)
		return nil
	}
	var resultMap map[string]string
	walkDetailList(node, resultMap)
	if len(resultMap) != 0 {
		return resultMap
	}
	return nil
}

func walkDetailList(node *html.Node, resultMap map[string]string) {
	if node == nil {
		return
	}
	for c := node.FirstChild; c != nil; c = c.NextSibling {
		for _, name := range c.Attr {
			if name.Key == "class" && name.Val == "x-container" {
				generateDetail(c, resultMap)
			}
		}
	}
}

// <div class="article-title">
// 	<div class="h24 __WebInspectorHideElement__">

// 		“紫砂·九雋”作品展在中国美术馆揭幕
// 	</div>
// 	<div class="sub">
// 		<span class="sub-item" title="腾讯网">
// 		<img src="/Public/static/themes/image/temp/png34.png" alt="" class="ico">
// 			来源：腾讯网
// 			</span>
// 		<span class="sub-item">
// 			<img src="/Public/static/themes/image/temp/png36.png" alt="" class="ico">创建时间：<span class="en">2019-06-24 14:01:00</span></span>						</div>
// 			<div class="t_line">
// 			<div class="bd">
// 		</div>
// 	</div>
// </div>
func generateDetail(node *html.Node, resultMap map[string]string) {
	for n := node.FirstChild; n != nil; n = node.NextSibling {
		if n.Attr[0].Val == "newsdetails1" {
			getNewsContent(n, resultMap)
		} else if n.Attr[0].Val == "newsdetails2" {
			getRelevantNews(n, resultMap)
		}
	}
}

func getNewsContent(node *html.Node, resultMap map[string]string) {
	node = node.FirstChild.FirstChild
	for n := node.FirstChild; n != nil; n = n.NextSibling {
		switch n.Attr[0].Val {
		case "article-title":
			switch n.FirstChild.Attr[0].Val {
			case "h24 __WebInspectorHideElement__":
				resultMap["title"] = n.Data
			case "sub":
				resultMap["from"] = node.FirstChild.Data
				resultMap["time"] = node.FirstChild.NextSibling.FirstChild.NextSibling.Data
			}
		case "article-cont":
			resultMap["content"] = generateNewscontentList(node)
		}
	}
}

func generateNewscontentList(node *html.Node) string {
	const typeImg = "img"
	const typeText = "text"
	type contentStruct struct {
		contentType  string
		contentValue string
	}
	contentList := make([]contentStruct, 0)
	for n := node.FirstChild; n != nil; n = n.NextSibling {
		var singleLine contentStruct
		if child := n.FirstChild; child != nil { //如果有子节点说明这是个这行是个图片
			singleLine.contentType = typeImg
			singleLine.contentValue = child.Attr[0].Val
		} else {
			singleLine.contentType = typeText
			singleLine.contentValue = n.Data
		}
		contentList = append(contentList, singleLine)
	}
	resultByte, err := json.Marshal(contentList)
	if err != nil {
		log.Println(err)
		return ""
	}
	return string(resultByte)
}

func getRelevantNews(node *html.Node, resultMap map[string]string) {

}
