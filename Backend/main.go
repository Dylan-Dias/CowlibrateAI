package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os/exec"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/jackc/pgx/v5"
	"golang.org/x/crypto/bcrypt"
)

var jwtSecret = []byte("your_secret_key_here")

// ===== Structs =====

type User struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
	Role     string `json:"role"`
}

type Credentials struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type Claims struct {
	Username string `json:"username"`
	Role     string `json:"role"`
	jwt.RegisteredClaims
}

type Animal struct {
	ID             int     `json:"id"`
	MilkYield      float64 `json:"milk_yield"`
	Health         string  `json:"health"`
	Breed          string  `json:"breed"`
	LactationStage string  `json:"lactation_stage"`
	Age            int     `json:"age"`
}

type Feed struct {
	FeedType       string  `json:"feed_type"`
	FeedQuantity   float64 `json:"feed_quantity"`
	FeedPercentage float64 `json:"feed_percentage"`
}

// Input format for insertions (POST /api/optimize)
type OptimizeRequest struct {
	Goats   []Animal `json:"goats"`
	Bovines []Animal `json:"bovines"`
	Feeds   []Feed   `json:"feeds"`
}

// ===== Middleware =====
func enableCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		origin := r.Header.Get("Origin")
		if origin == "http://localhost:5173" {
			w.Header().Set("Access-Control-Allow-Origin", origin)
		}
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func main() {
	conn, err := pgx.Connect(context.Background(), "postgres://postgres:root@localhost:5432/CowlibrateAI")
	if err != nil {
		log.Fatal("❌ Failed to connect to DB:", err)
	}
	defer conn.Close(context.Background())

	mux := http.NewServeMux()

	// User routes
	mux.HandleFunc("/api/register", func(w http.ResponseWriter, r *http.Request) {
		handleRegister(w, r, conn)
	})
	mux.HandleFunc("/api/login", func(w http.ResponseWriter, r *http.Request) {
		handleLogin(w, r, conn)
	})

	// Insert data route (insert cows/goats + feeds)
	mux.HandleFunc("/api/optimize", func(w http.ResponseWriter, r *http.Request) {
		handleOptimizeInsert(w, r, conn)
	})

	// Fetch + optimize cows
	mux.HandleFunc("/api/optimize-run/cows", func(w http.ResponseWriter, r *http.Request) {
		handleOptimizeRun(w, r, conn, "cow_entries", "cow_feeds")
	})

	// Fetch + optimize goats
	mux.HandleFunc("/api/optimize-run/goats", func(w http.ResponseWriter, r *http.Request) {
		handleOptimizeRun(w, r, conn, "goat_entries", "goat_feeds")
	})

	fmt.Println("🚀 Server running at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", enableCORS(mux)))
}

// ===== User registration =====
func handleRegister(w http.ResponseWriter, r *http.Request, conn *pgx.Conn) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if user.Username == "" || user.Email == "" || user.Password == "" || user.Role == "" {
		http.Error(w, "Missing required fields", http.StatusBadRequest)
		return
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		http.Error(w, "Error hashing password", http.StatusInternalServerError)
		return
	}

	_, err = conn.Exec(context.Background(), `
		INSERT INTO users (username, email, password, role)
		VALUES ($1, $2, $3, $4)
	`, user.Username, user.Email, string(hashedPassword), user.Role)

	if err != nil {
		log.Println("DB error during registration:", err)
		http.Error(w, "Could not register user", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	fmt.Fprint(w, "User registered successfully")
}

// ===== User login =====
func handleLogin(w http.ResponseWriter, r *http.Request, conn *pgx.Conn) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	var creds Credentials
	if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if creds.Username == "" || creds.Password == "" {
		http.Error(w, "Missing username or password", http.StatusBadRequest)
		return
	}

	var storedHash, role string
	err := conn.QueryRow(context.Background(), `
		SELECT password, role FROM users WHERE username=$1
	`, creds.Username).Scan(&storedHash, &role)

	if err != nil || bcrypt.CompareHashAndPassword([]byte(storedHash), []byte(creds.Password)) != nil {
		http.Error(w, "Invalid credentials", http.StatusUnauthorized)
		return
	}

	expiration := time.Now().Add(24 * time.Hour)
	claims := &Claims{
		Username: creds.Username,
		Role:     role,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expiration),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(jwtSecret)
	if err != nil {
		http.Error(w, "Could not create token", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"token": tokenString,
		"role":  role,
	})
}

