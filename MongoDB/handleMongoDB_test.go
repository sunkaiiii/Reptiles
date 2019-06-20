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

func TestUpdateNewsImage(t *testing.T) {
	mongoClient, ctx, _ := InitMongoDBConnection()
	defer mongoClient.Disconnect(ctx)
	UpdateNewsImage("213", "/Uploads/Picture/2019/04/22/s5cbd18c3404ac_1071_601_0_0.jpg")
}
