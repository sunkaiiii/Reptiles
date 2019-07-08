package handlewebsite

import (
	"testing"

	mongodb "github.com/sunkaiiii/Reptiles/MongoDB"
)

func TestDownloadNewsImage(t *testing.T) {
	mongoClient, ctx, _ := mongodb.InitMongoDBConnection()
	defer mongoClient.Disconnect(ctx)
	downloadNewsImage("/Uploads/Picture/2019/04/22/s5cbd18c3404ac_1071_601_0_0.jpg")
}
