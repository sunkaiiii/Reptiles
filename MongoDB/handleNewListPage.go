package mongodb

import (
	"fmt"
	"log"

	"go.mongodb.org/mongo-driver/bson"
)

const DUPLICATED = 1
const ERROR = 2

type searchListInfoStructure struct {
	Href string
}

//FindNewsListTitleInMongoDB 查找是否已经录入了相同的新闻
func FindNewsListTitleInMongoDB(href string) int {
	cur := universalSearch(newsListCollectionName, bson.M{"href": href})
	var result searchListInfoStructure
	cur.Decode(&result)
	fmt.Println(result.Href)
	if len(result.Href) != 0 {
		return DUPLICATED
	}
	return 0
}

//WriteNewsToMongoDB 写入MongoDB
func WriteNewsToMongoDB(resultMap map[string]string) error {
	ctx := createContext()
	_, err := mongoClient.Database(dataBaseName).Collection(newsListCollectionName).InsertOne(ctx, resultMap)
	if err != nil {
		log.Println(err)
	}
	return err
}

//UpdateNewsImage 缓存图片到本地之后更新一个新的Key"localImage"
func UpdateNewsImage(path string, originalURL string) {
	ctx := createContext()
	update := bson.D{{"$set",
		bson.D{
			{"localImage", path},
		},
	}}
	_, err := mongoClient.Database(dataBaseName).Collection(newsListCollectionName).UpdateOne(ctx, bson.M{"image": originalURL}, update)
	if err != nil {
		log.Println(err)
	}
}
