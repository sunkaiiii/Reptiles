package mongodb

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var mongoClient *mongo.Client

const dataBaseName = "heritage_online"
const mainPageCollectionName = "mainPage"
const newsListCollectionName = "newsList"

func createContext() context.Context {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	return ctx
}

//FindInMongoDB 会寻找是否有重复新闻并返回结果
func FindInMongoDB(href string) bool {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	cur := mongoClient.Database(dataBaseName).Collection(mainPageCollectionName).FindOne(ctx, bson.M{"href": href})
	var result struct {
		Href string
	}
	cur.Decode(&result)
	fmt.Println(result.Href)
	return len(result.Href) != 0
}

//WriteInfoToMongoDB 将这个新闻写入MongoDB
func WriteInfoToMongoDB(resultInfo map[string]string) error {
	ctx := createContext()
	_, err := mongoClient.Database(dataBaseName).Collection(mainPageCollectionName).InsertOne(ctx, resultInfo)
	if err != nil {
		log.Println(err)
	}
	return err
}

//InitMongoDBConnection 初始化mongoDB的连接，并返回连接的指针
func InitMongoDBConnection() (*mongo.Client, context.Context, error) {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		return nil, nil, err
	}
	mongoClient = client
	return mongoClient, ctx, nil
}
