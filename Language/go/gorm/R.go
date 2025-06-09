package main

import "fmt"

func main() {
	db := GetConnect()

	//var users []User
	var user User
	result := db.First(&user) //SELECT * FROM `users` ORDER BY `users`.`id` LIMIT 1
	fmt.Println(user, result.Error, result.RowsAffected)

	db.Take(&user)
	fmt.Println(user) //SELECT * FROM `users` WHERE `users`.`id` = 1 LIMIT 1

	db.Last(&user)
	fmt.Println(user) // SELECT * FROM `users` WHERE `users`.`id` = 1 ORDER BY `users`.`id` DESC LIMIT 1

	db.First(&user, "id=?", 10)
	fmt.Println(user)

	//内联条件
	var user2 User
	var users2 []User
	db.Find(&users2, "name in ?", []string{"Mike", "Judy"})
	fmt.Println(users2)

	db.First(&user2, "id=?", 20)
	fmt.Println(user2)

	//not
	db.Not("name in ?", []string{"Mike", "Judy"}).Find(&users2)
	fmt.Println(users2)

	db.Not(&User{Name: "Mike"}).Find(&users2)
	fmt.Println(users2)

	db.Not([]int{1, 2, 3, 4, 5, 6, 7}).Find(&users2)
	fmt.Println(users2)

	//or
	db.Where("id in (?)", []int{1, 2, 3, 4, 5, 6, 7}).Or(&User{Name: "Bob"}).Find(&users2) //SELECT * FROM `users` WHERE id in (1,2,3,4,5,6,7) OR `users`.`name` = 'Bob'
	fmt.Println(users2)

	db.Where("id in (?)", []int{1, 2, 3, 4, 5, 6, 7}).Or(map[string]interface{}{"name": "Bob"}).Find(&users2) //同上
	fmt.Println(users2)

	//选择特定字段
	db.Select([]string{"id", "name"}).Find(&users2)
	fmt.Println(users2)

	rows, _ := db.Table("users").Select("COALESCE(age,?)", 42).Rows() //SELECT COALESCE(age,42) FROM `users`
	defer rows.Close()

	// 遍历结果
	for rows.Next() {
		var age int
		if err := rows.Scan(&age); err != nil {
			// 处理扫描错误
		}
		fmt.Println("Age:", age) // 输出：所有 NULL 均被替换为 42
	}

	//排序
	db.Order("age desc").Order("name").Find(&users2) //SELECT * FROM `users` ORDER BY age desc,name
	fmt.Println(users2)

	//Limit & Offset
	db.Limit(10).Offset(5).Find(&users2)
	fmt.Println(users2)

	//join查询，需要手动处理扁平化结果
	rows, err := db.Raw(`
    SELECT 
        users.id as user_id,
        users.name as user_name,
        orders.id as order_id,
        orders.amount as order_amount
    FROM users
    LEFT JOIN orders ON orders.user_id = users.id`).Rows()
	if err != nil {
		// 处理错误
	}
	defer rows.Close()

	// 手动解析结果
	usersMap := make(map[uint]*User)
	var (
		userID      uint
		userName    string
		orderID     uint
		orderAmount int
	)
	for rows.Next() {
		if err := rows.Scan(&userID, &userName, &orderID, &orderAmount); err != nil {
			// 处理扫描错误
		}

		// 如果用户不存在，创建新用户
		if _, ok := usersMap[userID]; !ok {
			usersMap[userID] = &User{
				ID:     userID,
				Name:   userName,
				Orders: []Order{},
			}
		}

		// 如果订单存在，添加到用户的订单列表
		if orderID != 0 {
			usersMap[userID].Orders = append(usersMap[userID].Orders, Order{
				ID:     orderID,
				Amount: orderAmount,
			})
		}
	}
	for _, user := range usersMap {
		fmt.Println(user.ID, user.Name, user.Orders)
	}

	/*预加载,自动映射到结构化对象
	主查询：执行用户指定的查询（如 Find(&users)）。
	分析关联：根据 Preload() 指定的关联字段，确定需要预加载的模型。
	批量查询关联：对每个关联模型，执行一次查询获取所有关联数据。
	内存关联：将关联数据映射到主模型的对应字段。
	*/
	db.Preload("Orders").Find(&users2)
	fmt.Println(users2)

	//scan
	type Result struct {
		Name string
		Age  int
	}

	var res Result
	db.Table("users").Select("name", "age").Where("name = ?", "Mike").Scan(&res)
	fmt.Println(res)
}
