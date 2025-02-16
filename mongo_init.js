// Connect to the medical database
db = db.getSiblingDB('medical_db');

// Create user securely (use environment variables for sensitive data)
db.createUser({
  user: process.env.MONGO_USER || "medical_user",
  pwd: process.env.MONGO_PASSWORD || "securepassword",
  roles: [{ role: "readWrite", db: "medical_db" }],
});

// Create collections with schema validation
db.createCollection("patient_summaries", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["summary_id", "patient_id", "date", "summary", "flag"],
      properties: {
        summary_id: { bsonType: "string" },
        patient_id: { bsonType: "string" },
        date: { bsonType: "date" },
        summary: { bsonType: "string" },
        flag: { bsonType: "string" }
      }
    }
  }
});

db.createCollection("practitioners", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["practitioner_id", "name", "address", "latitude", "longitude"],
      properties: {
        practitioner_id: { bsonType: "string" },
        name: { bsonType: "string" },
        address: { bsonType: "string" },
        latitude: { bsonType: "double", minimum: -90, maximum: 90 },
        longitude: { bsonType: "double", minimum: -180, maximum: 180 }
      }
    }
  }
});

db.createCollection("patients", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "name", "age"],
      properties: {
        patient_id: { bsonType: "string" },
        name: { bsonType: "string" },
        age: { bsonType: "int", minimum: 0, maximum: 150 }
      }
    }
  }
});

db.createCollection("available_slots", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["practitioner_id", "available_slots", "flag"],
      properties: {
        practitioner_id: { bsonType: "string" },
        available_slots: {
          bsonType: "array",
          items: { bsonType: "date" }
        },
        flag: { bsonType: "string" }
      }
    }
  }
});

// Insert sample data
db.patient_summaries.insertOne({
  summary_id: "0001",
  patient_id: "0001",
  date: new Date("2024-01-12"),
  summary: "Hypertension with mild symptoms.",
  flag: "1/10"
});

db.practitioners.insertOne({
  practitioner_id: "0001",
  name: "John Doe",
  address: "4 av de la Grande Armée",
  latitude: 48.8742,
  longitude: 2.2935
});

db.patients.insertOne({
  patient_id: "0001",
  name: "John Doe",
  age: 45
});

db.available_slots.insertOne({
  practitioner_id: "0001",
  available_slots: [
    new Date("2025-04-12T12:00:00Z"),
    new Date("2025-04-12T13:00:00Z"),
    new Date("2025-04-12T14:00:00Z")
  ],
  flag: "1/10"
});

// Create indexes for efficient querying
db.patient_summaries.createIndex({ patient_id: 1 });
db.practitioners.createIndex({ practitioner_id: 1 });
db.patients.createIndex({ patient_id: 1 });
db.available_slots.createIndex({ practitioner_id: 1 });
