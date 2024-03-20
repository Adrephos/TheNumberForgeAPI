package main

import (
	"fmt"
	"os"
	"github.com/Adrephos/TheNumberForgeAPI/routes"
)
func main() {
	router := routes.SetupRouter()

	fmt.Print("Server running on port ", os.Getenv("PORT"), "\n\n")
	router.Run()
}
