package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"./mongodb"
	"golang.org/x/net/html"
)

const mainPage = "http://www.ihchina.cn/"

var divide = map[string]string{
	"新闻动态": "ul1",
	"论坛":   "ul2",
	"专题报道": "ul3",
}

func main() {
	client, ctx, err := mongodb.InitMongoDBConnection()
	if err != nil {
		panic(err)
	}
	defer client.Disconnect(ctx)
	resp, err := http.Get(mainPage)
	if err != nil {
		log.Println(err)
	}
	defer resp.Body.Close()
	doc, err := html.Parse(resp.Body)
	if err != nil {
		fmt.Fprintf(os.Stderr, "findlinks1:%v\n", err)
		os.Exit(1)
	}
	println("开始解析")
	visit(doc)
}

func visit(n *html.Node) {
	if n.Type == html.ElementNode && n.Data == "div" {
		for _, a := range n.Attr {
			if a.Key == "class" {
				for key, name := range divide {
					if name == a.Val {
						readInfo(key, n)
					}
				}
			}
		}
	}
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		visit(c)
	}

}

func readInfo(key string, n *html.Node) {
	if n.Type == html.ElementNode && n.Data == "div" {
		for _, a := range n.Attr {
			if a.Key == "class" && a.Val == "li" {
				tryToWriteMongoDB(key, n)
			}
		}
	}
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		readInfo(key, c)
	}
}

func tryToWriteMongoDB(key string, attr *html.Node) bool {
	resultMap := map[string]string{}
	for c := attr.FirstChild; c != nil; c = c.NextSibling {
		for _, name := range c.Attr {
			if name.Key == "class" {
				switch name.Val {
				case "date":
					resultMap["date"] = c.FirstChild.Data
				case "h16":
					if !readEachSection(resultMap, c.FirstChild) {
						return false
					}
				case "p":
					resultMap["shortContent"] = c.FirstChild.Data
				}
			}
		}
	}
	resultMap["type"] = key
	fmt.Println(resultMap)
	mongodb.WriteInfoToMongoDB(resultMap)
	return true
}

func readEachSection(resultMap map[string]string, c *html.Node) bool {
	for _, name := range c.Attr {
		if name.Key == "href" && mongodb.FindInMongoDB(name.Val) {
			return false
		}
	}
	for _, name := range c.Attr {
		resultMap[name.Key] = name.Val
	}
	return true
}
