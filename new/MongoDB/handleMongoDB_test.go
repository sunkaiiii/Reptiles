package mongodb

import (
	"fmt"
	"testing"
)

func TestFindInMongoDB(t *testing.T) {
	_, _, _ = InitMongoDBConnection()
	fmt.Println(FindInMongoDB("123"))
}

func TestWriteInfoToMongoDB(t *testing.T) {
	mongoClient, ctx, _ := InitMongoDBConnection()
	defer mongoClient.Disconnect(ctx)
	_ = WriteInfoToMongoDB(map[string]string{"123": "123"})
}

func TestFindNewsListTitleInMongoDB(t *testing.T) {
	mongoClient, ctx, _ := InitMongoDBConnection()
	defer mongoClient.Disconnect(ctx)
	fmt.Println(FindNewsListTitleInMongoDB("/news2_details/1854.html"))
}
