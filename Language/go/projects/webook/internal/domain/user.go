package domain

type User struct {
	Id         int64
	Email      string
	Password   string
	Phone      string
	Nickname   string
	Birthday   string
	AboutMe    string
	FeiShuInfo FeiShuInfo
}
