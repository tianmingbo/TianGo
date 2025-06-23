package response

type UserResponse struct {
	Id       int32  `json:"id"`
	Name     string `json:"name"`
	Gender   string `json:"gender"`
	Mobile   string `json:"mobile"`
	Birthday string `json:"birthday"`
}