// ===== Insert cows/goats + feeds =====
func handleOptimizeInsert(w http.ResponseWriter, r *http.Request, db *pgx.Conn) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	var req OptimizeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Insert Goats + their feeds
	for _, g := range req.Goats {
		var goatID int
		err := db.QueryRow(context.Background(), `
			INSERT INTO goat_entries (milk_yield, health, breed, lactation_stage, age)
			VALUES ($1, $2, $3, $4, $5) RETURNING id
		`, g.MilkYield, g.Health, g.Breed, g.LactationStage, g.Age).Scan(&goatID)

		if err != nil {
			log.Printf("❌ Failed to insert goat entry: %v", err)
			http.Error(w, "Failed to store goat data", http.StatusInternalServerError)
			return
		}

		for _, f := range req.Feeds {
			_, err := db.Exec(context.Background(), `
				INSERT INTO goat_feeds (goat_entry_id, feed_type, feed_quantity, feed_percentage)
				VALUES ($1, $2, $3, $4)
			`, goatID, f.FeedType, f.FeedQuantity, f.FeedPercentage)

			if err != nil {
				log.Println("❌ Feed insert error (goat):", err)
				http.Error(w, "Failed to store goat feed data", http.StatusInternalServerError)
				return
			}
		}
	}

	// Insert Cows + their feeds
	for _, c := range req.Bovines {
		var cowID int
		err := db.QueryRow(context.Background(), `
			INSERT INTO cow_entries (milk_yield, health, breed, lactation_stage, age)
			VALUES ($1, $2, $3, $4, $5) RETURNING id
		`, c.MilkYield, c.Health, c.Breed, c.LactationStage, c.Age).Scan(&cowID)

		if err != nil {
			log.Printf("❌ Failed to insert cow entry: %v", err)
			http.Error(w, "Failed to store cow data", http.StatusInternalServerError)
			return
		}

		for _, f := range req.Feeds {
			_, err := db.Exec(context.Background(), `
				INSERT INTO cow_feeds (cow_entry_id, feed_type, feed_quantity, feed_percentage)
				VALUES ($1, $2, $3, $4)
			`, cowID, f.FeedType, f.FeedQuantity, f.FeedPercentage)

			if err != nil {
				log.Println("❌ Feed insert error (cow):", err)
				http.Error(w, "Failed to store cow feed data", http.StatusInternalServerError)
				return
			}
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]any{
		"message": "Optimization and storage complete",
	})
}

// ===== Fetch + Optimize animals =====
// Generic handler to fetch animals + feeds, call python optimizer and return optimized result
func handleOptimizeRun(w http.ResponseWriter, r *http.Request, db *pgx.Conn, entriesTable, feedsTable string) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return

		
	}

	
	// Query animal entries
	query := fmt.Sprintf("SELECT id, milk_yield, health, breed, lactation_stage, age FROM %s", entriesTable)
	rows, err := db.Query(context.Background(), query)
	if err != nil {
		http.Error(w, "DB query error: "+err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var animals []Animal
	for rows.Next() {
		var a Animal
		if err := rows.Scan(&a.ID, &a.MilkYield, &a.Health, &a.Breed, &a.LactationStage, &a.Age); err != nil {
			http.Error(w, "DB scan error: "+err.Error(), http.StatusInternalServerError)
			return
		}
		animals = append(animals, a)
	}

	// Query feeds
	queryFeeds := fmt.Sprintf("SELECT feed_type, feed_quantity, feed_percentage FROM %s", feedsTable)
	feedRows, err := db.Query(context.Background(), queryFeeds)
	if err != nil {
		http.Error(w, "DB feed query error: "+err.Error(), http.StatusInternalServerError)
		return
	}
	defer feedRows.Close()

	var feeds []Feed
	for feedRows.Next() {
		var f Feed
		if err := feedRows.Scan(&f.FeedType, &f.FeedQuantity, &f.FeedPercentage); err != nil {
			http.Error(w, "DB feed scan error: "+err.Error(), http.StatusInternalServerError)
			return
		}
		feeds = append(feeds, f)
	}

	// Prepare request for python optimizer (same JSON format as your python script expects)
	reqData := struct {
		Bovines []Animal `json:"bovines"`
		Feeds   []Feed   `json:"feeds"`
	}{
		Bovines: animals,
		Feeds:   feeds,
	}

	// Marshal to JSON
	jsonInput, err := json.Marshal(reqData)
	if err != nil {
		http.Error(w, "Failed to marshal input JSON: "+err.Error(), http.StatusInternalServerError)
		return
	}



log.Printf("🐍 Calling Python with %d animals and %d feeds", len(animals), len(feeds))

// Call python optimization script
optimizedJSON, err := runOptimizationPython(jsonInput)
if err != nil {
	log.Println("❌ Python script error:", err)
	http.Error(w, "Optimization error: "+err.Error(), http.StatusInternalServerError)
	return
}

	// Return python's output directly
	w.Header().Set("Content-Type", "application/json")
	w.Write(optimizedJSON)
}

// Run the Python optimization script via stdin/stdout
func runOptimizationPython(inputJSON []byte) ([]byte, error) {
	cmd := exec.Command("python", "optimize.py")

	stdin, err := cmd.StdinPipe()
	if err != nil {
		return nil, err
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return nil, err
	}

	if err := cmd.Start(); err != nil {
		return nil, err
	}

	if _, err := stdin.Write(inputJSON); err != nil {
		return nil, err
	}
	stdin.Close()

	output, err := io.ReadAll(stdout)
	if err != nil {
		return nil, err
	}

	if err := cmd.Wait(); err != nil {
		return nil, err
	}

	return output, nil
}
