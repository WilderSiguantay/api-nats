package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/nats-io/nats.go"
)

//Persona estructura persona
type Persona struct {
	Nombre        string `json:"Nombre"`
	Departamento  string `json:"Departamento"`
	Edad          int    `json:"Edad"`
	FormaContagio string `json:"Forma de contagio"`
	Estado        string `json:"Estado"`
}

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/", sendDatos).Methods("POST")
	log.Fatal(http.ListenAndServe(":5000", myRouter))
}

func sendDatos(w http.ResponseWriter, r *http.Request) {
	//leemos todo lo que entra por el metodo post
	reqBody, err := ioutil.ReadAll(r.Body)
	//creamos una variable tipo persona[]
	var persona Persona
	json.Unmarshal(reqBody, &persona)
	if err != nil {
		log.Fatal(err)
	}

	// Imprimimos el resultado
	fmt.Println("%s\n", string(reqBody))

	// se publica en mensaje en nats

	nc, err := nats.Connect("nats://nats:4222")
	if err != nil {
		json.NewEncoder(w).Encode("No se puede conectar al servidor nats")
	} else {
		ec, err := nats.NewEncodedConn(nc, nats.JSON_ENCODER)
		if err != nil {
			json.NewEncoder(w).Encode("can't get json encoder")
		} else {
			//servicio publicado foo
			if err := ec.Publish("foo", persona); err != nil {
				log.Fatal(err)
			}
			json.NewEncoder(w).Encode(&persona)
		}
	}
}

func main() {
	fmt.Println("Iniciamos api")
	handleRequests()
}
