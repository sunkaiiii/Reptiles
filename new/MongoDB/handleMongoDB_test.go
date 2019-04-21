package mongodb

import (
	"fmt"
	"testing"
)

func TestFindInMongoDB(t *testing.T) {
	InitMongoDBConnection()
	fmt.Println(FindInMongoDB("123"))
}

func TestWriteInfoToMongoDB(t *testing.T) {
	mongoClient, ctx, _ := InitMongoDBConnection()
	defer mongoClient.Disconnect(ctx)
	WriteInfoToMongoDB(map[string]string{"123": "123"})
}
