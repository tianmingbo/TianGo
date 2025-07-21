package main

import (
	"fmt"
	"time"
)

func main() {
	// 1. 创建协调者
	coordinator := NewCoordinator()

	// 2. 创建并注册服务
	orderService := NewOrderService()
	inventoryService := NewInventoryService()
	paymentService := NewPaymentService()

	coordinator.RegisterService("order", orderService)
	coordinator.RegisterService("inventory", inventoryService)
	coordinator.RegisterService("payment", paymentService)

	// 3. 初始化测试数据
	inventoryService.InitInventory("product_1", 100) // 初始化产品1库存为100
	paymentService.InitAccount("user_1", 1000)       // 初始化用户1账户余额为1000

	// 4. 执行正常的TCC事务流程
	fmt.Println("=== 执行正常的TCC事务流程 ===")
	txID1 := TxID("tx_" + time.Now().Format("20060102150405") + "_001")

	// 准备各服务的参数
	params := map[string]interface{}{
		"order": CreateOrderParams{
			OrderID:   "order_001",
			UserID:    "user_1",
			ProductID: "product_1",
			Quantity:  10,
			Amount:    299.99,
		},
		"inventory": DeductInventoryParams{
			ProductID: "product_1",
			Quantity:  10,
		},
		"payment": PaymentParams{
			UserID: "user_1",
			Amount: 299.99,
		},
	}

	// 执行事务
	if err := coordinator.ExecuteTx(txID1, params); err != nil {
		fmt.Printf("事务执行失败: %v\n", err)
	} else {
		fmt.Printf("事务执行成功，状态: %v\n", coordinator.GetTxStatus(txID1))

		// 查看结果
		order, _ := orderService.GetOrder("order_001")
		fmt.Printf("订单状态: %s\n", order.Status)

		inventory, _ := inventoryService.GetInventory("product_1")
		fmt.Printf("产品1库存状态 - 总库存: %d, 已分配: %d\n", inventory.Total, inventory.Allocated)

		account, _ := paymentService.GetAccount("user_1")
		fmt.Printf("用户1账户状态 - 余额: %.2f, 已支付: %.2f\n", account.Balance, account.Paid)
	}

	// 5. 测试失败的TCC事务流程（库存不足场景）
	fmt.Println("\n=== 测试失败的TCC事务流程（库存不足） ===")
	txID2 := TxID("tx_" + time.Now().Format("20060102150405") + "_002")

	// 准备参数（请求1000个库存，实际只有90个）
	params2 := map[string]interface{}{
		"order": CreateOrderParams{
			OrderID:   "order_002",
			UserID:    "user_1",
			ProductID: "product_1",
			Quantity:  1000,
			Amount:    29999.99,
		},
		"inventory": DeductInventoryParams{
			ProductID: "product_1",
			Quantity:  1000,
		},
		"payment": PaymentParams{
			UserID: "user_1",
			Amount: 29999.99,
		},
	}

	// 执行事务
	if err := coordinator.ExecuteTx(txID2, params2); err != nil {
		fmt.Printf("事务执行失败: %v\n", err)
		fmt.Printf("事务状态: %v\n", coordinator.GetTxStatus(txID2))

		// 查看结果（应回滚到初始状态）
		order, _ := orderService.GetOrder("order_002")
		if order != nil {
			fmt.Printf("订单状态: %s\n", order.Status)
		} else {
			fmt.Println("订单未创建")
		}

		inventory, _ := inventoryService.GetInventory("product_1")
		fmt.Printf("产品1库存状态 - 总库存: %d, 已分配: %d, 预留: %d\n",
			inventory.Total, inventory.Allocated, inventory.Reserved)

		account, _ := paymentService.GetAccount("user_1")
		fmt.Printf("用户1账户状态 - 余额: %.2f, 已支付: %.2f, 冻结: %.2f\n",
			account.Balance, account.Paid, account.Frozen)
	}
}
