package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type Goods struct {
	Name  string  `json:"name"`
	ID    string  `json:"id"`
	Price float64 `json:"price"`
}

type Order struct {
	Total  float64 `json:"total"`
	Addr   string  `json:"addr"`
	ID     string  `json:"id"`
	Status string  `json:"status"`
}

var goods = []Goods{
	{"apple", "12345678", 6666.66},
	{"HW", "9876543", 3333.33},
	{"XM", "876543", 333.22},
}

func getAddr() string {
	adds := []string{"SH", "BJ", "HN", "TJ", "SR"}
	return adds[rand.Intn(len(adds))]
}

type PaymentRes struct {
	OrderID string `json:"order_id"`
	Success bool   `json:"success"`
	Error   string `json:"error"`
}

type InventoryRes struct {
	OrderID string `json:"order_id"`
	Success bool   `json:"success"`
	Error   string `json:"error"`
}

type ShippingRes struct {
	OrderID  string `json:"order_id"`
	Success  bool   `json:"success"`
	Error    string `json:"error"`
	Tracking string `json:"tracking"`
}

func genOrder(ctx context.Context, order chan<- Order) {
	defer close(order)
	for {
		select {
		case <-ctx.Done():
			return
		default:
			buy := goods[rand.Intn(len(goods))]
			time.Sleep(200 * time.Millisecond)
			fmt.Printf("buy %s, orderID is %s\n", buy.Name, buy.ID)
			order <- Order{
				Total:  buy.Price,
				Addr:   getAddr(),
				ID:     buy.ID,
				Status: "pending",
			}
		}
	}

}

func processPayment(ctx context.Context, orders <-chan Order, payment chan<- PaymentRes) {
	defer close(payment)
	for order := range orders {
		select {
		case <-ctx.Done():
			return
		default:
			success := rand.Intn(10) > 3
			time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
			res := PaymentRes{
				OrderID: order.ID,
				Success: success,
			}
			if !success {
				res.Error = "payment failed"
			}
			payment <- res
		}
	}
}

func checkInventory(ctx context.Context, payment <-chan PaymentRes, inventory chan<- InventoryRes) {
	defer close(inventory)
	for payment := range payment {
		if !payment.Success {
			inventory <- InventoryRes{
				OrderID: payment.OrderID,
				Success: false,
				Error:   payment.Error,
			}
			continue
		}
		select {
		case <-ctx.Done():
			return
		default:
			success := rand.Intn(10) > 1
			time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
			res := InventoryRes{
				OrderID: payment.OrderID,
				Success: success,
			}
			if !success {
				res.Error = "inventory failed"
			}
			inventory <- res
		}
	}

}

func arrangeShipping(ctx context.Context, inventory <-chan InventoryRes, shipping chan<- ShippingRes) {
	defer close(shipping)
	for payment := range inventory {
		if !payment.Success {
			shipping <- ShippingRes{
				OrderID: payment.OrderID,
				Success: false,
				Error:   payment.Error,
			}
			continue
		}

		select {
		case <-ctx.Done():
			return
		default:
			success := rand.Intn(10) > 4
			time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
			res := ShippingRes{
				OrderID: payment.OrderID,
				Success: success,
			}
			if !success {
				res.Error = "shipping failed"
			} else {
				res.Tracking = time.Now().Format(time.DateTime)
			}
			shipping <- res
		}
	}
}

func handlerRes(ctx context.Context, shipping <-chan ShippingRes, wg *sync.WaitGroup) {
	defer wg.Done()
	for res := range shipping {
		select {
		case <-ctx.Done():
			return
		default:
			if res.Error != "" {
				fmt.Printf("Order %s failed: %s\n", res.OrderID, res.Error)
			} else {
				fmt.Printf("Order %s success\n", res.OrderID)
			}
		}
	}
}

func main() {
	order := make(chan Order)
	payment := make(chan PaymentRes)
	inventory := make(chan InventoryRes)
	shipping := make(chan ShippingRes)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	var wg sync.WaitGroup

	go genOrder(ctx, order)

	go processPayment(ctx, order, payment)

	go checkInventory(ctx, payment, inventory)

	go arrangeShipping(ctx, inventory, shipping)

	wg.Add(1)
	go handlerRes(ctx, shipping, &wg)
	wg.Wait()
	fmt.Println("Done")
}
