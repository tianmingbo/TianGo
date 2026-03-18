package dao

import "gorm.io/gorm"

func Init(db *gorm.DB) error {
	err := db.AutoMigrate(&User{}, &Article{})
	if err != nil {
		return err
	}
	return nil
}
