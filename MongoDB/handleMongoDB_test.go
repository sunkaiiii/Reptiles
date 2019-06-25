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
	duplicatedResult := FindNewsListTitleInMongoDB("/news2_details/18841.html")
	if duplicatedResult != DUPLICATED {
		t.Log(duplicatedResult)
		t.Errorf("should be DUPLICATED")
	}
	passResult := FindNewsListTitleInMongoDB("/news_details/asfknj3nrk2j3.html")
	if passResult != 0 {
		t.Log(passResult)
		t.Errorf("should be 0")
	}
}

func TestUpdateNewsImage(t *testing.T) {
	mongoClient, ctx, _ := InitMongoDBConnection()
	defer mongoClient.Disconnect(ctx)
	UpdateNewsImage("213", "/Uploads/Picture/2019/04/22/s5cbd18c3404ac_1071_601_0_0.jpg")
}
