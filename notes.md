# architecture_notes.md
*A concise reference for understanding the backend architecture of the Life Insights Engine.*

## 🏛 Overall System Architecture

```
Client → API (FastAPI) → Service Layer → Repository Layer → Database (SQLite)
```

### ✔ API Layer  
Handles input/output.  
Receives requests, validates using Pydantic models, returns clean JSON.

### ✔ Service Layer  
Applies **business logic**.  
Decides *when* and *why* to interact with the database.  
Validates data beyond structural validation.

### ✔ Repository Layer  
Handles **database operations only**.  
Creates, reads, updates, deletes entries using SQLAlchemy ORM.

### ✔ Database Layer  
Stores data efficiently in SQLite.  
Uses compact formats (e.g., tags stored as a string).

---

## 🧱 Database Concepts

### **1. Why tags are stored as a string in the DB**
SQLite does not natively support storing lists.  
Storing `"tag1,tag2,tag3"` is simple, efficient, and works with the ORM.

### **2. Why tags are returned as a list in the API**
Clients expect structured JSON.  
`["tag1", "tag2"]` is more natural and usable than `"tag1,tag2"`.

### **3. Conversions**
- On write: list → string (`",".join(tags)`)
- On read: string → list (`tags.split(",")`)

### **4. How the ORM works**
- Each class maps to a table (`EntryModel → entries`)
- Each class attribute maps to a column
- SQLAlchemy generates SQL under the hood

### **5. Base concepts**
- `engine`: manages the DB connection
- `SessionLocal()`: creates a session for queries/transactions
- `Base`: parent class tracking all ORM models
- `Base.metadata.create_all()`: creates tables from models

---

## 📄 API Layer Concepts

### **1. Why Pydantic models exist**
They validate and convert JSON input before the service layer sees it.

- `EntryCreate` → validates request body  
- `EntryResponse` → formats outgoing data  

### **2. Why API responses differ from DB rows**
API should return **client-friendly** shapes.  
DB should store **efficient, compact** shapes.  
These two do not need to match.

### **3. Dependency injection**
`Depends(get_db)` automatically gives routes access to a DB session.

### **4. How an API call flows**
```
JSON request → Pydantic → Service → Repository → DB  
DB result → Repository → Service → API layer → JSON response
```

---

## 🧠 Service Layer Concepts

### **1. Responsibility**
Implements **business rules**, NOT SQL.  
Examples:
- Validate entry type
- Clean tags
- Prevent empty content
- Choose which repository functions to call

### **2. Separation of concerns**
Services do logic.  
Repositories do data.  
APIs do communication.  
DB does storage.

### **3. Why use services instead of calling repositories directly**
- Easier to expand logic later
- Easier to test
- Cleaner architecture
- More realistic to real systems

---

## 🗄 Repository Layer Concepts

### **1. Responsibility**
Pure database access — nothing more.

Examples:
- Insert entry  
- Query all entries  
- Query by filter  

### **2. Why it shouldn’t contain business logic**
Repositories must stay reusable and predictable.

---

## 🔍 Data Shape Rules

### **DB Shape (storage-optimized)**
- Strings  
- Integers  
- Floats  
- Timestamps  
- CSV-style strings (`"tag1,tag2"`)

### **API Shape (client-optimized)**
- JSON arrays  
- JSON objects  
- Clean timestamp format  
- Explicit fields

### **Service converts between shapes when needed.**

---

## 🌱 Notes for Future Development

- If upgrading to Postgres: store tags as a JSONB array.
- If scaling: move from SQLite to a relational DB.
- If clients need more insights: add analytics endpoints in service layer.
