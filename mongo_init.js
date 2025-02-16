db = db.getSiblingDB('medical_db');

db.createUser({
  user: "medical_user",
  pwd: "securepassword",
  roles: [{ role: "readWrite", db: "medical_db" }],
});

db.createCollection("patient_summaries");

db.patient_summaries.insertOne({
  patient_id: "0001",
  name: "John Doe",
  age: 45,
  summary: "Hypertension with mild symptoms.",
});
