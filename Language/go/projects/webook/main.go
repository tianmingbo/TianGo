package main

func main() {
	server := InitWebUser()
	_ = server.Run(":28080")
}
