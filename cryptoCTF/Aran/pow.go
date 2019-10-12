package main

import (
	"os"
	"fmt"
	"math/rand"
	"time"
	"crypto/sha1"
	"encoding/hex"
)

var (
    letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456790123456790123456790123456790")
)

func randSeq(n int) string {
    b := make([]rune, n)
    for i := range b {
        b[i] = letters[rand.Intn(len(letters))]
    }
    return string(b)
}

func GetHash(nonce string) string{
     h := sha1.New()
     h.Write([]byte(nonce))
     return hex.EncodeToString(h.Sum(nil))
}

func ComputeBlock(target string) interface{} {

	rand.Seed(time.Now().UnixNano())
	for true {
		nonce := randSeq(30)
		hash := GetHash(nonce)
		if(hash[len(hash)-len(target):len(hash)] == target){
			fmt.Println(hash)
			fmt.Println("nonce: " + nonce)
			return nil
		}
	}
	return nil
}

func main() {
	target := os.Args[1]

	ComputeBlock(target)
}
