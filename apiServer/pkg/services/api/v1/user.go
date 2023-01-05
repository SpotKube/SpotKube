package v1services

import (
	res "github.com/SpotKube/SpotKube/apiServer/pkg/helpers/api/v1"

	u "github.com/SpotKube/SpotKube/apiServer/pkg/helpers"
)

// User structure
type User struct {
	ID    uint   `gorm:"primary_key" json:"id,omitempty"`
	Name  string `gorm:"type:varchar(50)" json:"name" validate:"required"`
	Email string `gorm:"type:varchar(50)" json:"email" validate:"required,email"`
}

// UserService struct
type UserService struct {
	User User
}

// UserList function returns the list of users
func (us *UserService) UserList() map[string]interface{} {
	user := us.User

	userData := res.UserResponse{
		ID:    user.ID,
		Name:  "test",
		Email: "test@gmail.com",
	}
	response := u.Message(0, "This is from version 1 api")
	response["data"] = userData
	return response
}
