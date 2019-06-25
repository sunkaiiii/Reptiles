package mongodb

import "go.mongodb.org/mongo-driver/bson"

const newsDetailCollectionName = "newsDetail"

type newsDetailSearchStructure struct {
	Href string
}

func FindNewsDetailInMongodb(href string) int {
	cur := universalSearch(newsDetailCollectionName, bson.M{
		"href": href,
	})
	var result newsDetailSearchStructure
	cur.Decode(&result)
	if len(result.Href) > 0 {
		return DUPLICATED
	}
	return 0
}
