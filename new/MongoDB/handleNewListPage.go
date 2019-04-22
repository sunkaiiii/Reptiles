package mongodb

import (
	"context"
	"fmt"
	"go.mongodb.org/mongo-driver/bson"
	"log"
	"time"
)

const DUPLICATED = 1
const ERROR = 2

//FindNewsListTitleInMongoDB 查找是否已经录入了相同的新闻
func FindNewsListTitleInMongoDB(href string) int {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	cur := mongoClient.Database(dataBaseName).Collection(newsListCollectionName).FindOne(ctx, bson.M{"href": href})
	var result struct {
		Href string
	}
	_ = cur.Decode(&result)
	fmt.Println(result.Href)
	if len(result.Href) != 0 {
		return DUPLICATED
	} else {
		return 0
	}
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
