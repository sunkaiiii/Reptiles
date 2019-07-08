package handlewebsite

import (
	"fmt"
	"testing"

	mongodb "github.com/sunkaiiii/Reptiles/MongoDB"
)

func TestStartGenerateDetailPage(t *testing.T) {
	client, ctx, _ := mongodb.InitMongoDBConnection()
	defer client.Disconnect(ctx)
	result := startGenerateDetailPage("http://www.ihchina.cn/news_details/18867.html")
	fmt.Println(result)
	t.Log(result)
}
